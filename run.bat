@echo off
echo ================================
echo GesMonth - Sistema de Gestion
echo ================================
echo.

REM Verificar si existe el entorno virtual
if not exist "venv\Scripts\activate.bat" (
    echo ERROR: Entorno virtual no encontrado
    echo Por favor ejecuta primero: install.bat
    pause
    exit /b 1
)

REM Activar entorno virtual y ejecutar aplicación
call venv\Scripts\activate.bat
python main.py

pause
