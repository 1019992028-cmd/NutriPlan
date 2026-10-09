# NutriPlan (versión web: Flask + SQLAlchemy + SQLite)

Migración de la app de escritorio (pywebview + MySQL) a una aplicación web según el
*Plan de acción completo*. La interfaz sigue siendo una sola página; ahora habla con
una API JSON de Flask y cada usuario solo ve sus propios datos.

## Puesta en marcha

```bash
python -m venv .venv
.venv\Scripts\activate          # Windows   (Linux/macOS: source .venv/bin/activate)
pip install -r requirements.txt
python app.py                   # http://127.0.0.1:5000
```

Al arrancar crea `database/nutriplan.db` y carga los catálogos (116 alimentos, 5 tipos
de comida, etc.). La clave de sesión se genera sola en `database/.secret_key`
(o usa la variable `NUTRIPLAN_SECRET_KEY`).

Producción: `NUTRIPLAN_PRODUCTION=1 gunicorn "app:create_app()"` detrás de HTTPS.

## Estructura

```
NutriPlan/
├── app.py            Flask: rutas, sesiones (Flask-Login), validaciones
├── config.py         Configuración y cookies de sesión
├── models.py         Modelos SQLAlchemy (usuarios, perfiles, planes, días, comidas...)
├── seed.py           Carga idempotente de catálogos
├── seed_data.py      Datos de Model.sql + columna nueva «fibra»
├── seed_menus.py     Menús predefinidos (Fitness, Vegetariano): semana completa cada uno
├── services/nutricion.py   Cálculo de calorías/macros/fibra (comida, día, semana)
├── services/menus.py       Meta calórica por perfil y ajuste de porciones de los menús
├── templates/index.html    Interfaz (antes index.html)
├── static/script.js, styles.css
├── database/         nutriplan.db (se crea sola)
└── tests/            test_nutricion.py, test_api.py, test_menus.py
```

## Pruebas

```bash
python -m unittest tests.test_nutricion -v   # sin dependencias extra
python -m unittest tests.test_menus -v       # sin dependencias extra
python -m unittest tests.test_metas -v       # sin dependencias extra
python -m unittest tests.test_api -v         # necesita requirements.txt instalado
```

## API

| Método | Ruta | Descripción |
|---|---|---|
| POST | `/api/registro`, `/api/login`, `/api/logout` | Cuenta y sesión |
| POST | `/api/sesion/entrar` | Entrar desde «perfiles guardados» (solo la cuenta con sesión abierta) |
| GET/PUT | `/api/perfil` | Peso, altura, objetivo, edad |
| GET | `/api/perfil/historial-peso` | Últimos 10 pesos |
| PUT | `/api/usuario` | Nombre, correo, género, avatar |
| GET | `/api/catalogos` | Categorías, alimentos (con fibra) y tipos de comida |
| GET/POST | `/api/planes` | Listar / crear: `{"fecha_inicio": "AAAA-MM-DD", "dias": 7, "nombre": "...", "copiar_de": 3}` (`dias` 1–31, por defecto 7; `copiar_de` opcional) |
| POST | `/api/planes/<id>/extender` | Añade días al final del plan: `{"dias": 7}` (máximo 31 días en total) |
| GET | `/api/planes/actual?hoy=AAAA-MM-DD` | Plan que incluye esa fecha, o `info: null` si no tiene (**no se crea solo**) |
| GET/PUT/DELETE | `/api/planes/<id>` | Ver / guardar alimentos / eliminar |
| GET | `/api/planes/<id>/resumen` | Totales por comida, día y plan (calculados en el servidor); los días se identifican por su posición (`"1"`, `"2"`...) |
| GET | `/api/menus` | Menús predefinidos con las kcal de cada día **ya ajustadas al usuario**, el `factor` de porciones y su `meta` (`min`, `max`, `objetivo`) |
| POST | `/api/planes/<id>/menu` | Aplica un menú a los días elegidos del plan (por posición): `{"menu": "fitness", "dias": ["1", "4"]}` |
| GET/PUT | `/api/hidratacion` | Vasos de agua por día |

## Qué cambió respecto al proyecto original

* **Backend:** `app.py`/`conexion.py` (pywebview + MySQL) → Flask + SQLAlchemy + SQLite.
* **Base de datos:** `plan_semanal` plano → `planes → dias_plan → comidas → comida_alimentos`
  (con historial). Nuevos: `tipos_comida` (5), `alimentos.fibra`, `perfiles.edad`.
* **script.js:** `callApi` usa `fetch`; fuera pywebview y modo demo; 5 comidas; fibra;
  edad; ventana «Mis planes» (historial, crear, copiar, eliminar).
* **index.html:** rutas con `url_for`, sin botones «Cerrar programa».

## Planes opcionales y menús

* **El plan no es obligatorio.** Al entrar ya no se crea ningún plan: si no hay uno que
  incluya el día de hoy, «Hoy» y «Plan semanal» ofrecen *Crear plan* o *Mis planes* (los menús están
  solo en el menú de usuario). Sin plan se siguen usando la meta, el IMC y la hidratación.
* **Menús** (solo en el menú de usuario → *Menús*): se elige un menú, se
  eligen los días (toda la semana o solo algunos) y se aplica. En esos días **reemplaza** los
  alimentos (la app avisa antes si ya había); los demás días no cambian. Si no hay plan abierto,
  se crea uno de 7 días que empieza hoy. Después todo se puede editar como cualquier otro alimento.
  Cada día del menú se copia al mismo día del plan (el lunes del menú → el lunes del plan).
* **Fitness:** ≈ 1.960 kcal/día, ≈ 165 g de proteína magra. **Vegetariano:** ≈ 1.870 kcal/día y
  100 % de origen vegetal (sin carnes, pescados, huevo, lácteos ni miel). Esas cifras son las del menú
  **base** (persona de ~70 kg); al mostrarlos y aplicarlos las porciones se ajustan a cada usuario
  (ver «Menús y metas personalizados»).
* **Agregar un menú nuevo:** añade su semana en `seed_menus.py` (nombres de alimento exactos de
  `seed_data.py`) y inclúyelo en `MENUS`. Al arrancar se inserta solo; los que ya existen no se
  modifican (para cambiar uno ya guardado, bórralo de las tablas `menus`/`menu_items`).
* Las tablas `menus` y `menu_items` se crean solas en una base de datos existente.

## Menús y metas personalizados

* **Meta calórica por perfil.** Sale de peso, altura, edad y género (Mifflin-St Jeor × 1,4 de actividad
  ligera) y del objetivo: bajar ≈ 80 % del gasto, mantener 100 %, subir 115 %. El rango sugerido es la
  meta ± 8 % y nunca baja de 1.200 kcal. Sin edad se usa 30 años; con género «otro»/sin especificar se
  usa el punto medio. La app no pregunta el nivel de actividad.
* **La misma fórmula** está en `services/menus.py` (`rango_kcal`) y en `static/script.js` (`kcalRange`):
  la usan «Hoy», las alertas, «Control de Meta» y los menús. Si cambias una, cambia la otra.
* **Menús a medida.** Al listar o aplicar un menú, todas sus cantidades se multiplican por un mismo factor
  (promedio diario del menú base → meta del usuario), así se conserva la forma de la semana y las
  proporciones de cada comida. Las cantidades se redondean a algo servible (g/ml de 5 en 5, unidades de
  media en media). El factor se acota entre 0,5 y 2,5, y si queda a menos de un 3 % de 1 se deja el menú
  original. Lo que se anuncia en la ventana de menús es exactamente lo que queda en el plan.
* **Qué NO se ajusta:** la mezcla de macronutrientes (la proteína sube o baja en proporción a las kcal) y
  los alimentos; si necesitas otra composición, edita después los alimentos del plan.

## Planes de duración libre

* **Un plan empieza el día que se elija** (no hace falta que sea lunes) y dura **de 1 a 31 días**
  (7 por defecto). Un plan de miércoles a martes cruza la semana sin problema.
* **Extender:** con un plan abierto, el botón *Extender plan* (junto a Exportar/Importar) añade días al
  final (+1 día, +3 días, +1 semana o los que se escriban). Los días nuevos empiezan vacíos y lo ya
  planeado no cambia.
* **Sin cruces:** dos planes de un mismo usuario no pueden ocupar el mismo día (así «Hoy» siempre sabe
  cuál abrir). Crear o extender un plan que choque con otro responde 409 indicando con cuál.
* **Los días se muestran solo con su nombre** (Lunes, Martes…), sin fecha ni número de semana. Si el plan
  dura más de una semana aparece un **selector «Semana 1 · Semana 2…»** sobre los días: cada semana son
  7 días seguidos del plan (la última puede ser más corta) y los botones muestran solo los de la semana
  elegida. «Semana Completa», las gráficas y las estadísticas de abajo se refieren a esa semana. La ventana
  de menús tiene el mismo selector (además de *Toda la semana* y *Todo el plan*). Las fechas exactas solo
  salen al pasar el cursor por el botón de una semana o de un día.
* **Los días del plan son posiciones**, no nombres: `"1"` es el primer día, `"2"` el segundo... La fecha y
  el día de la semana reales se calculan a partir de `fecha_inicio`. En la base de datos se reutiliza la
  columna `dias_plan.dia_semana` como posición, por lo que **no hace falta migrar** bases existentes
  (en los planes antiguos, que empezaban en lunes, la posición coincide con el día de la semana).
* **Menús:** cada día del plan recibe el día del menú que cae en su mismo día de la semana (el miércoles
  de tu plan toma el miércoles del menú). En planes de más de 7 días el menú se repite cada semana.
* **Copiar un plan** copia día a día: el día 1 del origen pasa al día 1 del nuevo, y así sucesivamente.
* **Exportar/importar JSON:** la versión 2 guarda los días como posiciones e incluye `plan_inicio` y
  `plan_dias`. Los archivos antiguos (`"lunes"`, `"martes"`...) se siguen pudiendo importar: cada día va
  al primer día del plan abierto que caiga en ese día de la semana.

## Notas

* Los valores de **fibra** son aproximados (tipo USDA) por cantidad base; revísalos si
  necesitas precisión.
* Protección de datos: todas las consultas filtran por el usuario con sesión; un plan
  ajeno responde 404. Contraseñas con hash (Werkzeug). Límite de 5 intentos de login
  fallidos cada 5 minutos (en memoria; con varios procesos usa Flask-Limiter + Redis).
* Las rutas que modifican datos exigen `Content-Type: application/json` y la cookie es
  `SameSite=Lax`, lo que evita peticiones forjadas desde otros sitios.
