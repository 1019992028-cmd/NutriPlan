"""Modelos SQLAlchemy de NutriPlan (secciones 5 a 11 del plan de acción)."""
import sqlite3
from datetime import datetime, timezone

from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import event
from sqlalchemy.engine import Engine
from werkzeug.security import check_password_hash, generate_password_hash

db = SQLAlchemy()


def ahora():
    """Fecha y hora UTC (sin zona, como las guarda SQLite)."""
    return datetime.now(timezone.utc).replace(tzinfo=None)


@event.listens_for(Engine, "connect")
def _activar_claves_foraneas(dbapi_conn, _record):
    """SQLite ignora las claves foráneas (y los ON DELETE CASCADE) si no se activan."""
    if isinstance(dbapi_conn, sqlite3.Connection):
        cur = dbapi_conn.cursor()
        cur.execute("PRAGMA foreign_keys=ON")
        cur.close()


# ---------------------------------------------------------------------------
# Catálogos unificados: géneros, objetivos, días y tipos de comida comparten
# una tabla con discriminador. Las subclases conservan la API ORM existente.
# ---------------------------------------------------------------------------
class Catalogo(db.Model):
    __tablename__ = "catalogos"
    id = db.Column(db.Integer, primary_key=True)
    tipo_catalogo = db.Column(db.String(30), nullable=False)
    clave = db.Column(db.String(30), nullable=False)
    nombre = db.Column(db.String(150), nullable=False)
    descripcion = db.Column(db.String(255))
    orden = db.Column(db.Integer)
    hora = db.Column(db.String(5))
    __table_args__ = (db.UniqueConstraint("tipo_catalogo", "clave", name="uq_catalogo_tipo_clave"),)
    __mapper_args__ = {"polymorphic_on": tipo_catalogo, "polymorphic_identity": "catalogo"}


class Genero(Catalogo):
    __mapper_args__ = {"polymorphic_identity": "genero"}


class Objetivo(Catalogo):
    __mapper_args__ = {"polymorphic_identity": "objetivo"}


class TipoComida(Catalogo):
    __mapper_args__ = {"polymorphic_identity": "tipo_comida"}


class Categoria(Catalogo):
    __mapper_args__ = {"polymorphic_identity": "categoria"}


class Alimento(db.Model):
    __tablename__ = "alimentos"
    id = db.Column(db.Integer, primary_key=True)
    categoria_id = db.Column(db.Integer, db.ForeignKey("catalogos.id", onupdate="CASCADE", ondelete="RESTRICT"), nullable=False)
    nombre = db.Column(db.String(100), nullable=False)
    unidad_base = db.Column(db.String(20), nullable=False, default="g")
    cantidad_base = db.Column(db.Float, nullable=False, default=100)
    calorias = db.Column(db.Float, nullable=False, default=0)
    proteinas = db.Column(db.Float, nullable=False, default=0)
    carbohidratos = db.Column(db.Float, nullable=False, default=0)
    grasas = db.Column(db.Float, nullable=False, default=0)
    fibra = db.Column(db.Float, nullable=False, default=0)

    categoria = db.relationship("Categoria")


# ---------------------------------------------------------------------------
# Usuarios
# ---------------------------------------------------------------------------
class Usuario(UserMixin, db.Model):
    __tablename__ = "usuarios"
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(300), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    fecha_creacion = db.Column(db.DateTime, nullable=False, default=ahora)

    perfil = db.relationship("Perfil", uselist=False, back_populates="usuario",
                             cascade="all, delete-orphan", passive_deletes=True)
    planes = db.relationship("Plan", back_populates="usuario",
                             cascade="all, delete-orphan", passive_deletes=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Perfil(db.Model):
    __tablename__ = "perfiles"
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuarios.id", onupdate="CASCADE", ondelete="CASCADE"),
                           unique=True, nullable=False)
    genero_id = db.Column(db.Integer, db.ForeignKey("catalogos.id", onupdate="CASCADE", ondelete="RESTRICT"), nullable=False)
    objetivo_id = db.Column(db.Integer, db.ForeignKey("catalogos.id", onupdate="CASCADE", ondelete="RESTRICT"), nullable=False)
    edad = db.Column(db.Integer)
    peso = db.Column(db.Float, nullable=False, default=70)
    altura = db.Column(db.Float, nullable=False, default=170)
    avatar = db.Column(db.Text)
    actualizado_en = db.Column(db.DateTime, nullable=False, default=ahora, onupdate=ahora)

    usuario = db.relationship("Usuario", back_populates="perfil")
    genero = db.relationship("Genero", foreign_keys=[genero_id])
    objetivo = db.relationship("Objetivo", foreign_keys=[objetivo_id])


class HistorialPeso(db.Model):
    __tablename__ = "historial_peso"
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuarios.id", onupdate="CASCADE", ondelete="CASCADE"),
                           nullable=False, index=True)
    peso = db.Column(db.Float, nullable=False)
    registrado_en = db.Column(db.DateTime, nullable=False, default=ahora)


class Hidratacion(db.Model):
    __tablename__ = "hidratacion"
    __table_args__ = (db.UniqueConstraint("usuario_id", "fecha", name="uq_hidratacion_usuario_dia"),)
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuarios.id", onupdate="CASCADE", ondelete="CASCADE"), nullable=False)
    fecha = db.Column(db.Date, nullable=False)
    vasos = db.Column(db.Integer, nullable=False, default=0)
    actualizado_en = db.Column(db.DateTime, nullable=False, default=ahora, onupdate=ahora)


# ---------------------------------------------------------------------------
# Planes semanales
#   Usuario 1─N Plan 1─31 DiaPlan 1─N Comida N─N Alimento (vía ComidaAlimento)
# ---------------------------------------------------------------------------
class Plan(db.Model):
    __tablename__ = "planes"
    __table_args__ = (db.UniqueConstraint("usuario_id", "fecha_inicio", name="uq_plan_usuario_semana"),)
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuarios.id", onupdate="CASCADE", ondelete="CASCADE"),
                           nullable=False, index=True)
    nombre = db.Column(db.String(120), nullable=False)
    fecha_inicio = db.Column(db.Date, nullable=False)
    fecha_fin = db.Column(db.Date, nullable=False)
    fecha_creacion = db.Column(db.DateTime, nullable=False, default=ahora)
    estado = db.Column(db.String(20), nullable=False, default="activo")  # activo | archivado

    usuario = db.relationship("Usuario", back_populates="planes")
    dias = db.relationship("DiaPlan", back_populates="plan", order_by="DiaPlan.dia_semana",
                           cascade="all, delete-orphan", passive_deletes=True)


class DiaPlan(db.Model):
    __tablename__ = "dias_plan"
    __table_args__ = (db.UniqueConstraint("plan_id", "dia_semana", name="uq_dia_plan"),)
    id = db.Column(db.Integer, primary_key=True)
    plan_id = db.Column(db.Integer, db.ForeignKey("planes.id", onupdate="CASCADE", ondelete="CASCADE"),
                        nullable=False, index=True)
    # POSICIÓN del día dentro del plan: 1 = primer día, 2 = segundo... (hasta la duración del plan).
    # El plan puede empezar cualquier día de la semana; el día real sale de `fecha`.
    # (El nombre de la columna se conserva para no migrar bases de datos existentes: en los planes
    # antiguos, que siempre empezaban en lunes, la posición coincide con el día de la semana.)
    dia_semana = db.Column(db.Integer, nullable=False)
    fecha = db.Column(db.Date, nullable=False)

    plan = db.relationship("Plan", back_populates="dias")
    comidas = db.relationship("Comida", back_populates="dia", cascade="all, delete-orphan", passive_deletes=True)


class Comida(db.Model):
    __tablename__ = "comidas"
    __table_args__ = (db.UniqueConstraint("dia_id", "tipo_id", name="uq_comida_dia_tipo"),)
    id = db.Column(db.Integer, primary_key=True)
    dia_id = db.Column(db.Integer, db.ForeignKey("dias_plan.id", onupdate="CASCADE", ondelete="CASCADE"),
                       nullable=False, index=True)
    tipo_id = db.Column(db.Integer, db.ForeignKey("catalogos.id", onupdate="CASCADE", ondelete="RESTRICT"), nullable=False)
    nombre = db.Column(db.String(130))
    hora = db.Column(db.String(5))

    dia = db.relationship("DiaPlan", back_populates="comidas")
    tipo = db.relationship("TipoComida", foreign_keys=[tipo_id])
    alimentos = db.relationship("ComidaAlimento", back_populates="comida",
                                cascade="all, delete-orphan", passive_deletes=True)


class ComidaAlimento(db.Model):
    """Tabla intermedia N:N entre comidas y alimentos."""
    __tablename__ = "comida_alimentos"
    id = db.Column(db.Integer, primary_key=True)
    comida_id = db.Column(db.Integer, db.ForeignKey("comidas.id", onupdate="CASCADE", ondelete="CASCADE"),
                          nullable=False, index=True)
    alimento_id = db.Column(db.Integer, db.ForeignKey("alimentos.id", onupdate="CASCADE", ondelete="RESTRICT"), nullable=False)
    cantidad = db.Column(db.Float, nullable=False)
    unidad = db.Column(db.String(20), nullable=False, default="g")

    comida = db.relationship("Comida", back_populates="alimentos")
    alimento = db.relationship("Alimento")


# ---------------------------------------------------------------------------
# Menús predefinidos (p. ej. «Fitness», «Vegetariano»)
#   Menu 1─N MenuItem: una semana completa de comidas que el usuario puede
#   copiar a los días que quiera de su plan.
# ---------------------------------------------------------------------------
class Menu(db.Model):
    __tablename__ = "menus"
    id = db.Column(db.Integer, primary_key=True)
    clave = db.Column(db.String(30), unique=True, nullable=False)
    nombre = db.Column(db.String(60), nullable=False)
    descripcion = db.Column(db.String(255))
    orden = db.Column(db.Integer, nullable=False, default=0)

    items = db.relationship("MenuItem", back_populates="menu", order_by="MenuItem.id",
                            cascade="all, delete-orphan", passive_deletes=True)


class MenuItem(db.Model):
    __tablename__ = "menu_items"
    id = db.Column(db.Integer, primary_key=True)
    menu_id = db.Column(db.Integer, db.ForeignKey("menus.id", onupdate="CASCADE", ondelete="CASCADE"),
                        nullable=False, index=True)
    dia_semana = db.Column(db.Integer, nullable=False)  # 1 = lunes ... 7 = domingo
    tipo_id = db.Column(db.Integer, db.ForeignKey("catalogos.id", onupdate="CASCADE", ondelete="RESTRICT"), nullable=False)
    alimento_id = db.Column(db.Integer, db.ForeignKey("alimentos.id", onupdate="CASCADE", ondelete="RESTRICT"), nullable=False)
    cantidad = db.Column(db.Float, nullable=False)
    unidad = db.Column(db.String(20), nullable=False, default="g")

    menu = db.relationship("Menu", back_populates="items")
    tipo = db.relationship("TipoComida", foreign_keys=[tipo_id])
    alimento = db.relationship("Alimento")
