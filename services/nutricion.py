"""Cálculos nutricionales (sección 18 del plan): por alimento, comida, día y semana.

Replica la misma fórmula que usa el frontend (script.js → calculateMacros).
"""
import math
from decimal import ROUND_HALF_UP, Decimal

CAMPOS = ("kcal", "proteina", "grasa", "carbohidratos", "fibra")


def unidades_validas(unidad_base):
    """Unidades que el usuario puede elegir según la unidad base del alimento."""
    if unidad_base == "g":
        return ("g", "kg")
    if unidad_base == "ml":
        return ("ml", "l")
    return ("unidad",)


def _redondear(x, decimales=1):
    """Redondea igual que Number.toFixed de JavaScript (mitad hacia arriba sobre
    el valor binario exacto), para que servidor y pantalla muestren lo mismo."""
    paso = Decimal(1).scaleb(-decimales)
    return float(Decimal(x).quantize(paso, rounding=ROUND_HALF_UP))


def nutrientes(alimento, cantidad, unidad):
    """Aporte nutricional de `cantidad` `unidad` de un alimento.

    `alimento` debe tener: unidad_base, cantidad_base, calorias, proteinas,
    grasas, carbohidratos y fibra.
    """
    vacio = {c: 0 for c in CAMPOS}
    if alimento is None or cantidad is None or not math.isfinite(cantidad) or cantidad <= 0:
        return vacio

    base = alimento.cantidad_base or 1
    cant = cantidad * 1000 if unidad in ("kg", "l") else cantidad
    mult = cant / base if alimento.unidad_base in ("g", "ml") else cantidad / base

    return {
        "kcal": int(math.floor(alimento.calorias * mult + 0.5)),
        "proteina": _redondear(alimento.proteinas * mult),
        "grasa": _redondear(alimento.grasas * mult),
        "carbohidratos": _redondear(alimento.carbohidratos * mult),
        "fibra": _redondear(alimento.fibra * mult),
    }


def sumar(lista):
    total = {c: 0 for c in CAMPOS}
    for n in lista:
        for c in CAMPOS:
            total[c] += n[c]
    total["kcal"] = int(total["kcal"])
    for c in CAMPOS[1:]:
        total[c] = _redondear(total[c])
    return total


def resumen_plan(filas):
    """filas: iterable de (dia_clave, comida_clave, alimento, cantidad, unidad).

    Devuelve totales por comida, por día y de la semana completa.
    """
    por_comida, por_dia = {}, {}
    for dia, comida, alimento, cantidad, unidad in filas:
        n = nutrientes(alimento, cantidad, unidad)
        por_comida.setdefault(dia, {}).setdefault(comida, []).append(n)
        por_dia.setdefault(dia, []).append(n)

    comidas = {d: {c: sumar(v) for c, v in cs.items()} for d, cs in por_comida.items()}
    dias = {d: sumar(v) for d, v in por_dia.items()}
    semana = sumar(dias.values())
    return {"comidas": comidas, "dias": dias, "semana": semana}
