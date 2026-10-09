"""Metas calóricas personalizadas y ajuste de porciones de los menús predefinidos.

Los menús de seed_menus.py están escritos para una persona de referencia (~70 kg,
~2.000 kcal al día). Al mostrarlos o aplicarlos, las cantidades se multiplican por un
factor para que el promedio diario coincida con la meta de CADA usuario.

La meta sale de peso, altura, edad, género y objetivo. La MISMA fórmula está en
static/script.js (función kcalRange): si cambias una, cambia la otra.
"""
import math

# Sin dato de actividad física en la app se asume actividad ligera
FACTOR_ACTIVIDAD = 1.4
# Qué parte del gasto diario se come según el objetivo: (centro de la meta)
AJUSTE_OBJETIVO = {"bajar": 0.80, "mantener": 1.00, "subir": 1.15}
MARGEN = 0.08                  # el rango sugerido es la meta ± 8 %
KCAL_MINIMAS = 1200            # nunca se recomienda menos que esto
KCAL_MAXIMAS = 5000
EDAD_POR_DEFECTO = 30          # si el usuario no ha puesto su edad

# Límites del ajuste de porciones: fuera de este rango el menú ya no se parece al original
FACTOR_MIN, FACTOR_MAX = 0.5, 2.5


def _redondear(x):
    """Redondeo «normal» (0,5 sube), igual que Math.round en JavaScript."""
    return int(math.floor(x + 0.5))


def gasto_diario(peso, altura, edad, genero):
    """Gasto energético diario estimado (Mifflin-St Jeor × actividad ligera), en kcal."""
    peso = peso if peso and peso > 0 else 70
    altura = altura if altura and altura > 0 else 170
    edad = edad if edad and edad > 0 else EDAD_POR_DEFECTO
    ajuste_genero = {"masculino": 5, "femenino": -161}.get(genero, -78)   # -78 = punto medio
    basal = 10 * peso + 6.25 * altura - 5 * edad + ajuste_genero
    return basal * FACTOR_ACTIVIDAD


def rango_kcal(peso, altura, edad, genero, objetivo):
    """(mínimo, máximo, objetivo) de kcal diarias para este perfil."""
    centro = gasto_diario(peso, altura, edad, genero) * AJUSTE_OBJETIVO.get(objetivo, 1.0)
    centro = min(KCAL_MAXIMAS, max(KCAL_MINIMAS, centro))
    minimo = max(KCAL_MINIMAS, _redondear(centro * (1 - MARGEN)))
    return minimo, _redondear(centro * (1 + MARGEN)), _redondear(centro)


def factor_porciones(kcal_objetivo, kcal_menu):
    """Cuánto multiplicar las porciones del menú. Cerca de 1 se deja el menú tal cual."""
    if not kcal_menu or kcal_menu <= 0:
        return 1.0
    f = kcal_objetivo / kcal_menu
    if abs(f - 1) < 0.03:
        return 1.0
    return round(min(FACTOR_MAX, max(FACTOR_MIN, f)), 3)


def escalar_cantidad(cantidad, unidad, factor):
    """Cantidad multiplicada por `factor` y redondeada a algo que se pueda servir:
    de 5 en 5 para g/ml (de 1 en 1 si es muy poca), y de media en media para unidades."""
    if factor == 1:
        return cantidad
    x = cantidad * factor
    if unidad in ("g", "ml"):
        paso = 5 if x >= 10 else 1
        return float(max(paso, _redondear(x / paso) * paso))
    return max(0.5, _redondear(x * 2) / 2)
