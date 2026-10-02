-- =========================================================
-- NutriPlan · BD_Setup (10 Tablas Originales Simplificadas)
-- Compatible con Supabase (PostgreSQL)
-- =========================================================

-- 1. Limpieza de tablas previas (en orden inverso de dependencias)
DROP TABLE IF EXISTS hidratacion CASCADE;
DROP TABLE IF EXISTS plan_semanal CASCADE;
DROP TABLE IF EXISTS historial_peso CASCADE;
DROP TABLE IF EXISTS perfil_usuario CASCADE;
DROP TABLE IF EXISTS usuarios CASCADE;
DROP TABLE IF EXISTS alimentos CASCADE;
DROP TABLE IF EXISTS categorias CASCADE;
DROP TABLE IF EXISTS comidas CASCADE;
DROP TABLE IF EXISTS dias CASCADE;
DROP TABLE IF EXISTS objetivos CASCADE;
DROP TABLE IF EXISTS generos CASCADE;

-- ---------------------------------------------------------
-- 2. Tablas Catálogo
-- ---------------------------------------------------------

-- 1) generos — Opciones de género
CREATE TABLE generos (
  id_genero INT PRIMARY KEY,
  nombre VARCHAR(150) NOT NULL
);

-- 2) objetivos — Metas de peso
CREATE TABLE objetivos (
  id_objetivo INT PRIMARY KEY,
  nombre VARCHAR(150) NOT NULL,
  descripcion VARCHAR(255) DEFAULT NULL
);

-- 3) dias — Días de la semana
CREATE TABLE dias (
  id_dia INT PRIMARY KEY,
  nombre VARCHAR(20) NOT NULL,
  orden INT NOT NULL
);

-- 4) comidas — Tiempos de comida (desayuno, almuerzo, cena)
CREATE TABLE comidas (
  id_comida INT PRIMARY KEY,
  nombre VARCHAR(130) NOT NULL,
  orden INT NOT NULL
);

-- 5) categorias — Grupos de alimentos
CREATE TABLE categorias (
  id_categoria INT PRIMARY KEY,
  nombre VARCHAR(100) NOT NULL
);

-- ---------------------------------------------------------
-- 3. Catálogo de Alimentos
-- ---------------------------------------------------------

-- 6) alimentos — Información nutricional
CREATE TABLE alimentos (
  id_alimento INT PRIMARY KEY,
  id_categoria INT NOT NULL,
  nombre VARCHAR(100) NOT NULL,
  unidad_base VARCHAR(20) NOT NULL DEFAULT 'g',
  cantidad_base REAL NOT NULL DEFAULT 100,
  kcal REAL NOT NULL DEFAULT 0,
  proteina REAL NOT NULL DEFAULT 0,
  grasa REAL NOT NULL DEFAULT 0,
  carbohidratos REAL NOT NULL DEFAULT 0,
  CONSTRAINT fk_alimentos_categorias FOREIGN KEY (id_categoria) 
    REFERENCES categorias(id_categoria) ON UPDATE CASCADE ON DELETE RESTRICT
);

-- ---------------------------------------------------------
-- 4. Usuario y Perfil (Separados)
-- ---------------------------------------------------------

-- 7) usuarios — Cuentas de la app
CREATE TABLE usuarios (
  id_usuario INT PRIMARY KEY,
  nombre VARCHAR(300) NOT NULL,
  email VARCHAR(150) NOT NULL UNIQUE,
  password_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- 8) perfil_usuario — Datos físicos del usuario (1 a 1)
CREATE TABLE perfil_usuario (
  id_perfil INT PRIMARY KEY,
  id_usuario INT NOT NULL UNIQUE,
  id_genero INT NOT NULL,
  id_objetivo INT NOT NULL,
  peso REAL NOT NULL DEFAULT 70,
  altura REAL NOT NULL DEFAULT 170,
  avatar TEXT DEFAULT 'default.png',
  updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT fk_perfil_usuarios FOREIGN KEY (id_usuario) 
    REFERENCES usuarios(id_usuario) ON UPDATE CASCADE ON DELETE CASCADE,
  CONSTRAINT fk_perfil_generos FOREIGN KEY (id_genero) 
    REFERENCES generos(id_genero) ON UPDATE CASCADE ON DELETE RESTRICT,
  CONSTRAINT fk_perfil_objetivos FOREIGN KEY (id_objetivo) 
    REFERENCES objetivos(id_objetivo) ON UPDATE CASCADE ON DELETE RESTRICT
);

-- ---------------------------------------------------------
-- 5. Seguimiento y Planificación
-- ---------------------------------------------------------

-- 9) historial_peso — Registro de progreso de peso
CREATE TABLE historial_peso (
  id_historial INT PRIMARY KEY,
  id_usuario INT NOT NULL,
  peso REAL NOT NULL,
  registrado_en TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT fk_historial_usuarios FOREIGN KEY (id_usuario) 
    REFERENCES usuarios(id_usuario) ON UPDATE CASCADE ON DELETE CASCADE
);

-- 10) plan_semanal — Detalle de plan alimenticio por día/comida
CREATE TABLE plan_semanal (
  id_plan INT PRIMARY KEY,
  id_usuario INT NOT NULL,
  id_dia INT NOT NULL,
  id_comida INT NOT NULL,
  id_alimento INT NOT NULL,
  cantidad REAL NOT NULL CHECK (cantidad > 0),
  unidad VARCHAR(20) NOT NULL DEFAULT 'g',
  CONSTRAINT fk_plan_usuarios FOREIGN KEY (id_usuario) 
    REFERENCES usuarios(id_usuario) ON UPDATE CASCADE ON DELETE CASCADE,
  CONSTRAINT fk_plan_dias FOREIGN KEY (id_dia) 
    REFERENCES dias(id_dia) ON UPDATE CASCADE ON DELETE RESTRICT,
  CONSTRAINT fk_plan_comidas FOREIGN KEY (id_comida) 
    REFERENCES comidas(id_comida) ON UPDATE CASCADE ON DELETE RESTRICT,
  CONSTRAINT fk_plan_alimentos FOREIGN KEY (id_alimento) 
    REFERENCES alimentos(id_alimento) ON UPDATE CASCADE ON DELETE RESTRICT
);

-- 11) hidratacion — Vasos de agua por día (un registro por usuario y fecha)
CREATE TABLE IF NOT EXISTS hidratacion (
  id_hidratacion INT PRIMARY KEY,
  id_usuario INT NOT NULL,
  fecha DATE NOT NULL,
  vasos INT NOT NULL DEFAULT 0 CHECK (vasos >= 0),
  updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT fk_hidratacion_usuarios FOREIGN KEY (id_usuario)
    REFERENCES usuarios(id_usuario) ON UPDATE CASCADE ON DELETE CASCADE,
  CONSTRAINT uq_hidratacion_usuario_dia UNIQUE (id_usuario, fecha)
);

-- =========================================================
-- Inserción de Datos Adaptada a Esquema con SERIAL e ID Numéricos
-- =========================================================

INSERT INTO generos (id_genero, nombre) VALUES
  (1, 'Femenino'),
  (2, 'Masculino'),
  (3, 'No binario / Otro'),
  (4, 'Prefiero no decir'),
  (5, 'No especificado');

INSERT INTO objetivos (id_objetivo, nombre, descripcion) VALUES
  (1, 'Bajar de peso', 'Déficit calórico moderado y sostenible, priorizando proteína para conservar masa muscular.'),
  (2, 'Mantener peso', 'Rango de calorías balanceado para sostener el peso actual.'),
  (3, 'Subir de peso', 'Superávit calórico controlado, con más carbohidratos y proteína, para ganar peso gradualmente.');

INSERT INTO dias (id_dia, nombre, orden) VALUES
  (1, 'Lunes', 1),
  (2, 'Martes', 2),
  (3, 'Miércoles', 3),
  (4, 'Jueves', 4),
  (5, 'Viernes', 5),
  (6, 'Sábado', 6),
  (7, 'Domingo', 7);

INSERT INTO comidas (id_comida, nombre, orden) VALUES
  (1, 'Desayuno', 1),
  (2, 'Almuerzo', 2),
  (3, 'Cena', 3);

INSERT INTO categorias (id_categoria, nombre) VALUES
  (1, 'Granos, Cereales y Tubérculos'),
  (2, 'Legumbres'),
  (3, 'Carnes y Aves'),
  (4, 'Pescados y Mariscos'),
  (5, 'Verduras y Hortalizas'),
  (6, 'Frutas'),
  (7, 'Lácteos y Huevos'),
  (8, 'Grasas, Aceites y Frutos Secos'),
  (9, 'Bebidas'),
  (10, 'Procesados y Snacks'),
  (11, 'Condimentos y Salsas');

INSERT INTO alimentos (id_alimento, id_categoria, nombre, unidad_base, cantidad_base, kcal, proteina, grasa, carbohidratos) VALUES
  -- Granos (id_categoria: 1)
  (1, 1, 'Arroz blanco (cocido)', 'g', 100, 130, 2.7, 0.3, 28),
  (2, 1, 'Arroz integral (cocido)', 'g', 100, 111, 2.6, 0.9, 23),
  (3, 1, 'Avena en hojuelas', 'g', 100, 389, 16.9, 6.9, 66),
  (4, 1, 'Pasta (cocida)', 'g', 100, 131, 5, 1.1, 25),
  (5, 1, 'Pan integral', 'g', 100, 247, 13, 3.4, 41),
  (6, 1, 'Pan blanco', 'g', 100, 265, 9, 3.2, 49),
  (7, 1, 'Quinoa (cocida)', 'g', 100, 120, 4.4, 1.9, 21.3),
  (8, 1, 'Papa cocida', 'g', 100, 87, 1.9, 0.1, 20),
  (9, 1, 'Papa horneada con cáscara', 'unidad', 1, 161, 4.3, 0.2, 37),
  (10, 1, 'Yuca cocida', 'g', 100, 160, 1.4, 0.3, 38),
  (11, 1, 'Plátano verde cocido', 'g', 100, 122, 1.3, 0.3, 32),
  (12, 1, 'Maíz dulce (grano)', 'g', 100, 96, 3.4, 1.5, 21),
  (13, 1, 'Tortilla de maíz', 'unidad', 1, 52, 1.4, 0.6, 11),
  (14, 1, 'Cuscús cocido', 'g', 100, 112, 3.8, 0.2, 23),

  -- Legumbres (id_categoria: 2)
  (15, 2, 'Lentejas (cocidas)', 'g', 100, 116, 9, 0.4, 20),
  (16, 2, 'Garbanzos (cocidos)', 'g', 100, 164, 8.9, 2.6, 27),
  (17, 2, 'Frijol negro (cocido)', 'g', 100, 132, 8.9, 0.5, 24),
  (18, 2, 'Frijol rojo (cocido)', 'g', 100, 127, 8.7, 0.5, 22.8),
  (19, 2, 'Arvejas / Guisantes', 'g', 100, 81, 5.4, 0.4, 14.5),
  (20, 2, 'Habas cocidas', 'g', 100, 110, 7.9, 0.4, 19.6),
  (21, 2, 'Soya texturizada (hidratada)', 'g', 100, 120, 18, 1, 9),

  -- Carnes y Aves (id_categoria: 3)
  (22, 3, 'Pechuga de pollo (cocida)', 'g', 100, 165, 31, 3.6, 0),
  (23, 3, 'Muslo de pollo (cocido, sin piel)', 'g', 100, 178, 24, 8.5, 0),
  (24, 3, 'Carne de res magra', 'g', 100, 250, 26, 15, 0),
  (25, 3, 'Carne molida (80/20, cocida)', 'g', 100, 254, 25.6, 16.5, 0),
  (26, 3, 'Lomo de cerdo (cocido)', 'g', 100, 242, 27, 14, 0),
  (27, 3, 'Pechuga de pavo (cocida)', 'g', 100, 135, 30, 0.7, 0),
  (28, 3, 'Tocino frito', 'g', 100, 541, 37, 42, 1.4),
  (29, 3, 'Jamón de pavo/cerdo', 'g', 100, 145, 21, 4.5, 1.5),
  (30, 3, 'Chorizo', 'g', 100, 455, 24, 38, 3),
  (31, 3, 'Hígado de res (cocido)', 'g', 100, 175, 26, 4.9, 3.9),
  (32, 3, 'Tofu firme', 'g', 100, 76, 8, 4.8, 1.9),
  (33, 3, 'Huevo entero', 'unidad', 1, 72, 6.3, 4.8, 0.4),
  (34, 3, 'Clara de huevo', 'unidad', 1, 17, 3.6, 0.1, 0.2),

  -- Pescados y Mariscos (id_categoria: 4)
  (35, 4, 'Filete de salmón', 'g', 100, 208, 20, 13, 0),
  (36, 4, 'Atún en agua (enlatado)', 'g', 100, 116, 26, 1, 0),
  (37, 4, 'Atún fresco (a la plancha)', 'g', 100, 184, 30, 6.3, 0),
  (38, 4, 'Filete de tilapia', 'g', 100, 128, 26, 2.7, 0),
  (39, 4, 'Camarones cocidos', 'g', 100, 99, 24, 0.3, 0.2),
  (40, 4, 'Merluza al horno', 'g', 100, 90, 18.6, 1, 0),
  (41, 4, 'Sardinas en aceite (enlatadas)', 'g', 100, 208, 25, 11, 0),
  (42, 4, 'Pulpo cocido', 'g', 100, 164, 30, 2.1, 4.4),

  -- Verduras y Hortalizas (id_categoria: 5)
  (43, 5, 'Brócoli (cocido)', 'g', 100, 35, 2.4, 0.4, 7),
  (44, 5, 'Espinaca fresca', 'g', 100, 23, 2.9, 0.4, 3.6),
  (45, 5, 'Zanahoria', 'g', 100, 41, 0.9, 0.2, 10),
  (46, 5, 'Tomate fresco', 'g', 100, 18, 0.9, 0.2, 3.9),
  (47, 5, 'Aguacate', 'g', 100, 160, 2, 15, 9),
  (48, 5, 'Lechuga', 'g', 100, 15, 1.4, 0.2, 2.9),
  (49, 5, 'Pepino', 'g', 100, 15, 0.7, 0.1, 3.6),
  (50, 5, 'Cebolla', 'g', 100, 40, 1.1, 0.1, 9.3),
  (51, 5, 'Pimentón / Pimiento', 'g', 100, 31, 1, 0.3, 6),
  (52, 5, 'Coliflor (cocida)', 'g', 100, 25, 1.9, 0.3, 5),
  (53, 5, 'Calabacín / Zucchini', 'g', 100, 17, 1.2, 0.3, 3.1),
  (54, 5, 'Champiñones', 'g', 100, 22, 3.1, 0.3, 3.3),
  (55, 5, 'Remolacha cocida', 'g', 100, 44, 1.7, 0.2, 10),
  (56, 5, 'Apio', 'g', 100, 16, 0.7, 0.2, 3),

  -- Frutas (id_categoria: 6)
  (57, 6, 'Manzana', 'unidad', 1, 95, 0.5, 0.3, 25),
  (58, 6, 'Banano / Plátano', 'unidad', 1, 105, 1.3, 0.4, 27),
  (59, 6, 'Fresas', 'g', 100, 32, 0.7, 0.3, 7.7),
  (60, 6, 'Naranja', 'unidad', 1, 62, 1.2, 0.2, 15),
  (61, 6, 'Pera', 'unidad', 1, 101, 0.6, 0.2, 27),
  (62, 6, 'Uvas', 'g', 100, 69, 0.7, 0.2, 18),
  (63, 6, 'Piña', 'g', 100, 50, 0.5, 0.1, 13),
  (64, 6, 'Mango', 'unidad', 1, 202, 2.8, 1.3, 50),
  (65, 6, 'Papaya', 'g', 100, 43, 0.5, 0.3, 11),
  (66, 6, 'Sandía', 'g', 100, 30, 0.6, 0.2, 7.6),
  (67, 6, 'Melón', 'g', 100, 34, 0.8, 0.2, 8.2),
  (68, 6, 'Kiwi', 'unidad', 1, 42, 0.8, 0.4, 10),
  (69, 6, 'Mandarina', 'unidad', 1, 47, 0.7, 0.3, 12),
  (70, 6, 'Moras', 'g', 100, 43, 1.4, 0.5, 9.6),

  -- Lácteos y Huevos (id_categoria: 7)
  (71, 7, 'Leche entera', 'ml', 100, 61, 3.2, 3.2, 4.8),
  (72, 7, 'Leche descremada', 'ml', 100, 35, 3.4, 0.1, 5),
  (73, 7, 'Yogur griego natural', 'g', 100, 59, 10, 0.4, 3.6),
  (74, 7, 'Yogur natural entero', 'g', 100, 61, 3.5, 3.3, 4.7),
  (75, 7, 'Queso fresco', 'g', 100, 264, 18, 20, 3),
  (76, 7, 'Queso mozzarella', 'g', 100, 280, 28, 17, 3.1),
  (77, 7, 'Queso crema', 'g', 100, 342, 6, 34, 4),
  (78, 7, 'Mantequilla', 'g', 100, 717, 0.9, 81, 0.1),
  (79, 7, 'Kumis / Kéfir', 'ml', 100, 56, 3.3, 2, 4.5),

  -- Grasas, Aceites y Frutos Secos (id_categoria: 8)
  (80, 8, 'Aceite de oliva', 'ml', 15, 119, 0, 13.5, 0),
  (81, 8, 'Aceite vegetal', 'ml', 15, 120, 0, 14, 0),
  (82, 8, 'Almendras', 'g', 100, 579, 21, 50, 22),
  (83, 8, 'Nueces', 'g', 100, 654, 15, 65, 14),
  (84, 8, 'Maní / Cacahuate', 'g', 100, 567, 26, 49, 16),
  (85, 8, 'Mantequilla de maní', 'g', 100, 588, 25, 50, 20),
  (86, 8, 'Semillas de chía', 'g', 100, 486, 17, 31, 42),
  (87, 8, 'Frutos secos mixtos', 'g', 100, 607, 20, 54, 21),
  (88, 8, 'Coco rallado', 'g', 100, 660, 6.9, 64, 24),

  -- Bebidas (id_categoria: 9)
  (89, 9, 'Agua', 'ml', 250, 0, 0, 0, 0),
  (90, 9, 'Jugo de naranja natural', 'ml', 200, 90, 1.4, 0.4, 21),
  (91, 9, 'Café negro sin azúcar', 'ml', 200, 2, 0.3, 0, 0),
  (92, 9, 'Té verde', 'ml', 200, 2, 0, 0, 0),
  (93, 9, 'Gaseosa / Refresco', 'ml', 350, 140, 0, 0, 39),
  (94, 9, 'Bebida energizante', 'ml', 250, 110, 0, 0, 28),
  (95, 9, 'Cerveza', 'ml', 330, 150, 1.6, 0, 13),
  (96, 9, 'Batido de proteína (agua)', 'g', 30, 120, 24, 1.5, 3),
  (97, 9, 'Leche de almendras', 'ml', 100, 15, 0.6, 1.2, 0.6),

  -- Procesados y Snacks (id_categoria: 10)
  (98, 10, 'Papas fritas', 'g', 100, 536, 7, 35, 53),
  (99, 10, 'Chocolate negro 70%', 'g', 100, 598, 7.8, 42, 46),
  (100, 10, 'Chocolate con leche', 'g', 100, 535, 7.6, 30, 59),
  (101, 10, 'Galletas dulces', 'g', 100, 480, 6, 22, 65),
  (102, 10, 'Helado de vainilla', 'g', 100, 207, 3.5, 11, 24),
  (103, 10, 'Pizza (porción)', 'g', 100, 266, 11, 10, 33),
  (104, 10, 'Hamburguesa completa', 'unidad', 1, 540, 25, 27, 45),
  (105, 10, 'Nuggets de pollo', 'g', 100, 296, 15, 19, 17),
  (106, 10, 'Cereal azucarado', 'g', 100, 380, 5, 2, 84),
  (107, 10, 'Barra energética / granola', 'unidad', 1, 190, 4, 7, 29),
  (108, 10, 'Pan dulce / ponqué', 'g', 100, 371, 5.5, 15, 55),

  -- Condimentos y Salsas (id_categoria: 11)
  (109, 11, 'Sal', 'g', 5, 0, 0, 0, 0),
  (110, 11, 'Azúcar blanca', 'g', 5, 19, 0, 0, 5),
  (111, 11, 'Miel de abejas', 'g', 15, 46, 0, 0, 12.5),
  (112, 11, 'Salsa de tomate / ketchup', 'g', 20, 20, 0.3, 0.1, 4.7),
  (113, 11, 'Mayonesa', 'g', 15, 94, 0.1, 10.3, 0.6),
  (114, 11, 'Mostaza', 'g', 15, 11, 0.6, 0.6, 1),
  (115, 11, 'Salsa de soya', 'ml', 15, 8, 1.3, 0, 0.8),
  (116, 11, 'Vinagreta / aderezo', 'ml', 15, 45, 0, 4.5, 1.5);

-- ---------------------------------------------------------
-- 7. Permisos y Políticas de Seguridad (RLS Supabase)
-- ---------------------------------------------------------

GRANT USAGE ON SCHEMA public TO anon, authenticated;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO anon, authenticated;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO anon, authenticated;
GRANT SELECT, INSERT, UPDATE, DELETE ON hidratacion TO anon, authenticated;

ALTER TABLE generos ENABLE ROW LEVEL SECURITY;
ALTER TABLE objetivos ENABLE ROW LEVEL SECURITY;
ALTER TABLE dias ENABLE ROW LEVEL SECURITY;
ALTER TABLE comidas ENABLE ROW LEVEL SECURITY;
ALTER TABLE categorias ENABLE ROW LEVEL SECURITY;
ALTER TABLE alimentos ENABLE ROW LEVEL SECURITY;
ALTER TABLE usuarios ENABLE ROW LEVEL SECURITY;
ALTER TABLE perfil_usuario ENABLE ROW LEVEL SECURITY;
ALTER TABLE historial_peso ENABLE ROW LEVEL SECURITY;
ALTER TABLE plan_semanal ENABLE ROW LEVEL SECURITY;
ALTER TABLE hidratacion ENABLE ROW LEVEL SECURITY;

CREATE POLICY "acceso_total_generos" ON generos FOR ALL TO anon USING (true) WITH CHECK (true);
CREATE POLICY "acceso_total_objetivos" ON objetivos FOR ALL TO anon USING (true) WITH CHECK (true);
CREATE POLICY "acceso_total_dias" ON dias FOR ALL TO anon USING (true) WITH CHECK (true);
CREATE POLICY "acceso_total_comidas" ON comidas FOR ALL TO anon USING (true) WITH CHECK (true);
CREATE POLICY "acceso_total_categorias" ON categorias FOR ALL TO anon USING (true) WITH CHECK (true);
CREATE POLICY "acceso_total_alimentos" ON alimentos FOR ALL TO anon USING (true) WITH CHECK (true);
CREATE POLICY "acceso_total_usuarios" ON usuarios FOR ALL TO anon USING (true) WITH CHECK (true);
CREATE POLICY "acceso_total_perfil_usuario" ON perfil_usuario FOR ALL TO anon USING (true) WITH CHECK (true);
CREATE POLICY "acceso_total_historial_peso" ON historial_peso FOR ALL TO anon USING (true) WITH CHECK (true);
CREATE POLICY "acceso_total_plan_semanal" ON plan_semanal FOR ALL TO anon USING (true) WITH CHECK (true);
DROP POLICY IF EXISTS "hidratacion_acceso_app" ON hidratacion;
CREATE POLICY "hidratacion_acceso_app" ON hidratacion
  FOR ALL TO anon, authenticated
  USING (true) WITH CHECK (true);

notify pgrst, 'reload schema';