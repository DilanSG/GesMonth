#!/bin/bash

# ============================================
# GesMonth - Preparar Paquete de Distribución
# Crea un archivo tar.gz listo para distribuir
# ============================================

echo "============================================"
echo "GesMonth - Preparar Distribución v1.0.0"
echo "============================================"
echo ""

# Verificar que dist existe
if [ ! -d "dist" ]; then
    echo "ERROR: La carpeta dist no existe"
    echo "Por favor compila primero con ./build.sh"
    exit 1
fi

# Crear carpeta temporal
echo "Creando paquete de distribución..."
rm -rf GesMonth-v1.0.0-Linux
mkdir -p GesMonth-v1.0.0-Linux

# Copiar ejecutable y assets
echo "Copiando archivos..."
cp -r dist/* GesMonth-v1.0.0-Linux/

# Copiar documentación para usuarios
cp LEER_PRIMERO.txt GesMonth-v1.0.0-Linux/
cp VERSION GesMonth-v1.0.0-Linux/

# Crear archivo de licencia simple
cat > GesMonth-v1.0.0-Linux/LICENSE.txt << EOF
GesMonth v1.0.0

Este software es de código abierto.
Disponible para uso personal, educativo y comercial.

Desarrollado por Dilan Acuña
Diciembre 2025
EOF

# Dar permisos de ejecución
chmod +x GesMonth-v1.0.0-Linux/GesMonth

# Crear archivo tar.gz
echo "Comprimiendo..."
tar -czf GesMonth-v1.0.0-Linux.tar.gz GesMonth-v1.0.0-Linux/

if [ $? -eq 0 ]; then
    echo ""
    echo "============================================"
    echo "Paquete creado exitosamente!"
    echo "============================================"
    echo ""
    echo "Archivo: GesMonth-v1.0.0-Linux.tar.gz"
    echo ""
    echo "Este archivo está listo para distribuir."
    echo "Los usuarios solo necesitan:"
    echo "1. Descomprimir el tar.gz"
    echo "2. Ejecutar ./GesMonth"
    echo ""
else
    echo ""
    echo "ERROR: No se pudo crear el archivo comprimido"
    exit 1
fi

echo "Carpeta temporal: GesMonth-v1.0.0-Linux/"
echo ""
