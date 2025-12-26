# GesMonth v2.1.0 - Guía Técnica para Desarrolladores

## Tabla de Contenidos

1. [Visión General](#visión-general)
2. [Arquitectura del Sistema](#arquitectura-del-sistema)
3. [Stack Tecnológico](#stack-tecnológico)
4. [Estructura del Proyecto](#estructura-del-proyecto)
5. [Base de Datos](#base-de-datos)
6. [Patrones de Diseño](#patrones-de-diseño)
7. [Flujos de Negocio](#flujos-de-negocio)
8. [Guía de Desarrollo](#guía-de-desarrollo)
9. [Testing](#testing)
10. [Compilación y Distribución](#compilación-y-distribución)
11. [Contribuciones](#contribuciones)

---

## Visión General

### Propósito del Proyecto

GesMonth v2.1.0 es un sistema de gestión de pagos mensuales diseñado para pequeños negocios que requieren:

- Control de clientes y membresías
- Seguimiento de pagos recurrentes
- Gestión de mora y deudas acumuladas
- Reportes financieros básicos
- Sistema de autenticación multi-nivel
- Persistencia local sin dependencias cloud

### Decisiones Arquitectónicas

#### ¿Por qué Desktop?

**Ventajas:**
- Privacidad total (datos 100% locales)
- Sin costos de hosting o infraestructura
- Velocidad (sin latencia de red)
- Autonomía (funciona offline)
- Simplicidad de despliegue

**Desventajas asumidas:**
- No hay sincronización multi-dispositivo
- Actualizaciones manuales
- No accesible remotamente

#### ¿Por qué Python + PyQt6?

**Python:**
- Rápido desarrollo y mantenimiento
- Ecosistema rico (pandas, openpyxl futuro)
- Type hints para mejor IDE support
- Multiplataforma sin cambios de código

**PyQt6:**
- Framework GUI maduro y estable
- Widgets profesionales nativos
- Multiplataforma (Windows/Linux/macOS)
- QSS para estilos CSS-like
- Mejor que alternativas:
  - Tkinter: Limitado visualmente
  - Electron: Pesado (>100MB)
  - Web local: Complejidad innecesaria

#### ¿Por qué SQLite?

**Ventajas:**
- Archivo único portable
- Sin servidor DB externo
- ACID transactions
- Suficiente para <100k registros
- SQL estándar (migrable a Postgres/MySQL)

**Limitaciones conocidas:**
- No concurrencia write masiva
- No queries distribuidas
- Límite de 2GB (no es problema aquí)

### Historial de Versiones

**v2.1.0 (26 dic 2025):**
- Licencia Source Available (SAL)
- Sistema de datos persistente (.data/)
- Versionado dinámico
- Persistencia de tema y pantalla completa
- Toggle switches modernos
- Splash screen inteligente

**v2.0.0 (25 dic 2024):**
- Sistema de autenticación (bcrypt)
- 4 roles de usuario
- Gestión de usuarios y auditoría
- Protección anti-fuerza bruta
- Sistema de temas claro/oscuro

**v1.0.1 (23 dic 2024):**
- Ejecutable standalone con PyInstaller
- Scripts de compilación y empaquetado
- Optimización de assets y rutas
- GitHub Actions para builds automáticos

**v1.0.0 (23 dic 2024):**
- Release inicial
- Dashboard con métricas clave
- Gestión completa de clientes (CRUD)
- Control de cuotas mensuales
- Registro de pagos
- Reportes y estadísticas
- Interfaz glassmorphism

---

## Arquitectura del Sistema

### Patrón MVC (Modelo-Vista-Controlador)

```
┌─────────────────────────────────────────────┐
│              VISTA (UI Layer)               │
│  PyQt6 Widgets, QSS Styles, User Events    │
└──────────────────┬──────────────────────────┘
                   │
                   │ User Actions
                   ↓
┌─────────────────────────────────────────────┐
│        CONTROLADOR (Business Logic)         │
│  Validaciones, Reglas de Negocio, Flujos   │
└──────────────────┬──────────────────────────┘
                   │
                   │ CRUD Operations
                   ↓
┌─────────────────────────────────────────────┐
│          MODELO (Data Layer)                │
│  SQLite DB, Models, Queries, Schemas       │
└─────────────────────────────────────────────┘
```

### Separación de Bases de Datos

**gesmonth.db** (Datos de negocio):
- clientes
- cuotas_mensuales
- pagos
- metodos_pago
- configuracion

**users.db** (Autenticación y seguridad):
- usuarios
- sesiones
- auditoria

**Razón**: Separar concerns de negocio y seguridad permite mejor mantenimiento y respaldos selectivos.

### Flujo de Ejecución

```
main.py
  ↓
splash_screen.py (2 seg)
  ↓
login_view.py (autenticación)
  ↓
main_window.py (sidebar + contenido)
  ↓
[dashboard_view | clientes_view | cuotas_view | reportes_view | configuracion_view]
```

---

## Stack Tecnológico

### Core

| Tecnología | Versión | Propósito |
|-----------|---------|-----------|
| Python | 3.9+ | Lenguaje base |
| PyQt6 | 6.7.1 | Framework GUI |
| SQLite | 3.x | Base de datos |
| bcrypt | Latest | Encriptación passwords |

### Herramientas de Desarrollo

| Tool | Propósito |
|------|-----------|
| PyInstaller | Compilación a ejecutable |
| Git | Control de versiones |
| VSCode/PyCharm | IDE recomendado |

### Estructura de Dependencias

```
requirements.txt:
  - PyQt6==6.7.1
  - PyQt6-Qt6==6.6.1
  - PyQt6-sip==13.6.0
  - bcrypt>=4.0.0
```

---

## Estructura del Proyecto

```
GesMonth/
├── main.py                      # Entry point
├── VERSION                      # 2.1.0
├── LICENSE                      # SAL License
├── requirements.txt
├── gesmonth.spec               # PyInstaller config
│
├── database/                    # Data Layer
│   ├── connection.py           # Singleton gesmonth.db
│   ├── user_connection.py      # Singleton users.db
│   ├── models.py               # Business models
│   └── user_models.py          # Auth models
│
├── ui/                         # View Layer
│   ├── main_window.py          # Main container + sidebar
│   ├── login_view.py           # Auth screen
│   ├── splash_screen.py        # Loading screen
│   ├── dashboard_view.py       # Home metrics
│   ├── clientes_view.py        # Clients CRUD
│   ├── cuotas_view.py          # Monthly fees grid
│   ├── pagos_view.py           # Payments registry
│   ├── reportes_view.py        # Reports
│   ├── configuracion_view.py   # Settings
│   ├── usuarios_management.py  # User management (superadmin)
│   ├── theme_colors.py         # Color palette
│   └── detalles_cuota_dialog.py
│
├── controllers/                # Business Logic
│   ├── auth_controller.py      # Login, roles, tokens
│   ├── cliente_controller.py   # Client operations
│   ├── pago_controller.py      # Payment operations
│   ├── reporte_controller.py   # Report generation
│   ├── config_controller.py    # App configuration
│   └── theme_controller.py     # Theme switching
│
├── utils/                      # Utilities
│   └── __init__.py             # get_resource_path, get_data_path
│
├── assets/                     # Static Resources
│   ├── icons/                  # SVG icons
│   │   ├── home.svg
│   │   ├── cuotas.svg
│   │   ├── clientes.svg
│   │   ├── reportes.svg
│   │   ├── settings.svg
│   │   ├── logout-session.svg
│   │   └── power-off.svg
│   └── styles/                 # QSS Stylesheets
│       ├── dark.qss
│       └── light.qss
│
├── scripts/                    # Automation
│   ├── build.sh / build.bat    # Compile
│   ├── install.sh / install.bat
│   ├── run.sh / run.bat
│   ├── package.sh / package.bat
│   └── ver_datos.py            # DB inspector
│
├── docs/                       # Documentation
│   ├── DESARROLLO.md           # Deep technical guide
│   ├── README-user.md          # User manual
│   ├── README-dev.md           # This file
│   ├── BUILD.md                # Compilation guide
│   ├── DISTRIBUCION.md         # Distribution guide
│   └── SISTEMA-AUTENTICACION.md
│
└── .data/                      # Persistent Data (not in repo)
    ├── gesmonth.db             # Business database
    └── users.db                # Auth database
```

---

## Base de Datos

### Esquema: gesmonth.db

#### Tabla: clientes

```sql
CREATE TABLE clientes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    documento TEXT UNIQUE NOT NULL,
    telefono TEXT,
    estado TEXT DEFAULT 'activo',  -- 'activo' | 'inactivo'
    valor_cuota REAL NOT NULL,
    dia_cobro INTEGER NOT NULL CHECK(dia_cobro BETWEEN 1 AND 31)
);

CREATE INDEX idx_clientes_estado ON clientes(estado);
CREATE INDEX idx_clientes_documento ON clientes(documento);
```

#### Tabla: cuotas_mensuales

```sql
CREATE TABLE cuotas_mensuales (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cliente_id INTEGER NOT NULL,
    año INTEGER NOT NULL,
    mes INTEGER NOT NULL CHECK(mes BETWEEN 1 AND 12),
    monto REAL NOT NULL,
    estado TEXT DEFAULT 'pendiente',  -- 'pagado' | 'impago' | 'con_deuda' | 'pendiente'
    metodo_pago TEXT,
    fecha_pago DATE,
    deuda_acumulada REAL DEFAULT 0,
    fecha_inicio_mora DATE,
    FOREIGN KEY (cliente_id) REFERENCES clientes(id) ON DELETE CASCADE,
    UNIQUE(cliente_id, año, mes)
);

CREATE INDEX idx_cuotas_cliente ON cuotas_mensuales(cliente_id);
CREATE INDEX idx_cuotas_año_mes ON cuotas_mensuales(año, mes);
CREATE INDEX idx_cuotas_estado ON cuotas_mensuales(estado);
```

**Estados explicados:**
- **pagado**: Cuota completamente pagada
- **impago**: Sin pago, genera mora
- **con_deuda**: Pago parcial o deuda heredada del mes anterior
- **pendiente**: Mes aún no vencido

#### Tabla: pagos

```sql
CREATE TABLE pagos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cliente_id INTEGER NOT NULL,
    fecha_pago DATE NOT NULL,
    mes_correspondiente TEXT NOT NULL,  -- Format: 'YYYY-MM'
    monto REAL NOT NULL,
    metodo_pago TEXT,
    FOREIGN KEY (cliente_id) REFERENCES clientes(id) ON DELETE CASCADE
);

CREATE INDEX idx_pagos_cliente ON pagos(cliente_id);
CREATE INDEX idx_pagos_mes ON pagos(mes_correspondiente);
```

#### Tabla: metodos_pago

```sql
CREATE TABLE metodos_pago (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT UNIQUE NOT NULL,
    activo INTEGER DEFAULT 1  -- 1=activo, 0=inactivo
);

-- Métodos por defecto
INSERT INTO metodos_pago (nombre) VALUES ('Efectivo'), ('Transferencia'), ('Tarjeta');
```

#### Tabla: configuracion

```sql
CREATE TABLE configuracion (
    clave TEXT PRIMARY KEY,
    valor TEXT
);

-- Configuraciones por defecto
INSERT INTO configuracion (clave, valor) VALUES 
    ('tema', 'dark'),
    ('pantalla_completa', 'false'),
    ('años_facturacion', '2024,2025');
```

### Esquema: users.db

#### Tabla: usuarios

```sql
CREATE TABLE usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,  -- bcrypt hash
    rol TEXT NOT NULL CHECK(rol IN ('superadmin', 'admin', 'operador', 'solo_lectura')),
    activo INTEGER DEFAULT 1,
    intentos_fallidos INTEGER DEFAULT 0,
    bloqueado_hasta TIMESTAMP,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Usuario por defecto
INSERT INTO usuarios (username, password_hash, rol) 
VALUES ('admin', '$2b$12$...', 'superadmin');
```

**Roles:**
- **superadmin**: Acceso total + gestión de usuarios
- **admin**: Acceso total excepto usuarios
- **operador**: Ver y registrar, no eliminar
- **solo_lectura**: Solo consultas

#### Tabla: sesiones

```sql
CREATE TABLE sesiones (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario_id INTEGER NOT NULL,
    token TEXT UNIQUE NOT NULL,  -- UUID generado
    fecha_inicio TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_expiracion TIMESTAMP,
    activa INTEGER DEFAULT 1,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
);
```

#### Tabla: auditoria

```sql
CREATE TABLE auditoria (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario_id INTEGER,
    accion TEXT NOT NULL,  -- 'crear', 'editar', 'eliminar', 'login', etc.
    tabla_afectada TEXT,   -- 'clientes', 'pagos', etc.
    registro_id INTEGER,   -- ID del registro afectado
    detalles TEXT,         -- JSON con info adicional
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
);

CREATE INDEX idx_auditoria_usuario ON auditoria(usuario_id);
CREATE INDEX idx_auditoria_fecha ON auditoria(fecha);
```

---

## Patrones de Diseño

### 1. Singleton (Database Connections)

```python
class DatabaseConnection:
    _instance = None
    _connection = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if self._connection is None:
            db_path = get_data_path('gesmonth.db')
            self._connection = sqlite3.connect(db_path, check_same_thread=False)
            self._connection.row_factory = sqlite3.Row
```

**Razón**: Garantizar una única conexión DB, evitar múltiples handles abiertos.

### 2. Active Record (Models)

```python
class Cliente:
    @staticmethod
    def crear(nombre, documento, telefono, valor_cuota, dia_cobro):
        db = DatabaseConnection()
        cursor = db.get_connection().cursor()
        cursor.execute("""
            INSERT INTO clientes (nombre, documento, telefono, valor_cuota, dia_cobro)
            VALUES (?, ?, ?, ?, ?)
        """, (nombre, documento, telefono, valor_cuota, dia_cobro))
        db.get_connection().commit()
        return cursor.lastrowid
    
    @staticmethod
    def obtener_todos():
        db = DatabaseConnection()
        cursor = db.get_connection().cursor()
        cursor.execute("SELECT * FROM clientes WHERE estado = 'activo' ORDER BY nombre")
        return cursor.fetchall()
```

**Razón**: Encapsular lógica de datos en los modelos, métodos estáticos simples sin instancias.

### 3. MVC (Separation of Concerns)

**Vista** (ui/clientes_view.py):
```python
def _guardar_cliente(self):
    datos = {
        'nombre': self.input_nombre.text(),
        'documento': self.input_documento.text(),
        # ...
    }
    exito, mensaje = ClienteController.crear_cliente(datos)
    if exito:
        self._mostrar_exito(mensaje)
        self._cargar_clientes()
    else:
        self._mostrar_error(mensaje)
```

**Controlador** (controllers/cliente_controller.py):
```python
@staticmethod
def crear_cliente(datos):
    # Validaciones
    if not datos['nombre']:
        return False, "El nombre es obligatorio"
    
    # Lógica de negocio
    try:
        cliente_id = Cliente.crear(
            nombre=datos['nombre'],
            documento=datos['documento'],
            # ...
        )
        AuditoriaController.registrar('crear', 'clientes', cliente_id)
        return True, "Cliente creado exitosamente"
    except sqlite3.IntegrityError:
        return False, "El documento ya existe"
```

**Modelo** (database/models.py):
```python
class Cliente:
    @staticmethod
    def crear(nombre, documento, telefono, valor_cuota, dia_cobro):
        # Solo operaciones de base de datos
        # Sin validaciones, sin lógica de negocio
        pass
```

### 4. Observer (Qt Signals/Slots)

```python
# Vista registra eventos
self.btn_guardar.clicked.connect(self._guardar_cliente)

# Método reacciona al evento
def _guardar_cliente(self):
    # ...
    self._cargar_clientes()  # Notifica cambios
```

---

## Flujos de Negocio

### Flujo: Registrar Pago

```
Usuario click en mes → Dialog "Registrar Pago"
  ↓
Usuario ingresa monto y método
  ↓
Click "Guardar"
  ↓
PagoController.registrar_pago()
  ↓
Validaciones:
  - Monto > 0
  - Método válido
  - No duplicado (5 seg window)
  ↓
Pago.crear() → INSERT en tabla pagos
  ↓
Actualizar cuota:
  - Si monto >= valor_cuota → estado = 'pagado'
  - Si monto < valor_cuota → estado = 'con_deuda'
  - Calcular deuda_acumulada
  ↓
CuotaMensual.actualizar_estado()
  ↓
AuditoriaController.registrar()
  ↓
Vista: Mostrar éxito, recargar grid
```

### Flujo: Login

```
Usuario ingresa username/password
  ↓
Click "Iniciar Sesión"
  ↓
AuthController.autenticar()
  ↓
Buscar usuario en users.db
  ↓
¿Existe? NO → Error "Usuario no encontrado"
  ↓ SÍ
¿Bloqueado? SÍ → Error "Usuario bloqueado"
  ↓ NO
bcrypt.checkpw(password, hash_almacenado)
  ↓
¿Correcto? NO → Incrementar intentos_fallidos
             → Si intentos >= 5: Bloquear 15 min
             → Error "Contraseña incorrecta"
  ↓ SÍ
Resetear intentos_fallidos a 0
  ↓
Generar token de sesión (UUID)
  ↓
Insertar en tabla sesiones
  ↓
Auditoría: Registrar login
  ↓
Retornar usuario y token
  ↓
MainWindow: Cargar con permisos según rol
```

### Flujo: Calcular Mora

```
Dashboard necesita "Clientes en Mora"
  ↓
ReporteController.obtener_clientes_en_mora()
  ↓
Query: SELECT DISTINCT cliente_id 
       FROM cuotas_mensuales
       WHERE estado = 'impago'
       AND fecha_inicio_mora IS NOT NULL
  ↓
Por cada cliente_id:
  - Obtener datos del cliente
  - Calcular días en mora (HOY - fecha_inicio_mora)
  ↓
Retornar lista de clientes en mora
  ↓
Vista: Mostrar en tarjeta "Clientes en Mora"
```

---

## Guía de Desarrollo

### Setup Inicial

```bash
# 1. Clonar repositorio
git clone https://github.com/DIlanSG/GesMonth.git
cd GesMonth

# 2. Crear entorno virtual
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Ejecutar
python main.py
```

### Agregar Nueva Funcionalidad

#### Ejemplo: Agregar "Notas" a Clientes

**1. Actualizar Schema (database/connection.py)**

```python
def _init_schema(self):
    # ...
    cursor.execute("""
        ALTER TABLE clientes ADD COLUMN notas TEXT
    """)
```

**2. Actualizar Modelo (database/models.py)**

```python
class Cliente:
    @staticmethod
    def actualizar_notas(cliente_id, notas):
        db = DatabaseConnection()
        cursor = db.get_connection().cursor()
        cursor.execute("""
            UPDATE clientes SET notas = ? WHERE id = ?
        """, (notas, cliente_id))
        db.get_connection().commit()
```

**3. Actualizar Controlador (controllers/cliente_controller.py)**

```python
@staticmethod
def guardar_notas(cliente_id, notas):
    if len(notas) > 500:
        return False, "Notas demasiado largas"
    
    Cliente.actualizar_notas(cliente_id, notas)
    AuditoriaController.registrar('editar', 'clientes', cliente_id, 
                                   detalles={'campo': 'notas'})
    return True, "Notas guardadas"
```

**4. Actualizar Vista (ui/clientes_view.py)**

```python
def _agregar_campo_notas(self):
    self.text_notas = QTextEdit()
    self.text_notas.setPlaceholderText("Notas adicionales")
    self.form_layout.addRow("Notas:", self.text_notas)

def _guardar_notas(self):
    cliente_id = self.cliente_actual_id
    notas = self.text_notas.toPlainText()
    exito, mensaje = ClienteController.guardar_notas(cliente_id, notas)
    # Mostrar resultado
```

### Convenciones de Código

```python
# Clases: PascalCase
class ClienteController:
    pass

# Funciones/métodos: snake_case
def calcular_total_mes(mes: int, año: int) -> float:
    pass

# Constantes: UPPER_SNAKE_CASE
MAX_INTENTOS_LOGIN = 5
TIEMPO_BLOQUEO_MINUTOS = 15

# Privados: prefijo _
def _metodo_interno(self):
    pass

# Type hints
def procesar_pago(monto: float, metodo: str) -> tuple[bool, str]:
    return True, "Pago procesado"
```

### Debugging

**VSCode launch.json:**

```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "GesMonth Debug",
            "type": "python",
            "request": "launch",
            "program": "${workspaceFolder}/main.py",
            "console": "integratedTerminal",
            "justMyCode": false
        }
    ]
}
```

**Logs en consola:**

```python
# En desarrollo
print(f"DEBUG: Cliente {cliente_id} actualizado")

# Producción (comentar antes de release)
```

**Inspeccionar BD:**

```bash
python scripts/ver_datos.py

# O directamente
sqlite3 .data/gesmonth.db
.tables
SELECT * FROM clientes;
```

---

## Testing

### Testing Manual

Crear checklist antes de release:

```
[ ] Login funciona con credenciales correctas
[ ] Login bloquea tras 5 intentos fallidos
[ ] Crear cliente con datos válidos
[ ] Crear cliente con documento duplicado (debe fallar)
[ ] Registrar pago completo → estado "pagado"
[ ] Registrar pago parcial → estado "con_deuda"
[ ] Marcar impago → inicio de mora
[ ] Dashboard muestra métricas correctas
[ ] Cambio de tema persiste entre sesiones
[ ] Respaldo de BD funciona
[ ] Eliminar cliente elimina cuotas en cascada
[ ] Solo superadmin ve gestión de usuarios
```

### Testing Automatizado (Futuro)

```python
# tests/test_cliente_controller.py
import unittest
from controllers.cliente_controller import ClienteController

class TestClienteController(unittest.TestCase):
    def test_crear_cliente_valido(self):
        datos = {
            'nombre': 'Test Cliente',
            'documento': '12345678',
            'telefono': '555-1234',
            'valor_cuota': 100,
            'dia_cobro': 15
        }
        exito, mensaje = ClienteController.crear_cliente(datos)
        self.assertTrue(exito)
    
    def test_crear_cliente_sin_nombre(self):
        datos = {'nombre': '', 'documento': '12345678'}
        exito, mensaje = ClienteController.crear_cliente(datos)
        self.assertFalse(exito)
```

---

## Compilación y Distribución

### Compilar Ejecutable

**Linux:**
```bash
./scripts/build.sh
# Output: dist/GesMonth/GesMonth
```

**Windows:**
```cmd
scripts\build.bat
# Output: dist\GesMonth\GesMonth.exe
```

### Crear Paquete Distribuible

```bash
./scripts/package.sh  # Linux
scripts\package.bat   # Windows

# Output: GesMonth-v2.1.0-[OS].zip/tar.gz
```

**Contenido del paquete:**
```
GesMonth-v2.1.0-Linux/
├── GesMonth/
│   ├── GesMonth              # Ejecutable
│   ├── assets/               # Recursos estáticos
│   ├── _internal/            # Librerías PyInstaller
│   ├── .data/                # BDs placeholder (vacías)
│   └── VERSION
├── README.txt
└── LICENSE.txt
```

Ver [BUILD.md](BUILD.md) para detalles.

---

## Contribuciones

### Proceso

1. **Fork** el repositorio
2. **Clone** tu fork localmente
3. **Crea rama**: `git checkout -b feature/nueva-funcionalidad`
4. **Desarrolla** siguiendo convenciones
5. **Prueba** exhaustivamente
6. **Commit**: `git commit -m "Agrega validación de emails"`
7. **Push**: `git push origin feature/nueva-funcionalidad`
8. **Pull Request** al repo original

### Checklist Pre-PR

- [ ] Código sigue PEP 8
- [ ] Todas las funciones tienen docstrings
- [ ] Type hints donde sea posible
- [ ] No hay código comentado innecesario
- [ ] No hay imports no utilizados
- [ ] Probado localmente sin errores
- [ ] README actualizado si es necesario
- [ ] CHANGELOG.md actualizado

### Áreas que Necesitan Contribución

- **Testing**: Agregar suite de tests automatizados
- **Exportación Excel**: Implementar reportes en openpyxl
- **Gráficos**: Dashboard con matplotlib/plotly
- **Notificaciones**: Email/WhatsApp para recordatorios
- **Multi-idioma**: i18n para Español/Inglés
- **Tema claro**: Completar QSS para modo light

---

## Recursos

**Documentación:**
- [Manual de Usuario](README-user.md)
- [Guía Técnica Completa](DESARROLLO.md)
- [Sistema de Autenticación](SISTEMA-AUTENTICACION.md)
- [Guía de Compilación](BUILD.md)

**Referencias Técnicas:**
- [PyQt6 Docs](https://www.riverbankcomputing.com/static/Docs/PyQt6/)
- [SQLite Docs](https://www.sqlite.org/docs.html)
- [PEP 8 Style Guide](https://pep8.org/)

**Contacto:**
- GitHub Issues: https://github.com/DIlanSG/GesMonth/issues
- Email: dilansg@gesmonth.com

---

**GesMonth v2.1.0** - Sistema de Gestión de Pagos Mensuales

Desarrollado por Dilan Acuña | Licencia: Source Available (SAL)

Última actualización: 26 de diciembre de 2025
