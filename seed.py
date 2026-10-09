"""Carga los catálogos iniciales (idempotente: solo inserta si la tabla está vacía).

Uso manual:  python seed.py
"""
import seed_data as d
import seed_menus as m
from models import (Alimento, Categoria, Dia, Genero, Menu, MenuItem, Objetivo, TipoComida, db)


def _vacia(modelo):
    return db.session.query(modelo.id).first() is None


_UNIDAD_POR_BASE = {"g": "g", "ml": "ml", "unidad": "unidad"}


def seed_menus():
    """Inserta los menús de seed_menus.py que todavía no existan (por su clave).

    Los menús ya guardados no se modifican, así que se pueden agregar menús nuevos
    sin tocar los anteriores. Falla con un mensaje claro si un alimento no existe.
    """
    alimentos = {a.nombre: a for a in Alimento.query.all()}
    tipos = {t.clave: t.id for t in TipoComida.query.all()}
    orden_dia = {clave: orden for clave, _nombre, orden in d.DIAS}

    for clave, nombre, descripcion, orden, semana in m.MENUS:
        if Menu.query.filter_by(clave=clave).first():
            continue
        menu = Menu(clave=clave, nombre=nombre, descripcion=descripcion, orden=orden)
        for dia, comidas in semana.items():
            for comida, lista in comidas.items():
                for alimento_nombre, cantidad in lista:
                    alimento = alimentos.get(alimento_nombre)
                    if alimento is None:
                        raise ValueError(f"Menú «{nombre}»: el alimento «{alimento_nombre}» no existe en el catálogo.")
                    menu.items.append(MenuItem(
                        dia_semana=orden_dia[dia], tipo_id=tipos[comida], alimento_id=alimento.id,
                        cantidad=cantidad, unidad=_UNIDAD_POR_BASE[alimento.unidad_base]))
        db.session.add(menu)
    db.session.commit()


def seed_catalogs():
    if _vacia(Genero):
        db.session.add_all(Genero(clave=c, nombre=n) for c, n in d.GENEROS)
    if _vacia(Objetivo):
        db.session.add_all(Objetivo(clave=c, nombre=n, descripcion=ds) for c, n, ds in d.OBJETIVOS)
    if _vacia(Dia):
        db.session.add_all(Dia(clave=c, nombre=n, orden=o) for c, n, o in d.DIAS)
    if _vacia(TipoComida):
        db.session.add_all(TipoComida(clave=c, nombre=n, orden=o, hora=h) for c, n, o, h in d.TIPOS_COMIDA)
    if _vacia(Categoria):
        # Los ids siguen el orden de Model.sql (1 = granos ... 11 = condimentos)
        db.session.add_all(Categoria(id=i, clave=c, nombre=n) for i, (c, n) in enumerate(d.CATEGORIAS, start=1))
    db.session.flush()
    if _vacia(Alimento):
        db.session.add_all(
            Alimento(id=i, categoria_id=cat, nombre=n, unidad_base=u, cantidad_base=b, calorias=k,
                     proteinas=p, grasas=g, carbohidratos=ch, fibra=f)
            for i, cat, n, u, b, k, p, g, ch, f in d.ALIMENTOS
        )
    db.session.commit()
    seed_menus()


if __name__ == "__main__":
    from app import create_app
    app = create_app()
    with app.app_context():
        seed_catalogs()
        print("Catálogos cargados.")
