# GesMonth - Sistema de Gestión de Pagos Mensuales

![Version](https://img.shields.io/badge/Version-2.1.0-brightgreen.svg)
![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![PyQt6](https://img.shields.io/badge/PyQt6-6.7.1-green.svg)
![SQLite](https://img.shields.io/badge/SQLite-3-orange.svg)
![Security](https://img.shields.io/badge/Security-bcrypt-red.svg)

## Descripción

**GesMonth** es un sistema profesional de escritorio para la gestión de pagos y cuotas mensuales. Diseñado para pequeños negocios, academias, centros de formación y cualquier organización que requiera control de pagos recurrentes de manera eficiente y segura.

Desarrollado con Python y PyQt6, ofrece una interfaz moderna con efectos glassmorphism, autenticación multi-nivel, y gestión completa de clientes, cuotas y reportes financieros.

## Características Principales

### Autenticación y Seguridad
- Sistema de login con encriptación bcrypt
- 4 niveles de roles: Superadmin, Admin, Operador, Solo Lectura
- Gestión de usuarios con control de permisos
- Auditoría completa de acciones del sistema
- Protección contra ataques de fuerza bruta
- Sesiones basadas en tokens seguros

### Dashboard Inteligente
- Métricas en tiempo real del estado del negocio
- Total de clientes activos, en mora y al día
- Recaudado del mes actual y año en curso
- Visualización profesional con tarjetas informativas
- Footer con información de versión y timestamp

### Gestión de Clientes
- CRUD completo con validación de datos
- Búsqueda en tiempo real por nombre o documento
- Validación de documentos únicos
- Configuración personalizada de día de cobro (1-31)
- Valor de cuota mensual configurable
- Estados: activo/inactivo sin eliminación física

### Control de Cuotas Mensuales
- Grid visual organizado por año y mes
- Sistema de estados avanzado:
  - **Pago**: Cuota completamente pagada
  - **Impago**: Sin pago registrado (genera mora)
  - **Con Deuda**: Pago parcial o deuda heredada
  - **Pendiente**: Aún no vencido
- Seguimiento de deuda acumulada entre meses
- Registro automático de fecha de inicio de mora
- Soporte para pagos parciales y abonos
- Dialog detallado con historial completo

### Registro de Pagos
- Múltiples métodos de pago configurables
- Prevención automática de pagos duplicados
- Historial completo por cliente
- Asociación inteligente al mes correspondiente
- Gestión de pagos parciales

### Reportes y Estadísticas
- Filtrado por año y mes específico
- Estadísticas detalladas:
  - Total de cuotas registradas
  - Cantidad de pagos completados
  - Cantidad sin pagar (mora)
  - Cantidad con deuda parcial
- Desglose por método de pago
- Visualización con tarjetas profesionales

### Configuración Avanzada
- Gestión de métodos de pago personalizados
- Configuración de años de facturación
- Sistema de temas (claro/oscuro) con persistencia
- Modo pantalla completa configurable
- Respaldo manual de base de datos
- Limpieza de pagos duplicados
- Gestión de usuarios (solo superadmin)

## Tecnologías Utilizadas

### Frontend
- **PyQt6 6.7.1**: Framework GUI multiplataforma moderno
- **QSS (Qt Style Sheets)**: Sistema de estilos CSS para interfaces
- **Glassmorphism**: Efectos de cristal esmerilado y transparencias
- **SVG Icons**: Iconografía escalable y profesional

### Backend
- **Python 3.9+**: Lenguaje de programación principal
- **SQLite 3**: Base de datos embebida de alto rendimiento
- **bcrypt**: Encriptación de contraseñas con salt aleatorio

### Arquitectura
- **Patrón MVC**: Modelo-Vista-Controlador para separación de responsabilidades
- **Singleton Pattern**: Gestión única de conexiones de base de datos
- **Active Record**: Modelos con métodos CRUD integrados
- **Observer Pattern**: Sistema de eventos reactivos

### Herramientas de Desarrollo
- **PyInstaller**: Compilación a ejecutables standalone
- **Git**: Control de versiones
- **Type Hints**: Anotaciones de tipos para mejor mantenimiento

### Dashboard Inteligente
- Métricas clave del negocio en tiempo real
- Total de clientes activos
- Clientes en mora (basado en último registro)
- Clientes al día
- Total recaudado del mes actual con formato personalizado
- Total recaudado del año en curso
- Footer con información de la aplicación

### Gestión de Clientes
- CRUD completo (Crear, Leer, Actualizar, Eliminar)
- Día de cobro personalizable (1-31)
- Búsqueda por nombre o documento
- Validación de documentos únicos
- Estados: activo/inactivo
- Valor de cuota mensual configurable

### Control de Cuotas Mensuales
- Grid visual de meses organizados por año
- Sistema de estados avanzado:
  - Pago: Cuota completamente pagada
  - Impago: Sin pago registrado (genera mora)
  - Con Deuda: Pago parcial o deuda heredada
  - Pendiente: Aún no vencido
- Seguimiento de deuda acumulada entre meses
- Registro de fecha de inicio de mora
- Soporte para pagos parciales
- Colores visuales intuitivos
- Dialog con detalles completos de cada cuota

### Registro de Pagos
- Múltiples métodos de pago configurables
- Prevención automática de pagos duplicados
- Historial completo por cliente
- Asociación automática al mes correspondiente
- Eliminación en cascada al cambiar estados de cuotas

### Reportes y Estadísticas
- Filtrado por año y mes específico
- Estadísticas detalladas:
  - Total de cuotas registradas
  - Cantidad en pagos
  - Cantidad sin pagar
  - Cantidad con deuda
- Desglose por método de pago
- Visualización con tarjetas profesionales

### Configuración Completa
- Gestión de métodos de pago personalizados
- Configuración de años de facturación
- Respaldo manual de base de datos
- Limpieza de pagos duplicados
- Reinicio de aplicación integrado
- Modo pantalla completa
- Opción para salir de la aplicación

## Arquitectura

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

### Historial de Versiones
**v2.1.1 (26 dic 2025):**
Compatibilidad Mejorada con Windows
- Soporte universal para Windows (7/8/10/11)
- Encoding UTF-8 explícito en todas las operaciones de archivo
- Compatible con todos los codepages de Windows (CP-1252, CP-1250, etc.)
- Funcionamiento garantizado independientemente del idioma del sistema
- Gestión robusta de archivos SVG y recursos

**v2.1.0 (26 dic 2025):**
- Licencia Source Available (SAL)
- Sistema de datos persistente (.data/)
- Versionado dinámico
- Persistencia de tema y pantalla completa
- Toggle switches modernos
- Splash screen inteligente

**v2.0.0 (25 dic 2025):**
- Sistema de autenticación (bcrypt)
- 4 roles de usuario
- Gestión de usuarios y auditoría
- Protección anti-fuerza bruta
- Sistema de temas claro/oscuro

**v1.0.1 (23 dic 2025):**
- Ejecutable standalone con PyInstaller
- Scripts de compilación y empaquetado
- Optimización de assets y rutas
- GitHub Actions para builds automáticos

**v1.0.0 (23 dic 2025):**
- Release inicial
- Dashboard con métricas clave
- Gestión completa de clientes (CRUD)
- Control de cuotas mensuales
- Registro de pagos
- Reportes y estadísticas
- Interfaz glassmorphism

---

## Instalación

### Windows

1. Descargar `GesMonth-v2.1.0-Windows.zip`
2. Descomprimir el archivo ZIP
3. Entrar a la carpeta `GesMonth/`
4. Ejecutar `GesMonth.exe`

### Linux

1. Descargar `GesMonth-v2.1.0-Linux.tar.gz`
2. Descomprimir: `tar -xzf GesMonth-v2.1.0-Linux.tar.gz`
3. Entrar a la carpeta: `cd GesMonth-v2.1.0-Linux/GesMonth`
4. Ejecutar: `./GesMonth`

**Nota**: El ejecutable necesita estar junto a las carpetas `assets/` y `.data/` para funcionar correctamente. No mover archivos fuera de su ubicación original.

**Credenciales por defecto**:
```
Usuario: admin
Contraseña: admin123
```
*Cambiar después del primer inicio. Ver [docs/SISTEMA-AUTENTICACION.md](docs/SISTEMA-AUTENTICACION.md) para detalles.*

## Arquitectura del Sistema

GesMonth utiliza una arquitectura limpia basada en el patrón MVC (Modelo-Vista-Controlador):

### Estructura de Carpetas

```
GesMonth/
├── database/          # Modelos y conexiones de base de datos
├── ui/               # Interfaces gráficas (vistas)
├── controllers/      # Lógica de negocio
├── utils/            # Funciones auxiliares
├── assets/           # Recursos estáticos (iconos, estilos)
├── scripts/          # Scripts de automatización
└── .data/            # Datos persistentes (bases de datos)
```

### Bases de Datos

El sistema utiliza dos bases de datos SQLite separadas:

**gesmonth.db** - Datos del negocio:
- clientes: Información de clientes
- cuotas_mensuales: Registro de cuotas por período
- pagos: Historial de pagos realizados
- metodos_pago: Métodos de pago configurables
- configuracion: Ajustes del sistema

**users.db** - Autenticación y seguridad:
- usuarios: Cuentas de usuario con roles
- sesiones: Tokens de sesión activos
- auditoria: Registro de acciones del sistema

Ver documentación completa en [docs/DESARROLLO.md](docs/DESARROLLO.md)

## Documentación

### Para Usuarios
- [Guía de Usuario](docs/README-user.md): Manual de uso completo
- [Sistema de Autenticación](docs/SISTEMA-AUTENTICACION.md): Gestión de usuarios y permisos
- [Distribución](docs/DISTRIBUCION.md): Instrucciones de instalación

### Para Desarrolladores
- [Guía de Desarrollo](docs/DESARROLLO.md): Arquitectura y flujo de trabajo
- [Compilación](docs/BUILD.md): Crear ejecutables standalone
- [README Desarrollador](docs/README-dev.md): Configuración del entorno

## Solución de Problemas

## Dependencias

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

## Solución de Problemas

### La aplicación no inicia (Windows)
- Verifica que todas las carpetas estén presentes: `GesMonth.exe`, `assets/`, `_internal/`
- Ejecuta desde línea de comandos para ver errores: `cmd` > navega a la carpeta > `GesMonth.exe`
- Revisa que no haya antivirus bloqueando el ejecutable

### La aplicación no inicia (Linux)
- Verifica permisos de ejecución: `chmod +x GesMonth`
- Ejecuta desde terminal para ver errores: `./GesMonth`
- Instala librerías Qt6 si es necesario: `sudo apt install qt6-base-dev`

### Los estilos no se cargan correctamente
- Verifica que la carpeta `assets/` esté junto al ejecutable
- No muevas archivos fuera de su ubicación original
- La aplicación necesita acceso de lectura a `assets/styles/`

### La base de datos no funciona
- Verifica que la carpeta `.data/` tenga permisos de escritura
- Las bases de datos se crean automáticamente en `.data/gesmonth.db` y `.data/users.db`
- Si hay problemas, elimina la carpeta `.data/` y reinicia la aplicación

### Los pagos aparecen duplicados
- Ve a Configuración > Mantenimiento > Limpiar Pagos Duplicados
- El sistema ahora previene duplicados automáticamente

### Cliente en mora no se marca correctamente
- La mora se determina por el último registro del cliente
- Si el último mes registrado es "impago", el cliente está en mora
- Los meses sin registrar no cuentan como mora

## Seguridad

- Consultas preparadas: Prevención de inyección SQL
- Validación de entrada: Todos los formularios validan datos
- Sanitización: Los datos se limpian antes de insertar en BD
- Contraseñas encriptadas: bcrypt con salt aleatorio
- Sistema de bloqueo: Protección contra ataques de fuerza bruta
- Sesiones seguras: Tokens únicos por sesión de usuario

## Desarrollo

### Para Desarrolladores

Si deseas modificar el código fuente:

#### Requisitos
- Python 3.8 o superior
- pip (gestor de paquetes)

#### Pasos

1. Clonar el repositorio
2. Crear entorno virtual:
   - Windows: `python -m venv venv && venv\Scripts\activate`
   - Linux/Mac: `python3 -m venv venv && source venv/bin/activate`
3. Instalar dependencias: `pip install -r requirements.txt`
4. Ejecutar: `python main.py`

#### Compilar ejecutable
- Windows: `scripts\build.bat`
- Linux/Mac: `./scripts/build.sh`

Ver documentación completa en [docs/BUILD.md](docs/BUILD.md)

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


### Cliente en mora no se marca correctamente
- La mora se determina por el último registro del cliente
- Si el último mes registrado es "impago", el cliente está en mora
- Los meses sin registrar no cuentan como mora

## Licencia

Este proyecto está bajo la **Source Available License (SAL)**.

### Permisos:
- Ver y estudiar el código fuente
- Usar para fines personales o educativos
- Modificar para uso personal o interno
- Crear trabajos derivados para uso personal

### Restricciones:
- No redistribuir sin permiso explícito
- No uso comercial sin permiso
- No usar en servicios SaaS sin autorización
- No distribuir trabajos derivados sin permiso

Para uso comercial o redistribución, contacta: dilansg@gmail.com

Ver archivo [LICENSE](LICENSE) para más detalles.

## Contribuciones

Las contribuciones son bienvenidas siguiendo las directrices del proyecto:

1. Fork el repositorio
2. Crea una rama para tu feature: `git checkout -b feature/nueva-caracteristica`
3. Commit tus cambios: `git commit -am 'Agrega nueva característica'`
4. Push a la rama: `git push origin feature/nueva-caracteristica`
5. Abre un Pull Request

Ver [docs/DESARROLLO.md](docs/DESARROLLO.md) para guía completa de contribución.

## Soporte

- **Issues**: Reporta bugs o sugiere mejoras en [GitHub Issues](../../issues)
- **Documentación**: Consulta la carpeta `docs/` para guías detalladas
- **Email**: dilansag20@gmail.com

## Créditos

- **PyQt6**: Framework GUI multiplataforma
- **Python Community**: Herramientas y librerías
- **SQLite**: Base de datos embebida
- **bcrypt**: Encriptación de contraseñas

---

<div align="center">

**GesMonth v2.1.0**

Sistema profesional de gestión de pagos y cuotas mensuales

Desarrollado por Dilan Acuña | Licencia: Source Available (SAL)

[Documentación](docs/) | [Reportar Bug](../../issues) | [Sugerir Feature](../../issues)

</div>
