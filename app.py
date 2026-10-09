"""NutriPlan - servidor Flask.

Ejecutar:   python app.py          (abre http://127.0.0.1:5000)
Producción: gunicorn "app:create_app()"

La interfaz es una sola página (templates/index.html) que habla con esta API
JSON. La sesión se maneja con Flask-Login (cookie firmada).
"""
import math
import re
import time
from collections import defaultdict
from datetime import date, datetime, timedelta

from flask import Flask, jsonify, render_template, request
from flask_login import LoginManager, current_user, login_required, login_user, logout_user
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import selectinload

from config import Config
from models import (Alimento, Categoria, Comida, ComidaAlimento, Dia, DiaPlan, Genero, HistorialPeso,
                    Hidratacion, Menu, MenuItem, Objetivo, Perfil, Plan, TipoComida, Usuario, db)
from seed import seed_catalogs
from services import menus as menus_svc, nutricion

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
AVATAR_RE = re.compile(r"^data:image/(jpeg|png|webp);base64,[A-Za-z0-9+/=]+$")
MAX_AVATAR = 400_000          # caracteres del data URL
MAX_ITEMS_POR_DIA = 90        # alimentos por día de plan (un plan de 7 días admite 630)
MAX_DIAS_PLAN = 31            # duración máxima de un plan (al crearlo o al extenderlo)
MAX_VASOS = 40

# Límite de intentos de login fallidos: 5 por correo+IP cada 5 minutos
_INTENTOS = defaultdict(list)
_VENTANA, _MAX_INTENTOS = 300, 5


# ---------------------------------------------------------------------------
# Utilidades
# ---------------------------------------------------------------------------
def ok(**datos):
    return jsonify(status="success", **datos)


def error(mensaje, codigo=400):
    return jsonify(status="error", message=mensaje), codigo


def body():
    """Cuerpo JSON de la petición ({} si no hay o es inválido)."""
    datos = request.get_json(silent=True)
    return datos if isinstance(datos, dict) else {}


def parse_fecha(texto):
    try:
        return datetime.strptime(str(texto)[:10], "%Y-%m-%d").date()
    except (ValueError, TypeError):
        return None


def numero(valor, minimo, maximo):
    """Convierte a float y valida rango; devuelve None si no es válido."""
    try:
        n = float(valor)
    except (TypeError, ValueError):
        return None
    if not math.isfinite(n) or n < minimo or n > maximo:
        return None
    return n


def duracion_valida(valor, por_defecto=7):
    """Número de días (entero entre 1 y MAX_DIAS_PLAN) o None si no es válido."""
    if valor in (None, ""):
        return por_defecto
    n = numero(valor, 1, MAX_DIAS_PLAN)
    if n is None or n != int(n):
        return None
    return int(n)


def plan_solapado(usuario_id, inicio, fin, excluir_id=None):
    """Otro plan del usuario que ocupe algún día entre `inicio` y `fin` (o None).
    Dos planes no pueden cubrir el mismo día: así «Hoy» siempre sabe cuál abrir."""
    q = Plan.query.filter(Plan.usuario_id == usuario_id, Plan.fecha_inicio <= fin, Plan.fecha_fin >= inicio)
    if excluir_id is not None:
        q = q.filter(Plan.id != excluir_id)
    return q.order_by(Plan.fecha_inicio).first()


def aviso_solape(otro):
    return (f"Esas fechas se cruzan con tu plan «{otro.nombre}» "
            f"({otro.fecha_inicio.strftime('%d/%m/%Y')} – {otro.fecha_fin.strftime('%d/%m/%Y')}).")


def entero_o_none(valor):
    """«3» o 3 → 3; cualquier otra cosa → None (posición de un día dentro del plan)."""
    try:
        return int(str(valor))
    except (TypeError, ValueError):
        return None


def usuario_dict(u):
    p = u.perfil
    avatar = p.avatar if p and p.avatar and p.avatar != "default.png" else None
    return {
        "id": u.id,
        "nombre": u.nombre,
        "email": u.email,
        "genero": p.genero.clave if p and p.genero else "no_especificado",
        "avatar": avatar,
    }


def plan_dict(p):
    return {
        "id": p.id,
        "nombre": p.nombre,
        "fecha_inicio": p.fecha_inicio.isoformat(),
        "fecha_fin": p.fecha_fin.isoformat(),
        "estado": p.estado,
    }


def plan_del_usuario(plan_id):
    """Devuelve el plan SOLO si pertenece al usuario con sesión (sección 19)."""
    return Plan.query.filter_by(id=plan_id, usuario_id=current_user.id).first()


def filas_del_plan(plan):
    """Alimentos del plan como filas {dia, comida, alimento_id, cantidad, unidad}.
    `dia` es la POSICIÓN del día dentro del plan como texto ("1" = primer día)."""
    q = (db.session.query(DiaPlan.dia_semana, TipoComida.clave, ComidaAlimento)
         .join(Comida, Comida.dia_id == DiaPlan.id)
         .join(TipoComida, TipoComida.id == Comida.tipo_id)
         .join(ComidaAlimento, ComidaAlimento.comida_id == Comida.id)
         .filter(DiaPlan.plan_id == plan.id)
         .order_by(DiaPlan.dia_semana, TipoComida.orden, ComidaAlimento.id))
    return [{
        "dia": str(dia_semana),
        "comida": tipo_clave,
        # El frontend compara ids como texto (valores de <select>)
        "alimento_id": str(ca.alimento_id),
        "cantidad": ca.cantidad,
        "unidad": ca.unidad,
    } for dia_semana, tipo_clave, ca in q]


def agregar_dias(plan, desde, cantidad, tipos):
    """Añade `cantidad` días (con todas sus comidas vacías) al final del plan.
    `desde` es la posición del primer día nuevo; la fecha sale de fecha_inicio."""
    for i in range(desde, desde + cantidad):
        dia = DiaPlan(dia_semana=i, fecha=plan.fecha_inicio + timedelta(days=i - 1))
        plan.dias.append(dia)
        for t in tipos:
            dia.comidas.append(Comida(tipo_id=t.id, nombre=t.nombre, hora=t.hora))


def crear_plan_semana(usuario, nombre, fecha_inicio, copiar_de=None, dias=7):
    """Crea un plan que empieza en `fecha_inicio` (cualquier día de la semana) y dura
    `dias` días (7 por defecto), con todas sus comidas vacías."""
    plan = Plan(usuario_id=usuario.id, nombre=nombre, fecha_inicio=fecha_inicio,
                fecha_fin=fecha_inicio + timedelta(days=dias - 1), estado="activo")
    db.session.add(plan)
    agregar_dias(plan, 1, dias, TipoComida.query.order_by(TipoComida.orden).all())
    db.session.flush()

    if copiar_de is not None:
        # Se copia día a día: el día 1 del plan origen → el día 1 del nuevo, y así
        # sucesivamente (lo que no tenga equivalente se queda vacío).
        origen = {(dp.dia_semana, c.tipo_id): c for dp in copiar_de.dias for c in dp.comidas}
        for dp in plan.dias:
            for c in dp.comidas:
                src = origen.get((dp.dia_semana, c.tipo_id))
                if src:
                    for ca in src.alimentos:
                        c.alimentos.append(ComidaAlimento(alimento_id=ca.alimento_id,
                                                          cantidad=ca.cantidad, unidad=ca.unidad))
    return plan


def nombre_por_defecto(inicio, dias=7):
    base = "Plan semanal" if dias == 7 else f"Plan de {dias} días"
    return f"{base} {inicio.strftime('%d/%m/%Y')}"


def plan_actual(usuario, hoy):
    """El plan de la semana que contiene `hoy`, o None si el usuario no tiene plan
    para esa semana. Los planes son opcionales: ya no se crea ninguno solo."""
    return (Plan.query.filter(Plan.usuario_id == usuario.id, Plan.fecha_inicio <= hoy, Plan.fecha_fin >= hoy)
            .order_by(Plan.fecha_inicio.desc()).first())


def meta_del_usuario(usuario):
    """(mínimo, máximo, objetivo) de kcal diarias según peso, altura, edad, género y objetivo."""
    p = usuario.perfil
    return menus_svc.rango_kcal(p.peso, p.altura, p.edad,
                                p.genero.clave if p.genero else None,
                                p.objetivo.clave if p.objetivo else "mantener")


def cantidad_menu(it, factor):
    """Cantidad de un ítem del menú ya ajustada a la meta del usuario."""
    return menus_svc.escalar_cantidad(it.cantidad, it.unidad, factor)


def resumen_menu(menu, claves_dia, claves_tipo, factor=1.0):
    """kcal de cada día del menú, con las porciones ajustadas por `factor`."""
    filas = [(claves_dia[it.dia_semana], claves_tipo[it.tipo_id], it.alimento, cantidad_menu(it, factor), it.unidad)
             for it in menu.items]
    return nutricion.resumen_plan(filas)


def ajuste_menu(menu, claves_dia, claves_tipo, kcal_objetivo):
    """Factor de porciones para que el promedio diario del menú sea la meta del usuario."""
    dias = resumen_menu(menu, claves_dia, claves_tipo)["dias"]
    kcal = [d.get("kcal", 0) for d in dias.values() if d.get("kcal", 0) > 0]
    promedio = sum(kcal) / len(kcal) if kcal else 0
    return menus_svc.factor_porciones(kcal_objetivo, promedio)


# ---------------------------------------------------------------------------
# Aplicación
# ---------------------------------------------------------------------------
def init_db():
    db.create_all()
    seed_catalogs()


def create_app(config_overrides=None):
    app = Flask(__name__, static_folder="static", template_folder="templates")
    app.config.from_object(Config)
    if config_overrides:
        app.config.update(config_overrides)
    app.json.ensure_ascii = False
    db.init_app(app)

    login_manager = LoginManager(app)

    @login_manager.user_loader
    def cargar_usuario(user_id):
        return db.session.get(Usuario, int(user_id))

    @login_manager.unauthorized_handler
    def no_autorizado():
        return error("Debes iniciar sesión.", 401)

    with app.app_context():
        init_db()

    @app.after_request
    def cabeceras(resp):
        resp.headers.setdefault("X-Content-Type-Options", "nosniff")
        resp.headers.setdefault("X-Frame-Options", "DENY")
        resp.headers.setdefault("Referrer-Policy", "same-origin")
        if request.path.startswith("/api/"):
            resp.headers["Cache-Control"] = "no-store"
        return resp

    @app.errorhandler(404)
    def no_encontrado(_e):
        if request.path.startswith("/api/"):
            return error("Recurso no encontrado.", 404)
        return render_template("index.html"), 404

    @app.errorhandler(413)
    def muy_grande(_e):
        return error("La petición es demasiado grande.", 413)

    @app.errorhandler(500)
    def fallo_interno(_e):
        db.session.rollback()
        return error("Error interno del servidor.", 500)

    # -- Páginas ----------------------------------------------------------
    @app.get("/")
    @app.get("/login")
    @app.get("/registro")
    @app.get("/dashboard")
    def index():
        return render_template("index.html")

    # -- Cuentas ----------------------------------------------------------
    @app.post("/api/registro")
    def registro():
        d = body()
        nombre = str(d.get("nombre") or "").strip()
        email = str(d.get("email") or "").strip().lower()
        password = str(d.get("password") or "")
        clave_genero = str(d.get("genero") or "no_especificado")

        if len(nombre) < 2 or len(nombre) > 300:
            return error("Escribe tu nombre completo (mínimo 2 caracteres).")
        if not EMAIL_RE.match(email) or len(email) > 150:
            return error("Escribe un correo electrónico válido.")
        if len(password) < 6:
            return error("La contraseña debe tener al menos 6 caracteres.")
        if len(password) > 72:
            return error("La contraseña no puede superar los 72 caracteres.")
        genero = Genero.query.filter_by(clave=clave_genero).first()
        if genero is None:
            return error("Selecciona un género válido.")
        if Usuario.query.filter_by(email=email).first():
            return error("Ese correo ya está registrado.", 409)

        objetivo = Objetivo.query.filter_by(clave="mantener").first()
        u = Usuario(nombre=nombre, email=email)
        u.set_password(password)
        u.perfil = Perfil(genero_id=genero.id, objetivo_id=objetivo.id, peso=70, altura=170)
        db.session.add(u)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return error("Ese correo ya está registrado.", 409)

        login_user(u, remember=True)
        return ok(user=usuario_dict(u)), 201

    @app.post("/api/login")
    def login():
        d = body()
        email = str(d.get("email") or "").strip().lower()
        password = str(d.get("password") or "")

        clave = f"{request.remote_addr}|{email}"
        ahora_ts = time.time()
        _INTENTOS[clave] = [t for t in _INTENTOS[clave] if ahora_ts - t < _VENTANA]
        if len(_INTENTOS[clave]) >= _MAX_INTENTOS:
            return error("Demasiados intentos fallidos. Espera unos minutos e inténtalo de nuevo.", 429)

        u = Usuario.query.filter_by(email=email).first()
        if u is None or not u.check_password(password):
            _INTENTOS[clave].append(ahora_ts)
            return error("Correo o contraseña incorrectos.", 401)

        _INTENTOS.pop(clave, None)
        login_user(u, remember=True)
        return ok(user=usuario_dict(u))

    @app.post("/api/sesion/entrar")
    def entrar_por_id():
        """Pantalla de perfiles: solo deja entrar a la cuenta que YA tiene sesión
        abierta en este navegador. Cualquier otra pide la contraseña."""
        d = body()
        if current_user.is_authenticated and str(d.get("id")) == str(current_user.id):
            return ok(user=usuario_dict(current_user))
        return error("Inicia sesión de nuevo para entrar con este perfil.", 401)

    @app.post("/api/logout")
    def logout():
        logout_user()
        return ok()

    # -- Perfil -----------------------------------------------------------
    @app.get("/api/perfil")
    @login_required
    def obtener_perfil():
        p = current_user.perfil
        return ok(peso=p.peso, altura=p.altura, objetivo=p.objetivo.clave, edad=p.edad)

    @app.put("/api/perfil")
    @login_required
    def guardar_perfil():
        d = body()
        peso = numero(d.get("peso"), 20, 500)
        altura = numero(d.get("altura"), 50, 260)
        objetivo = Objetivo.query.filter_by(clave=str(d.get("objetivo"))).first()
        if peso is None:
            return error("El peso debe estar entre 20 y 500 kg.")
        if altura is None:
            return error("La altura debe estar entre 50 y 260 cm.")
        if objetivo is None:
            return error("Selecciona un objetivo válido.")

        edad = None
        if d.get("edad") not in (None, ""):
            e = numero(d.get("edad"), 10, 120)
            if e is None:
                return error("La edad debe estar entre 10 y 120 años.")
            edad = int(e)

        p = current_user.perfil
        cambio_peso = abs(p.peso - peso) > 1e-9
        p.peso, p.altura, p.objetivo_id, p.edad = peso, altura, objetivo.id, edad
        # Se guarda un registro de peso al guardar la meta (y siempre el primero)
        primero = HistorialPeso.query.filter_by(usuario_id=current_user.id).first() is None
        if cambio_peso or primero:
            db.session.add(HistorialPeso(usuario_id=current_user.id, peso=peso))
        db.session.commit()
        return ok()

    @app.get("/api/perfil/historial-peso")
    @login_required
    def historial_peso():
        filas = (HistorialPeso.query.filter_by(usuario_id=current_user.id)
                 .order_by(HistorialPeso.registrado_en.desc(), HistorialPeso.id.desc()).limit(10).all())
        filas.reverse()
        return ok(historial=[{"peso": h.peso, "registrado_en": h.registrado_en.isoformat()} for h in filas])

    @app.put("/api/usuario")
    @login_required
    def actualizar_usuario():
        d = body()
        nombre = str(d.get("nombre") or "").strip()
        email = str(d.get("email") or "").strip().lower()
        genero = Genero.query.filter_by(clave=str(d.get("genero"))).first()
        avatar = d.get("avatar")

        if len(nombre) < 2 or len(nombre) > 300:
            return error("Escribe tu nombre (mínimo 2 caracteres).")
        if not EMAIL_RE.match(email) or len(email) > 150:
            return error("Escribe un correo electrónico válido.")
        if genero is None:
            return error("Selecciona un género válido.")
        otro = Usuario.query.filter(Usuario.email == email, Usuario.id != current_user.id).first()
        if otro:
            return error("Ese correo ya lo usa otra cuenta.", 409)
        if avatar:
            if not isinstance(avatar, str) or len(avatar) > MAX_AVATAR or not AVATAR_RE.match(avatar):
                return error("La imagen no es válida (usa JPG, PNG o WEBP).")

        current_user.nombre, current_user.email = nombre, email
        current_user.perfil.genero_id = genero.id
        if avatar:
            current_user.perfil.avatar = avatar
        db.session.commit()
        return ok(user=usuario_dict(current_user))

    # -- Catálogos (públicos para usuarios con sesión) -----------------------
    @app.get("/api/catalogos")
    @login_required
    def catalogos():
        categorias = Categoria.query.order_by(Categoria.id).all()
        clave_cat = {c.id: c.clave for c in categorias}
        alimentos = Alimento.query.order_by(Alimento.categoria_id, Alimento.nombre).all()
        return ok(
            categorias=[{"id": c.clave, "nombre": c.nombre} for c in categorias],
            alimentos=[{
                "id": str(a.id), "categoria_id": clave_cat[a.categoria_id], "nombre": a.nombre,
                "unidad_base": a.unidad_base, "cantidad_base": a.cantidad_base, "kcal": a.calorias,
                "proteina": a.proteinas, "grasa": a.grasas, "carbohidratos": a.carbohidratos,
                "fibra": a.fibra,
            } for a in alimentos],
            tipos_comida=[{"id": t.clave, "label": t.nombre, "hora": t.hora}
                          for t in TipoComida.query.order_by(TipoComida.orden).all()],
        )

    # -- Planes -----------------------------------------------------------
    @app.get("/api/planes")
    @login_required
    def listar_planes():
        planes = Plan.query.filter_by(usuario_id=current_user.id).order_by(Plan.fecha_inicio.desc()).all()
        return ok(planes=[plan_dict(p) for p in planes])

    @app.post("/api/planes")
    @login_required
    def crear_plan():
        d = body()
        inicio = parse_fecha(d.get("fecha_inicio"))
        if inicio is None:
            return error("Elige una fecha de inicio válida.")
        if not (date(2000, 1, 1) <= inicio <= date(2100, 12, 31)):
            return error("La fecha de inicio está fuera de rango.")
        dias = duracion_valida(d.get("dias"))
        if dias is None:
            return error(f"La duración debe ser de 1 a {MAX_DIAS_PLAN} días.")
        fin = inicio + timedelta(days=dias - 1)
        nombre = str(d.get("nombre") or "").strip()[:120] or nombre_por_defecto(inicio, dias)

        otro = plan_solapado(current_user.id, inicio, fin)
        if otro is not None:
            return error(aviso_solape(otro), 409)

        origen = None
        if d.get("copiar_de"):
            origen = plan_del_usuario(d.get("copiar_de"))
            if origen is None:
                return error("El plan que quieres copiar no existe.", 404)

        try:
            plan = crear_plan_semana(current_user, nombre, inicio, copiar_de=origen, dias=dias)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return error("Ya tienes un plan que empieza ese día.", 409)
        return ok(plan=plan_dict(plan), rows=filas_del_plan(plan)), 201

    @app.post("/api/planes/<int:plan_id>/extender")
    @login_required
    def extender_plan(plan_id):
        """Alarga el plan `dias` días más (al final). Los días nuevos empiezan vacíos."""
        p = plan_del_usuario(plan_id)
        if p is None:
            return error("Plan no encontrado.", 404)
        extra = duracion_valida(body().get("dias"), por_defecto=None)
        if extra is None:
            return error(f"Indica cuántos días quieres añadir (1 a {MAX_DIAS_PLAN}).")
        actuales = len(p.dias)
        if actuales + extra > MAX_DIAS_PLAN:
            return error(f"Un plan puede durar como máximo {MAX_DIAS_PLAN} días (este ya tiene {actuales}).")
        nuevo_fin = p.fecha_fin + timedelta(days=extra)
        otro = plan_solapado(current_user.id, p.fecha_fin + timedelta(days=1), nuevo_fin, excluir_id=p.id)
        if otro is not None:
            return error(aviso_solape(otro), 409)

        try:
            agregar_dias(p, actuales + 1, extra, TipoComida.query.order_by(TipoComida.orden).all())
            p.fecha_fin = nuevo_fin
            db.session.commit()
        except Exception:
            db.session.rollback()
            return error("No se pudo extender el plan.", 500)
        return ok(plan=plan_dict(p), rows=filas_del_plan(p))

    @app.get("/api/planes/actual")
    @login_required
    def obtener_plan_actual():
        hoy = parse_fecha(request.args.get("hoy")) or date.today()
        p = plan_actual(current_user, hoy)
        if p is None:                       # sin plan esta semana: es válido
            return ok(plan=[], info=None)
        return ok(plan=filas_del_plan(p), info=plan_dict(p))

    @app.get("/api/planes/<int:plan_id>")
    @login_required
    def obtener_plan(plan_id):
        p = plan_del_usuario(plan_id)
        if p is None:
            return error("Plan no encontrado.", 404)
        return ok(plan=filas_del_plan(p), info=plan_dict(p))

    @app.put("/api/planes/<int:plan_id>")
    @login_required
    def guardar_plan(plan_id):
        p = plan_del_usuario(plan_id)
        if p is None:
            return error("Plan no encontrado.", 404)

        items = body().get("items")
        if not isinstance(items, list):
            return error("Formato de plan inválido.")
        maximo = MAX_ITEMS_POR_DIA * len(p.dias)
        if len(items) > maximo:
            return error(f"Un plan de {len(p.dias)} días no puede tener más de {maximo} alimentos.")

        comidas = {}
        for dp in p.dias:
            for c in dp.comidas:
                comidas[(dp.dia_semana, c.tipo.clave)] = c
        ids = set()
        for it in items:
            try:
                ids.add(int(it.get("alimento_id")))
            except (TypeError, ValueError, AttributeError):
                return error("Alimento inválido en el plan.")
        alimentos = {a.id: a for a in Alimento.query.filter(Alimento.id.in_(ids)).all()} if ids else {}

        nuevos = []
        for it in items:
            comida = comidas.get((entero_o_none(it.get("dia")), str(it.get("comida"))))
            alimento = alimentos.get(int(it["alimento_id"]))
            cantidad = numero(it.get("cantidad"), 0.0001, 100_000)
            unidad = str(it.get("unidad"))
            if comida is None or alimento is None:
                return error("El plan contiene un día, una comida o un alimento que no existe.")
            if cantidad is None:
                return error("Las cantidades deben ser mayores que 0.")
            if unidad not in nutricion.unidades_validas(alimento.unidad_base):
                return error(f"Unidad inválida para {alimento.nombre}.")
            nuevos.append(ComidaAlimento(comida_id=comida.id, alimento_id=alimento.id,
                                         cantidad=cantidad, unidad=unidad))

        try:
            ids_comidas = [c.id for c in comidas.values()]
            ComidaAlimento.query.filter(ComidaAlimento.comida_id.in_(ids_comidas)).delete(synchronize_session=False)
            db.session.add_all(nuevos)
            db.session.commit()
        except Exception:
            db.session.rollback()
            return error("No se pudo guardar el plan.", 500)
        return ok(guardados=len(nuevos))

    @app.delete("/api/planes/<int:plan_id>")
    @login_required
    def eliminar_plan(plan_id):
        p = plan_del_usuario(plan_id)
        if p is None:
            return error("Plan no encontrado.", 404)
        db.session.delete(p)
        db.session.commit()
        return ok()

    @app.get("/api/planes/<int:plan_id>/resumen")
    @login_required
    def resumen(plan_id):
        """Totales nutricionales por comida, día y semana, calculados en el servidor."""
        p = plan_del_usuario(plan_id)
        if p is None:
            return error("Plan no encontrado.", 404)
        filas = [(str(dp.dia_semana), c.tipo.clave, ca.alimento, ca.cantidad, ca.unidad)
                 for dp in p.dias for c in dp.comidas for ca in c.alimentos]
        return ok(resumen=nutricion.resumen_plan(filas))

    # -- Menús ------------------------------------------------------------
    @app.get("/api/menus")
    @login_required
    def listar_menus():
        """Menús predefinidos con las kcal de cada día (calculadas en el servidor)."""
        claves_dia = {d.orden: d.clave for d in Dia.query.all()}
        claves_tipo = {t.id: t.clave for t in TipoComida.query.all()}
        menus = (Menu.query.options(selectinload(Menu.items).joinedload(MenuItem.alimento))
                 .order_by(Menu.orden, Menu.id).all())
        minimo, maximo, objetivo = meta_del_usuario(current_user)
        salida = []
        for m in menus:
            factor = ajuste_menu(m, claves_dia, claves_tipo, objetivo)
            dias = resumen_menu(m, claves_dia, claves_tipo, factor)["dias"]
            kcal_dias = {clave: dias.get(clave, {}).get("kcal", 0) for clave in claves_dia.values()}
            salida.append({
                "id": m.clave, "nombre": m.nombre, "descripcion": m.descripcion,
                "kcal_por_dia": kcal_dias,
                "kcal_promedio": round(sum(kcal_dias.values()) / max(len(kcal_dias), 1)),
                "factor": factor,
            })
        return ok(menus=salida, meta={"min": minimo, "max": maximo, "objetivo": objetivo})

    @app.post("/api/planes/<int:plan_id>/menu")
    @login_required
    def aplicar_menu(plan_id):
        """Copia un menú a los días elegidos del plan (`dias` = posiciones: 1 es el primer
        día del plan), con las porciones ajustadas a la meta calórica del usuario (peso, altura,
        edad, género y objetivo). Cada día del plan recibe el día del menú que cae en su mismo día de la
        semana: un miércoles del plan toma el miércoles del menú. En esos días REEMPLAZA los
        alimentos que hubiera; los demás días no se tocan. Después todo se puede editar."""
        p = plan_del_usuario(plan_id)
        if p is None:
            return error("Plan no encontrado.", 404)

        d = body()
        menu = Menu.query.filter_by(clave=str(d.get("menu"))).first()
        if menu is None:
            return error("El menú que elegiste no existe.", 404)

        dias = d.get("dias")
        if not isinstance(dias, list) or not dias:
            return error("Elige al menos un día para aplicar el menú.")
        posiciones = set()
        for valor in dias:
            pos = entero_o_none(valor)
            if pos is None or not (1 <= pos <= len(p.dias)):
                return error("Uno de los días elegidos no es válido.")
            posiciones.add(pos)

        # día de la semana (1 = lunes ... 7 = domingo) → posiciones elegidas que caen en él
        por_semana = defaultdict(list)
        for dp in p.dias:
            if dp.dia_semana in posiciones:
                por_semana[dp.fecha.isoweekday()].append(dp.dia_semana)

        claves_dia = {x.orden: x.clave for x in Dia.query.all()}
        claves_tipo = {t.id: t.clave for t in TipoComida.query.all()}
        _minimo, _maximo, objetivo = meta_del_usuario(current_user)
        factor = ajuste_menu(menu, claves_dia, claves_tipo, objetivo)

        comidas = {(dp.dia_semana, c.tipo_id): c for dp in p.dias for c in dp.comidas}
        try:
            ids_comidas = [c.id for (pos, _tipo), c in comidas.items() if pos in posiciones]
            ComidaAlimento.query.filter(ComidaAlimento.comida_id.in_(ids_comidas)).delete(synchronize_session=False)
            aplicados = 0
            for it in menu.items:
                for pos in por_semana.get(it.dia_semana, []):
                    comida = comidas.get((pos, it.tipo_id))
                    if comida is None:
                        continue
                    db.session.add(ComidaAlimento(comida_id=comida.id, alimento_id=it.alimento_id,
                                                  cantidad=cantidad_menu(it, factor), unidad=it.unidad))
                    aplicados += 1
            db.session.commit()
        except Exception:
            db.session.rollback()
            return error("No se pudo aplicar el menú.", 500)
        return ok(aplicados=aplicados, rows=filas_del_plan(p), factor=factor, kcal_objetivo=objetivo)

    # -- Hidratación ------------------------------------------------------
    @app.get("/api/hidratacion")
    @login_required
    def obtener_hidratacion():
        desde = parse_fecha(request.args.get("desde")) or (date.today() - timedelta(days=6))
        filas = (Hidratacion.query.filter(Hidratacion.usuario_id == current_user.id, Hidratacion.fecha >= desde)
                 .order_by(Hidratacion.fecha).all())
        return ok(registros=[{"fecha": h.fecha.isoformat(), "vasos": h.vasos} for h in filas])

    @app.put("/api/hidratacion")
    @login_required
    def guardar_hidratacion():
        d = body()
        fecha = parse_fecha(d.get("fecha"))
        vasos = numero(d.get("vasos"), 0, MAX_VASOS)
        if fecha is None or vasos is None:
            return error("Datos de hidratación inválidos.")
        if abs((fecha - date.today()).days) > 2:
            return error("Solo puedes registrar agua de hoy (±1 día).")
        fila = Hidratacion.query.filter_by(usuario_id=current_user.id, fecha=fecha).first()
        if fila is None:
            fila = Hidratacion(usuario_id=current_user.id, fecha=fecha)
            db.session.add(fila)
        fila.vasos = int(vasos)
        db.session.commit()
        return ok()

    return app


if __name__ == "__main__":
    create_app().run(host="127.0.0.1", port=5000, debug=False)
