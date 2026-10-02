# NutriPlan Desktop - backend en Python: abre la ventana (pywebview) y ofrece a la interfaz web los métodos de la clase API
import datetime
import os
import re
import sys

import bcrypt
import webview

from conexion import get_supabase

# Validaciones básicas: formato de correo y unidades permitidas
EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

UNIDADES = {"g", "kg", "ml", "l", "unidad"}

# Listas de nombres (slugs). La posición + 1 es el id en la base de datos, no cambies el orden
GENERO_SLUGS = [
    'femenino', 'masculino', 'no_binario', 'prefiero_no_decir', 'no_especificado',
]

OBJETIVO_SLUGS = [
    'bajar', 'mantener', 'subir',
]

DIA_SLUGS = [
    'lunes', 'martes', 'miercoles', 'jueves', 'viernes', 'sabado', 'domingo',
]

COMIDA_SLUGS = [
    'desayuno', 'almuerzo', 'cena',
]

CATEGORIA_SLUGS = [
    'granos', 'legumbres', 'carnes', 'pescados', 'verduras', 'frutas', 'lacteos', 'grasas',
    'bebidas', 'procesados', 'condimentos',
]

ALIMENTO_SLUGS = [
    'arroz_blanco', 'arroz_integral', 'avena', 'pasta', 'pan_integral', 'pan_blanco', 'quinoa', 'papa',
    'papa_horneada', 'yuca', 'platano_verde', 'maiz', 'tortilla_maiz', 'cuscus', 'lentejas', 'garbanzos',
    'frijol_negro', 'frijol_rojo', 'arveja', 'habas', 'soya_texturizada', 'pechuga_pollo', 'muslo_pollo', 'carne_res',
    'carne_molida', 'lomo_cerdo', 'pavo_pechuga', 'tocino', 'jamon', 'chorizo', 'higado_res', 'tofu',
    'huevo', 'clara_huevo', 'salmon', 'atun', 'atun_fresco', 'tilapia', 'camaron', 'merluza',
    'sardina', 'pulpo', 'brocoli', 'espinacas', 'zanahoria', 'tomate', 'aguacate', 'lechuga',
    'pepino', 'cebolla', 'pimenton', 'coliflor', 'calabacin', 'champinones', 'remolacha', 'apio',
    'manzana', 'banano', 'fresa', 'naranja', 'pera', 'uva', 'piña', 'mango',
    'papaya', 'sandia', 'melon', 'kiwi', 'mandarina', 'mora', 'leche_entera', 'leche_descremada',
    'yogur_griego', 'yogur_natural', 'queso_fresco', 'queso_mozzarella', 'queso_crema', 'mantequilla', 'kumis', 'aceite_oliva',
    'aceite_vegetal', 'almendras', 'nueces', 'mani', 'mantequilla_mani', 'semillas_chia', 'frutos_secos', 'coco_rallado',
    'agua', 'jugo_naranja', 'cafe_negro', 'te_verde', 'gaseosa', 'bebida_energizante', 'cerveza', 'batido_proteina',
    'leche_almendras', 'papas_fritas', 'chocolate_negro', 'chocolate_leche', 'galletas_dulces', 'helado', 'pizza', 'hamburguesa',
    'nuggets_pollo', 'cereal_azucarado', 'barra_energetica', 'pan_dulce', 'sal', 'azucar', 'miel', 'salsa_tomate',
    'mayonesa', 'mostaza', 'salsa_soya', 'vinagreta',
]

# Crea los diccionarios nombre->id e id->nombre a partir de cada lista
def _mapas(slugs):
    slug_a_id = {slug: i + 1 for i, slug in enumerate(slugs)}
    id_a_slug = {i + 1: slug for i, slug in enumerate(slugs)}
    return slug_a_id, id_a_slug

# Diccionarios listos para convertir entre nombres e ids
GENERO_A_ID, ID_A_GENERO = _mapas(GENERO_SLUGS)
OBJETIVO_A_ID, ID_A_OBJETIVO = _mapas(OBJETIVO_SLUGS)
DIA_A_ID, ID_A_DIA = _mapas(DIA_SLUGS)
COMIDA_A_ID, ID_A_COMIDA = _mapas(COMIDA_SLUGS)
CATEGORIA_A_ID, ID_A_CATEGORIA = _mapas(CATEGORIA_SLUGS)
ALIMENTO_A_ID, ID_A_ALIMENTO = _mapas(ALIMENTO_SLUGS)


# Calcula el siguiente id libre de una tabla (así no se depende del autoincremento)
def _siguiente_id(sb, tabla, columna):
    res = sb.table(tabla).select(columna).order(columna, desc=True).limit(1).execute()
    if res.data:
        return res.data[0][columna] + 1
    return 1


# Traduce los errores técnicos de Supabase a mensajes entendibles
def _mensaje_error(e: Exception) -> str:
    txt = str(e)
    bajo = txt.lower()
    print(f"[NutriPlan] Error: {e!r}", file=sys.stderr)
    if "23505" in txt or "duplicate key" in bajo:
        return "Ese correo ya está registrado"
    if "pgrst204" in bajo or "pgrst205" in bajo or "could not find the" in bajo:
        m = re.search(r"Could not find the .*?in the schema cache", txt)
        detalle = m.group(0) if m else txt
        return f"Supabase no encuentra algo en tu base de datos: {detalle[:200]}"
    if "23502" in txt or "null value in column" in bajo:
        return f"Tu tabla tiene una columna obligatoria que la app no llena: {txt[:200]}"
    if "42501" in txt or "row-level security" in bajo:
        return "Supabase bloqueó la operación (RLS): a esa tabla le falta una política de acceso. Ejecuta el SQL de permisos de la tabla"
    if "invalid api key" in bajo or "jwt" in bajo:
        return "Clave de Supabase inválida. Revisa SUPABASE_KEY o actualiza: pip install -U supabase"
    if any(x in bajo for x in ("connect", "timed out", "getaddrinfo", "network", "resolve")):
        return "No hay conexión con el servidor. Revisa tu internet"
    return txt


# Une los datos de las tablas usuarios y perfil_usuario en un solo diccionario
def _usuario_completo(sb, id_usuario):
    filas = sb.table("usuarios").select("*").eq("id_usuario", id_usuario).limit(1).execute().data
    if not filas:
        return None
    u = filas[0]
    perfil = sb.table("perfil_usuario").select("*").eq("id_usuario", id_usuario).limit(1).execute().data
    p = perfil[0] if perfil else {}
    u["id_genero"] = p.get("id_genero")
    u["id_objetivo"] = p.get("id_objetivo")
    u["peso"] = p.get("peso", 70)
    u["altura"] = p.get("altura", 170)
    u["avatar"] = p.get("avatar", "default.png")
    return u


# Datos del usuario que sí se envían a la interfaz (nunca la contraseña)
def _usuario_publico(u: dict) -> dict:
    return {
        "id": u.get("id_usuario"),
        "nombre": u.get("nombre"),
        "email": u.get("email"),
        "genero": ID_A_GENERO.get(u.get("id_genero"), "no_especificado"),
        # 'default.png' no es una imagen real: sin foto, la app muestra la inicial del nombre.
        "avatar": u.get("avatar") if u.get("avatar") not in (None, "", "default.png") else None,
    }


# Métodos que la interfaz web (script.js) puede llamar con window.pywebview.api
class API:
    # Guarda el usuario con sesión iniciada y los catálogos válidos
    def __init__(self):
        self._usuario = None
        self._catalogos = {
            "generos": set(GENERO_SLUGS),
            "objetivos": set(OBJETIVO_SLUGS),
            "dias": set(DIA_SLUGS),
            "comidas": set(COMIDA_SLUGS),
        }

    # Devuelve categorías y alimentos desde la base de datos
    def obtener_catalogos(self):
        try:
            sb = get_supabase()
            cats_db = sb.table("categorias").select("id_categoria, nombre").execute().data or []
            categorias = [
                {"id": ID_A_CATEGORIA.get(c["id_categoria"], str(c["id_categoria"])), "nombre": c["nombre"]}
                for c in cats_db
            ]
            alim_db = (sb.table("alimentos")
                       .select("id_alimento, id_categoria, nombre, unidad_base, cantidad_base, kcal, proteina, grasa, carbohidratos")
                       .execute().data or [])
            alimentos = [
                {
                    "id": ID_A_ALIMENTO.get(a["id_alimento"], str(a["id_alimento"])),
                    "categoria_id": ID_A_CATEGORIA.get(a["id_categoria"], ""),
                    "nombre": a["nombre"],
                    "unidad_base": a["unidad_base"],
                    "cantidad_base": a["cantidad_base"],
                    "kcal": a["kcal"],
                    "proteina": a["proteina"],
                    "grasa": a["grasa"],
                    "carbohidratos": a["carbohidratos"],
                }
                for a in alim_db
            ]
            return {"status": "success", "categorias": categorias, "alimentos": alimentos}
        except Exception as e:
            return {"status": "error", "message": _mensaje_error(e), "categorias": [], "alimentos": []}

    # Devuelve los últimos pesos registrados del usuario
    def obtener_historial_peso(self, limite=10):
        if not self._usuario:
            return {"status": "success", "historial": []}
        try:
            res = (get_supabase().table("historial_peso")
                   .select("peso, registrado_en")
                   .eq("id_usuario", self._usuario["id_usuario"])
                   .order("registrado_en", desc=True)
                   .limit(limite)
                   .execute())
            return {"status": "success", "historial": res.data or []}
        except Exception as e:
            return {"status": "error", "message": _mensaje_error(e), "historial": []}

    # Crea la cuenta: valida los datos, cifra la contraseña con bcrypt y crea el perfil
    def registrar_usuario(self, nombre, email, password, genero="no_especificado"):
        try:
            nombre = (nombre or "").strip()
            email = (email or "").strip().lower()
            password = password or ""
            if genero not in GENERO_A_ID:
                genero = "no_especificado"

            if not nombre:
                return {"status": "error", "message": "Escribe tu nombre"}
            if not EMAIL_RE.match(email):
                return {"status": "error", "message": "Correo electrónico inválido"}
            if len(password) < 6:
                return {"status": "error", "message": "La contraseña debe tener al menos 6 caracteres"}
            if len(password.encode("utf-8")) > 72:
                return {"status": "error", "message": "La contraseña es demasiado larga (máx. 72 bytes)"}

            hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
            sb = get_supabase()

            nuevo_id = _siguiente_id(sb, "usuarios", "id_usuario")
            res = sb.table("usuarios").insert({
                "id_usuario": nuevo_id,
                "nombre": nombre,
                "email": email,
                "password_hash": hashed,
            }).execute()

            if not res.data:
                return {"status": "error", "message": "No se pudo crear la cuenta (respuesta vacía de Supabase)"}

            id_usuario = res.data[0]["id_usuario"]
            try:
                sb.table("perfil_usuario").insert({
                    "id_perfil": _siguiente_id(sb, "perfil_usuario", "id_perfil"),
                    "id_usuario": id_usuario,
                    "id_genero": GENERO_A_ID[genero],
                    "id_objetivo": OBJETIVO_A_ID["mantener"],
                    "peso": 70,
                    "altura": 170,
                }).execute()
            except Exception:
                pass

            user = _usuario_completo(sb, id_usuario) or {"id_usuario": id_usuario, "nombre": nombre, "email": email}
            self._usuario = user
            return {"status": "success", "message": "¡Cuenta creada con éxito!", "user": _usuario_publico(user)}
        except Exception as e:
            return {"status": "error", "message": _mensaje_error(e)}

    # Verifica correo y contraseña (el mensaje de error es el mismo para ambos casos)
    def iniciar_sesion(self, email, password):
        try:
            email = (email or "").strip().lower()
            sb = get_supabase()
            res = sb.table("usuarios").select("*").eq("email", email).limit(1).execute()
            generico = {"status": "error", "message": "Correo o contraseña incorrectos"}
            if not res.data:
                return generico

            fila = res.data[0]
            if not fila.get("password_hash"):
                return generico
            ok = bcrypt.checkpw((password or "").encode("utf-8"), fila["password_hash"].encode("utf-8"))
            if not ok:
                return generico

            user = _usuario_completo(sb, fila["id_usuario"]) or fila
            self._usuario = user
            return {"status": "success", "user": _usuario_publico(user)}
        except Exception as e:
            return {"status": "error", "message": _mensaje_error(e)}

    # Entra con un perfil guardado en el equipo, sin pedir contraseña
    def entrar_por_id(self, user_id):
        try:
            sb = get_supabase()
            user = _usuario_completo(sb, user_id)
            if not user:
                return {"status": "error", "message": "Este perfil ya no existe. Inicia sesión de nuevo."}
            self._usuario = user
            return {"status": "success", "user": _usuario_publico(user)}
        except Exception as e:
            return {"status": "error", "message": _mensaje_error(e)}

    # Actualiza nombre, correo, género y foto del usuario
    def actualizar_datos_usuario(self, nombre, email, genero, avatar=None):
        if not self._usuario:
            return {"status": "error", "message": "No hay sesión iniciada"}
        try:
            nombre = (nombre or "").strip()
            email = (email or "").strip().lower()
            if genero not in GENERO_A_ID:
                genero = ID_A_GENERO.get(self._usuario.get("id_genero"), "no_especificado")

            if not nombre:
                return {"status": "error", "message": "Escribe tu nombre"}
            if not EMAIL_RE.match(email):
                return {"status": "error", "message": "Correo electrónico inválido"}

            sb = get_supabase()
            id_usuario = self._usuario["id_usuario"]

            res = sb.table("usuarios").update({"nombre": nombre, "email": email}).eq("id_usuario", id_usuario).execute()
            if not res.data:
                return {"status": "error", "message": "No se pudo actualizar la cuenta"}

            perfil_datos = {"id_genero": GENERO_A_ID[genero]}
            if avatar:
                if len(avatar) > 2_000_000:
                    return {"status": "error", "message": "La imagen es demasiado pesada"}
                perfil_datos["avatar"] = avatar

            existe = sb.table("perfil_usuario").select("id_perfil").eq("id_usuario", id_usuario).limit(1).execute().data
            if existe:
                sb.table("perfil_usuario").update(perfil_datos).eq("id_usuario", id_usuario).execute()
            else:
                perfil_datos.update({
                    "id_perfil": _siguiente_id(sb, "perfil_usuario", "id_perfil"),
                    "id_usuario": id_usuario,
                    "id_objetivo": OBJETIVO_A_ID["mantener"],
                    "peso": 70, "altura": 170,
                })
                sb.table("perfil_usuario").insert(perfil_datos).execute()

            user = _usuario_completo(sb, id_usuario)
            self._usuario = user
            return {"status": "success", "user": _usuario_publico(user)}
        except Exception as e:
            return {"status": "error", "message": _mensaje_error(e)}

    # Olvida al usuario actual
    def cerrar_sesion(self):
        self._usuario = None
        return True

    # Cierra la ventana del programa
    def cerrar_programa(self):
        if len(webview.windows) > 0:
            webview.windows[0].destroy()
        else:
            sys.exit(0)
        return True

    # Devuelve peso, altura y objetivo del usuario
    def obtener_perfil(self):
        defecto = {"status": "success", "peso": 70, "altura": 170, "objetivo": "mantener"}
        if not self._usuario:
            return defecto
        try:
            res = (get_supabase().table("perfil_usuario")
                   .select("peso, altura, id_objetivo")
                   .eq("id_usuario", self._usuario["id_usuario"])
                   .limit(1).execute())
            if res.data:
                fila = res.data[0]
                return {
                    "status": "success",
                    "peso": fila.get("peso", 70),
                    "altura": fila.get("altura") or 170,
                    "objetivo": ID_A_OBJETIVO.get(fila.get("id_objetivo"), "mantener"),
                }
            return defecto
        except Exception as e:
            return {**defecto, "status": "error", "message": _mensaje_error(e)}

    # Guarda peso, altura y objetivo, y registra el peso en el historial
    def guardar_perfil(self, peso, altura, objetivo):
        if not self._usuario:
            return {"status": "error", "message": "No hay sesión iniciada"}
        try:
            peso = float(peso)
            altura = float(altura)
            if not (1 <= peso <= 500):
                return {"status": "error", "message": "Peso fuera de rango"}
            if not (50 <= altura <= 250):
                return {"status": "error", "message": "Altura fuera de rango"}
            id_objetivo = OBJETIVO_A_ID.get(objetivo, OBJETIVO_A_ID["mantener"])

            sb = get_supabase()
            id_usuario = self._usuario["id_usuario"]
            datos = {"peso": peso, "altura": altura, "id_objetivo": id_objetivo}

            existe = sb.table("perfil_usuario").select("id_perfil").eq("id_usuario", id_usuario).limit(1).execute().data
            if existe:
                sb.table("perfil_usuario").update(datos).eq("id_usuario", id_usuario).execute()
            else:
                datos.update({
                    "id_perfil": _siguiente_id(sb, "perfil_usuario", "id_perfil"),
                    "id_usuario": id_usuario,
                    "id_genero": GENERO_A_ID["no_especificado"],
                })
                sb.table("perfil_usuario").insert(datos).execute()

            try:
                sb.table("historial_peso").insert({
                    "id_historial": _siguiente_id(sb, "historial_peso", "id_historial"),
                    "id_usuario": id_usuario,
                    "peso": peso,
                }).execute()
            except Exception:
                pass
            return {"status": "success"}
        except Exception as e:
            return {"status": "error", "message": _mensaje_error(e)}

    # Agua tomada por día
    def obtener_hidratacion(self, desde=None):
        """Vasos de agua por día desde la fecha indicada (YYYY-MM-DD)."""
        if not self._usuario:
            return {"status": "success", "registros": []}
        try:
            q = (get_supabase().table("hidratacion")
                 .select("fecha, vasos")
                 .eq("id_usuario", self._usuario["id_usuario"]))
            if desde:
                q = q.gte("fecha", datetime.date.fromisoformat(str(desde)).isoformat())
            res = q.order("fecha").execute()
            return {
                "status": "success",
                "registros": [{"fecha": str(f["fecha"])[:10], "vasos": f["vasos"]} for f in (res.data or [])],
            }
        except Exception as e:
            return {"status": "error", "message": _mensaje_error(e), "registros": []}

    # Agua de un día
    def guardar_hidratacion(self, fecha, vasos):
        """Guarda el total de vasos de un día (crea o actualiza el registro)."""
        if not self._usuario:
            return {"status": "error", "message": "No hay sesión iniciada"}
        try:
            fecha = datetime.date.fromisoformat(str(fecha)).isoformat()
            vasos = int(vasos)
            if not (0 <= vasos <= 40):
                return {"status": "error", "message": "Cantidad de vasos fuera de rango"}

            sb = get_supabase()
            id_usuario = self._usuario["id_usuario"]
            existe = (sb.table("hidratacion").select("id_hidratacion")
                      .eq("id_usuario", id_usuario).eq("fecha", fecha).limit(1).execute().data)
            if existe:
                (sb.table("hidratacion")
                   .update({"vasos": vasos, "updated_at": datetime.datetime.now().isoformat()})
                   .eq("id_hidratacion", existe[0]["id_hidratacion"]).execute())
            else:
                sb.table("hidratacion").insert({
                    "id_hidratacion": _siguiente_id(sb, "hidratacion", "id_hidratacion"),
                    "id_usuario": id_usuario,
                    "fecha": fecha,
                    "vasos": vasos,
                }).execute()
            return {"status": "success"}
        except Exception as e:
            return {"status": "error", "message": _mensaje_error(e)}

    # Devuelve el plan semanal del usuario
    def obtener_plan(self):
        if not self._usuario:
            return {"status": "success", "plan": []}
        try:
            res = (get_supabase().table("plan_semanal")
                   .select("id_dia, id_comida, id_alimento, cantidad, unidad")
                   .eq("id_usuario", self._usuario["id_usuario"])
                   .order("id_plan")
                   .execute())

            plan = [
                {
                    "dia": ID_A_DIA.get(f["id_dia"]),
                    "comida": ID_A_COMIDA.get(f["id_comida"]),
                    "alimento_id": ID_A_ALIMENTO.get(f["id_alimento"]),
                    "cantidad": f["cantidad"],
                    "unidad": f["unidad"],
                }
                for f in (res.data or [])
                if f["id_dia"] in ID_A_DIA and f["id_comida"] in ID_A_COMIDA and f["id_alimento"] in ID_A_ALIMENTO
            ]
            return {"status": "success", "plan": plan}
        except Exception as e:
            return {"status": "error", "message": _mensaje_error(e), "plan": []}

    # Reemplaza el plan: inserta lo nuevo y luego borra lo viejo (si falla a la mitad no se pierde el plan anterior)
    def guardar_plan(self, items):
        if not self._usuario:
            return {"status": "error", "message": "No hay sesión iniciada"}
        try:
            sb = get_supabase()
            uid = self._usuario["id_usuario"]
            siguiente_id_plan = _siguiente_id(sb, "plan_semanal", "id_plan")

            filas = []
            for it in items or []:
                cantidad = float(it.get("cantidad", 0))
                id_dia = DIA_A_ID.get(it.get("dia"))
                id_comida = COMIDA_A_ID.get(it.get("comida"))
                id_alimento = ALIMENTO_A_ID.get(str(it.get("alimento_id")))
                if (id_dia is None or id_comida is None or id_alimento is None
                        or it.get("unidad") not in UNIDADES or cantidad <= 0):
                    continue
                filas.append({
                    "id_plan": siguiente_id_plan + len(filas),
                    "id_usuario": uid,
                    "id_dia": id_dia,
                    "id_comida": id_comida,
                    "id_alimento": id_alimento,
                    "cantidad": cantidad,
                    "unidad": it["unidad"],
                })

            viejos = sb.table("plan_semanal").select("id_plan").eq("id_usuario", uid).execute().data or []
            if filas:
                sb.table("plan_semanal").insert(filas).execute()
            ids_viejos = [r["id_plan"] for r in viejos]
            if ids_viejos:
                sb.table("plan_semanal").delete().in_("id_plan", ids_viejos).execute()
            return {"status": "success", "guardados": len(filas)}
        except Exception as e:
            return {"status": "error", "message": _mensaje_error(e)}


# Punto de entrada: arma el HTML con CSS y JS incrustados y abre la ventana
if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.abspath(__file__))

    def _leer(nombre):
        with open(os.path.join(base_dir, nombre), "r", encoding="utf-8") as f:
            return f.read()

    html = _leer("index.html")
    css = _leer("styles.css")
    js = _leer("script.js")

    # Se incrustan styles.css y script.js dentro del HTML (por eso esas etiquetas de index.html no deben cambiar)
    html = html.replace(
        '<link rel="stylesheet" type="text/css" href="styles.css">',
        f"<style>\n{css}\n</style>",
    )
    html = html.replace(
        '<script src="script.js"></script>',
        f"<script>\n{js}\n</script>",
    )

    try:
        webview.settings["ALLOW_DOWNLOADS"] = True
    except Exception:
        pass

    # Crea la ventana de escritorio y le conecta la API de Python
    api = API()
    webview.create_window(
        title="NutriPlan Desktop",
        html=html,
        js_api=api,
        width=1200,
        height=800,
        min_size=(360, 600),
    )
    try:
        webview.start(private_mode=False)
    except TypeError:
        webview.start()