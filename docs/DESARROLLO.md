# Guía de Desarrollo - GesMonth

Esta guía está diseñada para desarrolladores que desean contribuir, modificar o extender GesMonth.

## Tabla de Contenidos

1. [Requisitos del Sistema](#requisitos-del-sistema)
2. [Configuración del Entorno](#configuración-del-entorno)
3. [Arquitectura del Proyecto](#arquitectura-del-proyecto)
4. [Estructura de Archivos](#estructura-de-archivos)
5. [Patrones de Diseño](#patrones-de-diseño)
6. [Base de Datos](#base-de-datos)
7. [Flujo de Trabajo](#flujo-de-trabajo)
8. [Testing y Depuración](#testing-y-depuración)
9. [Compilación](#compilación)
10. [Contribuciones](#contribuciones)

## Requisitos del Sistema

### Software Necesario
- Python 3.8 o superior
- pip (gestor de paquetes de Python)
- Git (para control de versiones)
- Editor de código (recomendado: VSCode, PyCharm)

### Sistema Operativo
- Windows 10/11
- Linux (Ubuntu 20.04+, Fedora 35+, Arch)
- macOS 11+ (Big Sur o superior)

## Configuración del Entorno

### 1. Clonar el Repositorio

```bash
git clone https://github.com/DIlanSG/GesMonth.git
cd GesMonth
```

### 2. Crear Entorno Virtual

**Windows:**
```cmd
python -m venv venv
venv\Scripts\activate
```

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar Dependencias

```bash
pip install -r requirements.txt
```

### 4. Ejecutar en Modo Desarrollo

```bash
# Windows
python main.py

# Linux/Mac
python3 main.py
```

## Arquitectura del Proyecto

GesMonth sigue el patrón **MVC (Modelo-Vista-Controlador)** con las siguientes capas:

### Capa de Datos (Model)
- **Ubicación:** `database/`
- **Responsabilidad:** Gestión de conexiones, esquemas y modelos de datos
- **Componentes:**
  - `connection.py`: Singleton para conexión a gesmonth.db
  - `user_connection.py`: Singleton para conexión a users.db
  - `models.py`: Clases de modelos con métodos CRUD
  - `user_models.py`: Modelos de autenticación

### Capa de Vista (View)
- **Ubicación:** `ui/`
- **Responsabilidad:** Interfaces gráficas y presentación
- **Componentes:**
  - `main_window.py`: Ventana principal con sidebar
  - `login_view.py`: Pantalla de autenticación
  - `dashboard_view.py`: Dashboard con métricas
  - `clientes_view.py`: Gestión de clientes
  - `cuotas_view.py`: Control de cuotas mensuales
  - `pagos_view.py`: Registro de pagos
  - `reportes_view.py`: Estadísticas y reportes
  - `configuracion_view.py`: Panel de configuración
  - `usuarios_management.py`: Gestión de usuarios

### Capa de Controlador (Controller)
- **Ubicación:** `controllers/`
- **Responsabilidad:** Lógica de negocio
- **Componentes:**
  - `auth_controller.py`: Autenticación y autorización
  - `cliente_controller.py`: Lógica de clientes
  - `pago_controller.py`: Lógica de pagos
  - `reporte_controller.py`: Generación de reportes
  - `config_controller.py`: Configuración de la aplicación
  - `theme_controller.py`: Gestión de temas

### Capa de Utilidades
- **Ubicación:** `utils/`
- **Responsabilidad:** Funciones auxiliares
- **Componentes:**
  - `get_resource_path()`: Resolución de rutas para recursos
  - `get_data_path()`: Resolución de rutas para datos persistentes

## Estructura de Archivos

```
GesMonth/
├── main.py                      # Punto de entrada principal
├── VERSION                      # Versión actual (2.1.0)
├── LICENSE                      # Licencia SAL
├── requirements.txt             # Dependencias Python
├── gesmonth.spec               # Configuración PyInstaller
│
├── database/                    # Capa de datos
│   ├── __init__.py
│   ├── connection.py           # Conexión principal (gesmonth.db)
│   ├── user_connection.py      # Conexión de usuarios (users.db)
│   ├── models.py               # Modelos de negocio
│   └── user_models.py          # Modelos de autenticación
│
├── ui/                         # Capa de vista
│   ├── __init__.py
│   ├── main_window.py          # Ventana principal
│   ├── login_view.py           # Pantalla de login
│   ├── splash_screen.py        # Splash screen
│   ├── dashboard_view.py       # Dashboard
│   ├── clientes_view.py        # CRUD clientes
│   ├── cuotas_view.py          # Control cuotas
│   ├── pagos_view.py           # Registro pagos
│   ├── reportes_view.py        # Reportes
│   ├── configuracion_view.py   # Configuración
│   ├── usuarios_management.py  # Gestión usuarios
│   ├── theme_colors.py         # Paleta de colores
│   └── detalles_cuota_dialog.py  # Dialog de detalles
│
├── controllers/                # Capa de controlador
│   ├── __init__.py
│   ├── auth_controller.py      # Autenticación
│   ├── cliente_controller.py   # Lógica clientes
│   ├── pago_controller.py      # Lógica pagos
│   ├── reporte_controller.py   # Lógica reportes
│   ├── config_controller.py    # Configuración
│   └── theme_controller.py     # Temas
│
├── utils/                      # Utilidades
│   ├── __init__.py
│   └── (funciones auxiliares)
│
├── assets/                     # Recursos estáticos
│   ├── icons/                  # Iconos SVG
│   │   ├── home.svg
│   │   ├── cuotas.svg
│   │   ├── clientes.svg
│   │   ├── reportes.svg
│   │   ├── settings.svg
│   │   ├── logout-session.svg
│   │   └── power-off.svg
│   └── styles/                 # Hojas de estilo
│       ├── dark.qss
│       └── light.qss
│
├── scripts/                    # Scripts de automatización
│   ├── build.sh / build.bat    # Compilación
│   ├── install.sh / install.bat # Instalación
│   ├── run.sh / run.bat        # Ejecución
│   ├── package.sh / package.bat # Empaquetado
│   └── ver_datos.py            # Inspección de BD
│
├── docs/                       # Documentación
│   ├── BUILD.md                # Guía de compilación
│   ├── DESARROLLO.md           # Esta guía
│   ├── DISTRIBUCION.md         # Guía de distribución
│   └── SISTEMA-AUTENTICACION.md # Doc. autenticación
│
└── .data/                      # Datos persistentes (no en repo)
    ├── gesmonth.db             # Base de datos principal
    └── users.db                # Base de datos de usuarios
```

## Patrones de Diseño

### Singleton
Usado en las conexiones de base de datos para garantizar una única instancia:

```python
class DatabaseConnection:
    _instance = None
    _connection = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
```

### Active Record
Los modelos contienen métodos CRUD estáticos:

```python
class Cliente:
    @staticmethod
    def crear(nombre, documento, telefono, valor_cuota, dia_cobro):
        # Lógica de creación
        pass
    
    @staticmethod
    def obtener_todos():
        # Lógica de lectura
        pass
```

### Observer
Usado en las vistas para reaccionar a cambios:

```python
# Vista registra eventos
btn_guardar.clicked.connect(self._guardar_cliente)

# Controlador notifica cambios
self._cargar_clientes()  # Recarga la lista
```

## Base de Datos

### Esquema Principal (gesmonth.db)

**Tabla: clientes**
```sql
CREATE TABLE clientes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    documento TEXT UNIQUE NOT NULL,
    telefono TEXT,
    estado TEXT DEFAULT 'activo',
    valor_cuota REAL NOT NULL,
    dia_cobro INTEGER NOT NULL CHECK(dia_cobro BETWEEN 1 AND 31)
);
```

**Tabla: cuotas_mensuales**
```sql
CREATE TABLE cuotas_mensuales (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cliente_id INTEGER NOT NULL,
    año INTEGER NOT NULL,
    mes INTEGER NOT NULL CHECK(mes BETWEEN 1 AND 12),
    monto REAL NOT NULL,
    estado TEXT DEFAULT 'pendiente',
    metodo_pago TEXT,
    fecha_pago DATE,
    deuda_acumulada REAL DEFAULT 0,
    fecha_inicio_mora DATE,
    FOREIGN KEY (cliente_id) REFERENCES clientes(id) ON DELETE CASCADE,
    UNIQUE(cliente_id, año, mes)
);
```

**Tabla: pagos**
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

**Tabla: metodos_pago**
```sql
CREATE TABLE metodos_pago (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT UNIQUE NOT NULL,
    activo INTEGER DEFAULT 1
);
```

**Tabla: configuracion**
```sql
CREATE TABLE configuracion (
    clave TEXT PRIMARY KEY,
    valor TEXT
);
```

### Esquema de Usuarios (users.db)

**Tabla: usuarios**
```sql
CREATE TABLE usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    rol TEXT NOT NULL CHECK(rol IN ('superadmin', 'admin', 'operador', 'solo_lectura')),
    activo INTEGER DEFAULT 1,
    intentos_fallidos INTEGER DEFAULT 0,
    bloqueado_hasta TIMESTAMP,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Tabla: sesiones**
```sql
CREATE TABLE sesiones (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario_id INTEGER NOT NULL,
    token TEXT UNIQUE NOT NULL,
    fecha_inicio TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_expiracion TIMESTAMP,
    activa INTEGER DEFAULT 1,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
);
```

**Tabla: auditoria**
```sql
CREATE TABLE auditoria (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario_id INTEGER,
    accion TEXT NOT NULL,
    tabla_afectada TEXT,
    registro_id INTEGER,
    detalles TEXT,
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
);
```

## Flujo de Trabajo

### Agregar Nueva Funcionalidad

#### 1. Crear Modelo (si es necesario)

```python
# database/models.py

class NuevoModelo:
    @staticmethod
    def crear(campo1, campo2):
        db = DatabaseConnection()
        cursor = db.get_connection().cursor()
        cursor.execute("""
            INSERT INTO tabla_nueva (campo1, campo2)
            VALUES (?, ?)
        """, (campo1, campo2))
        db.get_connection().commit()
        return cursor.lastrowid
    
    @staticmethod
    def obtener_todos():
        db = DatabaseConnection()
        cursor = db.get_connection().cursor()
        cursor.execute("SELECT * FROM tabla_nueva")
        return cursor.fetchall()
```

#### 2. Crear Controlador

```python
# controllers/nuevo_controller.py

class NuevoController:
    @staticmethod
    def procesar_datos(datos):
        # Validación
        if not datos:
            return False, "Datos inválidos"
        
        # Lógica de negocio
        resultado = NuevoModelo.crear(
            campo1=datos['campo1'],
            campo2=datos['campo2']
        )
        
        return True, "Operación exitosa"
```

#### 3. Crear Vista

```python
# ui/nueva_view.py

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton
from controllers.nuevo_controller import NuevoController

class NuevaView(QWidget):
    def __init__(self):
        super().__init__()
        self._init_ui()
    
    def _init_ui(self):
        layout = QVBoxLayout(self)
        
        # Agregar componentes
        btn_guardar = QPushButton("Guardar")
        btn_guardar.clicked.connect(self._guardar)
        layout.addWidget(btn_guardar)
    
    def _guardar(self):
        datos = {
            'campo1': self.input1.text(),
            'campo2': self.input2.text()
        }
        
        exito, mensaje = NuevoController.procesar_datos(datos)
        # Mostrar mensaje al usuario
```

#### 4. Integrar en Ventana Principal

```python
# ui/main_window.py

from .nueva_view import NuevaView

# En __init__
self.nueva_view = NuevaView()
self.content_stack.addWidget(self.nueva_view)

# Agregar botón en sidebar
btn_nuevo = QPushButton("Nueva Sección")
btn_nuevo.clicked.connect(lambda: self.content_stack.setCurrentWidget(self.nueva_view))
```

## Testing y Depuración

### Ejecutar con Logs

```bash
# Windows
python main.py > debug.log 2>&1

# Linux/Mac
python3 main.py 2>&1 | tee debug.log
```

### Inspeccionar Base de Datos

```bash
# Usando script incluido
python scripts/ver_datos.py

# O directamente con sqlite3
sqlite3 .data/gesmonth.db
.tables
SELECT * FROM clientes;
```

### Debugging en VSCode

Crear `.vscode/launch.json`:

```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: GesMonth",
            "type": "python",
            "request": "launch",
            "program": "${workspaceFolder}/main.py",
            "console": "integratedTerminal",
            "justMyCode": false
        }
    ]
}
```

## Compilación

### Compilar Ejecutable

**Windows:**
```cmd
scripts\build.bat
```

**Linux/Mac:**
```bash
./scripts/build.sh
```

El ejecutable estará en `dist/GesMonth/`

### Crear Paquete Distribuible

**Windows:**
```cmd
scripts\package.bat
```

**Linux/Mac:**
```bash
./scripts/package.sh
```

El paquete estará en `GesMonth-v2.1.0-[OS].zip/tar.gz`

Ver [BUILD.md](BUILD.md) para detalles completos.

## Contribuciones

### Proceso de Contribución

1. **Fork** el repositorio en GitHub
2. **Clone** tu fork localmente
3. **Crea una rama** para tu feature:
   ```bash
   git checkout -b feature/nueva-funcionalidad
   ```
4. **Desarrolla** siguiendo las convenciones del proyecto
5. **Prueba** tus cambios exhaustivamente
6. **Commit** con mensajes descriptivos:
   ```bash
   git commit -m "Agrega validación de correos en clientes"
   ```
7. **Push** a tu fork:
   ```bash
   git push origin feature/nueva-funcionalidad
   ```
8. **Abre un Pull Request** en el repositorio original

### Convenciones de Código

#### Nomenclatura

```python
# Clases: PascalCase
class ClienteController:
    pass

# Funciones y métodos: snake_case
def calcular_total_mes():
    pass

# Constantes: UPPER_SNAKE_CASE
MAX_INTENTOS_LOGIN = 5

# Variables privadas: prefijo _
def _metodo_interno(self):
    pass
```

#### Docstrings

```python
def funcion_compleja(parametro1: str, parametro2: int) -> bool:
    """
    Descripción breve de la función.
    
    Args:
        parametro1: Descripción del primer parámetro
        parametro2: Descripción del segundo parámetro
    
    Returns:
        bool: True si exitoso, False en caso contrario
    
    Raises:
        ValueError: Si parametro2 es negativo
    """
    pass
```

#### Type Hints

```python
from typing import List, Dict, Optional

def procesar_clientes(clientes: List[Dict]) -> Optional[int]:
    """Procesa lista de clientes y retorna cantidad procesada"""
    pass
```

### Estándares de Calidad

- Seguir PEP 8 (estilo de código Python)
- Máximo 100 caracteres por línea
- Documentar todas las funciones públicas
- Agregar type hints donde sea posible
- Mantener funciones simples (máx. 50 líneas)
- Evitar código duplicado

### Checklist Pre-Commit

- [ ] Código sigue convenciones del proyecto
- [ ] Todas las funciones están documentadas
- [ ] No hay código comentado innecesario
- [ ] No hay imports no utilizados
- [ ] Cambios probados localmente
- [ ] Base de datos funciona correctamente
- [ ] No hay errores en consola
- [ ] README actualizado si es necesario

## Recursos Adicionales

- [Documentación PyQt6](https://www.riverbankcomputing.com/static/Docs/PyQt6/)
- [SQLite Documentation](https://www.sqlite.org/docs.html)
- [PEP 8 Style Guide](https://pep8.org/)
- [Python Type Hints](https://docs.python.org/3/library/typing.html)

## Contacto

Para preguntas sobre desarrollo:
- Issues: https://github.com/DIlanSG/GesMonth/issues
- Email: dilansag20@gmail.com

---

Última actualización: 26 de diciembre de 2025
Versión del documento: 2.1.0
