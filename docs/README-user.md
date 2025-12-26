# GesMonth v2.1.0 - Manual de Usuario

## Tabla de Contenidos

1. [Introducción](#introducción)
2. [Primeros Pasos](#primeros-pasos)
3. [Sistema de Autenticación](#sistema-de-autenticación)
4. [Navegación](#navegación)
5. [Dashboard](#dashboard)
6. [Gestión de Clientes](#gestión-de-clientes)
7. [Control de Cuotas](#control-de-cuotas)
8. [Registro de Pagos](#registro-de-pagos)
9. [Reportes](#reportes)
10. [Configuración](#configuración)
11. [Gestión de Usuarios](#gestión-de-usuarios)
12. [Solución de Problemas](#solución-de-problemas)
13. [Preguntas Frecuentes](#preguntas-frecuentes)

---

## Introducción

### ¿Qué es GesMonth?

GesMonth es un sistema profesional de escritorio para la gestión de pagos y cuotas mensuales. Diseñado específicamente para pequeños negocios, academias, centros de formación, gimnasios y cualquier organización que maneje cobros recurrentes.

### Características Principales

- **Sistema de autenticación multi-nivel**: 4 roles de usuario con permisos específicos
- **Dashboard inteligente**: Métricas en tiempo real del estado del negocio
- **Gestión completa de clientes**: Alta, baja, modificación y búsqueda avanzada
- **Control visual de cuotas**: Grid mensual con estados (Pagado, Impago, Con Deuda, Pendiente)
- **Seguimiento de mora**: Control automático de fechas de inicio de mora
- **Pagos parciales**: Soporte para abonos y deudas acumuladas
- **Reportes detallados**: Estadísticas por período y método de pago
- **Temas personalizables**: Modo claro y oscuro con persistencia
- **Respaldos seguros**: Exportación manual de base de datos
- **Datos locales**: Sin internet, máxima privacidad

### Ventajas

- **Privacidad total**: Todos los datos permanecen en tu equipo
- **Sin dependencias**: No requiere internet ni servidores externos
- **Multiplataforma**: Windows, Linux y macOS
- **Interfaz moderna**: Diseño glassmorphism profesional
- **Rápido y eficiente**: Sin latencia de red
- **Seguro**: Contraseñas encriptadas con bcrypt

---

## Primeros Pasos

### Requisitos del Sistema

**Mínimos:**
- Sistema operativo: Windows 10+, Linux (Ubuntu 20.04+), macOS 11+
- RAM: 2 GB
- Espacio en disco: 200 MB
- Resolución: 1024x768 píxeles

**Recomendados:**
- RAM: 4 GB o más
- Resolución: 1920x1080 píxeles o superior

### Instalación

#### Windows

1. Descargar `GesMonth-v2.1.0-Windows.zip`
2. Descomprimir el archivo
3. Abrir la carpeta `GesMonth/`
4. Ejecutar `GesMonth.exe`

#### Linux

1. Descargar `GesMonth-v2.1.0-Linux.tar.gz`
2. Abrir terminal y ejecutar:
   ```bash
   tar -xzf GesMonth-v2.1.0-Linux.tar.gz
   cd GesMonth-v2.1.0-Linux/GesMonth
   ./GesMonth
   ```

### Primera Ejecución

Al ejecutar GesMonth por primera vez:

1. Se mostrará un **splash screen** durante la carga
2. Aparecerá la **pantalla de login**
3. Usa las credenciales por defecto:
   ```
   Usuario: admin
   Contraseña: admin123
   ```
4. **IMPORTANTE**: Cambia la contraseña inmediatamente después del primer acceso

La aplicación creará automáticamente dos bases de datos en la carpeta `.data/`:
- `gesmonth.db`: Datos del negocio (clientes, cuotas, pagos)
- `users.db`: Usuarios y sesiones

---

## Sistema de Autenticación

### Niveles de Acceso

GesMonth implementa 4 niveles de roles con permisos diferenciados:

#### 1. Superadmin
- **Acceso completo** a todas las funciones
- Puede **gestionar usuarios** (crear, editar, eliminar)
- Acceso a **auditoría del sistema**
- Única persona que puede cambiar roles
- Por defecto: usuario `admin`

#### 2. Admin
- Acceso completo a gestión de negocio
- Puede gestionar clientes, cuotas y pagos
- Acceso a reportes y configuración
- **NO** puede gestionar usuarios

#### 3. Operador
- Puede ver y registrar pagos
- Puede buscar y ver información de clientes
- **NO** puede eliminar registros
- **NO** puede acceder a configuración avanzada

#### 4. Solo Lectura
- Solo puede **consultar** información
- Ver dashboard, clientes y reportes
- **NO** puede modificar ni registrar datos
- Ideal para supervisores o contadores

### Cambio de Contraseña

Para cambiar tu contraseña:

1. Ir a **Configuración**
2. Sección **"Usuario"** (aparece tu nombre)
3. Click en **"Cambiar Contraseña"**
4. Ingresar contraseña actual
5. Ingresar nueva contraseña (2 veces)
6. Confirmar

**Requisitos de contraseña:**
- Mínimo 6 caracteres
- Se recomienda usar mayúsculas, minúsculas y números

### Seguridad

- **Encriptación bcrypt**: Las contraseñas nunca se guardan en texto plano
- **Bloqueo automático**: Tras 5 intentos fallidos, la cuenta se bloquea por 15 minutos
- **Sesiones seguras**: Tokens únicos por sesión
- **Auditoría**: Todas las acciones importantes quedan registradas

---

## Navegación

### Barra Lateral (Sidebar)

La navegación principal se encuentra en el lado izquierdo de la ventana:

1. **Home** (Dashboard): Vista general del negocio
2. **Clientes**: Gestión de clientes
3. **Cuotas**: Control mensual de pagos
4. **Reportes**: Estadísticas y análisis
5. **Configuración**: Ajustes del sistema

### Header

En la parte superior encontrarás:
- **Nombre de usuario** actual
- **Fecha y hora** en tiempo real
- **Botón de logout** (cerrar sesión)
- **Botón de apagado** (salir de la aplicación)

### Atajos de Teclado

- **Esc**: Cerrar diálogos o cancelar acciones
- **Enter**: Confirmar en formularios
- **Ctrl+F**: Enfocar campo de búsqueda (donde aplique)

---

## Dashboard

El Dashboard muestra métricas clave del estado actual del negocio.

### Tarjetas de Información

**Total Clientes:**
- Cantidad de clientes activos en el sistema
- No incluye clientes inactivos

**Clientes en Mora:**
- Clientes con último mes registrado como "Impago"
- Color rojo indica alerta

**Clientes al Día:**
- Clientes con pagos al corriente
- Color verde indica estado positivo

**Total Recaudado (Mes Actual):**
- Suma de todos los pagos del mes en curso
- Se actualiza en tiempo real
- Formato de moneda local

**Total Recaudado (Año):**
- Suma de todos los pagos del año en curso
- Permite visualizar tendencia anual

### Actualización de Datos

El Dashboard se actualiza automáticamente al:
- Abrir la vista
- Registrar un nuevo pago
- Cambiar estado de una cuota
- Activar/desactivar clientes

---

## Gestión de Clientes

### Agregar Nuevo Cliente

1. Click en **"Agregar Cliente"**
2. Completar el formulario:
   - **Nombre**: Nombre completo
   - **Documento**: DNI, RUT, CC (único por cliente)
   - **Teléfono**: Número de contacto (opcional)
   - **Valor Cuota**: Monto mensual a cobrar
   - **Día de Cobro**: Día del mes (1-31)
3. Click en **"Guardar"**

**Validaciones:**
- El documento debe ser único (no duplicados)
- El valor de cuota debe ser mayor a 0
- El día de cobro debe estar entre 1 y 31

### Buscar Clientes

El campo de búsqueda en la parte superior permite filtrar por:
- Nombre (coincidencia parcial)
- Documento (coincidencia exacta)

La búsqueda es **instantánea** conforme escribes.

### Editar Cliente

1. Seleccionar cliente de la lista
2. Click en **"Editar"**
3. Modificar los campos necesarios
4. **Guardar cambios**

**Nota**: El documento no se puede cambiar una vez creado el cliente.

### Desactivar Cliente

En lugar de eliminar, se recomienda **desactivar**:

1. Seleccionar cliente
2. Click en **"Desactivar"**
3. El cliente desaparece de las vistas activas
4. Sus datos históricos se conservan

Para reactivar: Filtrar por "Inactivos" y click en "Activar"

### Eliminar Cliente

**Advertencia**: Esta acción es irreversible y elimina:
- Datos del cliente
- Todas sus cuotas registradas
- Todo su historial de pagos

Solo usar en casos excepcionales.

---

## Control de Cuotas

La vista de Cuotas muestra un grid visual organizado por año y mes.

### Grid de Meses

Cada cliente tiene 12 casillas por año, una por mes:

- **Verde (Pago)**: Cuota completamente pagada
- **Rojo (Impago)**: Sin pago registrado, genera mora
- **Amarillo (Con Deuda)**: Pago parcial o deuda heredada
- **Gris (Pendiente)**: Mes aún no vencido

### Seleccionar Año

En la parte superior, dropdown para seleccionar el año a visualizar.
Los años disponibles se configuran en **Configuración > Años de Facturación**.

### Registrar Pago

1. Click en el **mes** del cliente
2. Seleccionar **"Registrar Pago"**
3. Completar:
   - **Monto**: Cantidad pagada
   - **Método de pago**: Efectivo, Transferencia, etc.
   - **Fecha**: Por defecto es hoy
4. **Guardar**

**Comportamiento:**
- Si el monto cubre la cuota completa: Estado → "Pago"
- Si el monto es menor: Estado → "Con Deuda"
- La deuda acumulada se calcula automáticamente

### Marcar Impago

1. Click en el **mes** del cliente
2. Seleccionar **"Marcar como Impago"**
3. Confirmar

**Efecto:**
- Estado cambia a "Impago"
- Se registra fecha de inicio de mora
- El cliente aparece en "Clientes en Mora" del Dashboard

### Pago Parcial

Si un cliente paga menos del monto total:

1. Registrar el pago con el monto real
2. El sistema calcula la deuda: `Valor Cuota - Monto Pagado`
3. La deuda se **acumula** al siguiente mes

**Ejemplo:**
- Cuota: $100
- Pago: $60
- Deuda: $40
- Siguiente mes: $100 + $40 = $140 total a pagar

### Ver Detalles

Click en cualquier mes para ver el dialog de detalles:
- Historial de pagos del mes
- Deuda acumulada
- Fecha de mora (si aplica)
- Botones de acción rápida

---

## Registro de Pagos

### Vista de Pagos

Muestra el historial completo de pagos registrados:
- Fecha de pago
- Cliente
- Mes correspondiente
- Monto
- Método de pago

### Filtros

- **Por cliente**: Buscar por nombre
- **Por mes**: Filtrar por período (YYYY-MM)
- **Por método**: Solo pagos de un método específico

### Prevención de Duplicados

El sistema automáticamente previene registrar el mismo pago dos veces:
- Ventana de 5 segundos entre pagos del mismo cliente
- Alerta visual si se detecta duplicación potencial

### Eliminar Pago

Solo superadmin y admin pueden eliminar pagos.

**Precaución**: Al eliminar un pago:
- Se recalcula el estado de la cuota
- Se actualiza la deuda acumulada
- Puede afectar meses posteriores si había deuda

---

## Reportes

### Estadísticas Generales

Seleccionar **Año** y **Mes** para ver:

**Métricas de Cuotas:**
- Total cuotas registradas
- Cantidad pagadas
- Cantidad sin pagar (impagos)
- Cantidad con deuda parcial

**Por Método de Pago:**
- Desglose de montos por cada método
- Total recaudado por método
- Porcentaje de uso

### Exportación (Próximamente)

En versiones futuras se podrá exportar a Excel:
- Lista de clientes
- Historial de pagos
- Clientes en mora
- Reportes personalizados

---

## Configuración

### Métodos de Pago

Administra los métodos disponibles para registrar pagos:

**Agregar método:**
1. Ingresar nombre (ej: "Tarjeta de Crédito")
2. Click en "Agregar"

**Editar método:**
1. Seleccionar de la lista
2. Cambiar nombre
3. Guardar

**Desactivar método:**
- Los métodos no se eliminan, se desactivan
- Esto preserva el historial de pagos anteriores

### Años de Facturación

Define qué años aparecen en el Control de Cuotas:

- Por defecto: Año actual
- Agregar años anteriores o futuros según necesidad
- Los años se muestran en orden descendente

### Temas

Cambiar entre modo claro y oscuro:

1. Toggle en **"Tema Oscuro"**
2. El cambio es instantáneo
3. La preferencia se guarda para próximas sesiones

### Pantalla Completa

Activar/desactivar modo pantalla completa:
- Útil para maximizar espacio de trabajo
- La preferencia se guarda automáticamente

### Mantenimiento

**Respaldar Base de Datos:**
1. Click en "Respaldar Base de Datos"
2. Seleccionar ubicación
3. Se crea archivo `.db` con fecha y hora

**Recomendación**: Hacer respaldos semanales o antes de cambios importantes.

**Limpiar Pagos Duplicados:**
- Busca y elimina pagos duplicados automáticamente
- Útil si se detectan inconsistencias

### Reiniciar Aplicación

Cierra y reabre GesMonth (útil tras cambios de configuración importantes).

---

## Gestión de Usuarios

**Solo disponible para Superadmin**

### Crear Usuario

1. Ir a **Configuración > Gestión de Usuarios**
2. Click en **"Agregar Usuario"**
3. Completar:
   - Nombre de usuario (único)
   - Contraseña
   - Rol (Superadmin, Admin, Operador, Solo Lectura)
4. Guardar

### Editar Usuario

- Cambiar rol
- Resetear contraseña
- Activar/desactivar

### Auditoría

Ver registro completo de acciones:
- Usuario que realizó la acción
- Fecha y hora
- Tabla afectada
- Detalles de la operación

Útil para:
- Rastrear cambios importantes
- Resolver discrepancias
- Seguridad y control

---

## Solución de Problemas

### La aplicación no inicia

**Windows:**
- Verificar que todas las carpetas estén presentes: `GesMonth.exe`, `assets/`, `_internal/`, `.data/`
- Ejecutar desde cmd para ver errores
- Revisar antivirus (puede bloquear ejecutables desconocidos)

**Linux:**
- Dar permisos de ejecución: `chmod +x GesMonth`
- Instalar dependencias Qt6: `sudo apt install qt6-base-dev`
- Ejecutar desde terminal para ver mensajes de error

### No se ven los estilos

- Verificar que la carpeta `assets/` esté junto al ejecutable
- No mover archivos fuera de su ubicación original
- Reinstalar si el problema persiste

### Error al guardar datos

- Verificar permisos de escritura en la carpeta `.data/`
- Asegurar espacio en disco disponible
- Si el problema continúa, restaurar desde un respaldo

### Olvidé mi contraseña

**Si eres superadmin:**
- Solo otro superadmin puede resetear tu contraseña
- Si eres el único superadmin, contactar soporte técnico

**Si no eres superadmin:**
- Solicitar al superadmin que resetee tu contraseña

### Datos inconsistentes

1. Ir a **Configuración > Mantenimiento**
2. Ejecutar **"Limpiar Pagos Duplicados"**
3. Hacer **respaldo** de la base de datos
4. Si persiste, restaurar desde respaldo anterior

### Actualización de versión

Al actualizar GesMonth:
1. **Hacer respaldo** de `.data/gesmonth.db` y `.data/users.db`
2. Descomprimir nueva versión
3. Copiar archivos `.data/` de la versión anterior
4. Ejecutar nueva versión

---

## Preguntas Frecuentes

**¿Necesito internet para usar GesMonth?**
- No. GesMonth funciona completamente offline.

**¿Dónde se guardan mis datos?**
- En la carpeta `.data/` junto al ejecutable, en archivos SQLite.

**¿Puedo usar GesMonth en varios equipos?**
- Sí, pero deberás copiar manualmente la carpeta `.data/` entre equipos.
- No hay sincronización automática.

**¿Cuántos clientes puedo registrar?**
- Prácticamente ilimitado. SQLite soporta millones de registros.

**¿Puedo exportar mis datos?**
- Sí, haciendo respaldo de las bases de datos (archivos `.db`)
- Exportación a Excel próximamente

**¿Es seguro?**
- Sí. Contraseñas encriptadas, datos locales, sin conexión a internet.

**¿Cómo actualizo la aplicación?**
- Descargar nueva versión, copiar archivos `.data/` a la nueva instalación.

**¿Puedo cambiar los colores o el tema?**
- Los archivos QSS en `assets/styles/` se pueden editar manualmente.
- Requiere conocimientos de CSS.

**¿Hay versión móvil?**
- No. GesMonth está diseñado para escritorio.

**¿Puedo generar facturas?**
- Actualmente no. Está en el roadmap de futuras versiones.

---

## Soporte y Contacto

**Documentación adicional:**
- [Guía de Desarrollo](DESARROLLO.md)
- [Sistema de Autenticación](SISTEMA-AUTENTICACION.md)
- [Compilación](BUILD.md)

**Reportar problemas:**
- GitHub Issues: https://github.com/DIlanSG/GesMonth/issues
- Email: dilansg@gesmonth.com

**Antes de reportar:**
- Verificar que estás usando la última versión
- Revisar esta guía y la sección de solución de problemas
- Incluir capturas de pantalla y pasos para reproducir el error

---

**GesMonth v2.1.0** - Sistema de Gestión de Pagos Mensuales

Desarrollado por Dilan Acuña | Licencia: Source Available (SAL)

Última actualización: 26 de diciembre de 2025
python3 --version

# 2. Ve a la carpeta del proyecto
cd /ruta/a/GesMonth

# 3. Instala las dependencias
chmod +x install.sh
./install.sh

# 4. Ejecuta la aplicación
./run.sh
```

#### En Windows:
```cmd
# 1. Verifica Python (PowerShell o CMD)
python --version

# 2. Ve a la carpeta del proyecto
cd C:\ruta\a\GesMonth

# 3. Instala las dependencias (doble clic o desde CMD)
install.bat

# 4. Ejecuta la aplicación
run.bat
```

#### Instalación manual:
```bash
pip install -r requirements.txt
python main.py
```

---

## Primeros pasos

### Primera ejecución
1. Al abrir la app por primera vez, se creará automáticamente el archivo `gesmonth.db` (base de datos)
2. La aplicación abrirá en pantalla completa mostrando el Dashboard
3. Inicialmente no verás datos; es normal, empecemos a configurar

### Configuración inicial recomendada

#### Paso 1: Configurar métodos de pago
1. Ve a **Configuración** (última opción del menú lateral)
2. En la pestaña "Configuración para Pagos", sección "Métodos de Pago"
3. Haz clic en "Agregar Método"
4. Agrega los métodos que uses (ej: Efectivo, Transferencia, Tarjeta, QR)
5. Repite para cada método

#### Paso 2: Configurar años de facturación
1. En la misma pantalla de Configuración
2. Sección "Años de Facturación"
3. Selecciona el primer año y segundo año (ej: 2025 y 2026)
4. Haz clic en "Guardar Años"
5. Estos años aparecerán en la vista de Cuotas

#### Paso 3: Agregar tu primer cliente
1. Ve a **Clientes**
2. Haz clic en "Agregar Cliente"
3. Completa los campos:
   - **Nombre**: Nombre completo del cliente
   - **Documento**: DNI, CI, pasaporte (debe ser único)
   - **Teléfono**: Opcional pero recomendado
   - **Cuota Mensual**: Valor que paga mensualmente
   - **Estado**: Activo (por defecto)
4. Haz clic en "Guardar"

---

## Guía de pantallas

### 1. Dashboard (Inicio)
**Qué muestra:**
- Total recaudado en el mes actual
- Cantidad de clientes activos
- Clientes al día (pagaron este mes)
- Clientes en mora (no pagaron este mes)

**Cuándo usar:**
- Al iniciar la app para ver el estado general
- Para verificar rápidamente cuántos clientes faltan por pagar

### 2. Clientes
**Funciones disponibles:**
- **Agregar**: Botón superior derecho, abre formulario
- **Buscar**: Barra de búsqueda superior (busca por nombre o documento)
- **Editar**: Botón "Editar" en cada fila de la tabla
- **Eliminar**: Botón "Eliminar" (cuidado: borra todo su historial)

**Campos de cada cliente:**
- Nombre, Documento, Teléfono, Cuota Mensual, Estado

**Consejos:**
- Usa el buscador si tienes muchos clientes
- El documento debe ser único; la app no permite duplicados
- Al eliminar un cliente, se borran todos sus pagos y cuotas registradas
- Puedes cambiar el estado a "inactivo" si quieres mantener el historial pero ocultarlo

### 3. Pagos
**Funciones disponibles:**
- **Registrar Pago**: Botón superior derecho
- **Ver historial**: Tabla con todos los pagos registrados
- **Eliminar**: Botón en cada fila (útil para corregir errores)

**Al registrar un pago:**
1. Selecciona el cliente de la lista desplegable
2. Fecha del pago (por defecto: hoy)
3. Mes correspondiente (formato YYYY-MM, ej: 2025-01 para enero)
4. Monto (puede ser diferente a la cuota si hay descuentos/recargos)

**Comportamiento automático:**
- Al registrar un pago, la cuota correspondiente se marca como "pagada" automáticamente
- Aparece en el historial al instante
- Se actualiza el dashboard

### 4. Cuotas (Control mensual)
**Qué muestra:**
- Tarjetas por cliente con su información
- Grid de 12 meses por cada año configurado
- Estados visuales: Pagado (verde), Impago (rojo), Pendiente (gris)

**Cómo usar:**
1. Busca el cliente (barra superior)
2. Identifica el mes en el grid
3. Haz clic en la celda del mes
4. Elige:
   - **Registrar Pago**: Te pide el método de pago y marca como pagado
   - **Registrar Impago**: Marca que el cliente NO pagó ese mes (útil para llevar control de deudas)
   - **Cancelar**: Cierra el diálogo

**Estados posibles:**
- **Pagado**: Cliente pagó ese mes
- **Impago**: Cliente NO pagó ese mes (registrado explícitamente)
- **Pendiente**: Sin información aún (gris)

**Si ya está registrado:**
- Al hacer clic, pregunta si deseas eliminarlo
- Útil para corregir errores

### 5. Reportes
**Tipos de reportes disponibles:**

1. **Exportar Lista de Clientes**
   - Contiene: ID, Nombre, Documento, Teléfono, Cuota Mensual, Estado
   - Útil para: Respaldo, análisis externo, impresión

2. **Exportar Historial de Pagos**
   - Contiene: ID, Cliente, Documento, Fecha Pago, Mes Correspondiente, Monto
   - Útil para: Contabilidad, auditoría, declaraciones

3. **Exportar Clientes en Mora**
   - Contiene: ID, Nombre, Documento, Teléfono, Último Pago
   - Útil para: Cobranza, seguimiento de deudores

**Cómo exportar:**
1. Haz clic en el botón del reporte deseado
2. Elige ubicación y nombre del archivo
3. Se genera un `.xlsx` (Excel) que puedes abrir con Excel, LibreOffice, Google Sheets

### 6. Configuración
**Pestaña "General":**
- Pantalla Completa: Activa/desactiva modo fullscreen
- Crear Respaldo: Genera copia de `gesmonth.db` con timestamp

**Pestaña "Configuración para Pagos":**
- **Años de Facturación**: Define qué años mostrar en Cuotas (útil al cambiar de año)
- **Métodos de Pago**: Administra lista de métodos (Efectivo, Transferencia, etc.)

**Botón "Salir":**
- Cierra la aplicación completamente

---

## Casos de uso detallados

### Caso 1: Registrar pago del mes actual
**Escenario:** María pagó su cuota de enero 2025 el día 5 de enero.

**Flujo:**
1. Ve a **Pagos** → "Registrar Pago"
2. Selecciona "María García" en Cliente
3. Fecha: 2025-01-05 (5 de enero)
4. Mes correspondiente: 2025-01
5. Monto: (aparece el valor de su cuota, puedes cambiarlo si es diferente)
6. Haz clic en "Guardar"

**Resultado:**
- Aparece en la tabla de Pagos
- En Cuotas, el mes de enero aparece como "Pagado" (verde)
- El dashboard muestra 1 cliente más "al día"

---

### Caso 2: Registrar pago atrasado
**Escenario:** Pedro viene en marzo a pagar febrero, que ya pasó.

**Flujo:**
1. Ve a **Pagos** → "Registrar Pago"
2. Selecciona "Pedro López"
3. Fecha: 2025-03-10 (hoy, cuando realmente pagó)
4. Mes correspondiente: 2025-02 (el mes que está pagando)
5. Monto: (su cuota)
6. Guardar

**Resultado:**
- El pago aparece con fecha marzo pero corresponde a febrero
- En Cuotas, febrero se marca como "Pagado"
- Útil para llevar historial real de cuándo pagó vs. qué mes pagó

---

### Caso 3: Cliente que nunca pagó un mes
**Escenario:** Ana no pagó enero y ya estamos en febrero; quieres registrarlo como impago.

**Flujo:**
1. Ve a **Cuotas**
2. Busca "Ana"
3. Haz clic en la celda de "Enero"
4. Selecciona "Registrar Impago"
5. Confirma

**Resultado:**
- Enero queda marcado como "Impago" (rojo)
- Se acumula la deuda conceptualmente
- En Reportes → "Clientes en Mora" aparecerá Ana

---

### Caso 4: Error al registrar un pago
**Escenario:** Registraste un pago por error (mes incorrecto, monto incorrecto).

**Flujo - Opción 1 (desde Pagos):**
1. Ve a **Pagos**
2. Busca el pago en la tabla
3. Haz clic en "Eliminar" en esa fila
4. Confirma
5. Registra el pago correctamente de nuevo

**Flujo - Opción 2 (desde Cuotas):**
1. Ve a **Cuotas**
2. Busca el cliente y el mes
3. Haz clic en la celda del mes
4. Confirma eliminar
5. Registra correctamente

---

### Caso 5: Cambio de cuota mensual
**Escenario:** Carlos tenía cuota de $1000, ahora será $1200 desde marzo.

**Flujo:**
1. Ve a **Clientes**
2. Busca "Carlos"
3. Haz clic en "Editar"
4. Cambia "Cuota Mensual" a 1200
5. Guardar

**Resultado:**
- Los pagos futuros tomarán la nueva cuota como referencia
- Los pagos ya registrados no cambian
- En Cuotas, los meses siguientes mostrarán el nuevo valor al registrar

---

### Caso 6: Exportar para contabilidad mensual
**Escenario:** Fin de mes, necesitas enviar un reporte a tu contador.

**Flujo:**
1. Ve a **Reportes**
2. Haz clic en "Exportar Historial de Pagos"
3. Guarda como `pagos_enero_2025.xlsx`
4. Abre el Excel
5. Filtra por mes si es necesario
6. Envía al contador

**Tip adicional:**
- Puedes importar el Excel en software de contabilidad
- Si usas Google Sheets, sube el archivo para trabajar online

---

### Caso 7: Inicio de año nuevo
**Escenario:** Es enero 2026, quieres ver las cuotas de 2026.

**Flujo:**
1. Ve a **Configuración**
2. Sección "Años de Facturación"
3. Cambia primer año a 2025 y segundo a 2026 (o 2026 y 2027)
4. Haz clic en "Guardar Años"
5. Ve a **Cuotas**
6. Ahora verás los meses de 2026 disponibles

---

## Solución de problemas

### La aplicación no abre
**Posibles causas y soluciones:**

1. **Error: Python no encontrado**
   - Solución: Instala Python 3.11+ desde python.org
   - Verifica: `python --version` o `python3 --version`

2. **Error: ModuleNotFoundError (PyQt6, pandas, etc.)**
   - Solución: Ejecuta `pip install -r requirements.txt`
   - Si persiste: `pip install PyQt6 pandas openpyxl`

3. **Error: Permission denied (Linux/Mac)**
   - Solución: `chmod +x run.sh` y luego `./run.sh`

4. **Pantalla negra o se cierra inmediatamente**
   - Solución: Ejecuta desde terminal para ver el error
   - `python main.py` y revisa el mensaje

### No puedo agregar un cliente
**Error: "Ya existe un cliente con este documento"**
- Causa: El documento ya está registrado
- Solución: Usa un documento diferente o busca el cliente existente

**Los campos no se guardan**
- Verifica que Nombre y Documento no estén vacíos
- El valor de cuota debe ser mayor o igual a 0

### Los pagos no aparecen en el dashboard
- Verifica que el mes correspondiente sea del mes actual
- Dashboard solo cuenta pagos del mes en curso
- Si el pago es de un mes pasado, aparecerá en Pagos pero no en estadísticas del dashboard

### No veo los años en Cuotas
- Ve a Configuración → Años de Facturación
- Guarda los años deseados
- Vuelve a Cuotas (refresca navegando a otra vista y volviendo)

### La exportación a Excel falla
**Error: "No se pudo generar el reporte"**
- Verifica que tengas permisos de escritura en la carpeta destino
- Cierra el archivo Excel si ya está abierto
- Intenta guardar en otra ubicación

### Pantalla completa no se puede salir
- Presiona tecla `Esc` (puede no funcionar según tu sistema)
- Ve a Configuración → Desactiva "Pantalla Completa"
- Alternativa: Cierra y abre de nuevo, cambia configuración antes de usar la app

### Base de datos corrupta
**Error: "database disk image is malformed"**
- Causa: Cierre inesperado, fallo de disco
- Solución:
  1. Cierra la app
  2. Busca el último respaldo en la carpeta (`backup_database_*.db`)
  3. Renombra `gesmonth.db` a `gesmonth_old.db`
  4. Renombra el respaldo a `gesmonth.db`
  5. Abre la app

### La app está muy lenta
- Verifica que no tengas miles de registros (SQLite es rápido pero no infinito)
- Exporta reportes y archiva clientes antiguos (cámbialos a "inactivo")
- Cierra otras aplicaciones pesadas
- Considera crear una nueva base cada año (respaldo de la anterior)

---

## Mantenimiento y respaldos

### Respaldos automáticos
**Frecuencia recomendada:**
- Diario: Si registras muchos pagos
- Semanal: Uso moderado
- Mensual: Uso ligero

**Cómo hacer un respaldo:**
1. Ve a **Configuración**
2. Haz clic en "Crear Respaldo de Base de Datos"
3. Se genera `backup_database_YYYYMMDD_HHMMSS.db` en la carpeta del proyecto

**Respaldo manual (adicional):**
- Copia `gesmonth.db` a otra ubicación
- Usa servicios cloud (Dropbox, Google Drive, OneDrive)
- Copia en USB periódicamente

### Limpieza de datos antiguos
**Opción 1: Archivar clientes**
1. Clientes → Editar cliente
2. Cambia estado a "inactivo"
3. Ya no aparecerá en conteos del dashboard

**Opción 2: Exportar y borrar**
1. Exporta todos los reportes que necesites
2. Guarda los Excel en lugar seguro
3. Elimina clientes antiguos si no los necesitas

**Opción 3: Nueva base cada año**
1. Haz respaldo de `gesmonth.db` (renómbralo `gesmonth_2024.db`)
2. Elimina `gesmonth.db`
3. Al abrir la app se crea nueva base vacía
4. Vuelve a configurar años y métodos de pago

### Ubicación de archivos importantes
- Base de datos: `/ruta/proyecto/gesmonth.db`
- Respaldos: `/ruta/proyecto/backup_database_*.db`
- Estilos: `/ruta/proyecto/assets/styles/main.qss`

---

## Preguntas frecuentes

### ¿Puedo usar esto en varios equipos?
Sí, pero la base de datos está en cada equipo. Para sincronizar:
- Opción 1: Copia `gesmonth.db` entre equipos manualmente
- Opción 2: Usa la carpeta del proyecto en una carpeta sincronizada (Dropbox, etc.)
- Nota: No abras la app en dos equipos simultáneamente o habrá conflictos

### ¿Los datos están seguros?
- Están en tu equipo, no en internet
- Haz respaldos frecuentes
- Usa antivirus actualizado
- Si quieres cifrado, cifra la carpeta completa del proyecto

### ¿Puedo personalizar los colores?
Sí, edita `assets/styles/main.qss` (requiere conocimientos de QSS/CSS)

### ¿Cuántos clientes puedo tener?
SQLite soporta millones de registros, pero la interfaz se optimizó para hasta ~1000 clientes activos con buen rendimiento.

### ¿Hay versión móvil?
No actualmente, es solo para escritorio.

### ¿Puedo cambiar el idioma?
Actualmente solo en español. Cambiar el idioma requiere modificar el código fuente.

### ¿Cómo actualizo la aplicación?
1. Haz respaldo de `gesmonth.db`
2. Descarga la nueva versión
3. Copia tu `gesmonth.db` a la nueva carpeta
4. Ejecuta la nueva versión

### ¿Qué hago si encuentro un error?
1. Anota el mensaje de error exacto
2. Verifica si está en "Solución de problemas"
3. Contacta al desarrollador con:
   - Mensaje de error
   - Qué estabas haciendo
   - Sistema operativo y versión de Python

---

## Contacto y soporte
- Desarrollador: Dilan Acuña
- Versión: 1.0.1
- Última actualización: Diciembre 2025

---

## Notas finales
- **Respáldate frecuentemente**: Es tu responsabilidad
- **Prueba primero**: Si es tu primera vez, usa datos de prueba antes de datos reales
- **Lee este manual**: Ahorra tiempo y evita errores
- **Pregunta antes de eliminar**: Las eliminaciones son permanentes

¡Gracias por usar GesMonth!
