"""Pruebas de la API (Fases 10 y 11 del plan de acción).

Requiere las dependencias instaladas:  pip install -r requirements.txt
Ejecutar:  python -m unittest tests.test_api -v
Usa una base de datos SQLite en memoria; no toca database/nutriplan.db.
"""
import os
import sys
import unittest
from datetime import date

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app  # noqa: E402


def nuevo_cliente(app):
    return app.test_client()


class BaseApi(unittest.TestCase):
    def setUp(self):
        self.app = create_app({"TESTING": True, "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:"})
        self.c = nuevo_cliente(self.app)

    def registrar(self, cliente, email="ana@correo.com", nombre="Ana Pérez", password="secreto1"):
        return cliente.post("/api/registro", json={"nombre": nombre, "email": email, "password": password,
                                                    "genero": "femenino"})


class TestCuentas(BaseApi):
    def test_registro_login_logout(self):
        r = self.registrar(self.c)
        self.assertEqual(r.status_code, 201)
        self.assertEqual(r.json["user"]["email"], "ana@correo.com")
        self.assertNotIn("password", str(r.json))

        self.assertEqual(self.c.post("/api/logout", json={}).status_code, 200)
        self.assertEqual(self.c.get("/api/perfil").status_code, 401)

        ok = self.c.post("/api/login", json={"email": "ANA@correo.com", "password": "secreto1"})
        self.assertEqual(ok.status_code, 200)
        self.assertEqual(self.c.get("/api/perfil").status_code, 200)

    def test_contrasena_no_se_guarda_en_texto_plano(self):
        from models import Usuario, db
        self.registrar(self.c)
        with self.app.app_context():
            u = db.session.query(Usuario).first()
            self.assertNotEqual(u.password_hash, "secreto1")
            self.assertTrue(u.check_password("secreto1"))

    def test_validaciones_de_registro(self):
        casos = [
            {"nombre": "A", "email": "a@b.co", "password": "secreto1", "genero": "femenino"},
            {"nombre": "Ana", "email": "no-es-correo", "password": "secreto1", "genero": "femenino"},
            {"nombre": "Ana", "email": "a@b.co", "password": "123", "genero": "femenino"},
            {"nombre": "Ana", "email": "a@b.co", "password": "x" * 73, "genero": "femenino"},
            {"nombre": "Ana", "email": "a@b.co", "password": "secreto1", "genero": "inventado"},
        ]
        for datos in casos:
            self.assertEqual(self.c.post("/api/registro", json=datos).status_code, 400, datos)

    def test_correo_duplicado(self):
        self.registrar(self.c)
        self.assertEqual(self.registrar(nuevo_cliente(self.app)).status_code, 409)

    def test_login_incorrecto(self):
        self.registrar(self.c)
        self.c.post("/api/logout", json={})
        r = self.c.post("/api/login", json={"email": "ana@correo.com", "password": "mala"})
        self.assertEqual(r.status_code, 401)

    def test_entrar_por_id_solo_con_sesion_propia(self):
        r = self.registrar(self.c)
        uid = r.json["user"]["id"]
        self.assertEqual(self.c.post("/api/sesion/entrar", json={"id": uid}).status_code, 200)
        otro = nuevo_cliente(self.app)  # navegador sin sesión
        self.assertEqual(otro.post("/api/sesion/entrar", json={"id": uid}).status_code, 401)

    def test_rutas_privadas_sin_sesion(self):
        for metodo, ruta in [("get", "/api/perfil"), ("get", "/api/planes"), ("get", "/api/planes/actual"),
                             ("get", "/api/catalogos"), ("get", "/api/hidratacion"), ("put", "/api/planes/1")]:
            self.assertEqual(getattr(self.c, metodo)(ruta).status_code, 401, ruta)


class TestPerfil(BaseApi):
    def setUp(self):
        super().setUp()
        self.registrar(self.c)

    def test_guardar_y_leer_perfil_con_edad(self):
        r = self.c.put("/api/perfil", json={"peso": 62.5, "altura": 165, "objetivo": "bajar", "edad": 30})
        self.assertEqual(r.status_code, 200)
        p = self.c.get("/api/perfil").json
        self.assertEqual((p["peso"], p["altura"], p["objetivo"], p["edad"]), (62.5, 165, "bajar", 30))
        h = self.c.get("/api/perfil/historial-peso").json["historial"]
        self.assertEqual(h[-1]["peso"], 62.5)

    def test_perfil_invalido(self):
        for datos in [{"peso": 5, "altura": 170, "objetivo": "mantener"},
                      {"peso": 70, "altura": 999, "objetivo": "mantener"},
                      {"peso": 70, "altura": 170, "objetivo": "volar"},
                      {"peso": 70, "altura": 170, "objetivo": "mantener", "edad": 500}]:
            self.assertEqual(self.c.put("/api/perfil", json=datos).status_code, 400, datos)

    def test_avatar_invalido(self):
        r = self.c.put("/api/usuario", json={"nombre": "Ana", "email": "ana@correo.com", "genero": "femenino",
                                              "avatar": "javascript:alert(1)"})
        self.assertEqual(r.status_code, 400)


class TestPlanes(BaseApi):
    def setUp(self):
        super().setUp()
        self.registrar(self.c)

    def plan_de_esta_semana(self, cliente=None):
        """Crea el plan de la semana actual (los planes son opcionales) y devuelve su id."""
        r = (cliente or self.c).post("/api/planes", json={"fecha_inicio": date.today().isoformat()})
        self.assertEqual(r.status_code, 201)
        return r.json["plan"]["id"]

    def test_catalogos(self):
        r = self.c.get("/api/catalogos").json
        self.assertEqual(len(r["alimentos"]), 116)
        self.assertEqual(len(r["tipos_comida"]), 5)
        self.assertIsInstance(r["alimentos"][0]["id"], str)
        self.assertIn("fibra", r["alimentos"][0])

    def test_el_plan_es_opcional_y_no_se_crea_solo(self):
        hoy = date.today().isoformat()
        # Sin plan: la respuesta es válida, con info = None, y no se crea nada
        r = self.c.get(f"/api/planes/actual?hoy={hoy}")
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json["plan"], [])
        self.assertIsNone(r.json["info"])
        self.assertEqual(self.c.get("/api/planes").json["planes"], [])

        # El usuario decide crearlo: ahora sí aparece como plan de la semana
        pid = self.plan_de_esta_semana()
        info = self.c.get(f"/api/planes/actual?hoy={hoy}").json["info"]
        self.assertEqual(info["id"], pid)
        self.assertTrue(info["fecha_inicio"] <= hoy <= info["fecha_fin"])

    def test_plan_de_otra_semana_no_se_muestra_como_actual(self):
        self.c.post("/api/planes", json={"fecha_inicio": "2031-03-12"})
        r = self.c.get(f"/api/planes/actual?hoy={date.today().isoformat()}").json
        self.assertIsNone(r["info"])

    def test_flujo_completo(self):
        pid = self.plan_de_esta_semana()
        items = [
            {"dia": "1", "comida": "desayuno", "alimento_id": "3", "cantidad": 50, "unidad": "g"},
            {"dia": "1", "comida": "almuerzo", "alimento_id": "1", "cantidad": 150, "unidad": "g"},
            {"dia": "1", "comida": "merienda", "alimento_id": "57", "cantidad": 1, "unidad": "unidad"},
            {"dia": "7", "comida": "cena", "alimento_id": "35", "cantidad": 0.15, "unidad": "kg"},
        ]
        self.assertEqual(self.c.put(f"/api/planes/{pid}", json={"items": items}).status_code, 200)

        self.c.post("/api/logout", json={})
        self.c.post("/api/login", json={"email": "ana@correo.com", "password": "secreto1"})
        r = self.c.get(f"/api/planes/{pid}").json
        self.assertEqual(len(r["plan"]), 4)
        self.assertEqual(r["plan"][0]["alimento_id"], "3")

        resumen = self.c.get(f"/api/planes/{pid}/resumen").json["resumen"]
        self.assertEqual(resumen["comidas"]["1"]["almuerzo"]["kcal"], 195)
        self.assertGreater(resumen["semana"]["fibra"], 0)

        # Guardar de nuevo reemplaza (no duplica)
        self.c.put(f"/api/planes/{pid}", json={"items": items[:1]})
        self.assertEqual(len(self.c.get(f"/api/planes/{pid}").json["plan"]), 1)

    def test_datos_invalidos_en_plan(self):
        pid = self.plan_de_esta_semana()
        base = {"dia": "1", "comida": "desayuno", "alimento_id": "1", "cantidad": 100, "unidad": "g"}
        malos = [dict(base, cantidad=-5), dict(base, cantidad=0), dict(base, cantidad="abc"),
                 dict(base, unidad="l"), dict(base, dia="funday"), dict(base, dia="8"), dict(base, dia="0"), dict(base, comida="brunch"),
                 dict(base, alimento_id="9999"), dict(base, alimento_id="x")]
        for mal in malos:
            self.assertEqual(self.c.put(f"/api/planes/{pid}", json={"items": [mal]}).status_code, 400, mal)

    def test_un_usuario_no_ve_el_plan_de_otro(self):
        pid = self.plan_de_esta_semana()
        otro = nuevo_cliente(self.app)
        self.registrar(otro, email="luis@correo.com", nombre="Luis Gómez")
        self.assertEqual(otro.get(f"/api/planes/{pid}").status_code, 404)
        self.assertEqual(otro.put(f"/api/planes/{pid}", json={"items": []}).status_code, 404)
        self.assertEqual(otro.delete(f"/api/planes/{pid}").status_code, 404)
        self.assertEqual(otro.get(f"/api/planes/{pid}/resumen").status_code, 404)
        self.assertNotIn(pid, [p["id"] for p in otro.get("/api/planes").json["planes"]])

    def test_historial_y_copiar(self):
        pid = self.plan_de_esta_semana()
        self.c.put(f"/api/planes/{pid}", json={"items": [
            {"dia": "2", "comida": "cena", "alimento_id": "22", "cantidad": 200, "unidad": "g"}]})
        r = self.c.post("/api/planes", json={"nombre": "Siguiente", "fecha_inicio": "2031-03-12", "copiar_de": pid})
        self.assertEqual(r.status_code, 201)
        self.assertEqual(r.json["plan"]["fecha_inicio"], "2031-03-12")   # ya no se ajusta al lunes
        self.assertEqual(r.json["plan"]["fecha_fin"], "2031-03-18")      # 7 días: miércoles a martes
        self.assertEqual(len(r.json["rows"]), 1)
        self.assertEqual(r.json["rows"][0]["dia"], "2")                  # se copia día a día
        self.assertEqual(len(self.c.get("/api/planes").json["planes"]), 2)
        # fechas que se cruzan con ese plan → conflicto
        dup = self.c.post("/api/planes", json={"fecha_inicio": "2031-03-14"})
        self.assertEqual(dup.status_code, 409)

    def test_el_plan_puede_empezar_cualquier_dia_y_cruzar_la_semana(self):
        # 2031-03-12 es miércoles: el plan va de miércoles a martes de la semana siguiente
        r = self.c.post("/api/planes", json={"fecha_inicio": "2031-03-12"})
        self.assertEqual(r.status_code, 201)
        self.assertEqual((r.json["plan"]["fecha_inicio"], r.json["plan"]["fecha_fin"]), ("2031-03-12", "2031-03-18"))
        pid = r.json["plan"]["id"]
        # el 7.º día (martes 18) existe y se puede usar
        item = {"dia": "7", "comida": "cena", "alimento_id": "22", "cantidad": 100, "unidad": "g"}
        self.assertEqual(self.c.put(f"/api/planes/{pid}", json={"items": [item]}).status_code, 200)
        # y «Hoy» lo encuentra por fecha dentro del rango, aunque cruce la semana
        actual = self.c.get(f"/api/planes/actual?hoy=2031-03-16").json
        self.assertEqual(actual["info"]["id"], pid)

    def test_duracion_personalizada(self):
        r = self.c.post("/api/planes", json={"fecha_inicio": "2031-03-12", "dias": 10})
        self.assertEqual(r.status_code, 201)
        self.assertEqual(r.json["plan"]["fecha_fin"], "2031-03-21")
        pid = r.json["plan"]["id"]
        item = {"dia": "10", "comida": "cena", "alimento_id": "22", "cantidad": 100, "unidad": "g"}
        self.assertEqual(self.c.put(f"/api/planes/{pid}", json={"items": [item]}).status_code, 200)
        fuera = dict(item, dia="11")
        self.assertEqual(self.c.put(f"/api/planes/{pid}", json={"items": [fuera]}).status_code, 400)

    def test_duracion_invalida(self):
        for dias in (0, -3, 32, 2.5, "abc"):
            r = self.c.post("/api/planes", json={"fecha_inicio": "2031-03-12", "dias": dias})
            self.assertEqual(r.status_code, 400, dias)
        self.assertEqual(self.c.get("/api/planes").json["planes"], [])

    def test_no_se_pueden_cruzar_dos_planes(self):
        self.c.post("/api/planes", json={"fecha_inicio": "2031-03-12"})            # 12 → 18
        for inicio, dias in (("2031-03-18", 7), ("2031-03-08", 7), ("2031-03-14", 2), ("2031-03-01", 31)):
            r = self.c.post("/api/planes", json={"fecha_inicio": inicio, "dias": dias})
            self.assertEqual(r.status_code, 409, (inicio, dias))
        # justo antes y justo después sí caben
        self.assertEqual(self.c.post("/api/planes", json={"fecha_inicio": "2031-03-05"}).status_code, 201)   # 5 → 11
        self.assertEqual(self.c.post("/api/planes", json={"fecha_inicio": "2031-03-19"}).status_code, 201)   # 19 → 25

    def test_extender_plan(self):
        r = self.c.post("/api/planes", json={"fecha_inicio": "2031-03-12"})
        pid = r.json["plan"]["id"]
        item = {"dia": "2", "comida": "cena", "alimento_id": "22", "cantidad": 100, "unidad": "g"}
        self.c.put(f"/api/planes/{pid}", json={"items": [item]})

        e = self.c.post(f"/api/planes/{pid}/extender", json={"dias": 7})
        self.assertEqual(e.status_code, 200)
        self.assertEqual(e.json["plan"]["fecha_fin"], "2031-03-25")                  # 14 días en total
        self.assertEqual(e.json["rows"], [item])                                      # lo anterior sigue igual
        nuevo = dict(item, dia="14")
        self.assertEqual(self.c.put(f"/api/planes/{pid}", json={"items": [item, nuevo]}).status_code, 200)
        self.assertEqual(self.c.get(f"/api/planes/{pid}").json["info"]["fecha_fin"], "2031-03-25")

        # un día más
        e = self.c.post(f"/api/planes/{pid}/extender", json={"dias": 1})
        self.assertEqual(e.json["plan"]["fecha_fin"], "2031-03-26")

    def test_extender_plan_validaciones(self):
        pid = self.c.post("/api/planes", json={"fecha_inicio": "2031-03-12"}).json["plan"]["id"]
        for dias in (None, 0, -1, 1.5, "x", 32):
            self.assertEqual(self.c.post(f"/api/planes/{pid}/extender", json={"dias": dias}).status_code, 400, dias)
        # máximo 31 días en total: ya tiene 7, no caben 25 más
        self.assertEqual(self.c.post(f"/api/planes/{pid}/extender", json={"dias": 25}).status_code, 400)
        self.assertEqual(self.c.post(f"/api/planes/{pid}/extender", json={"dias": 24}).status_code, 200)
        self.assertEqual(self.c.get(f"/api/planes/{pid}").json["info"]["fecha_fin"], "2031-04-11")

    def test_extender_no_puede_pisar_el_plan_siguiente(self):
        a = self.c.post("/api/planes", json={"fecha_inicio": "2031-03-12"}).json["plan"]["id"]    # 12 → 18
        self.c.post("/api/planes", json={"fecha_inicio": "2031-03-22"})                          # 22 → 28
        self.assertEqual(self.c.post(f"/api/planes/{a}/extender", json={"dias": 3}).status_code, 200)   # → 21
        self.assertEqual(self.c.post(f"/api/planes/{a}/extender", json={"dias": 1}).status_code, 409)  # 22 ya es del otro
        self.assertEqual(self.c.get(f"/api/planes/{a}").json["info"]["fecha_fin"], "2031-03-21")

    def test_un_usuario_no_puede_extender_el_plan_de_otro(self):
        pid = self.plan_de_esta_semana()
        otro = nuevo_cliente(self.app)
        self.registrar(otro, email="luis@correo.com", nombre="Luis Gómez")
        self.assertEqual(otro.post(f"/api/planes/{pid}/extender", json={"dias": 3}).status_code, 404)
        self.assertEqual(nuevo_cliente(self.app).post(f"/api/planes/{pid}/extender", json={"dias": 3}).status_code, 401)

    def test_eliminar_plan(self):
        pid = self.plan_de_esta_semana()
        self.assertEqual(self.c.delete(f"/api/planes/{pid}").status_code, 200)
        self.assertEqual(self.c.get(f"/api/planes/{pid}").status_code, 404)


DIAS = ["lunes", "martes", "miercoles", "jueves", "viernes", "sabado", "domingo"]   # días de cada menú
POS = ["1", "2", "3", "4", "5", "6", "7"]                                          # días del plan (posición)
LUNES = "2031-03-10"                                                               # un lunes: posición 1 = lunes


class TestMenus(BaseApi):
    def setUp(self):
        super().setUp()
        self.registrar(self.c)
        self.pid = self.c.post("/api/planes", json={"fecha_inicio": LUNES}).json["plan"]["id"]

    def aplicar(self, menu, dias, cliente=None, pid=None):
        return (cliente or self.c).post(f"/api/planes/{pid or self.pid}/menu", json={"menu": menu, "dias": dias})

    def test_listar_menus(self):
        r = self.c.get("/api/menus")
        self.assertEqual(r.status_code, 200)
        menus = {m["id"]: m for m in r.json["menus"]}
        self.assertEqual(set(menus), {"fitness", "vegetariano"})
        for m in menus.values():
            self.assertEqual(set(m["kcal_por_dia"]), set(DIAS))
            self.assertTrue(all(k > 1000 for k in m["kcal_por_dia"].values()), m)
            self.assertTrue(m["descripcion"])

    def test_aplicar_a_toda_la_semana(self):
        r = self.aplicar("fitness", POS)
        self.assertEqual(r.status_code, 200)
        self.assertEqual({f["dia"] for f in r.json["rows"]}, set(POS))
        self.assertEqual(len(r.json["rows"]), r.json["aplicados"])
        # las 5 comidas de cada día quedan con alimentos
        self.assertEqual({(f["dia"], f["comida"]) for f in r.json["rows"]}.__len__(), 7 * 5)
        # lo que devuelve es lo que quedó guardado
        self.assertEqual(self.c.get(f"/api/planes/{self.pid}").json["plan"], r.json["rows"])
        # y el resumen del servidor coincide con las kcal anunciadas por el menú
        resumen = self.c.get(f"/api/planes/{self.pid}/resumen").json["resumen"]["dias"]
        anunciadas = {m["id"]: m for m in self.c.get("/api/menus").json["menus"]}["fitness"]["kcal_por_dia"]
        self.assertEqual({dia: resumen[pos]["kcal"] for dia, pos in zip(DIAS, POS)}, anunciadas)

    def test_aplicar_solo_a_algunos_dias_reemplaza_esos_dias_y_respeta_los_demas(self):
        previo = [
            {"dia": "1", "comida": "desayuno", "alimento_id": "106", "cantidad": 50, "unidad": "g"},   # se reemplaza
            {"dia": "2", "comida": "cena", "alimento_id": "98", "cantidad": 80, "unidad": "g"},       # se conserva
        ]
        self.c.put(f"/api/planes/{self.pid}", json={"items": previo})

        r = self.aplicar("vegetariano", ["1", "3"])
        self.assertEqual(r.status_code, 200)
        rows = r.json["rows"]
        self.assertEqual({f["dia"] for f in rows}, {"1", "2", "3"})
        self.assertNotIn(("1", "106"), {(f["dia"], f["alimento_id"]) for f in rows})   # cereal azucarado ya no está
        martes = [f for f in rows if f["dia"] == "2"]
        self.assertEqual([(f["comida"], f["alimento_id"], f["cantidad"]) for f in martes], [("cena", "98", 80.0)])

    def test_el_menu_se_aplica_segun_el_dia_de_la_semana_del_plan(self):
        # Plan que empieza un miércoles (2031-03-12): su día 1 es miércoles y recibe el miércoles del menú,
        # que es el mismo que recibe el día 3 de un plan que empieza en lunes.
        pid = self.c.post("/api/planes", json={"fecha_inicio": "2031-03-12"}).json["plan"]["id"]
        en_miercoles = self.aplicar("fitness", ["1"], pid=pid).json["rows"]
        en_lunes = self.aplicar("fitness", ["3"], pid=self.pid).json["rows"]
        self.assertTrue(en_miercoles)
        self.assertEqual({f["dia"] for f in en_miercoles}, {"1"})
        self.assertEqual([(f["comida"], f["alimento_id"], f["cantidad"]) for f in en_miercoles],
                         [(f["comida"], f["alimento_id"], f["cantidad"]) for f in en_lunes])

    def test_menu_en_un_plan_largo_se_repite_cada_semana(self):
        pid = self.c.post("/api/planes", json={"fecha_inicio": LUNES, "dias": 14}).json["plan"]["id"]
        r = self.aplicar("fitness", ["1", "8"], pid=pid)      # primer y segundo lunes
        self.assertEqual(r.status_code, 200)
        self.assertEqual({f["dia"] for f in r.json["rows"]}, {"1", "8"})
        uno = [(f["comida"], f["alimento_id"]) for f in r.json["rows"] if f["dia"] == "1"]
        ocho = [(f["comida"], f["alimento_id"]) for f in r.json["rows"] if f["dia"] == "8"]
        self.assertEqual(uno, ocho)
        self.assertEqual(self.aplicar("fitness", ["15"], pid=pid).status_code, 400)

    def test_aplicar_dos_veces_no_duplica(self):
        a = self.aplicar("fitness", ["1"]).json["rows"]
        b = self.aplicar("fitness", ["1"]).json["rows"]
        self.assertEqual(a, b)

    def test_el_menu_aplicado_se_puede_editar_y_guardar(self):
        rows = self.aplicar("fitness", POS).json["rows"]
        self.assertEqual(self.c.put(f"/api/planes/{self.pid}", json={"items": rows[:3]}).status_code, 200)
        self.assertEqual(len(self.c.get(f"/api/planes/{self.pid}").json["plan"]), 3)

    def test_vegetariano_no_tiene_alimentos_de_origen_animal(self):
        rows = self.aplicar("vegetariano", POS).json["rows"]
        catalogo = {a["id"]: a for a in self.c.get("/api/catalogos").json["alimentos"]}
        from tests.test_menus import es_de_origen_animal
        usados = {catalogo[f["alimento_id"]]["nombre"] for f in rows}
        self.assertTrue(usados)
        self.assertEqual([n for n in usados if es_de_origen_animal(n)], [])

    def test_validaciones_al_aplicar(self):
        self.assertEqual(self.aplicar("fitness", []).status_code, 400)
        self.assertEqual(self.aplicar("fitness", "1").status_code, 400)
        self.assertEqual(self.aplicar("fitness", ["1", "funday"]).status_code, 400)
        self.assertEqual(self.aplicar("fitness", ["lunes"]).status_code, 400)     # los días son posiciones del plan
        self.assertEqual(self.aplicar("fitness", ["0"]).status_code, 400)
        self.assertEqual(self.aplicar("fitness", ["8"]).status_code, 400)         # el plan solo tiene 7 días
        self.assertEqual(self.aplicar("keto", ["1"]).status_code, 404)
        self.assertEqual(self.aplicar("fitness", ["1"], pid=9999).status_code, 404)
        self.assertEqual(self.c.get(f"/api/planes/{self.pid}").json["plan"], [])   # no cambió nada

    def test_un_usuario_no_puede_aplicar_menus_al_plan_de_otro(self):
        otro = nuevo_cliente(self.app)
        self.registrar(otro, email="luis@correo.com", nombre="Luis Gómez")
        self.assertEqual(self.aplicar("fitness", ["1"], cliente=otro).status_code, 404)
        self.assertEqual(self.c.get(f"/api/planes/{self.pid}").json["plan"], [])

    def test_menus_requieren_sesion(self):
        anonimo = nuevo_cliente(self.app)
        self.assertEqual(anonimo.get("/api/menus").status_code, 401)
        self.assertEqual(self.aplicar("fitness", ["1"], cliente=anonimo).status_code, 401)

    # -- Menús ajustados al perfil (peso, altura, edad, género, objetivo) ------------------
    def perfil(self, peso, altura, edad, objetivo, cliente=None):
        r = (cliente or self.c).put("/api/perfil", json={"peso": peso, "altura": altura, "edad": edad, "objetivo": objetivo})
        self.assertEqual(r.status_code, 200)

    def promedio(self, menu_id, cliente=None):
        menus = {m["id"]: m for m in (cliente or self.c).get("/api/menus").json["menus"]}
        return menus[menu_id]["kcal_promedio"]

    def test_el_menu_se_ajusta_a_la_meta_del_usuario(self):
        from services.menus import rango_kcal
        casos = [(70, 170, 30, "mantener"), (55, 160, 25, "bajar"), (95, 185, 40, "subir"), (120, 190, 35, "bajar")]
        for peso, altura, edad, objetivo in casos:
            self.perfil(peso, altura, edad, objetivo)
            _min, _max, meta = rango_kcal(peso, altura, edad, "femenino", objetivo)
            for menu in ("fitness", "vegetariano"):
                prom = self.promedio(menu)
                # el promedio diario queda cerca de la meta (el redondeo de porciones deja unas pocas kcal de margen)
                self.assertAlmostEqual(prom / meta, 1, delta=0.06, msg=(peso, altura, edad, objetivo, menu, prom, meta))

    def test_el_objetivo_cambia_las_calorias_del_menu(self):
        self.perfil(70, 170, 30, "bajar")
        bajar = self.promedio("fitness")
        self.perfil(70, 170, 30, "mantener")
        mantener = self.promedio("fitness")
        self.perfil(70, 170, 30, "subir")
        subir = self.promedio("fitness")
        self.assertLess(bajar, mantener)
        self.assertLess(mantener, subir)

    def test_altura_y_edad_tambien_cuentan(self):
        self.perfil(70, 155, 60, "mantener")
        bajo_y_mayor = self.promedio("fitness")
        self.perfil(70, 190, 20, "mantener")
        alto_y_joven = self.promedio("fitness")
        self.assertLess(bajo_y_mayor, alto_y_joven)

    def test_lo_que_se_aplica_es_lo_que_se_anuncia(self):
        self.perfil(95, 185, 40, "subir")
        anunciadas = {m["id"]: m for m in self.c.get("/api/menus").json["menus"]}["fitness"]["kcal_por_dia"]
        r = self.aplicar("fitness", POS)
        self.assertEqual(r.status_code, 200)
        self.assertGreater(r.json["factor"], 1.1)                      # porciones más grandes que las del menú base
        resumen = self.c.get(f"/api/planes/{self.pid}/resumen").json["resumen"]["dias"]
        self.assertEqual({dia: resumen[pos]["kcal"] for dia, pos in zip(DIAS, POS)}, anunciadas)
        # las cantidades son «servibles»: g/ml de 5 en 5 y unidades de media en media
        catalogo = {a["id"]: a for a in self.c.get("/api/catalogos").json["alimentos"]}
        for f in r.json["rows"]:
            if catalogo[f["alimento_id"]]["unidad_base"] == "unidad":
                self.assertEqual(f["cantidad"] * 2, int(f["cantidad"] * 2), f)
            else:
                self.assertTrue(f["cantidad"] >= 1 and (f["cantidad"] < 10 or f["cantidad"] % 5 == 0), f)

    def test_el_menu_vegetariano_sigue_siendo_vegetal_al_ajustarlo(self):
        from tests.test_menus import es_de_origen_animal
        self.perfil(120, 190, 35, "subir")
        rows = self.aplicar("vegetariano", POS).json["rows"]
        catalogo = {a["id"]: a for a in self.c.get("/api/catalogos").json["alimentos"]}
        self.assertEqual([n for n in {catalogo[f["alimento_id"]]["nombre"] for f in rows} if es_de_origen_animal(n)], [])

    def test_cada_usuario_ve_su_propio_ajuste(self):
        otro = nuevo_cliente(self.app)
        self.registrar(otro, email="luis@correo.com", nombre="Luis Gómez")
        self.perfil(50, 155, 22, "bajar", cliente=otro)
        self.perfil(100, 185, 30, "subir")
        self.assertLess(self.promedio("fitness", cliente=otro), self.promedio("fitness"))
        meta = self.c.get("/api/menus").json["meta"]
        self.assertTrue(meta["min"] < meta["objetivo"] < meta["max"])

    def test_seed_de_menus_es_idempotente_y_repone_los_que_falten(self):
        from models import Menu, MenuItem, db
        from seed import seed_menus
        with self.app.app_context():
            antes = db.session.query(MenuItem).count()
            seed_menus()
            self.assertEqual(db.session.query(MenuItem).count(), antes)       # no duplica
            db.session.delete(Menu.query.filter_by(clave="fitness").first())  # una base que ya existía sin ese menú
            db.session.commit()
            seed_menus()
            self.assertEqual(db.session.query(Menu).count(), 2)
            self.assertEqual(db.session.query(MenuItem).count(), antes)


class TestHidratacion(BaseApi):
    def test_guardar_y_leer(self):
        self.registrar(self.c)
        hoy = date.today().isoformat()
        self.assertEqual(self.c.put("/api/hidratacion", json={"fecha": hoy, "vasos": 5}).status_code, 200)
        self.c.put("/api/hidratacion", json={"fecha": hoy, "vasos": 7})
        regs = self.c.get("/api/hidratacion?desde=" + hoy).json["registros"]
        self.assertEqual(regs, [{"fecha": hoy, "vasos": 7}])
        self.assertEqual(self.c.put("/api/hidratacion", json={"fecha": hoy, "vasos": 99}).status_code, 400)


if __name__ == "__main__":
    unittest.main()
