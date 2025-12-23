# GesMonth - Manual de Usuario Completo

## Índice
1. [Descripción general](#descripción-general)
2. [Instalación y requisitos](#instalación-y-requisitos)
3. [Primeros pasos](#primeros-pasos)
4. [Guía de pantallas](#guía-de-pantallas)
5. [Casos de uso detallados](#casos-de-uso-detallados)
6. [Solución de problemas](#solución-de-problemas)
7. [Mantenimiento y respaldos](#mantenimiento-y-respaldos)
8. [Preguntas frecuentes](#preguntas-frecuentes)

---

## Descripción general

### ¿Qué es GesMonth?
GesMonth es una aplicación de escritorio profesional diseñada para gestionar clientes, pagos mensuales y control de cuotas. Es ideal para pequeños negocios, academias, gimnasios o cualquier negocio con membresías o pagos recurrentes.

### Características principales
- **Gestión de clientes**: Registra información completa (nombre, documento, teléfono, cuota mensual)
- **Control de pagos**: Registra pagos con fecha, mes y método de pago
- **Seguimiento de cuotas**: Visualización mensual por año del estado de cada cliente (pagado/impago/pendiente)
- **Reportes Excel**: Exporta listas de clientes, historial de pagos y clientes en mora
- **Dashboard intuitivo**: Vista rápida de estadísticas clave del mes actual
- **Respaldos automáticos**: Crea copias de seguridad de tu base de datos
- **Búsqueda rápida**: Encuentra clientes por nombre o documento al instante

### Ventajas
- **Datos locales**: No depende de internet; toda la información está en tu computadora
- **Privacidad**: Tus datos nunca salen de tu equipo
- **Rápido y ligero**: Interfaz fluida sin latencia
- **Multiplataforma**: Funciona en Windows, Linux y Mac

---

## Instalación y requisitos

### Requisitos del sistema
- **Sistema operativo**: Windows 10+, Linux (Ubuntu 20.04+, Fedora 35+), macOS 11+
- **Python**: Versión 3.11 o superior
- **RAM**: Mínimo 2 GB (recomendado 4 GB)
- **Espacio en disco**: 100 MB para la aplicación + espacio para la base de datos (crece según uso)
- **Resolución**: Mínimo 1280x720 píxeles

### Instalación paso a paso

#### En Linux/Mac:
```bash
# 1. Asegúrate de tener Python 3.11+
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
- Versión: 1.0.0
- Última actualización: Diciembre 2025

---

## Notas finales
- **Respáldate frecuentemente**: Es tu responsabilidad
- **Prueba primero**: Si es tu primera vez, usa datos de prueba antes de datos reales
- **Lee este manual**: Ahorra tiempo y evita errores
- **Pregunta antes de eliminar**: Las eliminaciones son permanentes

¡Gracias por usar GesMonth!
