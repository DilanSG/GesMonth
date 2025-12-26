#!/bin/bash

echo "================================"
echo "GesMonth - Sistema de Gestión"
echo "================================"
echo ""

# Verificar si existe el entorno virtual
if [ ! -f "venv/bin/activate" ]; then
    echo "ERROR: Entorno virtual no encontrado"
    echo "Por favor ejecuta primero: ./install.sh"
    exit 1
fi

# Activar entorno virtual y ejecutar aplicación
source venv/bin/activate
python main.py
