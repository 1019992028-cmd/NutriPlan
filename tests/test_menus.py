"""Pruebas de los datos de los menús (seed_menus.py). No necesitan Flask.

Ejecutar:  python -m unittest tests.test_menus -v
"""
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import seed_data as d  # noqa: E402
import seed_menus as m  # noqa: E402
from services import nutricion  # noqa: E402
from types import SimpleNamespace  # noqa: E402

ALIMENTOS = {
    n: SimpleNamespace(categoria=d.CATEGORIAS[cat - 1][0], unidad_base=u, cantidad_base=b, calorias=k,
                       proteinas=p, grasas=g, carbohidratos=ch, fibra=f)
    for _id, cat, n, u, b, k, p, g, ch, f in d.ALIMENTOS
}
DIAS = [clave for clave, _nombre, _orden in d.DIAS]
COMIDAS = [clave for clave, _nombre, _orden, _hora in d.TIPOS_COMIDA]

# Categorías enteras de origen animal. Ojo: el tofu está en «carnes» pero es vegetal.
CATEGORIAS_ANIMALES = {"carnes", "pescados", "lacteos"}
VEGETALES_EN_CATEGORIA_ANIMAL = {"Tofu firme"}
# Otros alimentos que contienen huevo, leche, miel o carne
OTROS_ANIMALES = {
    "Miel de abejas", "Mayonesa", "Batido de proteína (agua)", "Galletas dulces", "Chocolate con leche",
    "Helado de vainilla", "Pizza (porción)", "Hamburguesa completa", "Nuggets de pollo",
    "Barra energética / granola", "Pan dulce / ponqué", "Cereal azucarado",
}


def es_de_origen_animal(nombre):
    """True si el alimento tiene (o puede tener) ingredientes de origen animal."""
    if nombre in VEGETALES_EN_CATEGORIA_ANIMAL:
        return False
    return ALIMENTOS[nombre].categoria in CATEGORIAS_ANIMALES or nombre in OTROS_ANIMALES


def totales_del_dia(comidas):
    nutrientes = [nutricion.nutrientes(ALIMENTOS[n], c, ALIMENTOS[n].unidad_base)
                  for lista in comidas.values() for n, c in lista]
    return nutricion.sumar(nutrientes)


class TestDatosDeMenus(unittest.TestCase):
    def test_hay_fitness_y_vegetariano_con_claves_unicas(self):
        claves = [clave for clave, *_ in m.MENUS]
        self.assertEqual(sorted(claves), ["fitness", "vegetariano"])
        self.assertEqual(len(set(claves)), len(claves))

    def test_todos_los_alimentos_existen_y_las_cantidades_son_validas(self):
        for clave, _nombre, _desc, _orden, semana in m.MENUS:
            for dia, comidas in semana.items():
                for comida, lista in comidas.items():
                    for nombre, cantidad in lista:
                        self.assertIn(nombre, ALIMENTOS, f"{clave}/{dia}/{comida}")
                        self.assertGreater(cantidad, 0, f"{clave}/{dia}/{comida}/{nombre}")

    def test_cada_menu_cubre_los_7_dias_y_las_5_comidas(self):
        for clave, _nombre, _desc, _orden, semana in m.MENUS:
            self.assertEqual(list(semana), DIAS, clave)
            for dia, comidas in semana.items():
                self.assertEqual(list(comidas), COMIDAS, f"{clave}/{dia}")
                for comida, lista in comidas.items():
                    self.assertTrue(lista, f"{clave}/{dia}/{comida} está vacía")

    def test_sin_alimentos_repetidos_en_la_misma_comida(self):
        # (el servidor no lo exige, pero sería un descuido de datos)
        for clave, _nombre, _desc, _orden, semana in m.MENUS:
            for dia, comidas in semana.items():
                for comida, lista in comidas.items():
                    nombres = [n for n, _c in lista]
                    self.assertEqual(len(nombres), len(set(nombres)), f"{clave}/{dia}/{comida}")

    def test_vegetariano_no_incluye_ningun_alimento_de_origen_animal(self):
        semana = {c: s for c, _n, _d, _o, s in m.MENUS}["vegetariano"]
        usados = {n for comidas in semana.values() for lista in comidas.values() for n, _c in lista}
        self.assertEqual(sorted(n for n in usados if es_de_origen_animal(n)), [])

    def test_el_detector_de_origen_animal_funciona(self):
        for animal in ("Huevo entero", "Pechuga de pollo (cocida)", "Filete de salmón", "Leche entera",
                       "Yogur griego natural", "Miel de abejas"):
            self.assertTrue(es_de_origen_animal(animal), animal)
        for vegetal in ("Tofu firme", "Lentejas (cocidas)", "Leche de almendras", "Aguacate"):
            self.assertFalse(es_de_origen_animal(vegetal), vegetal)

    def test_fitness_si_incluye_proteina_animal(self):
        semana = {c: s for c, _n, _d, _o, s in m.MENUS}["fitness"]
        usados = {n for comidas in semana.values() for lista in comidas.values() for n, _c in lista}
        self.assertTrue(any(es_de_origen_animal(n) for n in usados))

    def test_calorias_y_macros_razonables_cada_dia(self):
        """Cada día debe quedar dentro de los rangos que la propia app considera
        equilibrados para ~70 kg (sin alertas de carbohidratos ni grasas altas)."""
        for clave, _nombre, _desc, _orden, semana in m.MENUS:
            for dia, comidas in semana.items():
                t = totales_del_dia(comidas)
                etiqueta = f"{clave}/{dia}: {t}"
                self.assertTrue(1700 <= t["kcal"] <= 2150, etiqueta)
                self.assertLessEqual(t["carbohidratos"] * 4 / t["kcal"] * 100, 60, etiqueta)
                self.assertLessEqual(t["grasa"] * 9 / t["kcal"] * 100, 35, etiqueta)
                self.assertGreaterEqual(t["proteina"], 75, etiqueta)


if __name__ == "__main__":
    unittest.main()
