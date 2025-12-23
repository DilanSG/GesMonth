# GesMonth - Sistema de Gestión de Pagos Mensuales

![Version](https://img.shields.io/badge/Version-1.0.0-brightgreen.svg)
![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![PyQt6](https://img.shields.io/badge/PyQt6-6.6.1-green.svg)
![SQLite](https://img.shields.io/badge/SQLite-3-orange.svg)

## 📋 Descripción

**GesMonth** es un sistema profesional de escritorio para la gestión de pagos y cuotas mensuales desarrollado en Python. Utiliza PyQt6 para la interfaz gráfica y SQLite como base de datos, ofreciendo una solución completa, moderna y fácil de usar para el control de pagos recurrentes.

## ✨ Características Principales

### 📊 Dashboard Inteligente
- Métricas clave del negocio en tiempo real
- Total de clientes activos
- Clientes en mora (basado en último registro)
- Clientes al día
- Total recaudado del mes actual con formato personalizado
- Total recaudado del año en curso
- Footer con información de la aplicación

### 👥 Gestión de Clientes
- CRUD completo (Crear, Leer, Actualizar, Eliminar)
- Día de cobro personalizable (1-31)
- Búsqueda por nombre o documento
- Validación de documentos únicos
- Estados: activo/inactivo
- Valor de cuota mensual configurable

### 📅 Control de Cuotas Mensuales
- Grid visual de meses organizados por año
- Sistema de estados avanzado:
  - ✅ **Pagado**: Cuota completamente pagada
  - ❌ **Impago**: Sin pago registrado (genera mora)
  - ⚠️ **Con Deuda**: Pago parcial o deuda heredada
  - ⏳ **Pendiente**: Aún no vencido
- Seguimiento de deuda acumulada entre meses
- Registro de fecha de inicio de mora
- Soporte para pagos parciales
- Colores visuales intuitivos
- Dialog con detalles completos de cada cuota

### 💰 Registro de Pagos
- Múltiples métodos de pago configurables
- Prevención automática de pagos duplicados
- Historial completo por cliente
- Asociación automática al mes correspondiente
- Eliminación en cascada al cambiar estados de cuotas

### 📈 Reportes y Estadísticas
- Filtrado por año y mes específico
- Estadísticas detalladas:
  - Total de cuotas registradas
  - Cantidad en pagos
  - Cantidad sin pagar
  - Cantidad con deuda
- Desglose por método de pago
- Visualización con tarjetas profesionales

### ⚙️ Configuración Completa
- Gestión de métodos de pago personalizados
- Configuración de años de facturación
- Respaldo manual de base de datos
- Limpieza de pagos duplicados
- Reinicio de aplicación integrado
- Modo pantalla completa
- Opción para salir de la aplicación

## 🏗️ Arquitectura

El proyecto está organizado siguiendo el patrón MVC (Modelo-Vista-Controlador) y buenas prácticas de programación:

```
GesMonth/
├── main.py                     # Punto de entrada
├── VERSION                     # Archivo de versión
├── CHANGELOG.md               # Historial de cambios
├── requirements.txt           # Dependencias
├── gesmonth.db               # Base de datos SQLite
│
├── database/                  # Capa de datos
│   ├── connection.py          # Gestión de conexión y esquema
│   └── models.py              # Modelos: Cliente, Pago, CuotaMensual, MetodoPago
│
├── ui/                        # Interfaces de usuario
│   ├── main_window.py         # Ventana principal con sidebar
│   ├── dashboard_view.py      # Dashboard con métricas
│   ├── clientes_view.py       # Gestión de clientes
│   ├── cuotas_view.py         # Control de cuotas mensuales
│   ├── reportes_view.py       # Estadísticas y reportes
│   ├── configuracion_view.py  # Panel de configuración
│   └── detalles_cuota_dialog.py  # Dialog de detalles
│
├── controllers/               # Lógica de negocio
│   ├── cliente_controller.py  # Controlador de clientes
│   ├── pago_controller.py     # Controlador de pagos
│   ├── reporte_controller.py  # Controlador de reportes
│   └── config_controller.py   # Controlador de configuración
│
└── assets/                    # Recursos
    └── styles/
        └── main.qss           # Estilos CSS (Glassmorphismo)
```

## 🚀 Instalación Rápida

### Windows

1. Ejecutar `install.bat` para crear el entorno virtual e instalar dependencias
2. Ejecutar `run.bat` para iniciar la aplicación

### Linux / Mac

1. Ejecutar `./install.sh` para crear el entorno virtual e instalar dependencias
2. Ejecutar `./run.sh` para iniciar la aplicación

### Instalación Manual

#### Requisitos Previos
- Python 3.8 o superior
- pip (gestor de paquetes de Python)

#### Pasos

1. **Clonar o descargar el proyecto**
```bash
cd GesMonth
```

2. **Crear entorno virtual (recomendado)**

En Windows:
```bash
python -m venv venv
venv\Scripts\activate
```

En Linux/Mac:
```bash
python3 -m venv venv
source venv/bin/activate
```

3. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

4. **Ejecutar la aplicación**

Windows:
```bash
python main.py
```

Linux/Mac:
```bash
python3 main.py
```

## � Compilación a Ejecutable

### Para Desarrolladores

Si deseas distribuir GesMonth como un ejecutable standalone (sin necesidad de instalar Python):

#### Windows

```bash
build.bat
```

El ejecutable estará en: `dist\GesMonth.exe`

#### Linux/Mac

```bash
./build.sh
```

El ejecutable estará en: `dist/GesMonth`

### Distribución

Para distribuir a usuarios finales:

1. Copia toda la carpeta `dist` (no solo el .exe)
2. Incluye el archivo `LEER_PRIMERO.txt` con instrucciones
3. Comprime como: `GesMonth-v1.0.0-Windows.zip`

**Nota**: El ejecutable debe estar junto a la carpeta `assets` para funcionar correctamente.

📖 **Guía completa de compilación**: Ver [BUILD.md](BUILD.md)

## �💻 Guía de Uso

### 1. Dashboard
- **Métricas en tiempo real**: Total clientes, clientes en mora, clientes al día
- **Totales del mes**: Visualiza el recaudado del mes actual con nombre del mes
- **Totales del año**: Seguimiento del recaudado anual
- **Footer informativo**: Versión y descripción de la aplicación

### 2. Gestión de Clientes
- **Agregar**: Registra nuevos clientes con nombre, documento, teléfono, valor de cuota y día de cobro
- **Editar**: Modifica información de clientes existentes
- **Eliminar**: Elimina clientes (también elimina sus pagos y cuotas asociadas)
- **Buscar**: Filtra por nombre o documento en tiempo real
- **Estado**: Activa o desactiva clientes sin eliminarlos

### 3. Control de Cuotas
- **Vista mensual**: Grid de 12 meses por cada año configurado
- **Estados visuales**:
  - Verde: Pagado completamente
  - Rojo: Impago (genera mora)
  - Amarillo: Con deuda (parcial o heredada)
  - Gris: Pendiente (no vencido)
- **Acciones rápidas**: Click en cualquier mes para registrar pago o impago
- **Pagos parciales**: Registra abonos menores al valor total
- **Detalles**: Visualiza historial completo de cada cuota

### 4. Reportes
- **Filtrado mensual**: Selecciona año y mes específico para ver estadísticas
- **Métricas de cuotas**:
  - Total de cuotas registradas
  - Cantidad total en pagos
  - Cantidad sin pagar
  - Cantidad con deuda acumulada
- **Por método de pago**: Desglose de pagos por efectivo, transferencia, etc.

### 5. Configuración
- **Métodos de pago**: Agrega, edita o elimina métodos personalizados
- **Años de facturación**: Define qué años aparecen en el control de cuotas
- **Mantenimiento**:
  - Crear respaldo de base de datos
  - Limpiar pagos duplicados
- **Sistema**:
  - Reiniciar aplicación
  - Modo pantalla completa
  - Salir de la aplicación

## 🗄️ Base de Datos

SQLite con 5 tablas principales y índices optimizados:

### Tabla: clientes
| Campo | Tipo | Descripción |
|-------|------|-------------|
| id | INTEGER | ID único (autoincremental) |
| nombre | TEXT | Nombre del cliente |
| documento | TEXT | Documento de identidad (único) |
| telefono | TEXT | Número de teléfono |
| estado | TEXT | Estado (activo/inactivo) |
| valor_cuota | REAL | Monto de la cuota mensual |
| dia_cobro | INTEGER | Día del mes para cobro (1-31) |

### Tabla: cuotas_mensuales
| Campo | Tipo | Descripción |
|-------|------|-------------|
| id | INTEGER | ID único |
| cliente_id | INTEGER | ID del cliente (FK) |
| año | INTEGER | Año de la cuota |
| mes | INTEGER | Mes de la cuota (1-12) |
| monto | REAL | Monto de la cuota |
| estado | TEXT | pagado/impago/con_deuda/pendiente |
| metodo_pago | TEXT | Método usado (si aplica) |
| fecha_pago | DATE | Fecha del último pago |
| deuda_acumulada | REAL | Deuda pendiente |
| fecha_inicio_mora | DATE | Inicio de la mora |

### Tabla: pagos
| Campo | Tipo | Descripción |
|-------|------|-------------|
| id | INTEGER | ID único |
| cliente_id | INTEGER | ID del cliente (FK) |
| fecha_pago | DATE | Fecha en que se realizó el pago |
| mes_correspondiente | TEXT | Mes al que corresponde (YYYY-MM) |
| monto | REAL | Monto del pago |

### Tabla: metodos_pago
| Campo | Tipo | Descripción |
|-------|------|-------------|
| id | INTEGER | ID único |
| nombre | TEXT | Nombre del método (único) |
| activo | INTEGER | 1=activo, 0=inactivo |

### Tabla: configuracion
| Campo | Tipo | Descripción |
|-------|------|-------------|
| clave | TEXT | Nombre de la configuración (PK) |
| valor | TEXT | Valor de la configuración |

### Índices Optimizados
- `idx_clientes_estado`: Consultas por estado de cliente
- `idx_clientes_documento`: Búsqueda por documento
- `idx_pagos_cliente`: Historial de pagos por cliente
- `idx_pagos_mes`: Consultas mensuales
- `idx_cuotas_cliente`: Cuotas por cliente
- `idx_cuotas_año_mes`: Búsqueda por período
- `idx_cuotas_estado`: Filtrado por estado

## 🎨 Diseño y Personalización

### Interfaz de Usuario
- **Tema oscuro moderno** con degradados azules
- **Glassmorphismo**: Efectos de cristal esmerilado
- **Sidebar de navegación** intuitivo con 5 secciones
- **Tarjetas de información** con bordes sutiles y transparencias
- **Colores semánticos**: Verde (éxito), Rojo (error), Amarillo (advertencia), Azul (información)
- **Typography responsiva** con jerarquía visual clara
- **Timestamp en tiempo real** en el footer
- **Sin emojis** en la interfaz para mantener profesionalismo

### Personalizar Estilos

Los estilos se encuentran en `assets/styles/main.qss`. Puedes modificar:

```css
/* Cambiar color primario */
#sidebarHeader {
    color: #60a5fa;  /* Azul principal */
}

/* Modificar tarjetas */
QFrame {
    background: rgba(30, 41, 59, 0.5);
    border: 1px solid rgba(71, 85, 105, 0.5);
    border-radius: 12px;
}

/* Ajustar fuentes */
QLabel {
    font-family: 'Inter', 'Segoe UI', sans-serif;
    font-size: 14px;
}
```

## 🔧 Características Técnicas

### Arquitectura
- **Patrón MVC**: Separación clara de responsabilidades
- **Active Record simplificado**: Métodos estáticos en modelos
- **Row Factory**: Acceso a datos tipo diccionario
- **Programación Orientada a Objetos**: Código modular y reutilizable

### Optimizaciones
- **Índices de base de datos**: Consultas 10x más rápidas
- **Prevención de duplicados**: Validación en tiempo real (ventana de 5 segundos)
- **Eliminación en cascada**: Integridad referencial automática
- **Consultas preparadas**: Prevención de inyección SQL

### Validaciones
- **Documentos únicos**: No permite clientes con mismo documento
- **Montos positivos**: Validación de valores mayores a 0
- **Fechas válidas**: Verificación de rangos de fechas
- **Estados consistentes**: Transiciones de estado controladas

## 📦 Dependencias

```
PyQt6==6.6.1          # Framework GUI moderno
PyQt6-Qt6==6.6.1      # Bindings Qt6
PyQt6-sip==13.6.0     # Generador de bindings
openpyxl==3.1.2       # Exportación Excel (futuro)
pandas==2.1.4         # Análisis de datos (futuro)
```

Instalar todas:
```bash
pip install -r requirements.txt
```

## � Solución de Problemas

### La aplicación no inicia
- Verifica que Python 3.8+ esté instalado: `python --version`
- Asegúrate de haber activado el entorno virtual
- Instala las dependencias: `pip install -r requirements.txt`
- Revisa la consola para ver mensajes de error específicos

### Error "ModuleNotFoundError: No module named 'PyQt6'"
- El entorno virtual no está activado o las dependencias no están instaladas
- Solución: Activa el venv y ejecuta `pip install -r requirements.txt`

### La base de datos no se crea
- Verifica permisos de escritura en la carpeta del proyecto
- La base de datos `gesmonth.db` se crea automáticamente en la primera ejecución
- Si hay problemas, elimina `gesmonth.db` y reinicia la aplicación

### Los estilos no se cargan correctamente
- Verifica que exista el archivo `assets/styles/main.qss`
- Revisa la consola para mensajes de error al cargar estilos
- El archivo debe estar en la ruta correcta relativa al `main.py`

### Los pagos aparecen duplicados
- Ve a Configuración > Mantenimiento > Limpiar Pagos Duplicados
- El sistema ahora previene duplicados automáticamente

### Cliente en mora no se marca correctamente
- La mora se determina por el último registro del cliente
- Si el último mes registrado es "impago", el cliente está en mora
- Los meses sin registrar no cuentan como mora

## 🔒 Seguridad

- **Consultas preparadas**: Prevención de inyección SQL
- **Validación de entrada**: Todos los formularios validan datos
- **Sanitización**: Los datos se limpian antes de insertar en BD
- **Sin credenciales**: No se almacenan contraseñas (aplicación local)
- **Respaldos manuales**: El usuario controla cuándo y dónde respaldar

## 🚀 Roadmap (Futuras Mejoras)

- [ ] Exportación de reportes a Excel
- [ ] Gráficos estadísticos con matplotlib
- [ ] Recordatorios automáticos de cobro
- [ ] Envío de notificaciones por email/WhatsApp
- [ ] Generación de recibos de pago en PDF
- [ ] Multi-idioma (Español/Inglés)
- [ ] Modo claro/oscuro configurable
- [ ] Sistema de usuarios y permisos
- [ ] Backup automático programado
- [ ] Dashboard con gráficos interactivos

## 📝 Licencia

Este proyecto es de código abierto y está disponible para uso personal, educativo y comercial.

## 👨‍💻 Desarrollo

### Tecnologías Utilizadas
- **Python 3.8+**: Lenguaje de programación
- **PyQt6**: Framework para interfaces gráficas multiplataforma
- **SQLite**: Base de datos embebida
- **QSS**: Estilos CSS para Qt
- **Programación Orientada a Objetos**: Arquitectura modular
- **Patrón MVC**: Modelo-Vista-Controlador

### Estructura del Código
- **Modular**: Cada componente en su propio archivo
- **Documentado**: Docstrings en todas las funciones y clases
- **Type Hints**: Anotaciones de tipos para mejor mantenimiento
- **PEP 8**: Siguiendo convenciones de estilo de Python

### Agregar Nuevas Funcionalidades

1. **Nuevo modelo de datos**:
   - Edita `database/connection.py` para agregar la tabla
   - Crea la clase del modelo en `database/models.py`
   - Implementa métodos CRUD estáticos

2. **Nueva vista**:
   - Crea un archivo en `ui/` (ej: `nueva_view.py`)
   - Hereda de `QWidget` e implementa `_init_ui()`
   - Agrégala al `QStackedWidget` en `main_window.py`
   - Añade el botón de navegación en el sidebar

3. **Nuevo controlador**:
   - Crea un archivo en `controllers/` (ej: `nuevo_controller.py`)
   - Implementa la lógica de negocio como métodos estáticos
   - Importa y usa desde las vistas correspondientes

### Convenciones de Código

```python
# Nombres de clases: PascalCase
class ClienteController:
    pass

# Nombres de métodos/funciones: snake_case
def crear_cliente(nombre: str) -> int:
    pass

# Constantes: UPPER_SNAKE_CASE
MAX_RETRIES = 3

# Variables privadas: prefijo con _
def _metodo_privado(self):
    pass
```

### Contribuciones

Las contribuciones son bienvenidas. Para contribuir:

1. **Fork** el repositorio
2. Crea una **rama** para tu feature: `git checkout -b feature/nueva-caracteristica`
3. **Commit** tus cambios: `git commit -am 'Agrega nueva característica'`
4. **Push** a la rama: `git push origin feature/nueva-caracteristica`
5. Abre un **Pull Request**

### Guidelines para Pull Requests
- Describe claramente qué cambia el PR
- Incluye capturas de pantalla para cambios visuales
- Asegura que no hay errores de sintaxis
- Mantén el estilo de código existente
- Actualiza la documentación si es necesario

## 📧 Soporte y Contacto

- **Issues**: Reporta bugs o sugiere mejoras abriendo un issue
- **Documentación**: Consulta la carpeta `docs/` para más detalles
- **Preguntas**: Abre una discusión en el repositorio

## 🙏 Agradecimientos

- **PyQt6**: Por el excelente framework GUI
- **Python Community**: Por las herramientas y librerías
- **Usuarios**: Por su feedback y sugerencias

---

<div align="center">

**GesMonth v1.0.0**

Sistema profesional de gestión de pagos y cuotas mensuales

Desarrollado con ❤️ usando Python y PyQt6

[📖 Documentación](docs/) • [🐛 Reportar Bug](../../issues) • [💡 Sugerir Feature](../../issues)

</div>
