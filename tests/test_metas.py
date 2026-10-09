"""Pruebas de la meta calórica y del ajuste de porciones (services/menus.py). No necesitan Flask.

Ejecutar:  python -m unittest tests.test_metas -v
"""
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.menus import (FACTOR_MAX, FACTOR_MIN, KCAL_MINIMAS, escalar_cantidad,  # noqa: E402
                            factor_porciones, rango_kcal)


class TestMeta(unittest.TestCase):
    def test_el_objetivo_ordena_las_metas(self):
        bajar = rango_kcal(70, 170, 30, "masculino", "bajar")[2]
        mantener = rango_kcal(70, 170, 30, "masculino", "mantener")[2]
        subir = rango_kcal(70, 170, 30, "masculino", "subir")[2]
        self.assertLess(bajar, mantener)
        self.assertLess(mantener, subir)

    def test_peso_altura_edad_y_genero_cambian_la_meta(self):
        base = rango_kcal(70, 170, 30, "masculino", "mantener")[2]
        self.assertGreater(rango_kcal(90, 170, 30, "masculino", "mantener")[2], base)   # más peso
        self.assertGreater(rango_kcal(70, 190, 30, "masculino", "mantener")[2], base)   # más altura
        self.assertLess(rango_kcal(70, 170, 60, "masculino", "mantener")[2], base)      # más edad
        self.assertLess(rango_kcal(70, 170, 30, "femenino", "mantener")[2], base)       # género

    def test_rango_ordenado_y_con_suelo(self):
        for args in [(70, 170, 30, "femenino", "mantener"), (40, 140, 80, "femenino", "bajar"),
                     (150, 200, 25, "masculino", "subir")]:
            minimo, maximo, objetivo = rango_kcal(*args)
            self.assertLessEqual(minimo, objetivo)
            self.assertLessEqual(objetivo, maximo)
            self.assertGreaterEqual(minimo, KCAL_MINIMAS)

    def test_datos_que_faltan_usan_valores_razonables(self):
        self.assertEqual(rango_kcal(None, None, None, None, None), rango_kcal(70, 170, 30, None, "mantener"))


class TestFactor(unittest.TestCase):
    def test_cerca_de_la_meta_no_cambia_el_menu(self):
        self.assertEqual(factor_porciones(2000, 1980), 1.0)

    def test_se_acota(self):
        self.assertEqual(factor_porciones(10000, 1000), FACTOR_MAX)
        self.assertEqual(factor_porciones(300, 2000), FACTOR_MIN)
        self.assertEqual(factor_porciones(2000, 0), 1.0)

    def test_escalado_proporcional(self):
        self.assertAlmostEqual(factor_porciones(2400, 2000), 1.2)


class TestEscalado(unittest.TestCase):
    def test_sin_cambio_devuelve_lo_mismo(self):
        self.assertEqual(escalar_cantidad(180, "g", 1), 180)
        self.assertEqual(escalar_cantidad(1, "unidad", 1), 1)

    def test_gramos_de_5_en_5(self):
        self.assertEqual(escalar_cantidad(180, "g", 1.2), 215.0)
        self.assertEqual(escalar_cantidad(60, "g", 1.17), 70.0)

    def test_cantidades_pequenas_no_desaparecen(self):
        self.assertGreaterEqual(escalar_cantidad(5, "g", 0.5), 1)
        self.assertGreaterEqual(escalar_cantidad(1, "unidad", 0.5), 0.5)

    def test_unidades_de_media_en_media(self):
        self.assertEqual(escalar_cantidad(3, "unidad", 1.3), 4.0)
        self.assertEqual(escalar_cantidad(1, "unidad", 1.3), 1.5)
        for f in (0.6, 0.77, 1.4, 1.9):
            self.assertEqual(escalar_cantidad(2, "unidad", f) * 2, int(escalar_cantidad(2, "unidad", f) * 2))


if __name__ == "__main__":
    unittest.main()
