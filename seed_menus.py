"""Menús predefinidos de NutriPlan: una semana completa de comidas cada uno.

Cada menú es un diccionario  día → comida → [(nombre del alimento, cantidad)]
  * El nombre del alimento debe ser EXACTAMENTE el de seed_data.ALIMENTOS.
  * La unidad se toma de la unidad base del alimento (g, ml o unidad).

Para agregar otro menú basta con crear su semana y añadirlo a MENUS: al arrancar
la app se inserta solo (los menús que ya existen no se tocan).
"""

# ---------------------------------------------------------------------------
# FITNESS: alto en proteína magra, carbohidratos complejos y grasas buenas
# (≈ 2000 kcal al día, ≈ 150 g de proteína)
# ---------------------------------------------------------------------------
FITNESS = {
    "lunes": {
        "desayuno": [("Avena en hojuelas", 60), ("Leche descremada", 200), ("Banano / Plátano", 1), ("Almendras", 15)],
        "media_manana": [("Manzana", 1), ("Mantequilla de maní", 15)],
        "almuerzo": [("Pechuga de pollo (cocida)", 180), ("Arroz integral (cocido)", 180), ("Brócoli (cocido)", 120), ("Aceite de oliva", 10)],
        "merienda": [("Yogur griego natural", 200), ("Frutos secos mixtos", 15)],
        "cena": [("Filete de tilapia", 180), ("Papa cocida", 200), ("Calabacín / Zucchini", 150), ("Aceite de oliva", 8)],
    },
    "martes": {
        "desayuno": [("Huevo entero", 3), ("Pan integral", 60), ("Aguacate", 50), ("Tomate fresco", 80)],
        "media_manana": [("Yogur griego natural", 150), ("Moras", 80), ("Almendras", 10)],
        "almuerzo": [("Filete de salmón", 150), ("Quinoa (cocida)", 150), ("Espinaca fresca", 80), ("Brócoli (cocido)", 100)],
        "merienda": [("Batido de proteína (agua)", 30), ("Manzana", 1)],
        "cena": [("Pechuga de pollo (cocida)", 170), ("Coliflor (cocida)", 150), ("Arroz integral (cocido)", 150), ("Aceite de oliva", 5)],
    },
    "miercoles": {
        "desayuno": [("Yogur griego natural", 200), ("Avena en hojuelas", 40), ("Fresas", 100), ("Semillas de chía", 10), ("Nueces", 15)],
        "media_manana": [("Pera", 1), ("Almendras", 15)],
        "almuerzo": [("Pechuga de pavo (cocida)", 180), ("Pasta (cocida)", 200), ("Tomate fresco", 100), ("Espinaca fresca", 60), ("Aceite de oliva", 8)],
        "merienda": [("Pan integral", 60), ("Pechuga de pavo (cocida)", 60), ("Tomate fresco", 60)],
        "cena": [("Camarones cocidos", 180), ("Quinoa (cocida)", 120), ("Lechuga", 60), ("Pepino", 60), ("Aguacate", 50)],
    },
    "jueves": {
        "desayuno": [("Clara de huevo", 4), ("Huevo entero", 2), ("Pan integral", 60), ("Tomate fresco", 80), ("Espinaca fresca", 40), ("Naranja", 1)],
        "media_manana": [("Yogur griego natural", 150), ("Kiwi", 1), ("Nueces", 10)],
        "almuerzo": [("Atún fresco (a la plancha)", 170), ("Arroz integral (cocido)", 150), ("Zanahoria", 80), ("Aguacate", 50), ("Aceite de oliva", 5)],
        "merienda": [("Queso fresco", 60), ("Pera", 1)],
        "cena": [("Merluza al horno", 200), ("Papa cocida", 200), ("Brócoli (cocido)", 120), ("Aceite de oliva", 8)],
    },
    "viernes": {
        "desayuno": [("Avena en hojuelas", 60), ("Leche descremada", 200), ("Fresas", 100), ("Mantequilla de maní", 15), ("Semillas de chía", 10)],
        "media_manana": [("Batido de proteína (agua)", 30), ("Banano / Plátano", 1)],
        "almuerzo": [("Pechuga de pollo (cocida)", 180), ("Quinoa (cocida)", 150), ("Brócoli (cocido)", 120), ("Aceite de oliva", 10)],
        "merienda": [("Atún en agua (enlatado)", 100), ("Pan integral", 50)],
        "cena": [("Filete de salmón", 140), ("Calabacín / Zucchini", 150), ("Papa cocida", 150), ("Aceite de oliva", 5)],
    },
    "sabado": {
        "desayuno": [("Huevo entero", 3), ("Pan integral", 60), ("Champiñones", 80), ("Aguacate", 50), ("Naranja", 1)],
        "media_manana": [("Manzana", 1), ("Almendras", 15)],
        "almuerzo": [("Muslo de pollo (cocido, sin piel)", 180), ("Papa cocida", 250), ("Zanahoria", 100), ("Lechuga", 60), ("Aceite de oliva", 8)],
        "merienda": [("Yogur griego natural", 200), ("Moras", 80)],
        "cena": [("Filete de tilapia", 180), ("Quinoa (cocida)", 100), ("Espinaca fresca", 80), ("Aguacate", 40)],
    },
    "domingo": {
        "desayuno": [("Avena en hojuelas", 60), ("Leche descremada", 200), ("Banano / Plátano", 1), ("Nueces", 15)],
        "media_manana": [("Yogur griego natural", 150), ("Fresas", 100), ("Almendras", 10)],
        "almuerzo": [("Filete de salmón", 150), ("Arroz integral (cocido)", 150), ("Brócoli (cocido)", 120), ("Aceite de oliva", 5)],
        "merienda": [("Batido de proteína (agua)", 30), ("Manzana", 1)],
        "cena": [("Pechuga de pollo (cocida)", 170), ("Calabacín / Zucchini", 150), ("Papa cocida", 150), ("Aceite de oliva", 8)],
    },
}

# ---------------------------------------------------------------------------
# VEGETARIANO: 100 % de origen vegetal. No incluye ningún alimento de origen
# animal: ni carnes, ni pescados, ni huevo, ni lácteos, ni miel.
# (≈ 1900 kcal al día; la proteína sale de legumbres, tofu, soya y quinoa)
# ---------------------------------------------------------------------------
VEGETARIANO = {
    "lunes": {
        "desayuno": [("Avena en hojuelas", 60), ("Leche de almendras", 250), ("Banano / Plátano", 1), ("Semillas de chía", 10), ("Nueces", 15)],
        "media_manana": [("Manzana", 1), ("Almendras", 20)],
        "almuerzo": [("Lentejas (cocidas)", 200), ("Arroz integral (cocido)", 150), ("Zanahoria", 80), ("Espinaca fresca", 80), ("Aceite de oliva", 5)],
        "merienda": [("Pan integral", 60), ("Mantequilla de maní", 15)],
        "cena": [("Quinoa (cocida)", 120), ("Frijol negro (cocido)", 120), ("Tofu firme", 100), ("Aguacate", 50), ("Tomate fresco", 100)],
    },
    "martes": {
        "desayuno": [("Tofu firme", 150), ("Champiñones", 80), ("Espinaca fresca", 50), ("Pan integral", 60), ("Aceite de oliva", 5)],
        "media_manana": [("Frutos secos mixtos", 15), ("Naranja", 1)],
        "almuerzo": [("Garbanzos (cocidos)", 200), ("Quinoa (cocida)", 150), ("Pepino", 80), ("Tomate fresco", 100), ("Aceite de oliva", 10)],
        "merienda": [("Banano / Plátano", 1), ("Frutos secos mixtos", 20)],
        "cena": [("Tofu firme", 180), ("Pasta (cocida)", 200), ("Brócoli (cocido)", 100), ("Salsa de soya", 15), ("Aceite de oliva", 8)],
    },
    "miercoles": {
        "desayuno": [("Tortilla de maíz", 2), ("Frijol negro (cocido)", 100), ("Aguacate", 50), ("Tomate fresco", 80)],
        "media_manana": [("Pera", 1), ("Nueces", 20)],
        "almuerzo": [("Frijol rojo (cocido)", 200), ("Arroz integral (cocido)", 150), ("Soya texturizada (hidratada)", 100), ("Lechuga", 60)],
        "merienda": [("Tortilla de maíz", 2), ("Aguacate", 60), ("Almendras", 20)],
        "cena": [("Lentejas (cocidas)", 200), ("Calabacín / Zucchini", 150), ("Arroz integral (cocido)", 100), ("Aceite de oliva", 8)],
    },
    "jueves": {
        "desayuno": [("Avena en hojuelas", 40), ("Leche de almendras", 250), ("Fresas", 100), ("Mantequilla de maní", 15), ("Banano / Plátano", 1)],
        "media_manana": [("Manzana", 1), ("Almendras", 15)],
        "almuerzo": [("Soya texturizada (hidratada)", 150), ("Pasta (cocida)", 170), ("Tomate fresco", 150), ("Champiñones", 80), ("Aceite de oliva", 10)],
        "merienda": [("Garbanzos (cocidos)", 100), ("Zanahoria", 100), ("Aceite de oliva", 5)],
        "cena": [("Garbanzos (cocidos)", 150), ("Espinaca fresca", 100), ("Cuscús cocido", 100), ("Aceite de oliva", 10)],
    },
    "viernes": {
        "desayuno": [("Pan integral", 80), ("Aguacate", 70), ("Tomate fresco", 100), ("Semillas de chía", 10), ("Naranja", 1)],
        "media_manana": [("Manzana", 1), ("Almendras", 20)],
        "almuerzo": [("Tofu firme", 200), ("Arroz integral (cocido)", 150), ("Brócoli (cocido)", 150), ("Pimentón / Pimiento", 80), ("Salsa de soya", 15), ("Aceite vegetal", 10)],
        "merienda": [("Banano / Plátano", 1), ("Frutos secos mixtos", 25)],
        "cena": [("Soya texturizada (hidratada)", 150), ("Papa cocida", 200), ("Coliflor (cocida)", 150), ("Aceite de oliva", 8)],
    },
    "sabado": {
        "desayuno": [("Avena en hojuelas", 60), ("Leche de almendras", 250), ("Moras", 80), ("Nueces", 15), ("Semillas de chía", 10)],
        "media_manana": [("Pera", 1), ("Frutos secos mixtos", 20)],
        "almuerzo": [("Habas cocidas", 200), ("Cuscús cocido", 150), ("Calabacín / Zucchini", 100), ("Tomate fresco", 100), ("Aceite de oliva", 10)],
        "merienda": [("Pan integral", 60), ("Mantequilla de maní", 15)],
        "cena": [("Arvejas / Guisantes", 200), ("Soya texturizada (hidratada)", 100), ("Papa cocida", 150), ("Zanahoria", 80), ("Aceite de oliva", 8)],
    },
    "domingo": {
        "desayuno": [("Tofu firme", 150), ("Pan integral", 60), ("Aguacate", 50), ("Tomate fresco", 80), ("Naranja", 1)],
        "media_manana": [("Banano / Plátano", 1), ("Almendras", 15)],
        "almuerzo": [("Lentejas (cocidas)", 200), ("Quinoa (cocida)", 120), ("Brócoli (cocido)", 120), ("Zanahoria", 60), ("Aceite de oliva", 10)],
        "merienda": [("Manzana", 1), ("Frutos secos mixtos", 20)],
        "cena": [("Frijol negro (cocido)", 150), ("Arroz integral (cocido)", 90), ("Tofu firme", 100), ("Aguacate", 60), ("Tomate fresco", 100)],
    },
}

# (clave, nombre, descripción, orden, semana)
MENUS = [
    ("fitness", "Fitness",
     "Alto en proteína magra (pollo, pescado, huevo, yogur griego) con carbohidratos complejos y grasas saludables.",
     1, FITNESS),
    ("vegetariano", "Vegetariano",
     "100 % vegetal: sin carnes, pescados, huevo, lácteos ni miel. La proteína viene de legumbres, tofu, soya y quinoa.",
     2, VEGETARIANO),
]
