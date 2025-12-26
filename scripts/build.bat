@echo off
REM ============================================
REM GesMonth - Script de compilacion para Windows
REM Genera el ejecutable standalone con PyInstaller
REM ============================================

echo ============================================
echo GesMonth - Compilador v1.0.1
echo ============================================
echo.

REM Verificar que el entorno virtual este activado
if not exist "venv\Scripts\activate.bat" (
    echo ERROR: No se encontro el entorno virtual
    echo Por favor ejecuta install.bat primero
    pause
    exit /b 1
)

REM Activar entorno virtual
echo Activando entorno virtual...
call venv\Scripts\activate.bat

REM Verificar PyInstaller
echo Verificando PyInstaller...
pip show pyinstaller >nul 2>&1
if errorlevel 1 (
    echo PyInstaller no esta instalado. Instalando...
    pip install pyinstaller==6.3.0
    if errorlevel 1 (
        echo ERROR: No se pudo instalar PyInstaller
        pause
        exit /b 1
    )
)

echo.
echo ============================================
echo Limpiando compilaciones anteriores...
echo ============================================
if exist "build" rmdir /s /q build
if exist "dist" rmdir /s /q dist
if exist "GesMonth.exe" del /f GesMonth.exe

echo.
echo ============================================
echo Compilando aplicacion...
echo ============================================
echo Esto puede tardar varios minutos...
echo.

pyinstaller --clean --noconfirm gesmonth.spec

if errorlevel 1 (
    echo.
    echo ERROR: La compilacion fallo
    pause
    exit /b 1
)

echo.
echo ============================================
echo Compilacion exitosa!
echo ============================================
echo.
echo El ejecutable se encuentra en: dist\GesMonth.exe
echo.
echo Para distribuir la aplicacion:
echo 1. Copia la carpeta 'dist' completa
echo 2. Puedes renombrar 'dist' a 'GesMonth'
echo 3. Dentro estara el ejecutable GesMonth.exe
echo.
echo IMPORTANTE: El ejecutable necesita estar en la misma
echo carpeta que los archivos assets\ para funcionar.
echo.

pause
