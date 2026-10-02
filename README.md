# NutriPlan — PC + Android, misma base de datos

## Qué cambié y por qué

Tu app de escritorio usa **pywebview**: una ventana nativa que carga tu HTML/CSS/JS
y les da un "puente" a Python (`app.py`) para hablar con Supabase. **Android no puede
correr ese Python** (no hay intérprete, no hay pywebview), así que había dos caminos:

1. Reescribir todo en Kotlin/XML → perderías el 100% de tu diseño y lógica actual.
2. Empaquetar tu **mismo** HTML/CSS/JS dentro de un proyecto Android real usando
   **Capacitor**, y reemplazar solo la pieza que dependía de Python por un
   equivalente en JavaScript que habla directo con Supabase.

Fui por la opción 2. Resultado: **no perdiste nada** de tu diseño ni de tu lógica de
negocio (validaciones, reglas de cantidades, mensajes de error, etc.), y **`script.js`
no cambió ni una línea**.

### Cómo quedó sin romper nada

`script.js` nunca llama a Supabase directamente: siempre llama a
`window.pywebview.api.algo(...)`. En escritorio, ese objeto lo crea Python. Para
Android, agregué `mobile/www/supabase-bridge.js`, que **crea ese mismo objeto**
(`window.pywebview.api`) pero implementado en JavaScript puro, con exactamente
la misma lógica que tenía `app.py` (mismas validaciones, mismo manejo de errores,
mismo bcrypt para las contraseñas). Como usa la **misma URL y misma clave de
Supabase** que `conexion.py`, PC y celular leen y escriben en **la misma base
de datos**, en tiempo real.

```
                ┌────────────────────┐
                │   Supabase (nube)  │   ← MISMA base de datos
                └─────────┬──────────┘
           ┌──────────────┴──────────────┐
   app.py (Python, pywebview)     supabase-bridge.js (JS)
           │                              │
      index.html / styles.css / script.js (IDÉNTICOS)
           │                              │
         PC (Windows/Mac/Linux)      Android (Capacitor)
```

## Estructura de este proyecto

```
NutriPlan/
├── desktop/                 ← tu app de escritorio, intacta (solo con el CSS de días arreglado)
│   ├── app.py
│   ├── conexion.py
│   ├── diagnostico.py
│   ├── index.html
│   ├── styles.css
│   ├── script.js
│   └── BD_Setup.sql
│
└── mobile/                  ← lo nuevo: se convierte en tu proyecto de Android Studio
    ├── package.json
    ├── capacitor.config.json
    └── www/                 ← esta carpeta es la que Android muestra en pantalla
        ├── index.html       ← tu mismo index.html + 3 <script> nuevos al final
        ├── styles.css       ← tu mismo CSS + arreglos para pantallas de celular
        ├── script.js        ← IDÉNTICO al original, sin ningún cambio
        └── supabase-bridge.js  ← NUEVO: reemplaza a app.py, habla con Supabase
```

`desktop/` sigue funcionando exactamente igual que antes (`python app.py`).

## Lo que arreglé del diseño en celular

El problema de "los días que se salen" era una combinación de: los 7-8 pills de
días no cabían en pantallas angostas, no había ninguna pista visual de que se
podían deslizar, y no había manejo del área segura (barra de estado) de Android.
Agregué, en `styles.css` (de ambas versiones, para que se vean iguales):

- Difuminado en los bordes del selector de días, para que se note que hay más
  contenido si no cabe todo.
- Scroll con inercia (`-webkit-overflow-scrolling: touch`) y "scroll-snap" para
  que deslizar se sienta nativo, no brusco.
- Un breakpoint nuevo en `480px` y otro en `360px` que reduce el padding y el
  tamaño de letra de los pills, cabecera y barra de categorías para celulares
  chicos.
- `padding` con `env(safe-area-inset-top/bottom)` para que el contenido no
  quede debajo de la barra de estado o la barra de gestos de Android.

Esto no cambia nada visualmente en pantallas grandes (PC), solo activa en
pantallas angostas.

## Pasos para abrir esto en Android Studio

Necesitas Node.js instalado (LTS, ej. 20.x) y Android Studio con el SDK de
Android ya instalado. Yo no puedo ejecutar estos comandos por ti porque este
entorno no tiene acceso a internet ni al SDK de Android — corre esto en tu
computador:

1. Entra a la carpeta `mobile/`:
   ```
   cd mobile
   npm install
   ```

2. Genera el proyecto nativo de Android (esto crea una carpeta `android/` que
   es un proyecto de Android Studio de verdad):
   ```
   npx cap add android
   ```

3. Copia tu `www/` dentro del proyecto Android:
   ```
   npx cap sync android
   ```

4. Ábrelo en Android Studio:
   ```
   npx cap open android
   ```
   (o abre manualmente la carpeta `mobile/android` desde Android Studio)

5. Dale ▶ Run en un emulador o en tu celular conectado por USB (con
   "Depuración USB" activada).

Cada vez que edites algo dentro de `mobile/www/`, vuelve a correr
`npx cap sync android` antes de compilar de nuevo, para que Android Studio
tome los cambios.

### Permiso de Internet

Capacitor agrega automáticamente el permiso de Internet al
`AndroidManifest.xml` generado. Si algún día no conecta, revisa que exista:
```xml
<uses-permission android:name="android.permission.INTERNET" />
```

## Aviso de seguridad (ya existía, no lo introduje yo)

Revisé `BD_Setup.sql`: las políticas de seguridad (RLS) de Supabase están en
modo desarrollo, abiertas para todo el mundo (`using (true)`) en todas las
tablas, incluida `usuarios` (que contiene `password_hash`). Eso ya pasaba en
tu app de escritorio (Python usa la misma clave pública), así que el celular
no empeora nada — pero como ahora también quedará expuesto dentro del propio
APK (cualquiera puede extraer la URL y la clave de un APK), te recomiendo,
cuando tengas tiempo, moverte a políticas RLS más estrictas o a Supabase Auth
en vez de manejar tú mismo el registro/login. No es necesario para que esto
funcione hoy, pero es la única brecha real y ya estaba ahí antes de este
cambio.

## ¿Y si prefieres NO usar Capacitor?

Es, por lejos, la opción que menos te hace perder (mismo diseño, mismo CSS,
mismo JS). La alternativa sería reescribir toda la interfaz en Kotlin + XML
(Jetpack Compose o Views), lo cual sí implicaría rehacer virtualmente todo el
diseño desde cero dentro de Android Studio. Si en algún momento quieres ese
camino en lugar de este, dímelo y lo planeamos aparte.
