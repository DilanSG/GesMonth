@echo off
REM ============================================
REM GesMonth - Preparar Paquete de Distribución
REM Crea un ZIP listo para distribuir a usuarios
REM ============================================

REM Leer versión del archivo VERSION
set /p VERSION=<VERSION

echo ============================================
echo GesMonth - Preparar Distribución v%VERSION%
echo ============================================
echo.

REM Verificar que dist existe
if not exist "dist" (
    echo ERROR: La carpeta dist no existe
    echo Por favor compila primero con build.bat
    pause
    exit /b 1
)

REM Crear carpeta temporal
echo Creando paquete de distribución...
if exist "GesMonth-v%VERSION%-Windows" rmdir /s /q GesMonth-v%VERSION%-Windows
mkdir GesMonth-v%VERSION%-Windows

REM Copiar ejecutable y assets
echo Copiando archivos...
xcopy /E /I /Y dist\GesMonth GesMonth-v%VERSION%-Windows\GesMonth

REM Mover assets al nivel correcto (junto al ejecutable)
if exist "GesMonth-v%VERSION%-Windows\GesMonth\_internal\assets" (
    echo Moviendo assets al nivel del ejecutable...
    xcopy /E /I /Y GesMonth-v%VERSION%-Windows\GesMonth\_internal\assets GesMonth-v%VERSION%-Windows\GesMonth\assets
    rmdir /s /q GesMonth-v%VERSION%-Windows\GesMonth\_internal\assets
)

REM Copiar documentación con reemplazo de versión
echo Generando README con version %VERSION%...
powershell -Command "(Get-Content LEER_PRIMERO-WINDOWS.txt) -replace '{{VERSION}}', '%VERSION%' | Set-Content GesMonth-v%VERSION%-Windows\README.txt"
copy VERSION GesMonth-v%VERSION%-Windows\GesMonth\

REM Copiar licencia
copy LICENSE GesMonth-v%VERSION%-Windows\LICENSE.txt

REM Crear carpeta .data con archivos .db placeholder vacíos
echo Creando estructura de datos...
mkdir GesMonth-v%VERSION%-Windows\GesMonth\.data
type nul > GesMonth-v%VERSION%-Windows\GesMonth\.data\gesmonth.db
type nul > GesMonth-v%VERSION%-Windows\GesMonth\.data\users.db
REM Permisos de solo lectura (la app los eliminará y creará nuevos al iniciar)
attrib +R GesMonth-v%VERSION%-Windows\GesMonth\.data\gesmonth.db
attrib +R GesMonth-v%VERSION%-Windows\GesMonth\.data\users.db

REM Crear archivo ZIP
echo Comprimiendo...
powershell Compress-Archive -Path "GesMonth-v%VERSION%-Windows\*" -DestinationPath "GesMonth-v%VERSION%-Windows.zip" -Force

if errorlevel 1 (
    echo.
    echo ADVERTENCIA: No se pudo crear el ZIP automáticamente
    echo La carpeta GesMonth-v%VERSION%-Windows está lista para comprimir manualmente
) else (
    echo.
    echo ============================================
    echo Paquete creado exitosamente!
    echo ============================================
    echo.
    echo Archivo: GesMonth-v%VERSION%-Windows.zip
    echo.
    echo Este archivo está listo para distribuir.
    echo Los usuarios solo necesitan:
    echo 1. Descomprimir el ZIP
    echo 2. Entrar a la carpeta GesMonth\
    echo 3. Ejecutar GesMonth.exe
    echo.
)

echo Carpeta temporal: GesMonth-v%VERSION%-Windows\
echo.
pause
