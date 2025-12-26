#!/bin/bash

echo "================================"
echo "GesMonth - Instalador"
echo "================================"
echo ""

# Verificar Python
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python3 no está instalado"
    echo "Por favor instala Python3"
    exit 1
fi

echo "Python3 encontrado correctamente"
echo ""

# Instalar dependencias del sistema para PyQt6
echo "Verificando dependencias del sistema para PyQt6..."
if command -v apt &> /dev/null; then
    echo "Detectado sistema basado en Debian/Ubuntu"
    echo "Se requieren las siguientes dependencias del sistema:"
    echo "  - libxcb-cursor0 (para Qt platform plugin)"
    echo "  - libxcb-xinerama0"
    echo "  - libxkbcommon-x11-0"
    echo ""
    echo "Ejecuta el siguiente comando con privilegios de administrador:"
    echo "  sudo apt install -y libxcb-cursor0 libxcb-xinerama0 libxkbcommon-x11-0"
    echo ""
    read -p "¿Deseas instalar estas dependencias ahora? (s/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Ss]$ ]]; then
        sudo apt install -y libxcb-cursor0 libxcb-xinerama0 libxkbcommon-x11-0
    else
        echo "NOTA: Necesitarás instalar estas dependencias para ejecutar la aplicación"
    fi
fi

echo ""

# Crear entorno virtual
echo "Creando entorno virtual..."
python3 -m venv venv
if [ $? -ne 0 ]; then
    echo "ERROR: No se pudo crear el entorno virtual"
    exit 1
fi

echo "Entorno virtual creado"
echo ""

# Activar entorno virtual e instalar dependencias
echo "Instalando dependencias de Python..."
source venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "ERROR: No se pudieron instalar las dependencias"
    exit 1
fi

echo ""
echo "================================"
echo "Instalación completada!"
echo "================================"
echo ""
echo "Para ejecutar la aplicación:"
echo "  1. Ejecuta: ./run.sh"
echo "  2. O manualmente: source venv/bin/activate && python main.py"
echo ""
