@echo off
echo ================================
echo GesMonth - Instalador
echo ================================
echo.

REM Verificar Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python no esta instalado
    pause
    exit /b 1
)

echo Python encontrado correctamente
echo.

REM Crear entorno virtual
echo Creando entorno virtual...
python -m venv venv
if errorlevel 1 (
    echo ERROR: No se pudo crear el entorno virtual
    pause
    exit /b 1
)

echo Entorno virtual creado
echo.

REM Activar entorno virtual e instalar dependencias
echo Instalando dependencias...
call venv\Scripts\activate.bat
python -m pip install --upgrade pip
pip install -r requirements.txt

if errorlevel 1 (
    echo ERROR: No se pudieron instalar las dependencias
    pause
    exit /b 1
)

echo.
echo ================================
echo Instalacion completada!
echo ================================
echo.
echo Para ejecutar la aplicacion:
echo   1. Ejecuta: run.bat
echo   2. O manualmente: venv\Scripts\activate.bat y luego python main.py
echo.
pause
