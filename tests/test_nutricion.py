"""Pruebas del cálculo nutricional (no necesitan Flask ni base de datos).

Ejecutar:  python -m unittest tests.test_nutricion -v
"""
import os
import sys
import unittest
from types import SimpleNamespace

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import seed_data  # noqa: E402
from services import nutricion  # noqa: E402


def alimento(fila):
    _id, _cat, nombre, unidad, base, kcal, prot, grasa, carb, fibra = fila
    return SimpleNamespace(id=_id, nombre=nombre, unidad_base=unidad, cantidad_base=base, calorias=kcal,
                           proteinas=prot, grasas=grasa, carbohidratos=carb, fibra=fibra)


ALIMENTOS = {f[0]: alimento(f) for f in seed_data.ALIMENTOS}


class TestCalculo(unittest.TestCase):
    def test_ejemplo_del_plan_arroz(self):
        """Sección 18: 100 g = 130 kcal, 150 g = 195 kcal, 200 g = 260 kcal."""
        arroz = ALIMENTOS[1]
        self.assertEqual(nutricion.nutrientes(arroz, 100, "g")["kcal"], 130)
        self.assertEqual(nutricion.nutrientes(arroz, 150, "g")["kcal"], 195)
        self.assertEqual(nutricion.nutrientes(arroz, 200, "g")["kcal"], 260)

    def test_kilogramos_y_litros(self):
        self.assertEqual(nutricion.nutrientes(ALIMENTOS[1], 0.1, "kg")["kcal"], 130)
        self.assertEqual(nutricion.nutrientes(ALIMENTOS[71], 0.2, "l")["kcal"], 122)

    def test_unidades(self):
        huevo = ALIMENTOS[33]
        n = nutricion.nutrientes(huevo, 2, "unidad")
        self.assertEqual(n["kcal"], 144)
        self.assertEqual(n["proteina"], 12.6)

    def test_cantidades_invalidas(self):
        for cantidad in (0, -5, float("nan"), float("inf"), None):
            self.assertEqual(nutricion.nutrientes(ALIMENTOS[1], cantidad, "g")["kcal"], 0)

    def test_fibra(self):
        self.assertEqual(nutricion.nutrientes(ALIMENTOS[15], 200, "g")["fibra"], 15.8)  # lentejas

    def test_unidades_validas(self):
        self.assertEqual(nutricion.unidades_validas("g"), ("g", "kg"))
        self.assertEqual(nutricion.unidades_validas("ml"), ("ml", "l"))
        self.assertEqual(nutricion.unidades_validas("unidad"), ("unidad",))

    def test_resumen_plan(self):
        filas = [
            ("lunes", "desayuno", ALIMENTOS[3], 50, "g"),
            ("lunes", "almuerzo", ALIMENTOS[1], 150, "g"),
            ("martes", "cena", ALIMENTOS[1], 100, "g"),
        ]
        r = nutricion.resumen_plan(filas)
        self.assertEqual(r["comidas"]["lunes"]["almuerzo"]["kcal"], 195)
        self.assertEqual(r["dias"]["lunes"]["kcal"], 195 + 195)   # avena 50 g = 194.5 → 195
        self.assertEqual(r["semana"]["kcal"], 195 + 195 + 130)


class TestSemilla(unittest.TestCase):
    def test_cantidades_del_catalogo(self):
        self.assertEqual(len(seed_data.ALIMENTOS), 116)
        self.assertEqual(len(seed_data.CATEGORIAS), 11)
        self.assertEqual(len(seed_data.TIPOS_COMIDA), 5)
        self.assertEqual(len(seed_data.DIAS), 7)

    def test_ids_y_categorias_validas(self):
        ids = [f[0] for f in seed_data.ALIMENTOS]
        self.assertEqual(ids, sorted(set(ids)))
        self.assertTrue(all(1 <= f[1] <= 11 for f in seed_data.ALIMENTOS))


if __name__ == "__main__":
    unittest.main()
