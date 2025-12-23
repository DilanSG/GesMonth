#!/bin/bash

# ============================================
# GesMonth - Script de compilación para Linux/Mac
# Genera el ejecutable standalone con PyInstaller
# ============================================

echo "============================================"
echo "GesMonth - Compilador v1.0.0"
echo "============================================"
echo ""

# Verificar que el entorno virtual exista
if [ ! -f "venv/bin/activate" ]; then
    echo "ERROR: No se encontró el entorno virtual"
    echo "Por favor ejecuta ./install.sh primero"
    exit 1
fi

# Activar entorno virtual
echo "Activando entorno virtual..."
source venv/bin/activate

# Verificar PyInstaller
echo "Verificando PyInstaller..."
if ! pip show pyinstaller &> /dev/null; then
    echo "PyInstaller no está instalado. Instalando..."
    pip install pyinstaller==6.3.0
    if [ $? -ne 0 ]; then
        echo "ERROR: No se pudo instalar PyInstaller"
        exit 1
    fi
fi

echo ""
echo "============================================"
echo "Limpiando compilaciones anteriores..."
echo "============================================"
rm -rf build dist GesMonth

echo ""
echo "============================================"
echo "Compilando aplicación..."
echo "============================================"
echo "Esto puede tardar varios minutos..."
echo ""

pyinstaller --clean --noconfirm gesmonth.spec

if [ $? -ne 0 ]; then
    echo ""
    echo "ERROR: La compilación falló"
    exit 1
fi

echo ""
echo "============================================"
echo "Compilación exitosa!"
echo "============================================"
echo ""
echo "El ejecutable se encuentra en: dist/GesMonth"
echo ""
echo "Para distribuir la aplicación:"
echo "1. Copia la carpeta 'dist' completa"
echo "2. Puedes renombrar 'dist' a 'GesMonth'"
echo "3. Dentro estará el ejecutable GesMonth"
echo ""
echo "IMPORTANTE: El ejecutable necesita estar en la misma"
echo "carpeta que los archivos assets/ para funcionar."
echo ""
