import sys
from app import create_app
from models import db, Usuario

app = create_app()

def listar():
    for u in Usuario.query.order_by(Usuario.id).all():
        print(f"{u.id:>3} | {u.nombre} | {u.email} | {u.fecha_creacion:%Y-%m-%d %H:%M}")

def buscar(email):
    return Usuario.query.filter_by(email=email.strip().lower()).first()

with app.app_context():
    cmd = sys.argv[1] if len(sys.argv) > 1 else "listar"

    if cmd == "listar":
        listar()

    elif cmd == "nombre":            # python admin.py nombre correo@x.com "Nuevo Nombre"
        u = buscar(sys.argv[2]); u.nombre = sys.argv[3]
        db.session.commit(); print("Nombre actualizado.")

    elif cmd == "clave":             # python admin.py clave correo@x.com NuevaClave123
        u = buscar(sys.argv[2]); u.set_password(sys.argv[3])
        db.session.commit(); print("Contraseña restablecida.")

    elif cmd == "borrar":            # python admin.py borrar correo@x.com
        u = buscar(sys.argv[2])
        if u and input(f"¿Borrar a {u.nombre} ({u.email}) y todos sus datos? (s/n): ") == "s":
            db.session.delete(u); db.session.commit(); print("Usuario eliminado.")

    else:
        print("Comandos: listar | nombre | clave | borrar")