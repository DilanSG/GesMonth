@echo off
REM ============================================
REM GesMonth - Preparar Paquete de Distribución
REM Crea un ZIP listo para distribuir a usuarios
REM ============================================

echo ============================================
echo GesMonth - Preparar Distribución v1.0.0
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
if exist "GesMonth-v1.0.0-Windows" rmdir /s /q GesMonth-v1.0.0-Windows
mkdir GesMonth-v1.0.0-Windows

REM Copiar ejecutable y assets
echo Copiando archivos...
xcopy /E /I /Y dist GesMonth-v1.0.0-Windows

REM Copiar documentación para usuarios
copy LEER_PRIMERO.txt GesMonth-v1.0.0-Windows\
copy VERSION GesMonth-v1.0.0-Windows\

REM Crear archivo de licencia simple
echo GesMonth v1.0.0 > GesMonth-v1.0.0-Windows\LICENSE.txt
echo. >> GesMonth-v1.0.0-Windows\LICENSE.txt
echo Este software es de código abierto. >> GesMonth-v1.0.0-Windows\LICENSE.txt
echo Disponible para uso personal, educativo y comercial. >> GesMonth-v1.0.0-Windows\LICENSE.txt
echo. >> GesMonth-v1.0.0-Windows\LICENSE.txt
echo Desarrollado por Dilan Acuña >> GesMonth-v1.0.0-Windows\LICENSE.txt
echo Diciembre 2025 >> GesMonth-v1.0.0-Windows\LICENSE.txt

REM Crear archivo ZIP
echo Comprimiendo...
powershell Compress-Archive -Path "GesMonth-v1.0.0-Windows\*" -DestinationPath "GesMonth-v1.0.0-Windows.zip" -Force

if errorlevel 1 (
    echo.
    echo ADVERTENCIA: No se pudo crear el ZIP automáticamente
    echo La carpeta GesMonth-v1.0.0-Windows está lista para comprimir manualmente
) else (
    echo.
    echo ============================================
    echo Paquete creado exitosamente!
    echo ============================================
    echo.
    echo Archivo: GesMonth-v1.0.0-Windows.zip
    echo.
    echo Este archivo está listo para distribuir.
    echo Los usuarios solo necesitan:
    echo 1. Descomprimir el ZIP
    echo 2. Ejecutar GesMonth.exe
    echo.
)

echo Carpeta temporal: GesMonth-v1.0.0-Windows\
echo.
pause
