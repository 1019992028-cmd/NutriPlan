# Diagnóstico: revisa paso a paso que Python, las librerías y Supabase funcionen
import sys
import uuid
from importlib import metadata


def version(pkg):
    try:
        return metadata.version(pkg)
    except Exception:
        return "NO INSTALADO"


# Convierte un error técnico en una sugerencia de qué revisar
def pista(err: str) -> str:
    e = err.lower()
    if "invalid api key" in e or "jwt" in e:
        return "→ Clave inválida o supabase muy viejo. Ejecuta: pip install -U supabase"
    if "42501" in err or "permission denied" in e:
        return "→ Permisos: vuelve a ejecutar tu BD_Setup.sql completo (incluye los GRANT y las políticas)."
    if "row-level security" in e:
        return "→ RLS bloquea la operación: vuelve a ejecutar tu BD_Setup.sql completo."
    if "pgrst205" in e or "could not find the table" in e or "does not exist" in e:
        return "→ La tabla no existe en ESTE proyecto. ¿Ejecutaste el SQL en el proyecto correcto (jwhaqamaiuvsifrffrjo)?"
    if "pgrst204" in e or "could not find the" in e:
        return "→ Falta una columna: revisa que tu tabla tenga exactamente los nombres id_x que usa este diagnóstico."
    if "null value in column" in e and "id_" in e:
        return "→ Tu tabla no tiene autoincremento (SERIAL/IDENTITY): hay que calcular el id a mano antes de insertar (esto ya lo hace app.py con _siguiente_id)."
    if any(x in e for x in ("connect", "timed out", "getaddrinfo", "resolve", "network")):
        return "→ Sin conexión a internet / firewall / proxy."
    return ""


# Ejecuta una prueba y muestra OK o FALLA
def paso(nombre, fn):
    try:
        r = fn()
        print(f"  OK     {nombre}" + (f"  ({r})" if r else ""))
        return True
    except Exception as ex:
        txt = str(ex)
        print(f"  FALLA  {nombre}\n         {txt}\n         {pista(txt)}")
        return False


# Versiones instaladas
print("Python:", sys.version.split()[0])
for p in ("supabase", "bcrypt", "pywebview"):
    print(f"  {p}: {version(p)}")
print()

# Conexión a Supabase
from conexion import get_supabase, SUPABASE_URL  # noqa: E402

print("Proyecto:", SUPABASE_URL)
sb = None


def _cliente():
    global sb
    sb = get_supabase()


# Siguiente id libre de una tabla
def _siguiente_id(tabla, columna):
    res = sb.table(tabla).select(columna).order(columna, desc=True).limit(1).execute()
    return (res.data[0][columna] + 1) if res.data else 1


if not paso("Crear cliente Supabase", _cliente):
    sys.exit(1)

# Prueba de lectura de cada tabla
paso("Leer tabla usuarios", lambda: sb.table("usuarios").select("id_usuario").limit(1).execute() and None)
paso("Leer tabla perfil_usuario", lambda: sb.table("perfil_usuario").select("id_usuario, id_genero, altura").limit(1).execute() and None)
paso("Leer tabla plan_semanal", lambda: sb.table("plan_semanal").select("id_plan").limit(1).execute() and None)
paso("Leer tabla historial_peso", lambda: sb.table("historial_peso").select("id_historial").limit(1).execute() and None)
paso("Leer tabla hidratacion", lambda: sb.table("hidratacion").select("id_hidratacion").limit(1).execute() and None)
paso("Leer tabla alimentos (catálogo)", lambda: sb.table("alimentos").select("id_alimento").limit(1).execute() and None)
paso("Leer tabla categorias", lambda: sb.table("categorias").select("id_categoria").limit(1).execute() and None)
paso("Leer tabla generos", lambda: sb.table("generos").select("id_genero").limit(1).execute() and None)
paso("Leer tabla objetivos", lambda: sb.table("objetivos").select("id_objetivo").limit(1).execute() and None)
paso("Leer tabla dias", lambda: sb.table("dias").select("id_dia").limit(1).execute() and None)
paso("Leer tabla comidas", lambda: sb.table("comidas").select("id_comida").limit(1).execute() and None)

# Prueba de escritura: crea un usuario temporal, su perfil y lo borra
email = f"diagnostico-{uuid.uuid4().hex[:8]}@example.com"
nuevo = {}


def _insertar():
    nuevo_id = _siguiente_id("usuarios", "id_usuario")
    r = sb.table("usuarios").insert({
        "id_usuario": nuevo_id, "nombre": "Prueba", "email": email, "password_hash": "x",
    }).execute()
    if not r.data:
        raise RuntimeError("El insert no devolvió datos (falta política SELECT o RLS)")
    nuevo["id"] = r.data[0]["id_usuario"]
    return f"id_usuario {nuevo['id']}"


def _crear_perfil():
    id_perfil = _siguiente_id("perfil_usuario", "id_perfil")
    sb.table("perfil_usuario").insert({
        "id_perfil": id_perfil, "id_usuario": nuevo["id"], "id_genero": 5, "id_objetivo": 2,
        "peso": 70, "altura": 170,
    }).execute()


def _borrar():
    sb.table("perfil_usuario").delete().eq("id_usuario", nuevo["id"]).execute()
    sb.table("usuarios").delete().eq("id_usuario", nuevo["id"]).execute()


if paso("Insertar usuario de prueba", _insertar):
    paso("Crear perfil del usuario", _crear_perfil)
    paso("Borrar usuario de prueba", _borrar)

print("\nSi todo salió OK y el registro aún falla, el problema está en la app: copia el mensaje rojo que aparece "
      "en pantalla y/o lo que imprime la terminal donde ejecutas app.py.")