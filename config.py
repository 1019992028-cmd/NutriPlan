"""Configuración de NutriPlan."""
import os
import secrets
from datetime import timedelta

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_DIR = os.path.join(BASE_DIR, "database")
DB_PATH = os.path.join(DB_DIR, "nutriplan.db")
os.makedirs(DB_DIR, exist_ok=True)   # SQLite necesita que la carpeta exista


def _clave_secreta():
    """Usa NUTRIPLAN_SECRET_KEY si existe; si no, genera una y la guarda en
    database/.secret_key para que las sesiones sobrevivan a un reinicio."""
    clave = os.environ.get("NUTRIPLAN_SECRET_KEY")
    if clave:
        return clave
    ruta = os.path.join(DB_DIR, ".secret_key")
    if os.path.exists(ruta):
        with open(ruta, "r", encoding="utf-8") as f:
            return f.read().strip()
    clave = secrets.token_hex(32)
    with open(ruta, "w", encoding="utf-8") as f:
        f.write(clave)
    return clave


def _url_base_de_datos():
    """DATABASE_URL (Render/Postgres) si existe; si no, el SQLite local.

    Render entrega la URL como «postgres://...», pero SQLAlchemy 2 solo reconoce
    «postgresql://...», así que se corrige el prefijo.
    """
    url = os.environ.get("DATABASE_URL")
    if not url:
        return "sqlite:///" + DB_PATH.replace("\\", "/")
    if url.startswith("postgres://"):
        url = "postgresql://" + url[len("postgres://"):]
    return url


PRODUCCION = os.environ.get("NUTRIPLAN_PRODUCTION") == "1"


class Config:
    SECRET_KEY = _clave_secreta()
    SQLALCHEMY_DATABASE_URI = _url_base_de_datos()
    SQLALCHEMY_ENGINE_OPTIONS = {"pool_pre_ping": True}   # reconecta si Postgres cerró una conexión inactiva
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Cookies de sesión
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    SESSION_COOKIE_SECURE = PRODUCCION          # exige HTTPS en producción
    REMEMBER_COOKIE_DURATION = timedelta(days=30)
    REMEMBER_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_SAMESITE = "Lax"
    REMEMBER_COOKIE_SECURE = PRODUCCION

    # El avatar llega como imagen en base64 (~30 KB); 1 MB es de sobra para cualquier petición
    MAX_CONTENT_LENGTH = 1 * 1024 * 1024
