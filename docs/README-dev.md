# GesMonth - Guía Técnica Completa para Desarrolladores

## Índice
1. [Visión general y arquitectura](#visión-general-y-arquitectura)
2. [Stack tecnológico](#stack-tecnológico)
3. [Estructura del proyecto](#estructura-del-proyecto)
4. [Capas y patrones de diseño](#capas-y-patrones-de-diseño)
5. [Base de datos y modelos](#base-de-datos-y-modelos)
6. [Flujos de negocio detallados](#flujos-de-negocio-detallados)
7. [Guía de desarrollo](#guía-de-desarrollo)
8. [Testing y calidad](#testing-y-calidad)
9. [Despliegue y mantenimiento](#despliegue-y-mantenimiento)
10. [Mejores prácticas](#mejores-prácticas)

---

## Visión general y arquitectura

### Propósito del proyecto
GesMonth es una aplicación de escritorio diseñada para gestión de clientes y pagos recurrentes, orientada a pequeños negocios que necesitan:
- Control de membresías/cuotas mensuales
- Seguimiento de pagos y mora
- Reportería básica en Excel
- Persistencia local sin dependencias cloud

### Decisiones arquitectónicas clave

#### ¿Por qué aplicación de escritorio y no web?
1. **Privacidad**: Datos 100% locales, sin servidores ni riesgo de filtración
2. **Simplicidad**: No requiere servidor, hosting ni mantenimiento de infraestructura
3. **Velocidad**: Sin latencia de red; UI instantánea
4. **Autonomía**: Funciona sin internet
5. **Público objetivo**: Usuarios técnicos mínimos que prefieren instalar una vez y olvidarse

#### ¿Por qué Python + PyQt6?
- **Python**: Lenguaje de alto nivel, fácil mantenimiento, ecosistema rico (pandas, openpyxl)
- **PyQt6**: Framework GUI maduro, multiplataforma (Windows/Linux/Mac), widgets profesionales sin JavaScript/HTML
- **Alternativas descartadas**:
  - Electron: Pesado (>100MB), consume mucha RAM
  - Tkinter: Limitado visualmente, difícil hacer UIs modernas
  - Web local (Flask + webview): Complejidad innecesaria para este caso

#### ¿Por qué SQLite?
- **Embebido**: Archivo único, sin servidor DB aparte
- **Portable**: El `.db` se puede copiar/respaldar fácilmente
- **Suficiente**: Para <10k clientes y millones de pagos es rápido
- **ACID**: Transacciones seguras
- **Estándar**: SQL estándar, fácil migrar a Postgres/MySQL si crece

### Arquitectura en capas

```
┌─────────────────────────────────────────────┐
│             PRESENTATION LAYER              │
│  (PyQt6 Widgets - ui/*.py)                  │
│  - MainWindow (navegación sidebar)          │
│  - DashboardView, ClientesView, etc.        │
│  - Dialogs (formularios modales)            │
└─────────────────┬───────────────────────────┘
                  │ Eventos UI
                  ↓
┌─────────────────────────────────────────────┐
│            CONTROLLER LAYER                 │
│  (Business Logic - controllers/*.py)        │
│  - ClienteController (validaciones CRUD)    │
│  - PagoController (reglas de pago/cuotas)   │
│  - ReporteController (generación Excel)     │
│  - ConfigController (settings)              │
└─────────────────┬───────────────────────────┘
                  │ Llamadas a modelos
                  ↓
┌─────────────────────────────────────────────┐
│              MODEL LAYER                    │
│  (Data Access - database/models.py)         │
│  - Cliente (CRUD estático)                  │
│  - Pago, CuotaMensual, MetodoPago           │
│  - SQL queries directos (sin ORM)           │
└─────────────────┬───────────────────────────┘
                  │ Queries SQL
                  ↓
┌─────────────────────────────────────────────┐
│           DATA PERSISTENCE                  │
│  (SQLite - database/connection.py)          │
│  - DatabaseConnection (Singleton)           │
│  - gesmonth.db (archivo único)              │
└─────────────────────────────────────────────┘
```

**Flujo de datos típico:**
```
Usuario click → Vista captura evento → Controlador valida → 
Modelo ejecuta SQL → DB persiste → Modelo retorna resultado → 
Controlador procesa → Vista actualiza UI
```

---

## Stack tecnológico

### Dependencias core

#### 1. PyQt6 (6.7.1)
**Qué es**: Binding Python de Qt6, framework C++ para GUIs multiplataforma.

**Por qué se usa:**
- **Widgets nativos**: Botones, tablas, diálogos que se ven nativos en cada OS
- **QSS (Qt Style Sheets)**: Similar a CSS, permite estilizar sin tocar código
- **Señales y slots**: Patrón observer para eventos (click, cambio de texto, etc.)
- **Layouts avanzados**: QVBoxLayout, QHBoxLayout, QGridLayout para UIs responsivas
- **QTableWidget**: Tablas con sort, scroll, selección de filas integradas
- **QDialog**: Modales para formularios

**Cómo funciona en el proyecto:**
- `QApplication`: Loop de eventos, maneja toda la interacción
- `QMainWindow`: Ventana raíz con sidebar de navegación
- `QWidget`: Clase base de cada vista (Dashboard, Clientes, etc.)
- `QStackedWidget`: Cambia entre vistas sin crear ventanas nuevas
- `QLabel`, `QPushButton`, `QLineEdit`, etc.: Elementos UI

**Ejemplo de señal/slot:**
```python
btn_guardar = QPushButton("Guardar")
btn_guardar.clicked.connect(self._guardar_cliente)  # clicked es señal, _guardar_cliente es slot
```

#### 2. SQLite3 (built-in Python)
**Qué es**: Librería estándar de Python para SQLite, DB relacional embebida.

**Por qué se usa:**
- **Cero configuración**: No requiere instalar servidor
- **Transaccional**: ACID compliant
- **Portable**: Un archivo .db contiene todo
- **Rápido**: Para el volumen esperado (<1M registros)

**Cómo funciona:**
```python
conn = sqlite3.connect('gesmonth.db')  # Abre/crea archivo
conn.row_factory = sqlite3.Row  # Filas como dict-like
cursor = conn.cursor()
cursor.execute("SELECT * FROM clientes WHERE estado = ?", ('activo',))  # Prepared statements
rows = cursor.fetchall()
conn.commit()  # Persiste cambios
```

**Características usadas:**
- `PRAGMA foreign_keys = ON`: Habilita integridad referencial
- `ON DELETE CASCADE`: Eliminar cliente borra sus pagos automáticamente
- `UNIQUE` constraints: Evita documentos duplicados
- `INTEGER PRIMARY KEY AUTOINCREMENT`: IDs autoincrementales

#### 3. pandas (2.1.4)
**Qué es**: Librería de análisis de datos, especializada en DataFrames (tablas en memoria).

**Por qué se usa:**
- **Conversión rápida**: De lista de dicts a DataFrame en una línea
- **Exportación Excel**: Método `.to_excel()` integrado
- **Manipulación**: Fácil filtrar, ordenar, transformar datos antes de exportar

**Cómo funciona en el proyecto:**
```python
clientes = Cliente.obtener_todos()  # Lista de objetos Cliente
data = [{'Nombre': c.nombre, 'Documento': c.documento} for c in clientes]
df = pd.DataFrame(data)
df.to_excel('reporte.xlsx', index=False, sheet_name='Clientes')
```

**Alternativa descartada:**
- `csv.writer`: Requiere escribir CSV y luego convertir
- `xlsxwriter`: Más complejo, requiere escribir celda por celda

#### 4. openpyxl (3.1.2)
**Qué es**: Engine para leer/escribir archivos Excel (.xlsx).

**Por qué se usa:**
- pandas lo usa bajo el capó para `.to_excel()`
- Permite Excel moderno (no .xls viejo)

**Nota:** No se usa directamente, solo como dependencia de pandas.

---

## Estructura del proyecto

```
GesMonth/
├── main.py                          # Entrypoint, bootstrap de la app
├── requirements.txt                 # Dependencias pip
├── run.sh / run.bat                 # Scripts de ejecución
├── install.sh / install.bat         # Scripts de instalación
├── test.py                          # Suite de tests básicos
├── gesmonth.db                      # Base de datos (generado en runtime)
│
├── assets/                          # Recursos estáticos
│   └── styles/
│       └── main.qss                 # Estilos Qt (CSS-like)
│
├── database/                        # Capa de datos
│   ├── __init__.py
│   ├── connection.py                # Singleton de conexión SQLite
│   └── models.py                    # Modelos: Cliente, Pago, CuotaMensual, MetodoPago
│
├── controllers/                     # Capa de lógica de negocio
│   ├── __init__.py
│   ├── cliente_controller.py        # CRUD + validaciones de clientes
│   ├── pago_controller.py           # Lógica de pagos + sync cuotas
│   ├── reporte_controller.py        # Generación de reportes Excel
│   └── config_controller.py         # Configuración y respaldos
│
├── ui/                              # Capa de presentación
│   ├── __init__.py
│   ├── main_window.py               # Ventana principal (sidebar navigation)
│   ├── dashboard_view.py            # Vista de estadísticas
│   ├── clientes_view.py             # CRUD clientes (tabla + diálogos)
│   ├── pagos_view.py                # Historial pagos + registro
│   ├── cuotas_view.py               # Grid mensual por cliente
│   ├── reportes_view.py             # Botones de exportación
│   └── configuracion_view.py        # Settings (años, métodos pago, respaldo)
│
└── docs/                            # Documentación
    ├── README-user.md               # Manual de usuario
    └── README-dev.md                # Este archivo
```

### Convenciones de nombres
- **Archivos**: snake_case (ej: `cliente_controller.py`)
- **Clases**: PascalCase (ej: `ClienteController`)
- **Métodos/funciones**: snake_case (ej: `def crear_cliente()`)
- **Privados UI**: prefijo `_` (ej: `def _init_ui()`)
- **Constantes**: UPPER_SNAKE_CASE (no hay muchas en este proyecto)

---

## Capas y patrones de diseño

### 1. Patrón MVC adaptado (Model-View-Controller)

#### Model (database/models.py)
- **Responsabilidad**: Acceso a datos, SQL queries, mappeo objeto-relacional manual
- **Patrón usado**: Active Record simplificado (métodos estáticos en lugar de instancia)
- **Sin ORM**: Se evitó SQLAlchemy/Peewee para simplicidad; queries SQL directos

**Ejemplo:**
```python
class Cliente:
    @staticmethod
    def crear(nombre: str, documento: str, ...) -> int:
        cursor.execute("INSERT INTO clientes (...) VALUES (...)", (...))
        return cursor.lastrowid
    
    @staticmethod
    def obtener_todos() -> List['Cliente']:
        cursor.execute("SELECT * FROM clientes")
        return [Cliente(id=row['id'], ...) for row in cursor.fetchall()]
```

**Ventajas:**
- Sin magic: Lo que ves es lo que ejecuta
- Performance predecible
- Fácil debug de queries

**Desventajas:**
- Más código boilerplate
- SQL vulnerabilities si no usas prepared statements (mitigado con `?` placeholders)

#### View (ui/*.py)
- **Responsabilidad**: Renderizar widgets, capturar eventos, mostrar datos
- **Patrón usado**: Passive View (no tiene lógica de negocio, solo UI)
- **Widgets modulares**: Cada vista es un `QWidget` independiente

**Ejemplo de vista:**
```python
class ClientesView(QWidget):
    def __init__(self):
        self.controller = ClienteController()
        self._init_ui()  # Crea widgets
    
    def _init_ui(self):
        # Layout, botones, tabla
        self.btn_add.clicked.connect(self._show_add_dialog)
    
    def _show_add_dialog(self):
        dialog = ClienteDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            data = dialog.get_data()
            if self.controller.crear_cliente(**data):
                self.refresh_data()
```

#### Controller (controllers/*.py)
- **Responsabilidad**: Validaciones, orquestación de modelos, reglas de negocio
- **Patrón usado**: Thin Controllers (delegan en modelos)

**Ejemplo:**
```python
class ClienteController:
    def crear_cliente(self, nombre: str, documento: str, ...) -> bool:
        # Validaciones
        if not nombre.strip():
            return False
        
        try:
            cliente_id = Cliente.crear(nombre, documento, ...)
            return cliente_id > 0
        except Exception as e:
            print(f"Error: {e}")
            return False
```

### 2. Patrón Singleton (database/connection.py)
**Por qué:** SQLite recomienda una conexión por aplicación; múltiples conexiones pueden causar locks.

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
            self._connection = sqlite3.connect('gesmonth.db')
```

**Ventaja:** `DatabaseConnection()` siempre retorna la misma instancia.

### 3. Patrón Factory implícito (en vistas)
Cada vista se instancia en `MainWindow` y se agrega al `QStackedWidget`:

```python
self.dashboard_view = DashboardView()
self.clientes_view = ClientesView()
self.stacked_widget.addWidget(self.dashboard_view)
self.stacked_widget.addWidget(self.clientes_view)
```

### 4. Separation of Concerns
- **UI**: Solo sabe mostrar/capturar, llama a controladores
- **Controllers**: Solo validan/orquestan, llaman a modelos
- **Models**: Solo acceso a datos, ejecutan SQL

**Anti-pattern evitado:** No hay SQL en vistas ni lógica de negocio en modelos.

---

## Base de datos y modelos

### Esquema detallado

#### Tabla: `clientes`
```sql
CREATE TABLE clientes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    documento TEXT UNIQUE NOT NULL,
    telefono TEXT,
    estado TEXT DEFAULT 'activo',
    valor_cuota REAL DEFAULT 0.0
);
```

**Índices automáticos:**
- PK en `id`
- UNIQUE en `documento` (crea índice implícito)

**Reglas:**
- `documento` UNIQUE: Evita duplicados
- `estado`: 'activo' o 'inactivo' (no validado en DB, solo en app)
- `valor_cuota`: Puede ser 0 (clientes sin cuota)

#### Tabla: `pagos`
```sql
CREATE TABLE pagos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cliente_id INTEGER NOT NULL,
    fecha_pago DATE NOT NULL,
    mes_correspondiente TEXT NOT NULL,
    monto REAL NOT NULL,
    metodo_pago TEXT,
    FOREIGN KEY (cliente_id) REFERENCES clientes(id) ON DELETE CASCADE
);
```

**FK con CASCADE:** Si eliminas un cliente, sus pagos se borran automáticamente.

**Campos clave:**
- `fecha_pago`: Cuándo realmente pagó (puede ser distinto al mes que pagó)
- `mes_correspondiente`: YYYY-MM del mes que está pagando (ej: '2025-01' para enero)
- `metodo_pago`: Opcional (puede ser NULL)

#### Tabla: `cuotas_mensuales`
```sql
CREATE TABLE cuotas_mensuales (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cliente_id INTEGER NOT NULL,
    año INTEGER NOT NULL,
    mes INTEGER NOT NULL,
    estado TEXT DEFAULT 'pendiente',
    monto REAL NOT NULL,
    metodo_pago TEXT,
    fecha_registro DATE,
    FOREIGN KEY (cliente_id) REFERENCES clientes(id) ON DELETE CASCADE,
    UNIQUE(cliente_id, año, mes)
);
```

**UNIQUE compound key:** Un cliente no puede tener dos registros para el mismo año-mes.

**Estados:**
- `pendiente`: No hay info aún
- `pagado`: Cliente pagó
- `impago`: Cliente NO pagó (registrado explícitamente)

**Sincronización con `pagos`:** 
- Al crear un pago, `PagoController` también crea/actualiza la cuota correspondiente como 'pagado'

#### Tabla: `metodos_pago`
```sql
CREATE TABLE metodos_pago (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT UNIQUE NOT NULL,
    activo INTEGER DEFAULT 1
);
```

**Propósito:** Catálogo configurable de métodos (Efectivo, Transferencia, etc.)

**Campo `activo`:** SQLite no tiene BOOLEAN, usa INTEGER (0=false, 1=true)

#### Tabla: `configuracion`
```sql
CREATE TABLE configuracion (
    clave TEXT PRIMARY KEY,
    valor TEXT NOT NULL
);
```

**Patrón Key-Value:** Almacena settings app.

**Ejemplo:**
```sql
INSERT INTO configuracion (clave, valor) VALUES ('años_facturacion', '2025,2026');
```

### Modelos en código

#### Cliente
```python
class Cliente:
    def __init__(self, id, nombre, documento, telefono, estado, valor_cuota):
        self.id = id
        self.nombre = nombre
        # ...
    
    @staticmethod
    def crear(nombre, documento, telefono, estado, valor_cuota) -> int:
        # INSERT y retorna lastrowid
    
    @staticmethod
    def obtener_todos() -> List['Cliente']:
        # SELECT * y mapea a objetos
    
    @staticmethod
    def obtener_por_id(cliente_id) -> Optional['Cliente']:
        # SELECT WHERE id = ?
    
    @staticmethod
    def actualizar(cliente_id, ...) -> bool:
        # UPDATE retorna rowcount > 0
    
    @staticmethod
    def eliminar(cliente_id) -> bool:
        # DELETE (cascade eliminará pagos/cuotas)
    
    @staticmethod
    def buscar(termino) -> List['Cliente']:
        # SELECT WHERE nombre LIKE ? OR documento LIKE ?
```

**Pattern:** Todos los métodos son estáticos porque no necesitamos instancia para operar.

#### Pago
Similar a Cliente, con método adicional:

```python
@staticmethod
def obtener_estadisticas() -> Dict[str, Any]:
    # Calcula total mes actual, clientes activos, pagaron, mora
    # Usa queries agregadas (SUM, COUNT)
```

#### CuotaMensual
```python
@staticmethod
def registrar_pago(cliente_id, año, mes, monto, metodo_pago) -> int:
    # INSERT OR REPLACE (UPSERT)
    # Marca cuota como 'pagado'

@staticmethod
def registrar_impago(cliente_id, año, mes, monto) -> int:
    # Marca cuota como 'impago'

@staticmethod
def obtener_cuota(cliente_id, año, mes) -> Optional['CuotaMensual']:
    # SELECT WHERE cliente_id, año, mes

@staticmethod
def calcular_deuda_acumulada(cliente_id, hasta_año, hasta_mes) -> float:
    # SUM de cuotas con estado='impago'
```

---

## Flujos de negocio detallados

### Flujo 1: Registrar un pago

**Actor:** Usuario desde vista Pagos

**Diagrama:**
```
[Usuario] → [PagosView] → [PagoDialog] → [PagoController] → [Pago + CuotaMensual]
                                                              ↓
                                                         [Database]
```

**Pasos detallados:**

1. Usuario hace click en "Registrar Pago"
2. `PagosView._show_add_dialog()` abre `PagoDialog`
3. Usuario completa formulario:
   - Cliente (combo desplegable cargado desde `Cliente.obtener_todos()`)
   - Fecha pago (QDateEdit, default=hoy)
   - Mes correspondiente (QLineEdit, format YYYY-MM)
   - Monto (QLineEdit, puede sobrescribir cuota)
4. Usuario hace click "Guardar"
5. `PagoDialog._validate_and_accept()` valida campos no vacíos
6. `PagoDialog.get_data()` retorna dict con datos
7. `PagosView` llama `self.controller.registrar_pago(**data)`
8. `PagoController.registrar_pago()`:
   - Valida cliente existe (`Cliente.obtener_por_id()`)
   - Valida fecha (formato YYYY-MM-DD)
   - Valida mes (formato YYYY-MM)
   - Valida monto > 0
   - Llama `Pago.crear()` → INSERT en `pagos`
   - Parsea `mes_correspondiente` a año/mes
   - Llama `CuotaMensual.registrar_pago()` → INSERT OR REPLACE en `cuotas_mensuales` con estado='pagado'
   - Retorna True si ambos inserts OK
9. Si retorna True:
   - `PagosView` muestra mensaje "Pago registrado"
   - `PagosView.refresh_data()` recarga tabla
10. Dashboard se actualiza en próximo acceso (lazy refresh)

**Código simplificado:**
```python
# PagoController
def registrar_pago(self, cliente_id, fecha_pago, mes_correspondiente, monto):
    if not self._validar_cliente_existe(cliente_id):
        return False
    
    pago_id = Pago.crear(cliente_id, fecha_pago, mes_correspondiente, monto)
    
    if pago_id > 0:
        periodo = datetime.strptime(mes_correspondiente, '%Y-%m')
        CuotaMensual.registrar_pago(cliente_id, periodo.year, periodo.month, monto, "Pago registrado")
    
    return pago_id > 0
```

**Transaccionalidad:** 
- Si `Pago.crear()` falla, no se llama `CuotaMensual.registrar_pago()`
- Si `CuotaMensual` falla, el pago ya está registrado (inconsistencia)
- **Mejora futura:** Usar transacciones explícitas con BEGIN/COMMIT

---

### Flujo 2: Marcar cuota como pagada/impaga desde Cuotas

**Actor:** Usuario desde vista Cuotas

**Diagrama:**
```
[Usuario click celda mes] → [CuotasView] → [RegistroCuotaDialog] → [CuotaMensual + MetodoPago]
                                                                      ↓
                                                                 [Database]
```

**Pasos detallados:**

1. Usuario busca cliente en Cuotas (opcional, usa barra búsqueda)
2. `CuotasView` muestra tarjetas de clientes con grids de meses
3. Usuario hace click en celda de un mes
4. `CuotasView._on_celda_click()` verifica si ya hay cuota registrada:
   - Si existe: Pregunta si desea eliminarla (para corregir errores)
   - Si no existe: Abre `RegistroCuotaDialog`
5. Dialog muestra mes, año, monto (cuota del cliente) y dos botones:
   - "Registrar Pago"
   - "Registrar Impago"
6. **Si elige "Registrar Pago":**
   - Abre `MetodoPagoSeleccionDialog` con lista de métodos activos (`MetodoPago.obtener_todos()`)
   - Usuario elige método (ej: Efectivo)
   - Llama `CuotaMensual.registrar_pago(cliente_id, año, mes, monto, metodo)`
   - INSERT OR REPLACE con estado='pagado'
7. **Si elige "Registrar Impago":**
   - Pide confirmación (QMessageBox)
   - Llama `CuotaMensual.registrar_impago(cliente_id, año, mes, monto)`
   - INSERT OR REPLACE con estado='impago'
8. Dialog se cierra con `accept()`
9. `CuotasView._mostrar_clientes()` redibuja grid (celda cambia de color)

**Código grid de meses:**
```python
def _crear_celda_mes(self, cliente, año, mes, nombre_mes):
    cuota = CuotaMensual.obtener_cuota(cliente.id, año, mes)
    
    if cuota:
        if cuota.estado == 'pagado':
            color = verde
            texto = "Pagado"
        else:
            color = rojo
            texto = "Impago"
    else:
        color = gris
        texto = "Pendiente"
    
    frame = QFrame()
    frame.setStyleSheet(f"background: {color}")
    label = QLabel(texto)
    # ...
    frame.mousePressEvent = lambda e: self._on_celda_click(cliente, año, mes, cuota)
```

---

### Flujo 3: Exportar reporte a Excel

**Actor:** Usuario desde vista Reportes

**Diagrama:**
```
[Usuario] → [ReportesView] → [ReporteController] → [Modelo] → [pandas] → [Excel file]
```

**Pasos detallados:**

1. Usuario hace click en botón (ej: "Exportar Lista de Clientes")
2. `ReportesView._export_clientes()` abre `QFileDialog.getSaveFileName()`
3. Usuario elige ubicación y nombre (ej: `clientes_2025.xlsx`)
4. Llama `self.controller.exportar_clientes(file_path)`
5. `ReporteController.exportar_clientes()`:
   - Obtiene todos los clientes (`Cliente.obtener_todos()`)
   - Mapea a lista de dicts:
     ```python
     data = [{'ID': c.id, 'Nombre': c.nombre, ...} for c in clientes]
     ```
   - Crea DataFrame: `df = pd.DataFrame(data)`
   - Exporta: `df.to_excel(file_path, index=False, sheet_name='Clientes')`
   - Retorna True si no hay excepción
6. Si retorna True: Muestra mensaje "Reporte guardado en: {file_path}"
7. Usuario puede abrir el Excel con su app preferida

**Ejemplo de Excel generado:**
```
| ID | Nombre        | Documento | Teléfono  | Cuota Mensual | Estado |
|----|---------------|-----------|-----------|---------------|--------|
| 1  | Juan Pérez    | 12345678  | 555-1234  | 1500.00       | activo |
| 2  | María García  | 87654321  | 555-9876  | 1800.00       | activo |
```

**Alternativa para CSV:**
```python
df.to_csv('clientes.csv', index=False)
```

---

### Flujo 4: Respaldo de base de datos

**Actor:** Usuario desde Configuración

**Diagrama:**
```
[Usuario] → [ConfiguracionView] → [ConfigController] → [shutil.copy2] → [backup_*.db]
```

**Pasos detallados:**

1. Usuario hace click "Crear Respaldo de Base de Datos"
2. `ConfiguracionView._create_backup()` llama `self.config_controller.create_backup()`
3. `ConfigController.create_backup()`:
   - Obtiene ruta del DB: `db_path = self.db.get_db_path()` (ej: `/ruta/gesmonth.db`)
   - Genera nombre con timestamp: `backup_database_20251223_143052.db`
   - Usa `shutil.copy2(db_path, backup_path)` (copia con metadata)
   - Retorna `backup_path`
4. Muestra mensaje: "Respaldo creado: backup_database_20251223_143052.db"

**Restauración (manual):**
```bash
# 1. Cerrar app
# 2. Renombrar actual
mv gesmonth.db gesmonth_old.db
# 3. Copiar respaldo
cp backup_database_20251223_143052.db gesmonth.db
# 4. Abrir app
```

**Mejora futura:** Botón "Restaurar desde respaldo" con selector de archivos.

---

## Guía de desarrollo

### Setup entorno de desarrollo

```bash
# 1. Clonar/descargar proyecto
cd GesMonth

# 2. Crear virtualenv (opcional pero recomendado)
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Instalar herramientas dev (opcional)
pip install black flake8 mypy

# 5. Ejecutar
python main.py
```

### Agregar un nuevo campo a Cliente

**Ejemplo:** Agregar campo `email`

**Paso 1: Modificar esquema DB**
```python
# database/connection.py
def _create_tables(self):
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS clientes (
            ...
            email TEXT,  # <-- AGREGAR
            valor_cuota REAL DEFAULT 0.0
        )
    ''')
```

**Paso 2: Actualizar modelo**
```python
# database/models.py
class Cliente:
    def __init__(self, id, nombre, documento, telefono, email, estado, valor_cuota):
        self.email = email  # <-- AGREGAR
    
    @staticmethod
    def crear(nombre, documento, telefono, email, estado, valor_cuota):
        cursor.execute('''
            INSERT INTO clientes (nombre, documento, telefono, email, estado, valor_cuota)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (nombre, documento, telefono, email, estado, valor_cuota))
```

**Paso 3: Actualizar controlador**
```python
# controllers/cliente_controller.py
def crear_cliente(self, nombre, documento, telefono, email, valor_cuota, estado):
    cliente_id = Cliente.crear(nombre, documento, telefono, email, valor_cuota, estado)
```

**Paso 4: Actualizar vista**
```python
# ui/clientes_view.py - ClienteDialog
self.input_email = QLineEdit()
layout.addRow("Email:", self.input_email)

def get_data(self):
    return {
        'nombre': self.input_nombre.text(),
        'email': self.input_email.text(),  # <-- AGREGAR
        # ...
    }
```

**Paso 5: Migrar DB existente**
```sql
-- Ejecutar manualmente o crear script de migración
ALTER TABLE clientes ADD COLUMN email TEXT;
```

**Nota:** SQLite no soporta DROP COLUMN; para eliminar campos hay que recrear tabla.

### Crear nueva vista

**Ejemplo:** Vista de "Estadísticas Avanzadas"

**Paso 1: Crear archivo**
```python
# ui/estadisticas_view.py
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel

class EstadisticasView(QWidget):
    def __init__(self):
        super().__init__()
        self._init_ui()
    
    def _init_ui(self):
        layout = QVBoxLayout(self)
        title = QLabel("Estadísticas Avanzadas")
        title.setObjectName("pageTitle")
        layout.addWidget(title)
        # ... más widgets
    
    def refresh_data(self):
        # Cargar datos
        pass
```

**Paso 2: Registrar en MainWindow**
```python
# ui/main_window.py
from .estadisticas_view import EstadisticasView

class MainWindow(QMainWindow):
    def __init__(self):
        # ...
        self.estadisticas_view = EstadisticasView()
        self.stacked_widget.addWidget(self.estadisticas_view)
        
        nav_items = [
            # ...
            ("Estadísticas", 5),  # índice 5
        ]
```

**Paso 3: Conectar navegación**
```python
# Ya funciona con el loop existente en _create_sidebar
```

### Debugging

#### Logs
- Prints van a terminal (captura stdout si ejecutas `python main.py`)
- Para logs persistentes, usar `logging`:
  ```python
  import logging
  logging.basicConfig(filename='gesmonth.log', level=logging.DEBUG)
  logging.debug("Cliente creado: %s", cliente_id)
  ```

#### Queries SQL
```python
# En models.py, antes de execute
print(f"SQL: {query}")
print(f"Params: {params}")
```

#### UI con Qt Designer (opcional)
- Puedes diseñar UIs en Qt Designer (.ui files)
- Convertir con `pyuic6`: `pyuic6 -x file.ui -o file.py`
- Este proyecto usa código puro (sin .ui) para evitar paso extra

---

## Testing y calidad

### Suite de tests actual (`test.py`)

**Cobertura:**
- Test de conexión DB
- CRUD de Cliente
- CRUD de Pago
- Controladores (Cliente, Pago)

**Ejecutar:**
```bash
python test.py
```

**Salida esperada:**
```
==================================================
PRUEBAS DE FUNCIONALIDAD - GesMonth
==================================================
Probando conexión a la base de datos...
Tablas creadas correctamente

Probando operaciones con clientes...
  Cliente creado con ID: 1
  ...
==================================================
TODAS LAS PRUEBAS PASARON EXITOSAMENTE
==================================================
```

### Mejoras de testing sugeridas

#### 1. Usar pytest
```bash
pip install pytest
```

```python
# tests/test_cliente.py
import pytest
from database.models import Cliente

def test_crear_cliente():
    cliente_id = Cliente.crear("Test", "12345678", "", "activo", 1000)
    assert cliente_id > 0
    Cliente.eliminar(cliente_id)

def test_documento_duplicado():
    Cliente.crear("Test1", "99999999", "", "activo", 1000)
    with pytest.raises(Exception):  # sqlite3.IntegrityError
        Cliente.crear("Test2", "99999999", "", "activo", 1000)
```

#### 2. Tests de UI (QTest)
```python
from PyQt6.QtTest import QTest
from PyQt6.QtCore import Qt

def test_cliente_dialog():
    app = QApplication([])
    dialog = ClienteDialog()
    dialog.input_nombre.setText("Test")
    dialog.input_documento.setText("12345678")
    
    # Simular click en guardar
    QTest.mouseClick(dialog.btn_save, Qt.MouseButton.LeftButton)
    
    assert dialog.result() == QDialog.DialogCode.Accepted
```

#### 3. Cobertura de código
```bash
pip install coverage
coverage run -m pytest
coverage report
coverage html  # Genera reporte HTML
```

### Validaciones y linting

#### Black (formateo)
```bash
pip install black
black .
```

#### Flake8 (linting)
```bash
pip install flake8
flake8 --max-line-length 120 .
```

#### Mypy (type checking)
```bash
pip install mypy
mypy --ignore-missing-imports .
```

**Nota:** Código actual no usa type hints extensivos; agregar gradualmente.

---

## Despliegue y mantenimiento

### Empaquetar como ejecutable (PyInstaller)

```bash
pip install pyinstaller

# Linux/Mac
pyinstaller --onefile --windowed \
    --add-data "assets:assets" \
    --name GesMonth \
    main.py

# Windows
pyinstaller --onefile --windowed ^
    --add-data "assets;assets" ^
    --name GesMonth ^
    --icon=assets/icon.ico ^
    main.py
```

**Resultado:** Ejecutable standalone en `dist/GesMonth` (o `.exe` en Windows)

**Ventaja:** Usuario no necesita Python instalado.

**Desventaja:** Binario grande (~50-100MB con PyQt6).

### Versionado

**Convención:** Semantic Versioning (MAJOR.MINOR.PATCH)
- v1.0.0: Release inicial
- v1.0.1: Bugfix
- v1.1.0: Nueva feature
- v2.0.0: Breaking change

**Actualizar:**
- `main.py`: Agregar `__version__ = "1.0.0"`
- `ui/configuracion_view.py`: Mostrar versión en info de app

### Migraciones de DB

**Problema:** Nuevas versiones pueden requerir cambios en schema.

**Solución:**
1. Guardar versión de schema en `configuracion`:
   ```sql
   INSERT INTO configuracion (clave, valor) VALUES ('db_version', '1');
   ```

2. Al arrancar app, verificar versión:
   ```python
   def _migrate_db(self):
       cursor.execute("SELECT valor FROM configuracion WHERE clave='db_version'")
       version = int(cursor.fetchone()['valor'])
       
       if version < 2:
           # Migración de v1 a v2
           cursor.execute("ALTER TABLE clientes ADD COLUMN email TEXT")
           cursor.execute("UPDATE configuracion SET valor='2' WHERE clave='db_version'")
   ```

3. Llamar `_migrate_db()` después de `_create_tables()` en `DatabaseConnection.__init__`

### Distribución

**Opción 1: Repositorio Git**
- GitHub/GitLab: Usuarios clonan y ejecutan
- Release con binarios en GitHub Releases

**Opción 2: Instalador**
- Windows: Inno Setup (crea .exe instalador)
- Mac: `py2app` (crea .app)
- Linux: `.deb` / `.rpm` packages

---

## Mejores prácticas

### 1. Seguridad

#### Prevenir SQL Injection
**Bien:**
```python
cursor.execute("SELECT * FROM clientes WHERE documento = ?", (documento,))
```

**Mal:**
```python
cursor.execute(f"SELECT * FROM clientes WHERE documento = '{documento}'")  # VULNERABLE
```

#### Validación de entrada
```python
def crear_cliente(self, nombre, documento, ...):
    if not nombre.strip():
        raise ValueError("Nombre obligatorio")
    
    if not re.match(r'^\d{7,9}$', documento):
        raise ValueError("Documento inválido")
```

### 2. Performance

#### Lazy loading de vistas
```python
# En MainWindow
def _change_view(self, index):
    self.stacked_widget.setCurrentIndex(index)
    
    # Refrescar solo la vista actual
    if index == 0:
        self.dashboard_view.refresh_data()
```

#### Índices en DB
```sql
-- Si las búsquedas por nombre son frecuentes
CREATE INDEX idx_clientes_nombre ON clientes(nombre);
```

#### Paginación en tablas grandes
```python
# Si hay >1000 clientes, implementar:
def obtener_todos_paginado(offset: int, limit: int):
    cursor.execute("SELECT * FROM clientes LIMIT ? OFFSET ?", (limit, offset))
```

### 3. UX

#### Feedback visual
```python
# Mientras se carga
QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)
# ... operación larga
QApplication.restoreOverrideCursor()
```

#### Confirmaciones
```python
reply = QMessageBox.question(
    self, "Confirmar", "¿Eliminar cliente?",
    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
)
if reply == QMessageBox.StandardButton.Yes:
    # eliminar
```

### 4. Mantenibilidad

#### Docstrings
```python
def crear_cliente(self, nombre: str, documento: str, ...) -> bool:
    """
    Crea un nuevo cliente con validaciones.
    
    Args:
        nombre: Nombre completo del cliente
        documento: DNI/CI único
        ...
    
    Returns:
        True si se creó exitosamente, False si falló validación
    
    Raises:
        ValueError: Si el documento ya existe
    """
```

#### Constantes
```python
# config.py
ESTADOS_CLIENTE = ['activo', 'inactivo']
ESTADOS_CUOTA = ['pendiente', 'pagado', 'impago']

# Usar en validaciones
if estado not in ESTADOS_CLIENTE:
    raise ValueError(f"Estado inválido: {estado}")
```

#### Separación de concerns en UI
```python
# Mal: lógica mezclada con UI
def _on_save(self):
    nombre = self.input_nombre.text()
    cursor.execute("INSERT INTO clientes ...")  # SQL en UI!

# Bien: delegar a controlador
def _on_save(self):
    nombre = self.input_nombre.text()
    self.controller.crear_cliente(nombre, ...)
```

---

## Roadmap y extensiones futuras

### Corto plazo (v1.1)
- [ ] Búsqueda avanzada (filtros por estado, rango de cuotas)
- [ ] Exportar configuración (métodos de pago, años) a JSON
- [ ] Notificaciones/alertas de clientes en mora
- [ ] Gráficos (matplotlib) en Dashboard

### Mediano plazo (v2.0)
- [ ] Multi-usuario con login (tabla `usuarios` + bcrypt)
- [ ] Auditoría (tabla `logs` con acciones y timestamps)
- [ ] Importar clientes desde CSV/Excel
- [ ] API REST (Flask) para acceso desde mobile
- [ ] Sincronización cloud (opcional, con cifrado)

### Largo plazo (v3.0)
- [ ] Migración a Postgres (para >10k clientes)
- [ ] Versión web (Vue.js + FastAPI)
- [ ] App móvil (Kivy o React Native)
- [ ] Recordatorios automáticos por email/SMS

---

## Recursos adicionales

### Documentación oficial
- PyQt6: https://doc.qt.io/qtforpython-6/
- SQLite: https://www.sqlite.org/docs.html
- pandas: https://pandas.pydata.org/docs/
- Python: https://docs.python.org/3/

### Libros recomendados
- "Rapid GUI Programming with Python and Qt" - Mark Summerfield
- "Python GUI Programming with Tkinter" (conceptos aplicables a PyQt)

### Comunidades
- Stack Overflow: [pyqt6] tag
- Reddit: r/learnpython, r/PyQt

---

## Changelog

### v1.0.0 (Diciembre 2025)
- Release inicial
- CRUD completo de clientes
- Registro de pagos y cuotas
- Exportación de reportes a Excel
- Dashboard con estadísticas
- Configuración de años y métodos de pago
- Respaldo de base de datos

---

## Licencia
Este proyecto es privado y propietario. Todos los derechos reservados.

---

## Contacto
- Desarrollador: Dilan Acuña
- Email: [garaydilan2002@gmail.com]
- GitHub: [DilanSG]

---

**Última actualización:** 23 de diciembre de 2025
