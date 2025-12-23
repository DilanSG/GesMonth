# Changelog

Todos los cambios notables de este proyecto serán documentados en este archivo.

## [1.0.1] - 2025-12-23

### Mejoras en Distribución

#### Cambios Principales
- **Ejecutable Standalone**: Aplicación empaquetada con PyInstaller
  - Scripts de compilación automatizados (build.bat/sh)
  - Scripts de empaquetado para distribución (package.bat/sh)
  - Paquetes listos para distribuir sin dependencias de Python

- **Optimización de Assets**
  - Corrección de rutas para PyInstaller (sys.frozen)
  - Assets movidos al nivel correcto junto al ejecutable
  - Eliminación de dependencias problemáticas (pkg_resources)

- **Documentación Mejorada**
  - README completo para usuarios finales (Linux y Windows)
  - Eliminación de emojis en toda la documentación
  - Estructura de paquete simplificada (solo ejecutable, LICENSE y README)

- **GitHub Actions**
  - Workflow configurado para builds automáticos
  - Generación de releases para Windows y Linux
  - Distribución automatizada con cada tag de versión

## [1.0.0] - 2025-12-23

### Primera Versión Estable

#### Características Principales
- **Dashboard Intuitivo**: Vista general con métricas clave del negocio
  - Total de clientes
  - Clientes en mora (basado en último registro impago)
  - Clientes al día
  - Total recaudado del mes actual con formato "Mes Año"
  - Total recaudado del año actual
  - Footer informativo con datos de la aplicación

- **Gestión de Clientes**: CRUD completo
  - Agregar, editar y eliminar clientes
  - Campo personalizable de día de cobro (1-31)
  - Búsqueda por nombre o documento
  - Validación de documentos únicos
  - Estado activo/inactivo

- **Control de Cuotas Mensuales**: Sistema avanzado de seguimiento
  - Grid visual de meses por año
  - Sistema de estados: pagado, impago, con deuda, pendiente
  - Seguimiento de deuda acumulada entre meses
  - Registro de mora con fecha de inicio
  - Pagos parciales soportados
  - Colores visuales según estado (verde, rojo, amarillo)
  - Detalles completos de cada cuota

- **Registro de Pagos**: Sistema robusto
  - Múltiples métodos de pago configurables
  - Prevención de duplicados automática
  - Historial completo por cliente
  - Asociación automática al mes correspondiente
  - Eliminación en cascada al cambiar estados

- **Reportes y Estadísticas**: Análisis mensual
  - Filtrado por año y mes
  - Estadísticas de cuotas: total, pagadas, impagos, deudas
  - Desglose por método de pago
  - Visualización clara con tarjetas

- **Configuración**: Panel de administración
  - Gestión de métodos de pago
  - Configuración de años de facturación
  - Respaldo de base de datos
  - Limpieza de pagos duplicados
  - Reinicio de aplicación
  - Opciones de pantalla completa
  - Modo oscuro/claro (futuro)

#### Interfaz de Usuario
- Diseño moderno con glassmorphismo
- Tema oscuro con degradados azules
- Sidebar de navegación intuitivo
- Tarjetas de información con bordes sutiles
- Timestamp en tiempo real en el footer
- Transiciones suaves
- Responsive y escalable
- Sin emojis en la interfaz

#### Base de Datos
- SQLite integrado
- 5 tablas principales: clientes, pagos, cuotas_mensuales, metodos_pago, configuracion
- Índices optimizados para consultas frecuentes
- Row factory para acceso tipo diccionario
- Migraciones automáticas de esquema

#### Optimizaciones
- Índices de base de datos para mejor rendimiento
- Consultas optimizadas con JOINs eficientes
- Prevención de duplicados en tiempo real
- Limpieza de código de debugging
- Manejo robusto de errores

#### Instalación y Distribución
- Scripts de instalación para Windows (`install.bat`, `run.bat`)
- Scripts de instalación para Linux/Mac (`install.sh`, `run.sh`)
- **Scripts de compilación**: `build.bat` y `build.sh` para generar ejecutables
- **PyInstaller**: Empaquetado standalone con todos los recursos
- Archivo `.spec` optimizado para compilación
- Requirements.txt con dependencias precisas incluido PyInstaller
- Documentación completa para usuarios y desarrolladores
- Guía de compilación detallada en `BUILD.md`
- Archivo `LEER_PRIMERO.txt` para usuarios finales
- `.gitignore` optimizado para desarrollo y distribución

#### Correcciones
- Corregida la detección de clientes en mora (basada en último mes registrado)
- Corregido el cálculo de estadísticas mensuales usando `mes_correspondiente`
- Eliminada la duplicación de pagos al cambiar estados
- Corregida la herencia de deuda entre meses
- Corregidos los estilos inconsistentes entre vistas

### Documentación
- README.md con guía de instalación y uso
- README-dev.md con documentación técnica detallada
- README-user.md con manual de usuario
- INSTALL.md con instrucciones de instalación
- Comentarios en código siguiendo buenas prácticas

### Seguridad
- Validación de entrada en formularios
- Sanitización de datos antes de insertar en BD
- Prevención de inyección SQL con parámetros
- Manejo seguro de archivos

---

## Formato del Changelog

Este proyecto sigue [Semantic Versioning](https://semver.org/):
- **MAJOR**: Cambios incompatibles en la API
- **MINOR**: Nueva funcionalidad compatible con versiones anteriores
- **PATCH**: Correcciones de bugs compatibles con versiones anteriores

Tipos de cambios:
- `Added` para nuevas características
- `Changed` para cambios en funcionalidad existente
- `Deprecated` para características que serán removidas
- `Removed` para características removidas
- `Fixed` para corrección de bugs
- `Security` para vulnerabilidades
