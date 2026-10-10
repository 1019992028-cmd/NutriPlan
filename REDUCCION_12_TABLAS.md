# NutriPlanV2 — esquema reducido a 12 tablas

La base SQLite incluida en este ZIP ya está migrada y contiene **12 tablas**. Se conservan los datos existentes del archivo de base de datos.

## Tablas finales

1. `usuarios`
2. `perfiles`
3. `catalogos` — reúne géneros, objetivos, tipos de comida y categorías de alimentos mediante `tipo_catalogo`.
4. `alimentos`
5. `historial_peso`
6. `hidratacion`
7. `planes`
8. `dias_plan`
9. `comidas`
10. `comida_alimentos`
11. `menus`
12. `menu_items`

## Cambios de estructura

- `generos`, `objetivos`, `tipos_comida` y `categorias` se consolidaron en `catalogos`. La columna `tipo_catalogo` distingue cada conjunto y la restricción única `(tipo_catalogo, clave)` evita claves repetidas dentro del mismo catálogo.
- `dias` se eliminó porque el día de la semana se representa mediante números y claves constantes en `seed_data.py`.
- Las claves foráneas de `perfiles`, `comidas`, `menu_items` y `alimentos` ahora apuntan a `catalogos`.
- Los IDs de los catálogos se reasignaron para ser únicos dentro de la tabla común y las referencias se actualizaron.
- Se comprobó `PRAGMA foreign_key_check`: no se encontraron referencias huérfanas al migrar el archivo SQLite incluido.

## Ejecución

Instala dependencias y ejecuta `python app.py`. La base incluida ya usa el esquema nuevo. Antes de reemplazarla en una instalación propia, guarda una copia de `database/nutriplan.db`.

## Pruebas

Se verificó por SQLite que hay 12 tablas y que la comprobación de claves foráneas no reporta errores. En el entorno de preparación no fue posible ejecutar la suite de Flask porque no se pudieron instalar las dependencias; ejecútala localmente con `python -m unittest discover -s tests`.
