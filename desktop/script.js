// Paletas de colores (temas): fondo, acento, texto y paneles de cada tema
const T = {
  breathe: { bg: '#08131a', accentHex: '#38bdf8', textMain: '#e0f2fe', textDim: '#7dd3fc', textFaint: 'rgba(224, 242, 254, 0.45)', navBg: 'rgba(8, 19, 26, 0.85)', navBorder: 'rgba(56, 189, 248, 0.3)', pillActive: '#0369a1', pillDim: 'rgba(224, 242, 254, 0.7)', pillActiveBg: '#38bdf8', thumbBg: 'rgba(56, 189, 248, 0.45)', vigA: 'rgba(12, 35, 48, 0.6)', vigB: 'rgba(4, 10, 15, 0.95)', panel: 'rgba(15, 32, 45, 0.65)', panelSolid: '#0f202d', border: 'rgba(56, 189, 248, 0.2)', borderSoft: 'rgba(56, 189, 248, 0.1)' },
  meditate: { bg: '#120d1c', accentHex: '#a855f7', textMain: '#f3e8ff', textDim: '#c084fc', textFaint: 'rgba(243, 232, 255, 0.45)', navBg: 'rgba(18, 13, 28, 0.85)', navBorder: 'rgba(168, 85, 247, 0.3)', pillActive: '#581c87', pillDim: 'rgba(243, 232, 255, 0.7)', pillActiveBg: '#a855f7', thumbBg: 'rgba(168, 85, 247, 0.45)', vigA: 'rgba(30, 18, 48, 0.6)', vigB: 'rgba(10, 6, 18, 0.95)', panel: 'rgba(28, 20, 44, 0.65)', panelSolid: '#1c142c', border: 'rgba(168, 85, 247, 0.2)', borderSoft: 'rgba(168, 85, 247, 0.1)' },
  anxiety: { bg: '#0e0904', accentHex: '#e86026', textMain: '#ede7d8', textDim: 'rgba(245, 238, 220, 0.65)', textFaint: 'rgba(245, 238, 220, 0.4)', navBg: 'rgba(14, 6, 2, 0.82)', navBorder: 'rgba(232, 96, 38, 0.28)', pillActive: '#fff0e0', pillDim: 'rgba(245, 225, 200, 0.82)', pillActiveBg: '#e86026', thumbBg: 'rgba(232, 96, 38, 0.45)', vigA: 'rgba(25, 14, 8, 0.54)', vigB: 'rgba(4, 2, 0, 0.92)', panel: 'rgba(28, 18, 12, 0.65)', panelSolid: '#1c120c', border: 'rgba(232, 96, 38, 0.25)', borderSoft: 'rgba(232, 96, 38, 0.12)' },
  nature: { bg: '#08140c', accentHex: '#22c55e', textMain: '#dcfce7', textDim: '#86efac', textFaint: 'rgba(220, 252, 231, 0.45)', navBg: 'rgba(8, 20, 12, 0.85)', navBorder: 'rgba(34, 197, 94, 0.3)', pillActive: '#14532d', pillDim: 'rgba(220, 252, 231, 0.7)', pillActiveBg: '#22c55e', thumbBg: 'rgba(34, 197, 94, 0.45)', vigA: 'rgba(15, 38, 22, 0.6)', vigB: 'rgba(4, 12, 6, 0.95)', panel: 'rgba(18, 38, 24, 0.65)', panelSolid: '#122618', border: 'rgba(34, 197, 94, 0.2)', borderSoft: 'rgba(34, 197, 94, 0.1)' },
  classical: { bg: '#141210', accentHex: '#d97706', textMain: '#fef3c7', textDim: '#fcd34d', textFaint: 'rgba(254, 243, 199, 0.45)', navBg: 'rgba(20, 18, 16, 0.85)', navBorder: 'rgba(217, 119, 6, 0.3)', pillActive: '#78350f', pillDim: 'rgba(254, 243, 199, 0.7)', pillActiveBg: '#d97706', thumbBg: 'rgba(217, 119, 6, 0.45)', vigA: 'rgba(38, 32, 24, 0.6)', vigB: 'rgba(12, 10, 8, 0.95)', panel: 'rgba(34, 28, 22, 0.65)', panelSolid: '#221c16', border: 'rgba(217, 119, 6, 0.2)', borderSoft: 'rgba(217, 119, 6, 0.1)' },
  jazz: { bg: '#180a14', accentHex: '#ec4899', textMain: '#fce7f3', textDim: '#f472b6', textFaint: 'rgba(252, 231, 243, 0.45)', navBg: 'rgba(24, 10, 20, 0.85)', navBorder: 'rgba(236, 72, 153, 0.3)', pillActive: '#831843', pillDim: 'rgba(252, 231, 243, 0.7)', pillActiveBg: '#ec4899', thumbBg: 'rgba(236, 72, 153, 0.45)', vigA: 'rgba(42, 16, 36, 0.6)', vigB: 'rgba(14, 5, 12, 0.95)', panel: 'rgba(38, 18, 32, 0.65)', panelSolid: '#261220', border: 'rgba(236, 72, 153, 0.2)', borderSoft: 'rgba(236, 72, 153, 0.1)' },
  sunset: { bg: '#18080c', accentHex: '#f43f5e', textMain: '#ffe4e6', textDim: '#fda4af', textFaint: 'rgba(255, 228, 230, 0.45)', navBg: 'rgba(24, 8, 12, 0.85)', navBorder: 'rgba(244, 63, 94, 0.3)', pillActive: '#881337', pillDim: 'rgba(255, 228, 230, 0.7)', pillActiveBg: '#f43f5e', thumbBg: 'rgba(244, 63, 94, 0.45)', vigA: 'rgba(45, 12, 20, 0.6)', vigB: 'rgba(15, 4, 7, 0.95)', panel: 'rgba(40, 15, 22, 0.65)', panelSolid: '#280f16', border: 'rgba(244, 63, 94, 0.2)', borderSoft: 'rgba(244, 63, 94, 0.1)' },
  teal: { bg: '#041416', accentHex: '#14b8a6', textMain: '#ccfbf1', textDim: '#5eead4', textFaint: 'rgba(204, 251, 241, 0.45)', navBg: 'rgba(4, 20, 22, 0.85)', navBorder: 'rgba(20, 184, 166, 0.3)', pillActive: '#134e4a', pillDim: 'rgba(204, 251, 241, 0.7)', pillActiveBg: '#14b8a6', thumbBg: 'rgba(20, 184, 166, 0.45)', vigA: 'rgba(10, 38, 40, 0.6)', vigB: 'rgba(2, 10, 12, 0.95)', panel: 'rgba(12, 35, 38, 0.65)', panelSolid: '#0c2326', border: 'rgba(20, 184, 166, 0.2)', borderSoft: 'rgba(20, 184, 166, 0.1)' }
};

// Qué tema de color usa cada día de la semana
const DAY_THEMES = { lunes: 'breathe', martes: 'meditate', miercoles: 'anxiety', jueves: 'nature', viernes: 'classical', sabado: 'jazz', domingo: 'sunset', semana: 'teal' };

// Atajo para buscar un elemento por su id
const $ = (id) => document.getElementById(id);

// Limpia el texto para que no se interprete como HTML (seguridad)
function escapeHtml(str) {
  const div = document.createElement('div');
  div.textContent = str ?? '';
  return div.innerHTML;
}

// Genera un id único y corto para cada alimento agregado
function uid() {
  return Date.now().toString(36) + Math.random().toString(36).slice(2, 8);
}

// Muestra un mensaje emergente (toast) de éxito o error
function notify(msg, type = 'error') {
  let box = $('toast-box');
  if (!box) {
    box = document.createElement('div');
    box.id = 'toast-box';
    document.body.appendChild(box);
  }
  const t = document.createElement('div');
  t.className = 'toast ' + type;
  t.textContent = msg;
  box.appendChild(t);
  setTimeout(() => t.remove(), 4500);
}

// Desactiva un botón mientras se espera una respuesta
function setBusy(btn, busy) {
  if (!btn) return;
  btn.disabled = busy;
  btn.style.opacity = busy ? '0.6' : '';
}

// Espera a que el backend de Python (pywebview) esté listo y devuelve su API
async function getApi() {
  const ready = () => window.pywebview && window.pywebview.api;
  if (ready()) return window.pywebview.api;
  await new Promise((resolve) => {
    const t = setTimeout(resolve, 1500);
    window.addEventListener('pywebviewready', () => { clearTimeout(t); resolve(); }, { once: true });
  });
  return ready() || null;
}

// Llama a un método del backend de Python; si falla devuelve un error en vez de romper la app
async function callApi(method, ...args) {
  const api = await getApi();
  if (!api || typeof api[method] !== 'function') return null;
  try {
    return await api[method](...args);
  } catch (e) {
    return { status: 'error', message: String(e && e.message ? e.message : e) };
  }
}

// Usuario con sesión, su perfil físico y si se está mostrando el formulario de login
let currentUser = null;
let userProfile = { weight: 70, height: 170, goal: 'mantener' };
let showingLogin = false; // al abrir se ve el formulario de registro

// Deja solo los datos seguros del usuario (sin contraseña) para guardarlos en el equipo
function publicUser(u) {
  return {
    id: u.id,
    nombre: u.nombre,
    email: u.email,
    genero: u.genero || 'no_especificado',
    avatar: u.avatar && u.avatar !== 'default.png' ? u.avatar : null
  };
}

// Lee de localStorage los perfiles guardados en este equipo
function loadSavedUsers() {
  try {
    const list = JSON.parse(localStorage.getItem('nutriplan_saved_users') || '[]');
    return Array.isArray(list) ? list.filter((u) => u && u.email).map(publicUser) : [];
  } catch (e) {
    return [];
  }
}

// Lista de perfiles guardados (decide si se muestra el registro o la pantalla de perfiles)
let savedUsers = loadSavedUsers();

// Guarda la lista de perfiles en localStorage
function persistSavedUsers() {
  try { localStorage.setItem('nutriplan_saved_users', JSON.stringify(savedUsers)); } catch (e) { /* sin almacenamiento */ }
}

// Agrega o actualiza un usuario en la lista guardada y recuerda el último correo
function saveUserToLocal(user) {
  const clean = publicUser(user);
  const i = savedUsers.findIndex((u) => u.email === clean.email);
  if (i === -1) savedUsers.push(clean); else savedUsers[i] = clean;
  persistSavedUsers();
  try { localStorage.setItem('nutriplan_last_email', clean.email); } catch (e) { /* sin almacenamiento */ }
}

// Quita un perfil de este equipo (no borra la cuenta del servidor)
function removeUser(email) {
  savedUsers = savedUsers.filter((u) => u.email !== email);
  persistSavedUsers();
  renderProfilesScreen();
}

// Cambia la paleta de colores de toda la app según el tema elegido
function switchTheme(themeKey) {
  const theme = T[themeKey];
  if (!theme) return;
  const root = document.documentElement;
  const vars = {
    '--bg': theme.bg, '--accent': theme.accentHex, '--accent-hex': theme.accentHex,
    '--accent-light': theme.textDim, '--text-main': theme.textMain, '--text-dim': theme.textDim,
    '--text-faint': theme.textFaint, '--nav-bg': theme.navBg, '--nav-border': theme.navBorder,
    '--pill-active': theme.pillActive, '--pill-dim': theme.pillDim, '--pill-active-bg': theme.pillActiveBg,
    '--thumb-bg': theme.thumbBg, '--vig-a': theme.vigA, '--vig-b': theme.vigB,
    '--panel': theme.panel, '--panel-solid': theme.panelSolid, '--border': theme.border,
    '--border-soft': theme.borderSoft
  };
  Object.entries(vars).forEach(([k, v]) => root.style.setProperty(k, v));
  const hex = theme.accentHex.replace('#', '');
  root.style.setProperty('--accent-rgb', [0, 2, 4].map((i) => parseInt(hex.substr(i, 2), 16)).join(', '));
}

// En registro y perfiles los temas rotan solos cada 7 segundos
const AUTH_THEME_ORDER = ['breathe', 'meditate', 'nature', 'jazz', 'teal', 'sunset', 'classical', 'anxiety'];
let authThemeIdx = 0;
let authThemeTimer = null;

// Inicia la rotación automática de temas
function startAuthThemes() {
  if (authThemeTimer) return;
  switchTheme(AUTH_THEME_ORDER[authThemeIdx]);
  if (window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  authThemeTimer = setInterval(() => {
    authThemeIdx = (authThemeIdx + 1) % AUTH_THEME_ORDER.length;
    switchTheme(AUTH_THEME_ORDER[authThemeIdx]);
  }, 7000);
}

// Detiene la rotación de temas (al entrar a la app)
function stopAuthThemes() {
  clearInterval(authThemeTimer);
  authThemeTimer = null;
}

// Muestra una sola pantalla (registro, perfiles o app) y oculta las demás
function showScreen(screenId) {
  if (screenId === 'profiles-screen' && savedUsers.length === 0) screenId = 'auth-screen';

  ['auth-screen', 'profiles-screen', 'app-screen'].forEach((id) => $(id).classList.add('is-hidden'));
  $(screenId).classList.remove('is-hidden');

  if (screenId === 'profiles-screen') renderProfilesScreen();
  if (screenId === 'auth-screen') {
    $('btn-back-to-profiles').style.visibility = savedUsers.length ? 'visible' : 'hidden';
  }
  if (screenId === 'app-screen') stopAuthThemes(); else startAuthThemes();
}

// Dibuja las tarjetas de perfiles; si no hay foto se muestra la inicial del nombre
function renderProfilesScreen() {
  const grid = $('profiles-grid');
  grid.innerHTML = '';

  savedUsers.forEach((u) => {
    const card = document.createElement('div');
    card.className = 'profile-card';

    const del = document.createElement('button');
    del.type = 'button';
    del.className = 'profile-delete-btn';
    del.title = 'Quitar este perfil del dispositivo';
    del.textContent = '✕';
    del.addEventListener('click', (ev) => { ev.stopPropagation(); removeUser(u.email); });

    const avatar = document.createElement('div');
    avatar.className = 'profile-avatar';
    if (u.avatar) {
      avatar.innerHTML = `<img src="${u.avatar}" alt="${escapeHtml(u.nombre || 'Usuario')}">`;
    } else {
      avatar.textContent = u.nombre ? u.nombre.charAt(0).toUpperCase() : 'U';
    }

    const name = document.createElement('div');
    name.className = 'profile-name';
    name.textContent = u.nombre || 'Usuario';

    const badge = document.createElement('div');
    badge.className = 'profile-gender-badge';
    badge.textContent = (u.genero || 'no especificado').replace(/_/g, ' ');

    card.append(del, avatar, name, badge);
    card.addEventListener('click', () => enterSavedProfile(u));
    grid.appendChild(card);
  });

  const addCard = document.createElement('div');
  addCard.className = 'profile-card profile-card-add';
  addCard.innerHTML = '<div class="profile-avatar">+</div><div class="profile-name">Agregar Usuario</div>';
  addCard.addEventListener('click', () => { showScreen('auth-screen'); });
  grid.appendChild(addCard);
}

// Lleva al formulario de inicio de sesión con el correo ya escrito
function goToLogin(email = '') {
  showScreen('auth-screen');
  if (!showingLogin) changeForm();
  $('login-email').value = email;
  $('login-pass').value = '';
  (email ? $('login-pass') : $('login-email')).focus();
}

// Entra a la app al tocar un perfil guardado
async function enterSavedProfile(u) {
  if (!u || !u.id) { goToLogin(u && u.email); return; }

  showLoading(`Cargando perfil de ${u.nombre || 'usuario'}...`);
  try {
    const res = await callApi('entrar_por_id', u.id);
    if (res === null) {
      await enterApp(u);
      return;
    }
    if (res.status !== 'success') {
      notify(res.message || 'No se pudo ingresar con este perfil. Inicia sesión de nuevo.');
      goToLogin(u.email);
      return;
    }
    saveUserToLocal(res.user);
    await enterApp(res.user);
  } finally {
    hideLoading();
  }
}

// Elementos de la animación que alterna entre registro e inicio de sesión
const switchCtn = document.querySelector('#switch-cnt');
const switchC1 = document.querySelector('#switch-c1');
const switchC2 = document.querySelector('#switch-c2');
const switchCircle = document.querySelectorAll('.switch__circle');
const aContainer = document.querySelector('#a-container');
const bContainer = document.querySelector('#b-container');

// Alterna entre el formulario de registro y el de inicio de sesión
function changeForm() {
  showingLogin = !showingLogin;
  switchCtn.classList.add('is-gx');
  setTimeout(() => switchCtn.classList.remove('is-gx'), 1250);

  switchCtn.classList.toggle('is-txr');
  switchCircle[0].classList.toggle('is-txr');
  switchCircle[1].classList.toggle('is-txr');

  switchC1.classList.toggle('is-hidden');
  switchC2.classList.toggle('is-hidden');
  aContainer.classList.toggle('is-txl');
  bContainer.classList.toggle('is-txl');
  bContainer.classList.toggle('is-z200');
}
document.querySelectorAll('.switch-btn').forEach((btn) => btn.addEventListener('click', changeForm));

// Guarda lo pendiente y cierra la sesión actual
async function leaveSession() {
  await flushPlanSave();
  await flushWaterSave();
  hydration.byDate = {};
  await callApi('cerrar_sesion');
  currentUser = null;
  planData = emptyPlan();
}

// Guarda lo pendiente y cierra la ventana del programa
const cerrarPrograma = async () => {
  await flushPlanSave();
  await flushWaterSave();
  const api = await getApi();
  if (api) await api.cerrar_programa(); else window.close();
};

// Botones de cerrar el programa y volver a los perfiles
$('btn-close-app-profiles').onclick = cerrarPrograma;
$('btn-close-app-auth').onclick = cerrarPrograma;

$('btn-back-to-profiles').onclick = () => { if (savedUsers.length > 0) showScreen('profiles-screen'); };

// Envío del formulario de registro
$('a-form').addEventListener('submit', async (e) => {
  e.preventDefault();
  const btn = e.target.querySelector('button[type="submit"]');
  const name = $('reg-name').value.trim();
  const email = $('reg-email').value.trim();
  const pass = $('reg-pass').value;
  const gender = $('reg-gender').value;

  setBusy(btn, true);
  try {
    const res = await callApi('registrar_usuario', name, email, pass, gender);
    if (res === null) {
      const mock = { nombre: name, email, genero: gender };
      saveUserToLocal(mock);
      await enterApp(mock);
      return;
    }
    if (res.status !== 'success') {
      notify(res.message || 'No se pudo crear la cuenta');
      return;
    }
    saveUserToLocal(res.user);
    e.target.reset();
    notify('¡Cuenta creada con éxito!', 'ok');
    await enterApp(res.user);
  } finally {
    setBusy(btn, false);
  }
});

// Envío del formulario de inicio de sesión
$('b-form').addEventListener('submit', async (e) => {
  e.preventDefault();
  const btn = e.target.querySelector('button[type="submit"]');
  const email = $('login-email').value.trim();
  const pass = $('login-pass').value;

  setBusy(btn, true);
  try {
    const res = await callApi('iniciar_sesion', email, pass);
    if (res === null) { // modo demo (sin Python)
      const mock = { nombre: email.split('@')[0], email, genero: 'no_especificado' };
      saveUserToLocal(mock);
      await enterApp(mock);
      return;
    }
    if (res.status !== 'success') {
      notify(res.message || 'No se pudo iniciar sesión');
      return;
    }
    saveUserToLocal(res.user);
    $('login-pass').value = '';
    await enterApp(res.user);
  } finally {
    setBusy(btn, false);
  }
});

// Datos base del plan: días de la semana y comidas del día
const DAYS = ['lunes', 'martes', 'miercoles', 'jueves', 'viernes', 'sabado', 'domingo'];
const DAY_NAMES = { lunes: 'Lunes', martes: 'Martes', miercoles: 'Miércoles', jueves: 'Jueves', viernes: 'Viernes', sabado: 'Sábado', domingo: 'Domingo' };
const MEALS = [{ id: 'desayuno', label: 'Desayuno' }, { id: 'almuerzo', label: 'Almuerzo' }, { id: 'cena', label: 'Cena' }];

// Categorías de alimentos (se reemplazan por las de la base de datos)
let CATEGORIES = [
  { id: 'todas', label: 'Todas' },
  { id: 'granos', label: 'Granos, Cereales y Tubérculos' },
  { id: 'legumbres', label: 'Legumbres' },
  { id: 'carnes', label: 'Carnes y Aves' },
  { id: 'pescados', label: 'Pescados y Mariscos' },
  { id: 'verduras', label: 'Verduras y Hortalizas' },
  { id: 'frutas', label: 'Frutas' },
  { id: 'lacteos', label: 'Lácteos y Huevos' },
  { id: 'grasas', label: 'Grasas, Aceites y Frutos Secos' },
  { id: 'bebidas', label: 'Bebidas' },
  { id: 'procesados', label: 'Procesados y Snacks' },
  { id: 'condimentos', label: 'Condimentos y Salsas' },
];

// Catálogo de alimentos con sus valores nutricionales (se reemplaza por el de la base de datos)
let FOOD_DATABASE = {
  granos: [
    { id: 'arroz_blanco', name: 'Arroz blanco (cocido)', baseUnit: 'g', baseAmount: 100, kcal: 130, protein: 2.7, fat: 0.3, carbs: 28 },
    { id: 'arroz_integral', name: 'Arroz integral (cocido)', baseUnit: 'g', baseAmount: 100, kcal: 111, protein: 2.6, fat: 0.9, carbs: 23 },
    { id: 'avena', name: 'Avena en hojuelas', baseUnit: 'g', baseAmount: 100, kcal: 389, protein: 16.9, fat: 6.9, carbs: 66 },
    { id: 'pasta', name: 'Pasta (cocida)', baseUnit: 'g', baseAmount: 100, kcal: 131, protein: 5, fat: 1.1, carbs: 25 },
    { id: 'pan_integral', name: 'Pan integral', baseUnit: 'g', baseAmount: 100, kcal: 247, protein: 13, fat: 3.4, carbs: 41 },
    { id: 'pan_blanco', name: 'Pan blanco', baseUnit: 'g', baseAmount: 100, kcal: 265, protein: 9, fat: 3.2, carbs: 49 },
    { id: 'quinoa', name: 'Quinoa (cocida)', baseUnit: 'g', baseAmount: 100, kcal: 120, protein: 4.4, fat: 1.9, carbs: 21.3 },
    { id: 'papa', name: 'Papa cocida', baseUnit: 'g', baseAmount: 100, kcal: 87, protein: 1.9, fat: 0.1, carbs: 20 },
    { id: 'papa_horneada', name: 'Papa horneada con cáscara', baseUnit: 'unidad', baseAmount: 1, kcal: 161, protein: 4.3, fat: 0.2, carbs: 37 },
    { id: 'yuca', name: 'Yuca cocida', baseUnit: 'g', baseAmount: 100, kcal: 160, protein: 1.4, fat: 0.3, carbs: 38 },
    { id: 'platano_verde', name: 'Plátano verde cocido', baseUnit: 'g', baseAmount: 100, kcal: 122, protein: 1.3, fat: 0.3, carbs: 32 },
    { id: 'maiz', name: 'Maíz dulce (grano)', baseUnit: 'g', baseAmount: 100, kcal: 96, protein: 3.4, fat: 1.5, carbs: 21 },
    { id: 'tortilla_maiz', name: 'Tortilla de maíz', baseUnit: 'unidad', baseAmount: 1, kcal: 52, protein: 1.4, fat: 0.6, carbs: 11 },
    { id: 'cuscus', name: 'Cuscús cocido', baseUnit: 'g', baseAmount: 100, kcal: 112, protein: 3.8, fat: 0.2, carbs: 23 }
  ],
  legumbres: [
    { id: 'lentejas', name: 'Lentejas (cocidas)', baseUnit: 'g', baseAmount: 100, kcal: 116, protein: 9, fat: 0.4, carbs: 20 },
    { id: 'garbanzos', name: 'Garbanzos (cocidos)', baseUnit: 'g', baseAmount: 100, kcal: 164, protein: 8.9, fat: 2.6, carbs: 27 },
    { id: 'frijol_negro', name: 'Frijol negro (cocido)', baseUnit: 'g', baseAmount: 100, kcal: 132, protein: 8.9, fat: 0.5, carbs: 24 },
    { id: 'frijol_rojo', name: 'Frijol rojo (cocido)', baseUnit: 'g', baseAmount: 100, kcal: 127, protein: 8.7, fat: 0.5, carbs: 22.8 },
    { id: 'arveja', name: 'Arvejas / Guisantes', baseUnit: 'g', baseAmount: 100, kcal: 81, protein: 5.4, fat: 0.4, carbs: 14.5 },
    { id: 'habas', name: 'Habas cocidas', baseUnit: 'g', baseAmount: 100, kcal: 110, protein: 7.9, fat: 0.4, carbs: 19.6 },
    { id: 'soya_texturizada', name: 'Soya texturizada (hidratada)', baseUnit: 'g', baseAmount: 100, kcal: 120, protein: 18, fat: 1, carbs: 9 }
  ],
  carnes: [
    { id: 'pechuga_pollo', name: 'Pechuga de pollo (cocida)', baseUnit: 'g', baseAmount: 100, kcal: 165, protein: 31, fat: 3.6, carbs: 0 },
    { id: 'muslo_pollo', name: 'Muslo de pollo (cocido, sin piel)', baseUnit: 'g', baseAmount: 100, kcal: 178, protein: 24, fat: 8.5, carbs: 0 },
    { id: 'carne_res', name: 'Carne de res magra', baseUnit: 'g', baseAmount: 100, kcal: 250, protein: 26, fat: 15, carbs: 0 },
    { id: 'carne_molida', name: 'Carne molida (80/20, cocida)', baseUnit: 'g', baseAmount: 100, kcal: 254, protein: 25.6, fat: 16.5, carbs: 0 },
    { id: 'lomo_cerdo', name: 'Lomo de cerdo (cocido)', baseUnit: 'g', baseAmount: 100, kcal: 242, protein: 27, fat: 14, carbs: 0 },
    { id: 'pavo_pechuga', name: 'Pechuga de pavo (cocida)', baseUnit: 'g', baseAmount: 100, kcal: 135, protein: 30, fat: 0.7, carbs: 0 },
    { id: 'tocino', name: 'Tocino frito', baseUnit: 'g', baseAmount: 100, kcal: 541, protein: 37, fat: 42, carbs: 1.4 },
    { id: 'jamon', name: 'Jamón de pavo/cerdo', baseUnit: 'g', baseAmount: 100, kcal: 145, protein: 21, fat: 4.5, carbs: 1.5 },
    { id: 'chorizo', name: 'Chorizo', baseUnit: 'g', baseAmount: 100, kcal: 455, protein: 24, fat: 38, carbs: 3 },
    { id: 'higado_res', name: 'Hígado de res (cocido)', baseUnit: 'g', baseAmount: 100, kcal: 175, protein: 26, fat: 4.9, carbs: 3.9 },
    { id: 'tofu', name: 'Tofu firme', baseUnit: 'g', baseAmount: 100, kcal: 76, protein: 8, fat: 4.8, carbs: 1.9 },
    { id: 'huevo', name: 'Huevo entero', baseUnit: 'unidad', baseAmount: 1, kcal: 72, protein: 6.3, fat: 4.8, carbs: 0.4 },
    { id: 'clara_huevo', name: 'Clara de huevo', baseUnit: 'unidad', baseAmount: 1, kcal: 17, protein: 3.6, fat: 0.1, carbs: 0.2 }
  ],
  pescados: [
    { id: 'salmon', name: 'Filete de salmón', baseUnit: 'g', baseAmount: 100, kcal: 208, protein: 20, fat: 13, carbs: 0 },
    { id: 'atun', name: 'Atún en agua (enlatado)', baseUnit: 'g', baseAmount: 100, kcal: 116, protein: 26, fat: 1, carbs: 0 },
    { id: 'atun_fresco', name: 'Atún fresco (a la plancha)', baseUnit: 'g', baseAmount: 100, kcal: 184, protein: 30, fat: 6.3, carbs: 0 },
    { id: 'tilapia', name: 'Filete de tilapia', baseUnit: 'g', baseAmount: 100, kcal: 128, protein: 26, fat: 2.7, carbs: 0 },
    { id: 'camaron', name: 'Camarones cocidos', baseUnit: 'g', baseAmount: 100, kcal: 99, protein: 24, fat: 0.3, carbs: 0.2 },
    { id: 'merluza', name: 'Merluza al horno', baseUnit: 'g', baseAmount: 100, kcal: 90, protein: 18.6, fat: 1, carbs: 0 },
    { id: 'sardina', name: 'Sardinas en aceite (enlatadas)', baseUnit: 'g', baseAmount: 100, kcal: 208, protein: 25, fat: 11, carbs: 0 },
    { id: 'pulpo', name: 'Pulpo cocido', baseUnit: 'g', baseAmount: 100, kcal: 164, protein: 30, fat: 2.1, carbs: 4.4 }
  ],
  verduras: [
    { id: 'brocoli', name: 'Brócoli (cocido)', baseUnit: 'g', baseAmount: 100, kcal: 35, protein: 2.4, fat: 0.4, carbs: 7 },
    { id: 'espinacas', name: 'Espinaca fresca', baseUnit: 'g', baseAmount: 100, kcal: 23, protein: 2.9, fat: 0.4, carbs: 3.6 },
    { id: 'zanahoria', name: 'Zanahoria', baseUnit: 'g', baseAmount: 100, kcal: 41, protein: 0.9, fat: 0.2, carbs: 10 },
    { id: 'tomate', name: 'Tomate fresco', baseUnit: 'g', baseAmount: 100, kcal: 18, protein: 0.9, fat: 0.2, carbs: 3.9 },
    { id: 'aguacate', name: 'Aguacate', baseUnit: 'g', baseAmount: 100, kcal: 160, protein: 2, fat: 15, carbs: 9 },
    { id: 'lechuga', name: 'Lechuga', baseUnit: 'g', baseAmount: 100, kcal: 15, protein: 1.4, fat: 0.2, carbs: 2.9 },
    { id: 'pepino', name: 'Pepino', baseUnit: 'g', baseAmount: 100, kcal: 15, protein: 0.7, fat: 0.1, carbs: 3.6 },
    { id: 'cebolla', name: 'Cebolla', baseUnit: 'g', baseAmount: 100, kcal: 40, protein: 1.1, fat: 0.1, carbs: 9.3 },
    { id: 'pimenton', name: 'Pimentón / Pimiento', baseUnit: 'g', baseAmount: 100, kcal: 31, protein: 1, fat: 0.3, carbs: 6 },
    { id: 'coliflor', name: 'Coliflor (cocida)', baseUnit: 'g', baseAmount: 100, kcal: 25, protein: 1.9, fat: 0.3, carbs: 5 },
    { id: 'calabacin', name: 'Calabacín / Zucchini', baseUnit: 'g', baseAmount: 100, kcal: 17, protein: 1.2, fat: 0.3, carbs: 3.1 },
    { id: 'champinones', name: 'Champiñones', baseUnit: 'g', baseAmount: 100, kcal: 22, protein: 3.1, fat: 0.3, carbs: 3.3 },
    { id: 'remolacha', name: 'Remolacha cocida', baseUnit: 'g', baseAmount: 100, kcal: 44, protein: 1.7, fat: 0.2, carbs: 10 },
    { id: 'apio', name: 'Apio', baseUnit: 'g', baseAmount: 100, kcal: 16, protein: 0.7, fat: 0.2, carbs: 3 }
  ],
  frutas: [
    { id: 'manzana', name: 'Manzana', baseUnit: 'unidad', baseAmount: 1, kcal: 95, protein: 0.5, fat: 0.3, carbs: 25 },
    { id: 'banano', name: 'Banano / Plátano', baseUnit: 'unidad', baseAmount: 1, kcal: 105, protein: 1.3, fat: 0.4, carbs: 27 },
    { id: 'fresa', name: 'Fresas', baseUnit: 'g', baseAmount: 100, kcal: 32, protein: 0.7, fat: 0.3, carbs: 7.7 },
    { id: 'naranja', name: 'Naranja', baseUnit: 'unidad', baseAmount: 1, kcal: 62, protein: 1.2, fat: 0.2, carbs: 15 },
    { id: 'pera', name: 'Pera', baseUnit: 'unidad', baseAmount: 1, kcal: 101, protein: 0.6, fat: 0.2, carbs: 27 },
    { id: 'uva', name: 'Uvas', baseUnit: 'g', baseAmount: 100, kcal: 69, protein: 0.7, fat: 0.2, carbs: 18 },
    { id: 'piña', name: 'Piña', baseUnit: 'g', baseAmount: 100, kcal: 50, protein: 0.5, fat: 0.1, carbs: 13 },
    { id: 'mango', name: 'Mango', baseUnit: 'unidad', baseAmount: 1, kcal: 202, protein: 2.8, fat: 1.3, carbs: 50 },
    { id: 'papaya', name: 'Papaya', baseUnit: 'g', baseAmount: 100, kcal: 43, protein: 0.5, fat: 0.3, carbs: 11 },
    { id: 'sandia', name: 'Sandía', baseUnit: 'g', baseAmount: 100, kcal: 30, protein: 0.6, fat: 0.2, carbs: 7.6 },
    { id: 'melon', name: 'Melón', baseUnit: 'g', baseAmount: 100, kcal: 34, protein: 0.8, fat: 0.2, carbs: 8.2 },
    { id: 'kiwi', name: 'Kiwi', baseUnit: 'unidad', baseAmount: 1, kcal: 42, protein: 0.8, fat: 0.4, carbs: 10 },
    { id: 'mandarina', name: 'Mandarina', baseUnit: 'unidad', baseAmount: 1, kcal: 47, protein: 0.7, fat: 0.3, carbs: 12 },
    { id: 'mora', name: 'Moras', baseUnit: 'g', baseAmount: 100, kcal: 43, protein: 1.4, fat: 0.5, carbs: 9.6 }
  ],
  lacteos: [
    { id: 'leche_entera', name: 'Leche entera', baseUnit: 'ml', baseAmount: 100, kcal: 61, protein: 3.2, fat: 3.2, carbs: 4.8 },
    { id: 'leche_descremada', name: 'Leche descremada', baseUnit: 'ml', baseAmount: 100, kcal: 35, protein: 3.4, fat: 0.1, carbs: 5 },
    { id: 'yogur_griego', name: 'Yogur griego natural', baseUnit: 'g', baseAmount: 100, kcal: 59, protein: 10, fat: 0.4, carbs: 3.6 },
    { id: 'yogur_natural', name: 'Yogur natural entero', baseUnit: 'g', baseAmount: 100, kcal: 61, protein: 3.5, fat: 3.3, carbs: 4.7 },
    { id: 'queso_fresco', name: 'Queso fresco', baseUnit: 'g', baseAmount: 100, kcal: 264, protein: 18, fat: 20, carbs: 3 },
    { id: 'queso_mozzarella', name: 'Queso mozzarella', baseUnit: 'g', baseAmount: 100, kcal: 280, protein: 28, fat: 17, carbs: 3.1 },
    { id: 'queso_crema', name: 'Queso crema', baseUnit: 'g', baseAmount: 100, kcal: 342, protein: 6, fat: 34, carbs: 4 },
    { id: 'mantequilla', name: 'Mantequilla', baseUnit: 'g', baseAmount: 100, kcal: 717, protein: 0.9, fat: 81, carbs: 0.1 },
    { id: 'kumis', name: 'Kumis / Kéfir', baseUnit: 'ml', baseAmount: 100, kcal: 56, protein: 3.3, fat: 2, carbs: 4.5 }
  ],
  grasas: [
    { id: 'aceite_oliva', name: 'Aceite de oliva', baseUnit: 'ml', baseAmount: 15, kcal: 119, protein: 0, fat: 13.5, carbs: 0 },
    { id: 'aceite_vegetal', name: 'Aceite vegetal', baseUnit: 'ml', baseAmount: 15, kcal: 120, protein: 0, fat: 14, carbs: 0 },
    { id: 'almendras', name: 'Almendras', baseUnit: 'g', baseAmount: 100, kcal: 579, protein: 21, fat: 50, carbs: 22 },
    { id: 'nueces', name: 'Nueces', baseUnit: 'g', baseAmount: 100, kcal: 654, protein: 15, fat: 65, carbs: 14 },
    { id: 'mani', name: 'Maní / Cacahuate', baseUnit: 'g', baseAmount: 100, kcal: 567, protein: 26, fat: 49, carbs: 16 },
    { id: 'mantequilla_mani', name: 'Mantequilla de maní', baseUnit: 'g', baseAmount: 100, kcal: 588, protein: 25, fat: 50, carbs: 20 },
    { id: 'semillas_chia', name: 'Semillas de chía', baseUnit: 'g', baseAmount: 100, kcal: 486, protein: 17, fat: 31, carbs: 42 },
    { id: 'frutos_secos', name: 'Frutos secos mixtos', baseUnit: 'g', baseAmount: 100, kcal: 607, protein: 20, fat: 54, carbs: 21 },
    { id: 'coco_rallado', name: 'Coco rallado', baseUnit: 'g', baseAmount: 100, kcal: 660, protein: 6.9, fat: 64, carbs: 24 }
  ],
  bebidas: [
    { id: 'agua', name: 'Agua', baseUnit: 'ml', baseAmount: 250, kcal: 0, protein: 0, fat: 0, carbs: 0 },
    { id: 'jugo_naranja', name: 'Jugo de naranja natural', baseUnit: 'ml', baseAmount: 200, kcal: 90, protein: 1.4, fat: 0.4, carbs: 21 },
    { id: 'cafe_negro', name: 'Café negro sin azúcar', baseUnit: 'ml', baseAmount: 200, kcal: 2, protein: 0.3, fat: 0, carbs: 0 },
    { id: 'te_verde', name: 'Té verde', baseUnit: 'ml', baseAmount: 200, kcal: 2, protein: 0, fat: 0, carbs: 0 },
    { id: 'gaseosa', name: 'Gaseosa / Refresco', baseUnit: 'ml', baseAmount: 350, kcal: 140, protein: 0, fat: 0, carbs: 39 },
    { id: 'bebida_energizante', name: 'Bebida energizante', baseUnit: 'ml', baseAmount: 250, kcal: 110, protein: 0, fat: 0, carbs: 28 },
    { id: 'cerveza', name: 'Cerveza', baseUnit: 'ml', baseAmount: 330, kcal: 150, protein: 1.6, fat: 0, carbs: 13 },
    { id: 'batido_proteina', name: 'Batido de proteína (agua)', baseUnit: 'g', baseAmount: 30, kcal: 120, protein: 24, fat: 1.5, carbs: 3 },
    { id: 'leche_almendras', name: 'Leche de almendras', baseUnit: 'ml', baseAmount: 100, kcal: 15, protein: 0.6, fat: 1.2, carbs: 0.6 }
  ],
  procesados: [
    { id: 'papas_fritas', name: 'Papas fritas', baseUnit: 'g', baseAmount: 100, kcal: 536, protein: 7, fat: 35, carbs: 53 },
    { id: 'chocolate_negro', name: 'Chocolate negro 70%', baseUnit: 'g', baseAmount: 100, kcal: 598, protein: 7.8, fat: 42, carbs: 46 },
    { id: 'chocolate_leche', name: 'Chocolate con leche', baseUnit: 'g', baseAmount: 100, kcal: 535, protein: 7.6, fat: 30, carbs: 59 },
    { id: 'galletas_dulces', name: 'Galletas dulces', baseUnit: 'g', baseAmount: 100, kcal: 480, protein: 6, fat: 22, carbs: 65 },
    { id: 'helado', name: 'Helado de vainilla', baseUnit: 'g', baseAmount: 100, kcal: 207, protein: 3.5, fat: 11, carbs: 24 },
    { id: 'pizza', name: 'Pizza (porción)', baseUnit: 'g', baseAmount: 100, kcal: 266, protein: 11, fat: 10, carbs: 33 },
    { id: 'hamburguesa', name: 'Hamburguesa completa', baseUnit: 'unidad', baseAmount: 1, kcal: 540, protein: 25, fat: 27, carbs: 45 },
    { id: 'nuggets_pollo', name: 'Nuggets de pollo', baseUnit: 'g', baseAmount: 100, kcal: 296, protein: 15, fat: 19, carbs: 17 },
    { id: 'cereal_azucarado', name: 'Cereal azucarado', baseUnit: 'g', baseAmount: 100, kcal: 380, protein: 5, fat: 2, carbs: 84 },
    { id: 'barra_energetica', name: 'Barra energética / granola', baseUnit: 'unidad', baseAmount: 1, kcal: 190, protein: 4, fat: 7, carbs: 29 },
    { id: 'pan_dulce', name: 'Pan dulce / ponqué', baseUnit: 'g', baseAmount: 100, kcal: 371, protein: 5.5, fat: 15, carbs: 55 }
  ],
  condimentos: [
    { id: 'sal', name: 'Sal', baseUnit: 'g', baseAmount: 5, kcal: 0, protein: 0, fat: 0, carbs: 0 },
    { id: 'azucar', name: 'Azúcar blanca', baseUnit: 'g', baseAmount: 5, kcal: 19, protein: 0, fat: 0, carbs: 5 },
    { id: 'miel', name: 'Miel de abejas', baseUnit: 'g', baseAmount: 15, kcal: 46, protein: 0, fat: 0, carbs: 12.5 },
    { id: 'salsa_tomate', name: 'Salsa de tomate / ketchup', baseUnit: 'g', baseAmount: 20, kcal: 20, protein: 0.3, fat: 0.1, carbs: 4.7 },
    { id: 'mayonesa', name: 'Mayonesa', baseUnit: 'g', baseAmount: 15, kcal: 94, protein: 0.1, fat: 10.3, carbs: 0.6 },
    { id: 'mostaza', name: 'Mostaza', baseUnit: 'g', baseAmount: 15, kcal: 11, protein: 0.6, fat: 0.6, carbs: 1 },
    { id: 'salsa_soya', name: 'Salsa de soya', baseUnit: 'ml', baseAmount: 15, kcal: 8, protein: 1.3, fat: 0, carbs: 0.8 },
    { id: 'vinagreta', name: 'Vinagreta / aderezo', baseUnit: 'ml', baseAmount: 15, kcal: 45, protein: 0, fat: 4.5, carbs: 1.5 }
  ],
};

// Pide a la base de datos las categorías y alimentos y reemplaza los de ejemplo
async function cargarCatalogosDesdeBD() {
  const res = await callApi('obtener_catalogos');
  if (!res || res.status !== 'success') return;

  if (Array.isArray(res.categorias) && res.categorias.length) {
    CATEGORIES = [
      { id: 'todas', label: 'Todas' },
      ...res.categorias.map((c) => ({ id: c.id, label: c.nombre })),
    ];
  }

  if (Array.isArray(res.alimentos) && res.alimentos.length) {
    const nuevo = {};
    res.alimentos.forEach((a) => {
      const catId = a.categoria_id || 'otros';
      if (!nuevo[catId]) nuevo[catId] = [];
      nuevo[catId].push({
        id: a.id,
        name: a.nombre,
        baseUnit: a.unidad_base,
        baseAmount: a.cantidad_base,
        kcal: a.kcal,
        protein: a.proteina,
        fat: a.grasa,
        carbs: a.carbohidratos,
      });
    });
    FOOD_DATABASE = nuevo;
  }
}

// Estado del plan semanal y de la interfaz (día, categoría y comida en edición)
let planData = null;
let activeTab = 'lunes';
let activeCategory = 'todas';
let editingTarget = null;
let editingItemIndex = null;

// Crea un plan vacío: cada día con desayuno, almuerzo y cena sin alimentos
function emptyPlan() {
  const plan = {};
  DAYS.forEach((d) => {
    plan[d] = {};
    MEALS.forEach((m) => { plan[d][m.id] = []; });
  });
  return plan;
}
planData = emptyPlan();

// Plan de ejemplo para el modo demo (cuando no hay backend)
const DEMO_ROWS = [
  { dia: 'lunes', comida: 'desayuno', alimento_id: 'avena', cantidad: 50, unidad: 'g' },
  { dia: 'lunes', comida: 'desayuno', alimento_id: 'banano', cantidad: 1, unidad: 'unidad' },
  { dia: 'lunes', comida: 'almuerzo', alimento_id: 'pechuga_pollo', cantidad: 200, unidad: 'g' },
  { dia: 'lunes', comida: 'almuerzo', alimento_id: 'arroz_blanco', cantidad: 150, unidad: 'g' },
  { dia: 'lunes', comida: 'almuerzo', alimento_id: 'brocoli', cantidad: 100, unidad: 'g' },
  { dia: 'lunes', comida: 'cena', alimento_id: 'salmon', cantidad: 150, unidad: 'g' }
];

// Busca un alimento por su id en todo el catálogo
function findFood(foodId) {
  for (const cat of Object.keys(FOOD_DATABASE)) {
    const food = FOOD_DATABASE[cat].find((f) => f.id === foodId);
    if (food) return { cat, food };
  }
  return null;
}

// Crea un alimento del plan con sus calorías y macros ya calculados
function buildItem(cat, food, qty, unit) {
  const m = calculateMacros(food, qty, unit);
  return {
    id: uid(),
    foodId: food.id,
    name: food.name,
    cat,
    qty,
    unit,
    portionStr: `${qty} ${unit}`,
    kcal: m.kcal,
    fat: m.fat,
    protein: m.protein,
    carbs: m.carbs
  };
}

// Convierte las filas de la base de datos en el plan semanal
function planFromRows(rows) {
  const plan = emptyPlan();
  (Array.isArray(rows) ? rows : []).forEach((r) => {
    if (!r || !plan[r.dia] || !plan[r.dia][r.comida]) return;
    const found = findFood(r.alimento_id);
    const qty = Number(r.cantidad);
    if (!found || !(qty > 0)) return;
    plan[r.dia][r.comida].push(buildItem(found.cat, found.food, qty, String(r.unidad)));
  });
  return plan;
}

// Convierte el plan semanal en filas para guardar en la base de datos
function planToRows() {
  const rows = [];
  DAYS.forEach((d) => MEALS.forEach((m) => {
    (planData[d][m.id] || []).forEach((i) => {
      rows.push({ dia: d, comida: m.id, alimento_id: i.foodId, cantidad: i.qty, unidad: i.unit });
    });
  }));
  return rows;
}

// Control del guardado automático del plan
let saveTimer = null;
let saving = false;
let dirty = false;

// Programa el guardado automático 0,6 s después del último cambio
function schedulePlanSave() {
  if (!currentUser) return;
  clearTimeout(saveTimer);
  saveTimer = setTimeout(savePlanNow, 600);
}

// Guarda el plan en la base de datos (si hay otro cambio durante el guardado, repite)
async function savePlanNow() {
  saveTimer = null;
  if (!currentUser) return;
  if (saving) { dirty = true; return; }
  saving = true;
  try {
    do {
      dirty = false;
      const res = await callApi('guardar_plan', planToRows());
      if (res && res.status === 'error') notify('No se pudo guardar el plan: ' + res.message);
    } while (dirty);
  } finally {
    saving = false;
  }
}

// Termina cualquier guardado pendiente (antes de salir o cerrar sesión)
async function flushPlanSave() {
  if (saveTimer) { clearTimeout(saveTimer); await savePlanNow(); }
  while (saving) await new Promise((r) => setTimeout(r, 50));
}

// Suma calorías y macros de una comida (con filtro opcional de categoría)
function getMealTotals(items, catFilter = 'todas') {
  let kcal = 0, fat = 0, protein = 0, carbs = 0, count = 0;
  items.forEach(i => {
    if (catFilter === 'todas' || i.cat === catFilter) {
      kcal += i.kcal || 0;
      fat += i.fat || 0;
      protein += i.protein || 0;
      carbs += i.carbs || 0;
      count++;
    }
  });
  return { kcal: Math.round(kcal), fat, protein, carbs, count };
}

// Suma los totales de un día completo
function getDayTotals(day, catFilter = 'todas') {
  const meals = planData[day] || {};
  let kcal = 0, fat = 0, protein = 0, carbs = 0, count = 0;
  Object.values(meals).forEach(itemList => {
    const t = getMealTotals(itemList, catFilter);
    kcal += t.kcal; fat += t.fat; protein += t.protein; carbs += t.carbs; count += t.count;
  });
  return { kcal: Math.round(kcal), fat, protein, carbs, count };
}

// Suma los totales de la semana completa
function getWeekTotals(catFilter = 'todas') {
  let kcal = 0, fat = 0, protein = 0, carbs = 0, count = 0;
  DAYS.forEach(d => {
    const t = getDayTotals(d, catFilter);
    kcal += t.kcal; fat += t.fat; protein += t.protein; carbs += t.carbs; count += t.count;
  });
  return { kcal, fat, protein, carbs, count };
}

// Calcula calorías, proteína, grasa y carbohidratos según la cantidad y la unidad
function calculateMacros(food, qty, unit) {
  if (!food || isNaN(qty) || qty <= 0) return { kcal: 0, protein: 0, fat: 0, carbs: 0 };
  let gramsOrMl = qty;
  if (unit === 'kg' || unit === 'l') gramsOrMl = qty * 1000;

  const multiplier = (food.baseUnit === 'g' || food.baseUnit === 'ml') 
    ? (gramsOrMl / food.baseAmount) 
    : (qty / food.baseAmount);

  return {
    kcal: Math.round(food.kcal * multiplier),
    protein: parseFloat((food.protein * multiplier).toFixed(1)),
    fat: parseFloat((food.fat * multiplier).toFixed(1)),
    carbs: parseFloat((food.carbs * multiplier).toFixed(1))
  };
}

// Cambia de día: aplica su tema de color y vuelve a dibujar
function selectDay(dayKey) {
  activeTab = dayKey;
  switchTheme(DAY_THEMES[dayKey] || 'anxiety');
  render();
}

// Dibuja los botones de días y de categorías
function renderNavs() {
  const daysNav = document.getElementById('daysNav');
  daysNav.innerHTML = '';

  DAYS.forEach(d => {
    const btn = document.createElement('button');
    btn.className = 'nav-item' + (activeTab === d ? ' active' : '') + (d === todayKey() ? ' is-today' : '');
    btn.textContent = DAY_NAMES[d];
    btn.onclick = () => selectDay(d);
    daysNav.appendChild(btn);
  });

  const weekBtn = document.createElement('button');
  weekBtn.className = 'nav-item' + (activeTab === 'semana' ? ' active' : '');
  weekBtn.textContent = 'Semana Completa';
  weekBtn.onclick = () => selectDay('semana');
  daysNav.appendChild(weekBtn);

  const catNav = document.getElementById('catNav');
  catNav.innerHTML = '';
  CATEGORIES.forEach(c => {
    const btn = document.createElement('button');
    btn.className = 'pill pill-cat' + (activeCategory === c.id ? ' active' : '');
    btn.textContent = c.label;
    btn.onclick = () => { activeCategory = c.id; render(); };
    catNav.appendChild(btn);
  });
}

// Rangos recomendados de calorías, carbohidratos y grasas según peso y objetivo
function getNutritionTargets() {
  const weight = userProfile.weight > 0 ? userProfile.weight : 70;
  let minKcal, maxKcal, carbPctRange, fatPctRange;

  if (userProfile.goal === 'bajar') {
    minKcal = Math.round(weight * 20);
    maxKcal = Math.round(weight * 25);
    carbPctRange = [35, 50];
    fatPctRange = [20, 30];
  } else if (userProfile.goal === 'subir') {
    minKcal = Math.round(weight * 33);
    maxKcal = Math.round(weight * 40);
    carbPctRange = [50, 65];
    fatPctRange = [20, 35];
  } else {
    minKcal = Math.round(weight * 26);
    maxKcal = Math.round(weight * 32);
    carbPctRange = [45, 60];
    fatPctRange = [20, 35];
  }

  return { minKcal, maxKcal, carbPctRange, fatPctRange };
}

// Compara lo planeado con los rangos y lista lo que está fuera de ellos
function evaluateNutrition(kcal, fat, carbs) {
  const t = getNutritionTargets();
  const issues = [];

  const goalText = userProfile.goal === 'bajar' ? 'tu objetivo de bajar peso' : (userProfile.goal === 'subir' ? 'tu objetivo de subir peso' : 'mantenimiento');

  if (kcal > t.maxKcal) {
    issues.push({
      level: 3,
      icon: '🚨',
      text: `exceso calórico (${Math.round(kcal)} kcal frente al máximo sugerido de ${t.maxKcal} kcal para ${goalText})`
    });
  } else if (kcal > 0 && kcal < t.minKcal) {
    issues.push({
      level: 2,
      icon: '💡',
      text: `ingesta calórica por debajo del objetivo (${Math.round(kcal)} kcal; se recomiendan al menos ${t.minKcal} kcal para ${goalText})`
    });
  }

  if (kcal > 0) {
    const carbPct = (carbs * 4 / kcal) * 100;
    const fatPct = (fat * 9 / kcal) * 100;
    const carbMax = t.carbPctRange[1];
    const fatMax = t.fatPctRange[1];

    if (carbPct > carbMax + 10) {
      issues.push({ level: 3, icon: '⚠️', text: `proporción de carbohidratos muy alta (${carbPct.toFixed(0)}% de tus calorías; ideal hasta ${carbMax}% para ${goalText})` });
    } else if (carbPct > carbMax) {
      issues.push({ level: 1, icon: '⚠️', text: `carbohidratos algo por encima de lo ideal (${carbPct.toFixed(0)}% de tus calorías; ideal hasta ${carbMax}% para ${goalText})` });
    }

    if (fatPct > fatMax + 10) {
      issues.push({ level: 3, icon: '⚠️', text: `proporción de grasas muy alta (${fatPct.toFixed(0)}% de tus calorías; ideal hasta ${fatMax}%)` });
    } else if (fatPct > fatMax) {
      issues.push({ level: 1, icon: '⚠️', text: `grasas algo por encima de lo ideal (${fatPct.toFixed(0)}% de tus calorías; ideal hasta ${fatMax}%)` });
    }
  }

  issues.sort((a, b) => b.level - a.level);
  return issues;
}

// Rangos recomendados para la semana completa
function getWeeklyNutritionTargets() {
  const t = getNutritionTargets();
  const days = DAYS.length;
  return { ...t, minWeekKcal: t.minKcal * days, maxWeekKcal: t.maxKcal * days };
}

// Arma el mensaje de alerta a partir de los problemas encontrados
function buildWarningFromIssues(issues, okMsg, targetLine, scopeLabel = 'del día') {
  const fullOkMsg = targetLine ? `${okMsg} ${targetLine}` : okMsg;

  if (issues.length === 0) {
    return { type: 'ok', icon: '✅', title: `Balance Óptimo ${scopeLabel}`, msg: fullOkMsg };
  }
  const top = issues[0];
  const type = top.level >= 3 ? 'danger' : 'warn';
  const title = top.level >= 3 ? `Ajusta tu alimentación ${scopeLabel}` : `Recomendación de Equilibrio ${scopeLabel}`;
  const detected = 'Se detectó ' + issues.map((i) => i.text).join('; ') + '.';
  const msg = targetLine ? `${detected} ${targetLine}` : detected;
  return { type, icon: top.icon, title, msg };
}

// Nombres legibles de cada objetivo
const GOAL_NAMES = { bajar: 'bajar de peso', mantener: 'mantener peso', subir: 'subir de peso' };

// Texto del perfil del usuario que se muestra en las alertas
function profileText() {
  return `tu peso de ${userProfile.weight} kg y tu objetivo de ${GOAL_NAMES[userProfile.goal] || 'mantener peso'}`;
}

// Genera la alerta nutricional de un día
function getWarning(dayTotals, dayLabel) {
  const { kcal, fat, count, carbs } = dayTotals;

  if (count === 0) {
    return { type: 'warn', icon: '⚠️', title: 'Sin registros', msg: 'No se encontraron alimentos en el menú actual con el filtro aplicado.' };
  }

  const t = getNutritionTargets();
  const issues = evaluateNutrition(kcal, fat, carbs);
  const perfilTxt = profileText();
  const targetLine = `Para ${dayLabel || 'este día'}, según ${perfilTxt}, el objetivo es de ${t.minKcal}–${t.maxKcal} kcal.`;
  return buildWarningFromIssues(issues, `El aporte nutricional de ${dayLabel || 'este día'} está bien equilibrado para ${perfilTxt}.`, targetLine, 'del día');
}

// Genera la alerta nutricional de la semana
function getWeeklyWarning(weekTotals) {
  if (!weekTotals.count) {
    return { type: 'warn', icon: '⚠️', title: 'Sin registros', msg: 'No se encontraron alimentos en el menú semanal con el filtro aplicado.' };
  }

  const days = DAYS.length;
  const t = getWeeklyNutritionTargets();
  const issues = evaluateNutrition(weekTotals.kcal / days, weekTotals.fat / days, weekTotals.carbs / days);
  const perfilTxt = profileText();
  const targetLine = `Según ${perfilTxt}, se recomienda consumir entre ${t.minKcal} y ${t.maxKcal} kcal al día, y entre ${t.minWeekKcal} y ${t.maxWeekKcal} kcal en total durante la semana.`;
  return buildWarningFromIssues(issues, `El promedio diario de la semana está bien equilibrado para ${perfilTxt}.`, targetLine, 'de la semana');
}

// Crea el HTML del cuadro de alerta
function buildAlertBox(warn, extraText = '', showFilter = true) {
  const div = document.createElement('div');
  div.className = `alert-box ${warn.type}`;
  const filtro = showFilter && activeCategory !== 'todas' ? ` (Filtro: ${activeCategory.toUpperCase()})` : '';
  div.innerHTML = `
    <div class="alert-icon">${warn.icon}</div>
    <div class="alert-content">
      <h4>${escapeHtml(warn.title)}${escapeHtml(filtro)}</h4>
      <p>${escapeHtml(warn.msg)}${escapeHtml(extraText)}</p>
    </div>
  `;
  return div;
}

// Dibuja el contenido principal: vista de un día o de la semana
function renderMain() {
  const container = document.getElementById('mainContainer');
  container.innerHTML = '';

  if (activeTab === 'semana') {
    renderWeekView(container);
  } else {
    renderDayView(container, activeTab);
  }
}

// Vista de un día: tarjetas de desayuno, almuerzo y cena
function renderDayView(container, day) {
  const totals = getDayTotals(day, activeCategory);
  container.appendChild(buildAlertBox(getWarning(totals, DAY_NAMES[day])));

  const grid = document.createElement('div');
  grid.className = 'day-grid';

  MEALS.forEach(m => {
    const items = planData[day][m.id] || [];
    const filteredItems = items.filter(i => activeCategory === 'todas' || i.cat === activeCategory);
    const mTotals = getMealTotals(items, activeCategory);

    const card = document.createElement('div');
    card.className = 'meal-card';

    let itemsHTML = filteredItems.length === 0 
      ? `<div class="meal-empty">No hay alimentos registrados</div>`
      : filteredItems.map(item => `
        <div class="food-item">
          <div class="food-info">
            <span class="food-name">${escapeHtml(item.name)}</span>
            <span class="food-portion">Porción: ${escapeHtml(item.portionStr)}</span>
            <span class="tag-cat tag-${item.cat}">${item.cat}</span>
          </div>
          <div class="food-macros">
            <div><b>${item.kcal}</b> kcal</div>
            <div>G: ${item.fat}g | P: ${item.protein}g | C: ${item.carbs}g</div>
          </div>
        </div>
      `).join('');

    card.innerHTML = `
      <div>
        <div class="meal-header">
          <span class="meal-type">${m.label}</span>
          <button class="btn-edit" onclick="openModal('${day}', '${m.id}')">+ Editar / Añadir</button>
        </div>
        <div class="food-list">${itemsHTML}</div>
      </div>
      <div class="meal-stats">
        <div><span class="mval">${mTotals.kcal}</span><span class="mlbl">kcal</span></div>
        <div><span class="mval">${mTotals.fat.toFixed(1)}g</span><span class="mlbl">Grasas</span></div>
        <div><span class="mval">${mTotals.protein.toFixed(1)}g</span><span class="mlbl">Prot</span></div>
        <div><span class="mval">${mTotals.carbs.toFixed(1)}g</span><span class="mlbl">Carb</span></div>
      </div>
    `;
    grid.appendChild(card);
  });
  container.appendChild(grid);

  const sumDiv = document.createElement('div');
  sumDiv.className = 'summary-card';
  sumDiv.innerHTML = `
    <div class="sum-item"><div class="num">${totals.kcal}</div><div class="label">Kcal Totales</div></div>
    <div class="sum-item"><div class="num">${totals.carbs.toFixed(1)}g</div><div class="label">Carbohidratos</div></div>
    <div class="sum-item"><div class="num">${totals.protein.toFixed(1)}g</div><div class="label">Proteína Total</div></div>
    <div class="sum-item"><div class="num">${totals.fat.toFixed(1)}g</div><div class="label">Grasa Total</div></div>
  `;
  container.appendChild(sumDiv);
}

// Vista de la semana completa: resumen de cada día
function renderWeekView(container) {
  const wTotals = getWeekTotals(activeCategory);
  const avgKcal = Math.round(wTotals.kcal / 7);
  container.appendChild(buildAlertBox(getWeeklyWarning(wTotals), ` Promedio diario aproximado: ${avgKcal} kcal.`));

  const targets = getWeeklyNutritionTargets();
  const targetAvgKcal = Math.round((targets.minKcal + targets.maxKcal) / 2);
  const weeklyTargetKcal = targetAvgKcal * 7;
  
  let progressPct = weeklyTargetKcal > 0 ? Math.round((wTotals.kcal / weeklyTargetKcal) * 100) : 0;
  let displayPct = Math.min(progressPct, 100);

  const summaryDiv = document.createElement('div');
  summaryDiv.className = 'week-summary-container';

  let maxDayKcal = 1;
  DAYS.forEach(d => {
    const dt = getDayTotals(d, activeCategory);
    if (dt.kcal > maxDayKcal) maxDayKcal = dt.kcal;
  });
  if (maxDayKcal < targets.maxKcal) maxDayKcal = targets.maxKcal;

  let barsHTML = '';
  DAYS.forEach(d => {
    const t = getDayTotals(d, activeCategory);
    const heightPct = Math.min(100, Math.round((t.kcal / maxDayKcal) * 100));
    const dayShort = DAY_NAMES[d].substring(0, 3);
    barsHTML += `
      <div class="bar-col">
        <span class="bar-val">${t.kcal}</span>
        <div class="bar-fill" style="height: ${heightPct}%;" title="${DAY_NAMES[d]}: ${t.kcal} kcal"></div>
        <span class="bar-label">${dayShort}</span>
      </div>
    `;
  });

  summaryDiv.innerHTML = `
    <div class="goal-progress-card">
      <h3 style="font-family:'Fraunces',serif; font-size:1.1rem; color:var(--text-main);">Cumplimiento Semanal</h3>
      <div class="progress-circle-outer" style="--pct: ${displayPct}">
        <div class="progress-circle-inner">
          <span class="progress-pct-text">${progressPct}%</span>
          <span style="font-size:0.65rem; color:var(--text-dim);">de la meta</span>
        </div>
      </div>
      <p style="font-size:0.8rem; color:var(--text-dim); text-align:center;">
        <b>${wTotals.kcal.toLocaleString()}</b> / ${weeklyTargetKcal.toLocaleString()} kcal
      </p>
    </div>
    <div class="chart-card">
      <div style="display:flex; justify-content:space-between; align-items:center;">
        <h3 style="font-family:'Fraunces',serif; font-size:1.1rem; color:var(--text-main);">Consumo Calórico por Día</h3>
        <span style="font-size:0.75rem; color:var(--accent);">Meta diaria: ~${targetAvgKcal} kcal</span>
      </div>
      <div class="chart-bars">
        ${barsHTML}
      </div>
    </div>
  `;

  container.appendChild(summaryDiv);

  const grid = document.createElement('div');
  grid.className = 'week-grid';

  DAYS.forEach(d => {
    const t = getDayTotals(d, activeCategory);
    const card = document.createElement('div');
    card.className = 'week-day-card';
    card.onclick = () => selectDay(d);

    card.innerHTML = `
      <div class="week-day-title">
        <span>${DAY_NAMES[d]}</span>
        <span style="font-size:.8rem; color:var(--text-dim);">${t.kcal} kcal</span>
      </div>
      <div style="font-size:.78rem; color:var(--text-dim); line-height:1.5;">
        <p>Grasas: ${t.fat.toFixed(1)}g</p>
        <p>Proteínas: ${t.protein.toFixed(1)}g</p>
        <p>Carbohidratos: ${t.carbs.toFixed(1)}g</p>
      </div>
    `;
    grid.appendChild(card);
  });
  container.appendChild(grid);
}

// Actualiza la barra inferior (promedio de calorías, grasas y estado semanal)
function renderStats() {
  const wTotals = getWeekTotals(activeCategory);
  const avg = Math.round(wTotals.kcal / 7);
  document.getElementById('statAvgKcal').textContent = `${avg} kcal`;
  document.getElementById('statTotalFat').textContent = `${wTotals.fat.toFixed(1)} g`;
  const statusElem = document.getElementById('statStatus');

  if (!wTotals.count) {
    statusElem.textContent = 'Sin datos';
    statusElem.style.color = 'var(--text-dim)';
    return;
  }

  const days = DAYS.length;
  const issues = evaluateNutrition(wTotals.kcal / days, wTotals.fat / days, wTotals.carbs / days);

  if (issues.length === 0) {
    statusElem.textContent = '✅ Equilibrado';
    statusElem.style.color = 'var(--ok)';
  } else if (issues[0].level >= 3) {
    statusElem.textContent = `${issues[0].icon} Fuera de rango`;
    statusElem.style.color = 'var(--danger)';
  } else {
    statusElem.textContent = `${issues[0].icon} Cerca del límite`;
    statusElem.style.color = 'var(--warn)';
  }
}

/* =========================================================
   FECHA DEL SISTEMA
   ========================================================= */
// Utilidades de fechas
const JS_DAY_KEYS = ['domingo', 'lunes', 'martes', 'miercoles', 'jueves', 'viernes', 'sabado'];

// Devuelve el día de hoy (lunes, martes...)
function todayKey() { return JS_DAY_KEYS[new Date().getDay()]; }

// Fecha en formato AAAA-MM-DD
function isoDate(d = new Date()) {
  const m = String(d.getMonth() + 1).padStart(2, '0');
  const day = String(d.getDate()).padStart(2, '0');
  return `${d.getFullYear()}-${m}-${day}`;
}

// Lista de las últimas n fechas
function lastDaysISO(n) {
  const out = [];
  for (let i = n - 1; i >= 0; i--) {
    const d = new Date();
    d.setDate(d.getDate() - i);
    out.push(isoDate(d));
  }
  return out;
}

/* =========================================================
   HIDRATACIÓN
   ========================================================= */
// Un vaso de agua = 250 ml
const GLASS_ML = 250;
const hydration = { byDate: {}, warned: false };
let waterTimer = null;
let waterPendingDate = null;

// Meta diaria de vasos según el peso (entre 6 y 16)
function hydrationGoal() {
  const w = userProfile.weight > 0 ? userProfile.weight : 70;
  return Math.min(16, Math.max(6, Math.round((w * 35) / GLASS_ML)));
}

// Clave de localStorage donde se guarda el agua de cada usuario
function waterKey() {
  return 'nutriplan_water_' + ((currentUser && (currentUser.email || currentUser.id)) || 'demo');
}

// Lee el agua guardada en este equipo
function readWaterCache() {
  try { return JSON.parse(localStorage.getItem(waterKey()) || '{}') || {}; } catch (e) { return {}; }
}

// Guarda el agua en este equipo
function writeWaterCache() {
  try { localStorage.setItem(waterKey(), JSON.stringify(hydration.byDate)); } catch (e) { /* sin almacenamiento */ }
}

// Avisa una sola vez si la hidratación no se pudo guardar en el servidor
function warnHydrationOnce(msg) {
  if (hydration.warned) return;
  hydration.warned = true;
  notify('La hidratación se guarda solo en este equipo por ahora. ' + (msg || ''));
}

// Carga el agua de los últimos 7 días (copia local + servidor)
async function loadHydration() {
  hydration.byDate = readWaterCache();
  const res = await callApi('obtener_hidratacion', lastDaysISO(7)[0]);
  if (res && res.status === 'success') {
    (res.registros || []).forEach((r) => { hydration.byDate[r.fecha] = Number(r.vasos) || 0; });
    writeWaterCache();
  } else if (res && res.status === 'error') {
    warnHydrationOnce(res.message);
  }
}

// Vasos tomados en una fecha
function getWater(date = isoDate()) { return hydration.byDate[date] || 0; }

// Envía al servidor los vasos de un día
async function saveWater(fecha) {
  waterTimer = null;
  const res = await callApi('guardar_hidratacion', fecha, getWater(fecha));
  if (res && res.status === 'error') warnHydrationOnce(res.message);
}

// Guarda de inmediato si hay un cambio de agua pendiente
async function flushWaterSave() {
  if (!waterTimer) return;
  clearTimeout(waterTimer);
  await saveWater(waterPendingDate);
}

// Cambia los vasos de hoy (0 a 40) y programa el guardado
function setWater(n) {
  const fecha = isoDate();
  hydration.byDate[fecha] = Math.max(0, Math.min(40, n));
  writeWaterCache();
  paintWater();
  waterPendingDate = fecha;
  clearTimeout(waterTimer);
  waterTimer = setTimeout(() => saveWater(fecha), 500);
}

// Actualiza en pantalla la barra y los números del agua
function paintWater() {
  const fill = $('waterFill');
  if (!fill) return;
  const goal = hydrationGoal();
  const n = getWater();
  const ml = n * GLASS_ML;
  const left = goal - n;

  $('waterNow').textContent = n;
  $('waterGoal').textContent = goal;
  fill.style.width = Math.min(100, Math.round((n / goal) * 100)) + '%';
  $('waterBar').setAttribute('aria-valuenow', String(n));
  $('waterBar').setAttribute('aria-valuemax', String(goal));
  $('waterMeta').textContent = left <= 0
    ? `¡Meta cumplida! ${ml} ml hoy${left < 0 ? ` (+${-left} extra)` : ''}`
    : `${ml} ml · te ${left === 1 ? 'falta 1 vaso' : `faltan ${left} vasos`}`;
  $('btnWaterMinus').disabled = n <= 0;

  $('waterWeek').innerHTML = lastDaysISO(7).map((iso) => {
    const v = getWater(iso);
    const h = Math.min(100, Math.round((v / goal) * 100));
    const label = JS_DAY_KEYS[new Date(iso + 'T00:00:00').getDay()].charAt(0).toUpperCase();
    const cls = 'wd' + (v >= goal ? ' hit' : '') + (iso === isoDate() ? ' today' : '');
    return `<div class="${cls}" title="${iso}: ${v} vasos"><div class="wd-bar"><i style="height:${h}%"></i></div><span>${label}</span></div>`;
  }).join('');
}

/* =========================================================
   DASHBOARDS
   ========================================================= */
// Panel activo (Hoy o Plan semanal) y fecha actual
let currentDash = 'today';
let todayStamp = isoDate();

// Cambia entre el panel «Hoy» y «Plan semanal»
function setDash(name) {
  currentDash = name === 'plan' ? 'plan' : 'today';
  $('app-screen').dataset.dash = currentDash;
  [['tabToday', 'today'], ['tabPlan', 'plan']].forEach(([id, key]) => {
    $(id).classList.toggle('active', currentDash === key);
    $(id).setAttribute('aria-selected', String(currentDash === key));
  });
  if (currentDash === 'today') {
    switchTheme(DAY_THEMES[todayKey()] || 'anxiety');
    renderToday();
  } else {
    selectDay(activeTab);
  }
}

// Botones de las pestañas Hoy / Plan semanal
$('tabToday').onclick = () => setDash('today');
$('tabPlan').onclick = () => setDash('plan');

// Clasifica el IMC (bajo peso, normal, sobrepeso...)
function bmiLabel(imc) {
  if (imc < 18.5) return 'Bajo';
  if (imc < 25) return 'Normal';
  if (imc < 30) return 'Sobrepeso';
  return 'Alto';
}

// Dibuja el panel «Hoy»: meta calórica, macros, agua, perfil y comidas
function renderToday() {
  const box = $('todayContainer');
  if (!box) return;
  todayStamp = isoDate();

  const key = todayKey();
  const now = new Date();
  const dateStr = now.toLocaleDateString('es-CO', { weekday: 'long', day: 'numeric', month: 'long', year: 'numeric' });
  const hour = now.getHours();
  const saludo = hour < 12 ? 'Buenos días' : (hour < 19 ? 'Buenas tardes' : 'Buenas noches');
  const firstName = ((currentUser && currentUser.nombre) || '').trim().split(/\s+/)[0];

  const totals = getDayTotals(key, 'todas');
  const t = getNutritionTargets();
  const mid = Math.round((t.minKcal + t.maxKcal) / 2);
  const pct = mid > 0 ? Math.round((totals.kcal / mid) * 100) : 0;

  let chip;
  if (totals.count === 0) chip = { cls: 'idle', txt: 'Sin plan para hoy' };
  else if (totals.kcal > t.maxKcal) chip = { cls: 'danger', txt: 'Por encima del rango' };
  else if (totals.kcal < t.minKcal) chip = { cls: 'warn', txt: 'Por debajo del rango' };
  else chip = { cls: 'ok', txt: 'Dentro de tu rango' };

  const warn = totals.count === 0
    ? { type: 'warn', icon: '🍽️', title: 'Hoy no tienes comidas planeadas', msg: 'Agrega alimentos a tu desayuno, almuerzo y cena para ver tu progreso de hoy.' }
    : getWarning(totals, 'hoy');

  const kcalOf = (g, per) => (totals.kcal > 0 ? (g * per / totals.kcal) * 100 : 0);
  const macros = [
    { name: 'Carbohidratos', g: totals.carbs, pct: kcalOf(totals.carbs, 4), band: t.carbPctRange },
    { name: 'Proteína', g: totals.protein, pct: kcalOf(totals.protein, 4), band: null },
    { name: 'Grasas', g: totals.fat, pct: kcalOf(totals.fat, 9), band: t.fatPctRange }
  ];
  const macrosHTML = macros.map((m) => {
    const over = m.band && m.pct > m.band[1];
    const band = m.band ? `<div class="macro-band" style="left:${m.band[0]}%; width:${m.band[1] - m.band[0]}%"></div>` : '';
    return `
      <div class="macro-row">
        <span class="macro-name">${m.name}</span>
        <div class="macro-track">${band}<div class="macro-fill${over ? ' over' : ''}" style="width:${Math.min(100, m.pct).toFixed(0)}%"></div></div>
        <span class="macro-val">${m.g.toFixed(1)} g<small>${m.pct.toFixed(0)}% de tus kcal</small></span>
      </div>`;
  }).join('');

  const heightM = (userProfile.height || 170) / 100;
  const imc = heightM > 0 ? userProfile.weight / (heightM * heightM) : 0;
  const goalName = GOAL_NAMES[userProfile.goal] || 'mantener peso';

  const mealsHTML = MEALS.map((m) => {
    const items = (planData[key] && planData[key][m.id]) || [];
    const mt = getMealTotals(items, 'todas');
    const names = items.slice(0, 3).map((i) => i.name).join(', ') + (items.length > 3 ? ` y ${items.length - 3} más` : '');
    return `
      <button type="button" class="meal-row${items.length ? '' : ' empty'}" data-meal="${m.id}">
        <span><b>${m.label}</b><small>${items.length ? escapeHtml(names) : 'Sin alimentos · toca para añadir'}</small></span>
        <span class="kc">${mt.kcal}<small> kcal</small></span>
      </button>`;
  }).join('');

  const wTotals = getWeekTotals('todas');
  const weekPct = mid > 0 ? Math.round((wTotals.kcal / (mid * 7)) * 100) : 0;
  const daysWithPlan = DAYS.filter((d) => getDayTotals(d, 'todas').count > 0).length;

  box.innerHTML = `
    <div class="today-head">
      <h2 class="today-date">${escapeHtml(dateStr.charAt(0).toUpperCase() + dateStr.slice(1))}</h2>
      <p class="today-sub">${saludo}${firstName ? ', ' + escapeHtml(firstName) : ''}. Así va tu día frente a tu meta de ${escapeHtml(goalName)}.</p>
    </div>
    <div id="todayAlert"></div>

    <div class="today-grid">
      <div class="t-card span-5">
        <div class="t-title">Meta calórica de hoy</div>
        <div class="cal-card">
          <div class="progress-circle-outer" style="--pct: ${Math.min(pct, 100)}">
            <div class="progress-circle-inner">
              <span class="progress-pct-text">${pct}%</span>
              <span style="font-size:0.65rem; color:var(--text-dim);">de la meta</span>
            </div>
          </div>
          <div class="cal-info">
            <div class="cal-big">${totals.kcal.toLocaleString()} <small>kcal planeadas</small></div>
            <div class="cal-range">Rango para hoy: ${t.minKcal}–${t.maxKcal} kcal</div>
            <span class="status-chip ${chip.cls}">${chip.txt}</span>
          </div>
        </div>
      </div>

      <div class="t-card span-7">
        <div class="t-title">Macronutrientes de hoy</div>
        ${macrosHTML}
        <p class="macro-note">La franja clara marca el rango ideal para tu objetivo.</p>
      </div>

      <div class="t-card span-7 water-card">
        <div class="water-title">
          <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2.5c-.4 0-.8.2-1 .5C9 5.8 5 10.6 5 14.5a7 7 0 0 0 14 0c0-3.9-4-8.7-6-11.5-.2-.3-.6-.5-1-.5z"/></svg>
          Hidratación del Día
        </div>
        <div class="water-count"><span id="waterNow">0</span> / <span id="waterGoal">${hydrationGoal()}</span><small>vasos</small></div>
        <div class="water-meta" id="waterMeta"></div>
        <div class="water-track" id="waterBar" role="progressbar" aria-label="Vasos de agua de hoy" aria-valuemin="0" aria-valuenow="0" aria-valuemax="${hydrationGoal()}"><div class="water-fill" id="waterFill"></div></div>
        <div class="water-actions">
          <button type="button" class="water-btn minus" id="btnWaterMinus" aria-label="Quitar un vaso">−</button>
          <button type="button" class="water-btn" id="btnWaterPlus">+ Registrar Vaso (+${GLASS_ML}ml)</button>
        </div>
        <div class="water-week" id="waterWeek" aria-label="Vasos de los últimos 7 días"></div>
      </div>

      <div class="t-card span-5">
        <div class="t-title">Tu meta</div>
        <div class="kv"><span>Objetivo</span><b>${escapeHtml(goalName.charAt(0).toUpperCase() + goalName.slice(1))}</b></div>
        <div class="kv"><span>Peso</span><b>${userProfile.weight} kg</b></div>
        <div class="kv"><span>Altura</span><b>${userProfile.height || 170} cm</b></div>
        <div class="kv"><span>IMC</span><b>${imc.toFixed(1)} · ${bmiLabel(imc)}</b></div>
        <div class="kv"><span>Agua diaria sugerida</span><b>${hydrationGoal()} vasos · ${(hydrationGoal() * GLASS_ML / 1000).toFixed(2)} L</b></div>
        <div class="goal-actions"><button type="button" class="t-link" id="btnTodayEditGoal">Editar mi meta</button></div>
      </div>

      <div class="t-card span-7">
        <div class="t-title">Comidas de hoy <button type="button" class="t-link" id="btnTodayGoPlan">Ver plan semanal</button></div>
        ${mealsHTML}
      </div>

      <div class="t-card span-5 week-mini">
        <div class="t-title">Tu semana</div>
        <div class="week-mini-pct">${weekPct}% <small>de la meta semanal</small></div>
        <div class="bar-track"><div class="bar-fill-h" style="width:${Math.min(100, weekPct)}%"></div></div>
        <div class="cal-range">${daysWithPlan} de 7 días con comidas planeadas · ${wTotals.kcal.toLocaleString()} kcal en total</div>
      </div>
    </div>
  `;

  $('todayAlert').appendChild(buildAlertBox(warn, '', false));

  box.querySelectorAll('.meal-row').forEach((b) => { b.onclick = () => openModal(key, b.dataset.meal); });
  $('btnWaterPlus').onclick = () => setWater(getWater() + 1);
  $('btnWaterMinus').onclick = () => setWater(getWater() - 1);
  $('btnTodayEditGoal').onclick = () => $('menuControlMeta').click();
  $('btnTodayGoPlan').onclick = () => setDash('plan');
  requestAnimationFrame(paintWater);
}

// Si la app queda abierta pasada la medianoche, pasa al nuevo día
setInterval(() => {
  if (!currentUser || isoDate() === todayStamp) return;
  todayStamp = isoDate();
  if (currentDash === 'today') setDash('today'); else renderNavs();
}, 60000);

// Vuelve a dibujar la pantalla según el panel activo
function render() {
  if (currentDash === 'today') {
    renderToday();
    return;
  }
  renderNavs();
  renderMain();
  renderStats();
}

// Menú desplegable del usuario
const userMenuWrapper = $('userMenuWrapper');
const userDropdown = $('userDropdown');

// Cierra el menú del usuario
function closeUserMenu() {
  userMenuWrapper.classList.remove('open');
  $('userProfileBtn').setAttribute('aria-expanded', 'false');
}

// Abre o cierra el menú al tocar el botón del usuario
$('userProfileBtn').addEventListener('click', (e) => {
  e.stopPropagation();
  const isOpen = userMenuWrapper.classList.toggle('open');
  $('userProfileBtn').setAttribute('aria-expanded', String(isOpen));
});

userDropdown.addEventListener('click', (e) => e.stopPropagation());
// Cierra el menú al tocar fuera de él
document.addEventListener('click', (e) => {
  if (userMenuWrapper && !userMenuWrapper.contains(e.target)) closeUserMenu();
});

// Muestra nombre y foto del usuario en el encabezado (sin foto, usa la inicial)
function applyUserToHeader(user) {
  const nombreUsuario = (user && user.nombre) || 'Usuario';
  const elNombre = $('userProfileBtn')?.querySelector('.user-name');
  if (elNombre) elNombre.textContent = nombreUsuario;

  const elAvatar = $('main-avatar-circle');
  if (elAvatar) {
    if (user && user.avatar) {
      elAvatar.innerHTML = `<img src="${user.avatar}" alt="${escapeHtml(nombreUsuario)}">`;
    } else {
      elAvatar.textContent = nombreUsuario.charAt(0).toUpperCase();
    }
  }
}

// Opciones del menú: cambiar de usuario, cerrar sesión y salir del programa
$('menuCambiarUsuario').onclick = async () => {
  closeUserMenu();
  await leaveSession();
  showScreen('profiles-screen');
};

$('menuCerrarSesion').onclick = async () => {
  closeUserMenu();
  await leaveSession();
  showScreen(savedUsers.length > 0 ? 'profiles-screen' : 'auth-screen');
};

$('menuSalirPrograma').onclick = () => {
  closeUserMenu();
  cerrarPrograma();
};

// Ventana «Control de Meta» (peso, altura y objetivo)
const metaModalOverlay = $('metaModalOverlay');

// Calcula el rango de calorías para un peso y un objetivo
function computeTargetsFor(weight, goal) {
  const w = weight > 0 ? weight : 70;
  if (goal === 'bajar') return { min: Math.round(w * 20), max: Math.round(w * 25) };
  if (goal === 'subir') return { min: Math.round(w * 33), max: Math.round(w * 40) };
  return { min: Math.round(w * 26), max: Math.round(w * 32) };
}

// Actualiza la caja de detalles de la meta mientras se escribe
function updateMetaDetailBox() {
  const weight = parseFloat($('metaWeight').value) || 70;
  const height = parseFloat($('metaHeight').value) || 170;
  const goal = $('metaGoal').value;
  const t = computeTargetsFor(weight, goal);
  const heightM = height / 100;
  const imc = heightM > 0 ? weight / (heightM * heightM) : 0;
  const goalText = GOAL_NAMES[goal] || 'mantener peso';

  let detalle;
  if (goal === 'bajar') {
    detalle = 'Se calcula un déficit calórico moderado y sostenible, priorizando proteína para conservar tu masa muscular mientras bajas de peso.';
  } else if (goal === 'subir') {
    detalle = 'Se calcula un superávit calórico controlado, con más carbohidratos y proteína, para ganar peso de forma gradual y saludable.';
  } else {
    detalle = 'Se calcula un rango de calorías balanceado, suficiente para mantener tu peso actual sin déficit ni superávit.';
  }

  $('metaDetailBox').innerHTML =
    `Con <b>${weight} kg</b>, <b>${height} cm</b> (IMC ≈ ${imc.toFixed(1)}) y el objetivo de <b>${escapeHtml(goalText)}</b>, ` +
    `tu rango sugerido es de <b>${t.min}–${t.max} kcal</b> al día.<br>${detalle}`;
}

$('metaWeight').addEventListener('input', updateMetaDetailBox);
$('metaHeight').addEventListener('input', updateMetaDetailBox);
$('metaGoal').addEventListener('change', updateMetaDetailBox);

// Muestra el historial de pesos guardados
async function renderMetaHistoryBox() {
  const box = $('metaHistoryBox');
  if (!box) return;
  box.textContent = 'Cargando historial...';
  const res = await callApi('obtener_historial_peso');
  if (res && res.status === 'success' && res.historial && res.historial.length) {
    const lista = res.historial.map((h) => {
      const fecha = h.registrado_en ? new Date(h.registrado_en).toLocaleDateString() : '';
      return `${h.peso} kg${fecha ? ' (' + fecha + ')' : ''}`;
    }).join(' · ');
    box.innerHTML = `<b>Tu historial de peso:</b> ${lista}`;
  } else {
    box.textContent = 'Aún no tienes registros de peso guardados. Se guarda uno cada vez que guardas tu meta.';
  }
}

// Abre la ventana de Control de Meta
$('menuControlMeta').onclick = () => {
  closeUserMenu();
  $('metaWeight').value = userProfile.weight;
  $('metaHeight').value = userProfile.height || 170;
  $('metaGoal').value = userProfile.goal || 'mantener';
  updateMetaDetailBox();
  renderMetaHistoryBox();
  metaModalOverlay.classList.add('show');
};

$('btnCloseMeta').onclick = () => metaModalOverlay.classList.remove('show');

// Guarda peso, altura y objetivo
$('btnSaveMeta').onclick = async () => {
  const weight = parseFloat($('metaWeight').value) || 70;
  const height = parseFloat($('metaHeight').value) || 170;
  const goal = $('metaGoal').value;
  userProfile.weight = weight;
  userProfile.height = height;
  userProfile.goal = goal;
  metaModalOverlay.classList.remove('show');
  render();

  const res = await callApi('guardar_perfil', weight, height, goal);
  if (res && res.status === 'error') notify('No se pudo guardar tu meta: ' + res.message);
  else if (res) notify('Meta guardada', 'ok');
  renderMetaHistoryBox();
};

// Ventana de Configuración (nombre, correo, género y foto)
const configModalOverlay = $('configModalOverlay');
let pendingAvatarDataUrl = null;

// Dibuja la vista previa de la foto (o la inicial si no hay foto)
function renderAvatarPreview(container, avatarUrl, nombre) {
  if (avatarUrl) {
    container.innerHTML = `<img src="${avatarUrl}" alt="${escapeHtml(nombre || 'Usuario')}">`;
  } else {
    container.innerHTML = `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2a5 5 0 0 1 5 5v2a5 5 0 0 1-10 0V7a5 5 0 0 1 5-2z"/><path d="M19 21v-2a4 4 0 0 0-4-4H9a4 4 0 0 0-4 4v2"/></svg>`;
  }
}

// Abre la ventana de Configuración
$('menuConfiguracion').onclick = () => {
  closeUserMenu();
  if (!currentUser) return;
  pendingAvatarDataUrl = null;
  $('configNombre').value = currentUser.nombre || '';
  $('configEmail').value = currentUser.email || '';
  $('configGenero').value = currentUser.genero || 'prefiero_no_decir';
  renderAvatarPreview($('configAvatarPreview'), currentUser.avatar, currentUser.nombre);
  configModalOverlay.classList.add('show');
};

$('btnCloseConfig').onclick = () => configModalOverlay.classList.remove('show');
// Elegir una foto nueva
$('btnChangeAvatar').onclick = () => $('configAvatarInput').click();

// Al elegir una imagen se reduce de tamaño antes de guardarla
$('configAvatarInput').addEventListener('change', (e) => {
  const file = e.target.files && e.target.files[0];
  if (!file) return;
  if (file.size > 2 * 1024 * 1024) {
    notify('La imagen no puede pesar más de 2MB');
    e.target.value = '';
    return;
  }
  const reader = new FileReader();
  reader.onload = () => {
    const img = new Image();
    img.onload = () => {
      const size = 200;
      const canvas = document.createElement('canvas');
      canvas.width = size; canvas.height = size;
      const ctx = canvas.getContext('2d');
      const minSide = Math.min(img.width, img.height);
      const sx = (img.width - minSide) / 2;
      const sy = (img.height - minSide) / 2;
      ctx.drawImage(img, sx, sy, minSide, minSide, 0, 0, size, size);
      pendingAvatarDataUrl = canvas.toDataURL('image/jpeg', 0.82);
      renderAvatarPreview($('configAvatarPreview'), pendingAvatarDataUrl, currentUser && currentUser.nombre);
    };
    img.src = reader.result;
  };
  reader.onerror = () => notify('No se pudo leer la imagen');
  reader.readAsDataURL(file);
  e.target.value = '';
});

// Guarda los cambios de Configuración
$('btnSaveConfig').onclick = async () => {
  if (!currentUser) return;
  const nombre = $('configNombre').value.trim();
  const email = $('configEmail').value.trim();
  const genero = $('configGenero').value;
  if (!nombre) { notify('Escribe tu nombre'); return; }

  const btn = $('btnSaveConfig');
  setBusy(btn, true);
  try {
    const res = await callApi('actualizar_datos_usuario', nombre, email, genero, pendingAvatarDataUrl);
    if (res === null) {
      currentUser = { ...currentUser, nombre, email, genero, avatar: pendingAvatarDataUrl || currentUser.avatar };
      saveUserToLocal(currentUser);
      applyUserToHeader(currentUser);
      configModalOverlay.classList.remove('show');
      notify('Datos actualizados', 'ok');
      return;
    }
    if (res.status !== 'success') {
      notify(res.message || 'No se pudieron guardar los cambios');
      return;
    }
    currentUser = res.user;
    saveUserToLocal(res.user);
    applyUserToHeader(res.user);
    configModalOverlay.classList.remove('show');
    notify('Datos actualizados', 'ok');
  } finally {
    setBusy(btn, false);
  }
};

// Ventana para agregar o editar los alimentos de una comida
const overlay = document.getElementById('formOverlay');
const catSelect = document.getElementById('f_cat_select');
const itemSelect = document.getElementById('f_item_select');
const unitSelect = document.getElementById('f_unit_select');
const qtyInput = document.getElementById('f_qty');

// Llena la lista de categorías del formulario
function initFormDropdowns() {
  catSelect.innerHTML = '';
  CATEGORIES.filter(c => c.id !== 'todas').forEach(c => {
    const opt = document.createElement('option'); opt.value = c.id; opt.textContent = c.label;
    catSelect.appendChild(opt);
  });
  catSelect.onchange = handleCategoryChange;
  itemSelect.onchange = handleFoodChange;
  unitSelect.onchange = updateLivePreview;
  qtyInput.oninput = updateLivePreview;
  handleCategoryChange();
}

// Al cambiar la categoría, carga sus alimentos
function handleCategoryChange() {
  const selectedCat = catSelect.value;
  const foodList = FOOD_DATABASE[selectedCat] || [];
  itemSelect.innerHTML = '';
  foodList.forEach(food => {
    const opt = document.createElement('option'); opt.value = food.id; opt.textContent = food.name;
    itemSelect.appendChild(opt);
  });
  handleFoodChange();
}

// Se ejecuta al elegir un alimento
function handleFoodChange() {
  const selectedCat = catSelect.value;
  const foodId = itemSelect.value;
  const food = (FOOD_DATABASE[selectedCat] || []).find(f => f.id === foodId);

  unitSelect.innerHTML = '';
  if (!food) return;

  if (food.baseUnit === 'g') {
    unitSelect.innerHTML = `<option value="g">Gramos (g)</option><option value="kg">Kilogramos (kg)</option>`;
    qtyInput.value = '100';
  } else if (food.baseUnit === 'ml') {
    unitSelect.innerHTML = `<option value="ml">Mililitros (ml)</option><option value="l">Litros (L)</option>`;
    qtyInput.value = '200';
  } else {
    unitSelect.innerHTML = `<option value="unidad">Unidades / Piezas</option>`;
    qtyInput.value = '1';
  }
  updateLivePreview();
}

// Muestra calorías y macros en vivo mientras se escribe la cantidad
function updateLivePreview() {
  const selectedCat = catSelect.value;
  const foodId = itemSelect.value;
  const food = (FOOD_DATABASE[selectedCat] || []).find(f => f.id === foodId);
  const qty = parseFloat(qtyInput.value) || 0;
  const unit = unitSelect.value;
  const macros = calculateMacros(food, qty, unit);

  document.getElementById('previewKcal').textContent = macros.kcal;
  document.getElementById('previewCarbs').textContent = `${macros.carbs}g`;
  document.getElementById('previewProtein').textContent = `${macros.protein}g`;
  document.getElementById('previewFat').textContent = `${macros.fat}g`;
}

// Abre la ventana de edición de una comida
function openModal(day, meal) {
  editingTarget = { day, meal };
  const mealObj = MEALS.find((m) => m.id === meal);
  $('modalTitle').textContent = `${DAY_NAMES[day]} · ${mealObj.label}`;
  initFormDropdowns();
  resetForm();
  renderModalItems();
  overlay.classList.add('show');
}

// Cierra la ventana, vuelve a dibujar y guarda
function closeModal() {
  overlay.classList.remove('show');
  editingTarget = null;
  resetForm();
  render();
  schedulePlanSave();
}

// Lista los alimentos ya agregados a la comida
function renderModalItems() {
  if (!editingTarget) return;
  const { day, meal } = editingTarget;
  const items = planData[day][meal] || [];
  const listContainer = $('modalItemList');

  if (items.length === 0) {
    listContainer.innerHTML = `<div class="meal-empty">Sin datos</div>`;
    return;
  }

  listContainer.innerHTML = items.map((item, index) => `
    <div class="modal-item-row">
      <div>
        <div style="font-weight:600; font-size:.85rem;">${escapeHtml(item.name)} (${escapeHtml(item.portionStr)})</div>
        <div style="font-size:.7rem; color:var(--text-dim);">${item.kcal} kcal (G: ${item.fat}g, P: ${item.protein}g, C: ${item.carbs}g)</div>
      </div>
      <div style="display:flex; gap:0.2rem;">
        <button type="button" class="btn-del" onclick="deleteFoodItem(${index})">✕</button>
      </div>
    </div>
  `).join('');
}

// Limpia el formulario de alimentos
function resetForm() {
  editingItemIndex = null;
  const titleEl = $('formSectionTitle');
  if (titleEl) titleEl.textContent = '+ Agregar Nuevo Alimento';
  
  const submitBtn = $('submitFoodBtn');
  if (submitBtn) submitBtn.textContent = '+ Añadir a la comida';

  const cancelBtn = $('cancelEditBtn');
  if (cancelBtn) cancelBtn.style.display = 'none';

  if (catSelect && catSelect.options.length > 0) {
    catSelect.selectedIndex = 0;
    handleCategoryChange();
  }
}

// Elimina un alimento de la comida
function deleteFoodItem(index) {
  if (!editingTarget) return;
  const { day, meal } = editingTarget;
  planData[day][meal].splice(index, 1);
  renderModalItems();
  schedulePlanSave();
}

// Agrega o actualiza un alimento al enviar el formulario
$('addFoodForm').onsubmit = (e) => {
  e.preventDefault();
  if (!editingTarget) return;

  const selectedCat = catSelect.value;
  const food = (FOOD_DATABASE[selectedCat] || []).find((f) => f.id === itemSelect.value);
  const qty = parseFloat(qtyInput.value) || 0;
  const unit = unitSelect.value;
  if (!food || qty <= 0) return;

  const { day, meal } = editingTarget;
  planData[day][meal].push(buildItem(selectedCat, food, qty, unit));

  resetForm();
  renderModalItems();
  schedulePlanSave();
};

// Botón «Listo» de la ventana de alimentos
$('btnDone').onclick = closeModal;

// Exportar el plan a un archivo JSON
$('btnExport').onclick = () => {
  const data = {
    app: 'NutriPlan',
    version: 1,
    exportado: new Date().toISOString(),
    perfil: { peso: userProfile.weight, altura: userProfile.height, objetivo: userProfile.goal },
    plan: planToRows()
  };
  const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = `nutriplan-${new Date().toISOString().slice(0, 10)}.json`;
  document.body.appendChild(a);
  a.click();
  a.remove();
  setTimeout(() => URL.revokeObjectURL(url), 2000);
};

// Importar un plan desde un archivo JSON
$('btnImportTrigger').onclick = () =>$('fileImport').click();

$('fileImport').addEventListener('change', (e) => {
  const file = e.target.files && e.target.files[0];
  if (!file) return;
  const reader = new FileReader();
  reader.onload = () => {
    try {
      const data = JSON.parse(reader.result);
      if (!data || !Array.isArray(data.plan)) throw new Error('formato');
      planData = planFromRows(data.plan);
      if (data.perfil && Number(data.perfil.peso) > 0) {
        userProfile.weight = Number(data.perfil.peso);
        if (Number(data.perfil.altura) > 0) userProfile.height = Number(data.perfil.altura);
        if (['bajar', 'mantener', 'subir'].includes(data.perfil.objetivo)) userProfile.goal = data.perfil.objetivo;
        callApi('guardar_perfil', userProfile.weight, userProfile.height, userProfile.goal);
      }
      render();
      schedulePlanSave();
      notify('Plan importado correctamente', 'ok');
    } catch (err) {
      notify('El archivo no es un JSON de NutriPlan válido');
    }
  };
  reader.onerror = () => notify('No se pudo leer el archivo');
  reader.readAsText(file);
  e.target.value = '';
});

// Muestra una pantalla de carga con un mensaje
function showLoading(msg = 'Cargando usuario...') {
  let overlay = $('loadingOverlay');
  if (!overlay) {
    overlay = document.createElement('div');
    overlay.id = 'loadingOverlay';
    overlay.className = 'loading-overlay';
    overlay.innerHTML = `
      <div class="loading-spinner"></div>
      <div class="loading-text" id="loadingText">${escapeHtml(msg)}</div>
    `;
    document.body.appendChild(overlay);
  } else {
    $('loadingText').textContent = msg;
    overlay.classList.remove('is-hidden');
  }
}

// Oculta la pantalla de carga
function hideLoading() {
  const overlay = $('loadingOverlay');
  if (overlay) overlay.classList.add('is-hidden');
}

// Entra a la app: carga perfil, plan, catálogo y agua, y muestra el panel «Hoy»
async function enterApp(user) {
  showLoading(`Cargando perfil de ${user.nombre || 'usuario'}...`);
  
  try {
    currentUser = user;
    applyUserToHeader(user);

    const [perfil, plan] = await Promise.all([
      callApi('obtener_perfil'),
      callApi('obtener_plan'),
      cargarCatalogosDesdeBD(),
      loadHydration(),
    ]);

    await new Promise((resolve) => setTimeout(resolve, 1000));

    if (perfil === null && plan === null) {
      userProfile = { weight: 70, height: 170, goal: 'mantener' };
      planData = planFromRows(DEMO_ROWS);
    } else {
      userProfile = {
        weight: perfil && perfil.peso ? Number(perfil.peso) : 70,
        height: perfil && perfil.altura ? Number(perfil.altura) : 170,
        goal: perfil && perfil.objetivo ? perfil.objetivo : 'mantener'
      };
      planData = planFromRows(plan && plan.plan ? plan.plan : []);
      if (plan && plan.status === 'error') notify('No se pudo cargar tu plan: ' + plan.message);
    }

    activeCategory = 'todas';
    activeTab = todayKey();
    showScreen('app-screen');
    setDash('today');
  } finally {
    hideLoading();
  }
}

// Animación de fondo con partículas conectadas
function initParticleNetwork() {
  const container = document.getElementById('particle-bg');
  if (!container) return;

  const canvas = document.createElement('canvas');
  container.appendChild(canvas);
  const ctx = canvas.getContext('2d');

  let width = 0;
  let height = 0;
  let particles = [];
  const mouseParticle = { x: null, y: null, active: false };

  function resize() {
    width = canvas.width = window.innerWidth;
    height = canvas.height = window.innerHeight;
    createParticles();
  }

  function getThemeAccentRGB() {
    return getComputedStyle(document.documentElement).getPropertyValue('--accent-rgb').trim() || '232, 96, 38';
  }

  class Particle {
    constructor(x, y) {
      this.x = x ?? Math.random() * width;
      this.y = y ?? Math.random() * height;
      this.radius = Math.random() * 1.2 + 1.0;
      this.opacity = 0;
      this.maxOpacity = Math.random() * 0.4 + 0.2;
      this.velocity = {
        x: (Math.random() - 0.5) * 0.5,
        y: (Math.random() - 0.5) * 0.5
      };
    }

    update() {
      if (this.opacity < this.maxOpacity) {
        this.opacity += 0.008;
      }
      this.x += this.velocity.x;
      this.y += this.velocity.y;

      if (this.x > width + 50 || this.x < -50) this.velocity.x *= -1;
      if (this.y > height + 50 || this.y < -50) this.velocity.y *= -1;
    }

    draw(accentRgb) {
      ctx.beginPath();
      ctx.arc(this.x, this.y, this.radius, 0, Math.PI * 2);
      ctx.fillStyle = `rgba(${accentRgb}, ${this.opacity})`;
      ctx.fill();
    }
  }

  function createParticles() {
    particles = [];
    const density = 15000;
    const count = Math.floor((width * height) / density);
    for (let i = 0; i < count; i++) {
      particles.push(new Particle());
    }
  }

  function animate() {
    ctx.clearRect(0, 0, width, height);

    const accentRgb = getThemeAccentRGB();
    const maxDistance = 150;

    const activeList = [...particles];
    if (mouseParticle.active && mouseParticle.x !== null) {
      activeList.push({ x: mouseParticle.x, y: mouseParticle.y, opacity: 1 });
    }

    for (let i = 0; i < activeList.length; i++) {
      for (let j = i + 1; j < activeList.length; j++) {
        const p1 = activeList[i];
        const p2 = activeList[j];

        const dx = p1.x - p2.x;
        const dy = p1.y - p2.y;
        const distSq = dx * dx + dy * dy;

        if (distSq < maxDistance * maxDistance) {
          const dist = Math.sqrt(distSq);
          const lineAlpha = (1 - dist / maxDistance) * 0.2 * (p1.opacity || 1) * (p2.opacity || 1);

          ctx.beginPath();
          ctx.moveTo(p1.x, p1.y);
          ctx.lineTo(p2.x, p2.y);
          ctx.strokeStyle = `rgba(${accentRgb}, ${lineAlpha})`;
          ctx.lineWidth = 0.7;
          ctx.stroke();
        }
      }
    }

    for (let i = 0; i < particles.length; i++) {
      particles[i].update();
      particles[i].draw(accentRgb);
    }

    requestAnimationFrame(animate);
  }

  window.addEventListener('resize', resize);

  window.addEventListener('mousemove', (e) => {
    mouseParticle.x = e.clientX;
    mouseParticle.y = e.clientY;
    mouseParticle.active = true;
  });

  window.addEventListener('mouseleave', () => {
    mouseParticle.active = false;
  });

  window.addEventListener('touchmove', (e) => {
    if (e.touches.length > 0) {
      mouseParticle.x = e.touches[0].clientX;
      mouseParticle.y = e.touches[0].clientY;
      mouseParticle.active = true;
    }
  }, { passive: true });

  window.addEventListener('touchend', () => {
    mouseParticle.active = false;
  });

  resize();
  animate();
}

if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', initParticleNetwork);
} else {
  initParticleNetwork();
}

// Al cerrar la ventana se guarda lo que esté pendiente
window.addEventListener('beforeunload', () => { if (saveTimer) savePlanNow(); if (waterTimer) saveWater(waterPendingDate); });

// Pantalla inicial: si ya hay usuarios guardados se omite el registro y se muestran los perfiles
showScreen(savedUsers.length > 0 ? 'profiles-screen' : 'auth-screen');

/* =========================================================
   PANTALLA DE CARGA INICIAL
   ========================================================= */
(function initSplash() {
  const splash = $('splash-screen');
  if (!splash) return;

  const TICK_MS = 30; // 100 pasos ≈ 3 s
  const STAGES = [
    { at: 0, text: 'Iniciando conexión...', node: -1 },
    { at: 20, text: 'Cargando perfil nutricional...', node: 0 },
    { at: 40, text: 'Verificando consumo de agua...', node: 1 },
    { at: 60, text: 'Sincronizando balance de macronutrientes...', node: 2 },
    { at: 80, text: 'Optimizando niveles de energía...', node: 3 },
    { at: 100, text: '¡Todo listo!', node: 4 }
  ];
  const nodes = document.querySelectorAll('.splash-node');

  // Saludo con el último usuario que entró (si existe)
  try {
    const email = localStorage.getItem('nutriplan_last_email');
    const last = savedUsers.find((u) => u.email === email) || savedUsers[savedUsers.length - 1];
    if (last && last.nombre) $('splash-greet').textContent = `Hola, ${last.nombre.trim().split(/\s+/)[0]}`;
  } catch (e) { /* sin almacenamiento */ }

  let progress = 0;
  let stageIdx = -1;
  let finished = false;

  function paintStage() {
    STAGES.forEach((st, i) => {
      if (progress >= st.at && i > stageIdx) {
        stageIdx = i;
        $('splash-text').textContent = st.text;
        if (st.node >= 0 && nodes[st.node]) nodes[st.node].classList.add('active');
      }
    });
  }

  function finish() {
    if (finished) return;
    finished = true;
    clearInterval(timer);
    document.removeEventListener('keydown', onKey);
    splash.classList.add('is-leaving');
    setTimeout(() => splash.classList.add('is-gone'), 600);
  }

  function onKey(e) { if (e.key === 'Escape' || e.key === 'Enter') finish(); }

  const timer = setInterval(() => {
    progress += 1;
    $('splash-fill').style.width = progress + '%';
    $('splash-percent').textContent = progress + '%';
    paintStage();
    if (progress >= 100) {
      clearInterval(timer);
      setTimeout(finish, 350);
    }
  }, TICK_MS);

  paintStage();
  splash.addEventListener('click', finish);
  document.addEventListener('keydown', onKey);
})();