# Changelog

Todos los cambios notables de este proyecto serán documentados en este archivo.

## [2.2.0] - 2025-01-03

### Añadido

#### Sistema de Logs Completo y Mejorado
- **Tabla `logs_sistema` simplificada**: 6 columnas esenciales (id, usuario_id, usuario_nombre, fecha_hora, accion, detalles)
- **Modelo LogSistema**: CRUD completo y optimizado en `database/models.py`
- **LogController**: Controlador dedicado con API simplificada para registro, consulta y exportación
- **Registro automático exhaustivo** en todas las operaciones críticas:
  - **Pagos**: Registrar, eliminar (con detalles del monto)
  - **Clientes**: Crear, editar (muestra campos modificados), eliminar
  - **Cuotas**: Eliminar registros (diferencia PAGADO/IMPAGO/PARCIAL con montos específicos)
  - **Métodos de pago**: Crear, editar (muestra cambio: anterior → nuevo), eliminar
  - **Usuarios**: Crear, editar (muestra campos actualizados), cambiar contraseña, activar/desactivar
- **Mensajes descriptivos en español**: Cada log usa lenguaje natural y claro para usuarios finales

#### Vista de Historial de Cambios (Superadmin)
- **Nueva pestaña en Configuración**: "Historial de Cambios" exclusiva para superadmin
- **Tabla interactiva** con todos los logs del sistema:
  - Columnas: Fecha y Hora, Usuario, Acción, Detalles, ID
  - Ordenados del más reciente al más antiguo
  - Últimos 1000 registros visibles
- **Colores por tipo de acción**:
  - Verde: Crear/Registrar
  - Rojo: Eliminar
  - Azul: Editar/Actualizar/Cambiar
  - Amarillo: Impago
- **Word wrap automático**: Detalles largos se expanden en múltiples líneas sin cortarse
- **Botón de actualizar**: Refresca los datos en tiempo real
- **Sin límite de texto**: Todos los detalles visibles sin "..." de truncamiento

#### Interfaz de Descarga de Logs Mejorada
- **Botón "Descargar Logs"** en Configuración → General → Mantenimiento
- **Exportación a CSV optimizada**: 
  - Formato compatible con Excel, LibreOffice y Google Sheets
  - Encoding UTF-8 con BOM para correcta visualización de acentos
  - 6 columnas: ID, Usuario ID, Usuario, Fecha y Hora, Acción, Detalles
- **Nombre automático con timestamp**: `logs_gesmonth_YYYYMMDD_HHMMSS.csv`
- **Estadísticas en exportación**: Muestra total de registros exportados
- **Diálogo de ubicación**: Permite elegir dónde guardar el archivo

#### Detalles Mejorados de Logs
Los mensajes de log ahora son descriptivos y específicos por tipo de acción:

**Clientes:**
- Crear: "Se registró un nuevo cliente con los siguientes datos: Nombre: [nombre], CC: [doc]"
- Editar: "Datos de cliente actualizados a: Nombre: [nuevo], CC: [nuevo], Cuota: $[nuevo]"
- Eliminar: "Se eliminó el cliente: [nombre], CC: [doc]"

**Métodos de Pago:**
- Crear: "Nuevo método de pago creado: [nombre]"
- Editar: "Método de pago anterior: [viejo], Método de pago nuevo: [nuevo]"
- Eliminar: "Método de pago eliminado: [nombre]"

**Usuarios:**
- Crear: "Se creó un nuevo usuario: [username], Nombre: [nombre], Rol: [rol]"
- Editar: "Datos de usuario actualizados a: Nombre: [nuevo], Rol: [nuevo]"
- Cambiar contraseña: "Se cambió la contraseña del usuario: [username]" (sin mostrar contraseña)
- Activar/Desactivar: "Usuario [username] activado/desactivado"

**Registros de Cuotas:**
- Eliminar PAGADO: "Se eliminó un registro PAGADO: Cliente: [nombre], Mes: [mes año], Monto: $[X], Método: [método]"
- Eliminar IMPAGO: "Se eliminó un registro IMPAGO: Cliente: [nombre], Mes: [mes año], Cuota: $[X]"
- Eliminar PARCIAL: "Se eliminó un registro PARCIAL: Cliente: [nombre], Mes: [mes año], Cuota: $[X], Deuda pendiente: $[Y]"

#### Optimización de Base de Datos
- **Índices optimizados** para consultas ultra rápidas:
  - `idx_logs_usuario`: Búsqueda por usuario
  - `idx_logs_fecha`: Búsqueda por rango de fechas
- **API simplificada**: Solo 4 parámetros (usuario_id, usuario_nombre, accion, detalles)
- **Métodos de filtrado mejorados**: Por acción, usuario, rango de fechas
- **Límite de consultas configurables**: Control de memoria con límite opcional

#### Testing y Validación
- **Script completo de pruebas**: `scripts/test_logs.py` con 6 tests
- **Verificaciones automáticas**:
  - Existencia y estructura de tabla
  - Creación de logs
  - Consulta y filtrado
  - Exportación a CSV
  - Estadísticas del sistema
- **Salida visual mejorada**: Formato con cajas y colores para fácil lectura
- **Script wrapper**: `scripts/test_logs.sh` para ejecución con entorno virtual

#### Documentación Completa
- **Comentarios en imports**: Explicación de cada módulo importado y su uso
- **Docstrings detallados**: Funciones complejas documentadas con:
  - Descripción del propósito
  - Algoritmos paso a paso
  - Ejemplos de uso
  - Advertencias y consideraciones
- **Comentarios en funciones críticas**:
  - Patrón Singleton en DatabaseConnection
  - Sistema de bloqueo por intentos fallidos en autenticación
  - Hashing con bcrypt y validaciones de seguridad
  - Lógica de pagos parciales y deuda acumulada
  - Toggle Switch animado con QPropertyAnimation
  - Renderizado SVG dinámico según tema

### Mejorado
- **Controladores completamente actualizados**:
  - ClienteController: Inyección de log_controller y usuario_actual
  - PagoController: Preparado para logs (por implementar en futuras versiones)
  - ConfigController: Logging en métodos de pago
- **Inyección de dependencias en vistas**:
  - CuotasView recibe usuario_actual para logs en eliminaciones
  - ClientesView configurada con log_controller en MainWindow
  - DetallesCuotaDialog recibe usuario_actual para logs
- **Interfaz más robusta**: Word wrap y ajuste automático de altura en tablas
- **Código más mantenible**: Comentarios exhaustivos en funciones complejas
- **Sistema de auditoría integral**: Complementa auditoría de usuarios con logs de negocio

### Técnico
- **Arquitectura mejorada**: Separación clara entre auditoría de usuarios y logs de negocio
- **Rendimiento optimizado**: Índices en columnas frecuentemente consultadas
- **Seguridad reforzada**: Logs inmutables, no se pierden al eliminar usuarios
- **Escalabilidad**: Sistema preparado para millones de registros con paginación
- **Internacionalización**: Todos los mensajes en español claro y profesional

## [2.1.1] - 2025-12-26

### Añadido
- **Compatibilidad Mejorada con Windows**: Soporte completo para sistemas Windows con diferentes configuraciones regionales
- Lectura de archivos con encoding UTF-8 explícito en todas las operaciones
- Compatibilidad con sistemas que usan codepage 1252, 1250 y otras variantes regionales
- Gestión robusta de archivos SVG en entornos Windows
- Lectura consistente del archivo VERSION independientemente del sistema operativo

## [2.1.0] - 2025-12-26

### Añadido

#### Licencia Source Available
- **Nueva licencia SAL**: El proyecto ahora está bajo Source Available License
- Código fuente visible y modificable para uso personal/educativo
- Restricciones de redistribución y uso comercial sin permiso
- Archivo LICENSE creado con términos completos

#### Sistema de Gestión de Datos
- **Carpeta `.data/` persistente**: Bases de datos ahora se almacenan junto al ejecutable
- Archivos placeholder en paquetes distribuibles (solo lectura)
- Sistema automático de inicialización de BDs en primera ejecución
- Script `ver_datos.py` para inspección y edición de bases de datos
- Separación clara entre recursos estáticos (assets) y datos persistentes (.data)

#### Organización de Scripts
- **Nueva carpeta `scripts/`**: Todos los scripts organizados (.sh, .bat)
- Rutas actualizadas en README.md y documentación
- Scripts de build, install, run y package centralizados

#### Versionado Dinámico
- **Plantillas con {{VERSION}}**: Archivos de distribución usan versión dinámica
- Script de empaquetado reemplaza automáticamente {{VERSION}} con valor de archivo VERSION
- README.txt generado con versión correcta en cada build
- Eliminación de versiones hardcodeadas

#### Sistema de Persistencia de Configuración
- **Persistencia de tema**: El tema seleccionado (claro/oscuro) ahora se guarda en la base de datos
- **Persistencia de pantalla completa**: La preferencia de pantalla completa se mantiene entre sesiones
- Nuevos métodos en `ConfigController`: `get_theme()`, `set_theme()`, `get_fullscreen()`, `set_fullscreen()`
- El login ahora carga automáticamente el último tema usado
- La ventana principal aplica automáticamente el modo pantalla completa guardado

#### Toggle Switch Moderno
- **Reemplazo de controles tradicionales**: Sustituido dropdown y checkbox por toggle switches animados
- Implementación personalizada de `ToggleSwitch` con `QPropertyAnimation`
- Animación suave de 200ms con curva `InOutCubic`
- Colores dinámicos: azul (#3b82f6) cuando está activo, gris (#cbd5e1) cuando está inactivo
- Integrado en vista de Configuración y vista de Login
- Sincronización automática del estado visual con el tema guardado

#### Splash Screen Inteligente
- **Responsividad adaptativa**: El splash screen ajusta su tamaño según el modo de visualización
  - Pantalla completa: cubre toda la pantalla
  - Modo ventana: mismo tamaño que la ventana principal (1200x700), centrado
- Transición fluida entre splash y ventana principal con animación de fade
- Posicionamiento perfecto para experiencia visual natural
- Elementos escalables (logo, título, espaciado) proporcionales al tamaño de pantalla

### Mejorado

#### Interfaz de Login
- **Diseño minimalista**: Removido texto de credenciales por defecto para mayor seguridad
- **Toggle de tema centralizado**: Control de tema con etiqueta "Tema Oscuro" centrada
- Implementación de `ToggleSwitch` reemplazando checkbox tradicional
- Estado inicial del toggle sincronizado con tema guardado
- Mejor experiencia de usuario con controles más intuitivos

#### Iconografía SVG
- **Icono de configuración mejorado**: Engranaje de 8 dientes con colores responsivos
- Reemplazo de `fill="#000000"` por colores adaptativos según tema
- Colores optimizados: `#94a3b8` (tema oscuro), `#64748b` (tema claro)
- SVGs más legibles en ambos temas

#### Header de Sidebar
- **Diseño centrado**: Información del usuario reorganizada con mejor alineación
- Texto "Bienvenido" seguido del nombre de usuario
- Badge de rol removido para diseño más limpio
- Mejor jerarquía visual de la información

#### Sistema de Temas
- **Integración completa**: ThemeController ahora integrado con ConfigController
- Acceso a configuración de pantalla completa desde ThemeController
- Cambios de tema se guardan automáticamente en la base de datos
- Sincronización perfecta entre login, splash screen y aplicación principal

### Corregido

- **Bug de toggle en configuración**: El toggle ahora muestra correctamente el estado visual cuando el tema es oscuro
- **Sincronización de tema**: Forzado el repintado del toggle con `update()` para visualización correcta
- **Posición del círculo en toggle**: Sincronización manual de `_circle_position` al cargar la vista
- **Transición de splash**: Reorganizado el flujo de carga para mostrar splash primero, luego cargar ventana
- **Centrado de ventana principal**: La ventana ahora se centra correctamente después del splash screen

### Archivos Modificados

```
main.py                          # Integración de splash responsivo y carga de configuración
ui/splash_screen.py              # Sistema responsivo según modo fullscreen
ui/login_view.py                 # Toggle switch, carga de tema, diseño minimalista
ui/configuracion_view.py         # Toggle switch, sincronización de estado visual
ui/main_window.py                # Aplicación de configuración guardada al inicio
controllers/config_controller.py # Métodos get/set para tema y fullscreen
controllers/theme_controller.py  # Integración con ConfigController
```

### Notas Técnicas

#### ToggleSwitch Implementation
- Basado en `QCheckBox` con pintura personalizada
- Tamaño fijo: 60x30 píxeles
- Posiciones del círculo: 3 (izquierda/claro), 33 (derecha/oscuro)
- Animación manejada manualmente en `mousePressEvent` para evitar conflictos

#### Persistencia de Configuración
- Tabla `configuracion` en base de datos con pares clave-valor
- Valores boolean guardados como strings "true"/"false"
- Carga automática al iniciar login y ventana principal

#### Flujo de Inicialización Mejorado
1. Login muestra con tema guardado
2. Splash screen se muestra con tamaño correcto (fullscreen o ventana)
3. Ventana principal se carga en segundo plano (oculta)
4. Splash hace fade out después de 5 segundos
5. Ventana principal aparece centrada en pantalla

---

## [2.0.0] - 2024-12-25

### Cambios y mejoras

#### Sistema de Temas
- Controlador de temas centralizado (ThemeController), con persistencia en la base de datos.
- Soporte para cambiar y recordar el tema (oscuro/claro) en toda la aplicación.
- QSS dinámico para ambos temas, incluyendo el login y la ventana principal.
- Icono de check SVG para el QCheckBox de selección de tema.

### Sistema de Autenticación Completo

#### Nuevas Funcionalidades Principales

**Sistema de Login**
- Autenticación segura con contraseñas encriptadas usando bcrypt
- Prevención de ataques de fuerza bruta (bloqueo tras 10 intentos fallidos)
- Desbloqueo automático después de 15 minutos
- Validación de credenciales en tiempo real

**Base de Datos de Usuarios**
- Nueva base de datos SQLite separada (users.db) en ~/gesmonth_data/
- Tres tablas: usuarios, sesiones, logs_auditoria
- Creación automática de superadministrador al primer inicio
  - Usuario: admin
  - Contraseña: admin123 (debe cambiarse)

**Sistema de Roles y Permisos**
- 4 niveles de acceso jerárquico:
  1. **Superadmin**: Control total + creación de usuarios
  2. **Admin**: Gestión completa de datos sin crear usuarios
  3. **Operador**: Crear y editar registros
  4. **Solo Lectura**: Visualización únicamente
- Control de acceso basado en roles (RBAC)
- Validación de permisos en cada acción

**Gestión de Usuarios**
- Panel exclusivo para superadministradores
- Crear usuarios con roles específicos
- Editar información de usuarios existentes
- Activar/Desactivar cuentas (sin eliminar historial)
- Cambiar contraseñas de otros usuarios
- Protección del usuario superadmin original (no editable)

**Sistema de Auditoría**
- Registro automático de todas las acciones
- Trazabilidad completa: usuario, acción, fecha/hora
- Base para futuras funcionalidades de reporting
- Logs persistentes en base de datos

**Sesiones y Seguridad**
- Sistema de tokens para gestionar sesiones activas
- Cierre de sesión seguro
- Display de usuario actual en sidebar
- Botón de logout visible en todo momento

#### Interfaz de Login
- Implementación de glassmorphism y gradientes en la UI.
- Selector de tema claro/oscuro con checkbox personalizado (icono SVG de check).
- El tema seleccionado se aplica y persiste en toda la app.


#### Otros
- Refactor de eventos de cierre: ahora la ventana de login se puede cerrar normalmente.
- Mejoras menores de accesibilidad y experiencia de usuario en el login.
- Actualización de dependencias y assets (nuevo SVG en assets/icons/checkmark.svg).

#### Archivos Nuevos

```
database/
├── user_connection.py       # Conexión y setup de users.db (usuarios, sesiones, auditoría)
├── user_models.py           # Modelos: Usuario, Sesion, AuditoriaLog

controllers/
├── auth_controller.py       # Lógica de autenticación, login y permisos
├── theme_controller.py      # Gestión y persistencia de tema claro/oscuro

ui/
├── login_view.py            # Pantalla de login moderna con selector de tema
├── usuarios_management.py   # Panel de gestión de usuarios (CRUD, roles, activación)
├── theme_colors.py          # Sistema de colores dinámicos para temas

assets/
├── icons/checkmark.svg      # Icono SVG para el check personalizado del QCheckBox
├── icons/LOGO.ico           # Nuevo icono de la app
├── icons/LOGO.png           # Nuevo icono de la app
├── styles/light.qss         # Estilos QSS para tema claro
├── styles/dark.qss          # Estilos QSS para tema oscuro

docs/
├── SISTEMA-AUTENTICACION.md # Documentación completa del sistema de login y roles
├── TEMAS.md                 # Documentación sobre el sistema de temas
```

#### Archivos Modificados

```
main.py                      # Integración del flujo de login y temas
ui/main_window.py            # Display de usuario, logout, y soporte de temas
ui/configuracion_view.py     # Nueva pestaña de gestión de usuarios, soporte de temas
ui/dashboard_view.py         # Ajustes visuales y soporte de temas
ui/clientes_view.py          # Mejoras visuales y soporte de temas
ui/pagos_view.py             # Mejoras visuales y soporte de temas
ui/cuotas_view.py            # Mejoras visuales y soporte de temas
ui/reportes_view.py          # Mejoras visuales y soporte de temas
requirements.txt             # Agregado bcrypt, PyQt6, y dependencias de UI modernas
README.md                    # Documentación actualizada para nuevas funciones y temas
VERSION                      # 1.0.1 → 2.0.0
```

#### Dependencias Agregadas

```
bcrypt==4.1.2                # Encriptación de contraseñas
PyQt6==6.7.1                 # Actualización de PyQt6 para soporte de nuevos estilos
PyQt6-Qt6==6.7.3             # Qt6 para compatibilidad visual
pandas, openpyxl, Pillow      # Para reportes y exportación
```

#### Mejoras de UI

**Sidebar**
- Información del usuario actual (nombre y rol)
- Separador visual después del header de usuario
- Botón "Cerrar Sesión" en la parte inferior

**Configuración**
- Nueva pestaña "Gestión de Usuarios" (visible solo para superadmin)
- Botones con glassmorphism design
- Tabla completa con acciones por usuario

**Login**
- Diseño moderno con gradientes
- Campos de texto con focus states
- Mensajes de error contextuales
- Prevención de cierre sin autenticación

#### Seguridad Implementada

- Contraseñas hasheadas con bcrypt (salt rounds)
- Validación de longitud mínima (6 caracteres)
- Bloqueo temporal tras intentos fallidos
- Sesiones con tokens únicos
- Prevención de inyección SQL (prepared statements)
- Separación de bases de datos (datos vs usuarios)

#### Notas de Migración

**Compatibilidad**
- Compatible con versiones anteriores
- Base de datos principal (gesmonth.db) no modificada
- Datos existentes permanecen intactos

**Primer Inicio**
- Se creará automáticamente ~/gesmonth_data/users.db
- Usuario superadmin generado con credenciales por defecto
- Recomendado: cambiar contraseña inmediatamente


#### Próximas Mejoras Planificadas

- Visualizador gráfico de logs de auditoría
- Exportación de logs a Excel
- Recuperación de contraseña
- Autenticación de dos factores (2FA)
- Expiración automática de sesiones
- Notificaciones de actividad sospechosa

---

## [1.0.1] - 2024-12-23

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
