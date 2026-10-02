# Conexión con Supabase (la base de datos en la nube)
from __future__ import annotations
import os
from supabase import create_client, Client

# Dirección y clave pública del proyecto (se pueden cambiar con variables de entorno)
SUPABASE_URL = os.environ.get("SUPABASE_URL", "https://jwhaqamaiuvsifrffrjo.supabase.co")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY", "sb_publishable_q47E-ArHO7RDRdJZQ2hq-w_kJfYtapp")

# Cliente compartido: se crea una sola vez
_client: Client | None = None


# Devuelve el cliente; se crea al primer uso para que el programa abra aunque no haya internet
def get_supabase() -> Client:
    """Crea el cliente la primera vez que se necesita (así el programa abre aunque no haya internet)."""
    global _client
    if _client is None:
        _client = create_client(SUPABASE_URL, SUPABASE_KEY)
    return _client


# Prueba rápida: ejecutar este archivo comprueba que la conexión funciona
if __name__ == "__main__":
    try:
        respuesta = get_supabase().table("usuarios").select("id_usuario,nombre,email").execute()
        print("Conexión exitosa. Usuarios registrados:", len(respuesta.data))
    except Exception as e:
        print("Error de conexión:", e)