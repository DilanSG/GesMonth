#!/bin/bash

# ============================================
# GesMonth - Preparar Paquete de Distribución
# Crea un archivo tar.gz listo para distribuir
# ============================================

# Leer versión del archivo VERSION
VERSION=$(cat VERSION 2>/dev/null || echo "1.0.0")

echo "============================================"
echo "GesMonth - Preparar Distribución v${VERSION}"
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
rm -rf "GesMonth-v${VERSION}-Linux"
mkdir -p "GesMonth-v${VERSION}-Linux"

# Copiar ejecutable y assets
echo "Copiando archivos..."
cp -r dist/GesMonth "GesMonth-v${VERSION}-Linux/"

# Mover assets al nivel correcto (junto al ejecutable)
if [ -d "GesMonth-v${VERSION}-Linux/GesMonth/_internal/assets" ]; then
    echo "Moviendo assets al nivel del ejecutable..."
    mv "GesMonth-v${VERSION}-Linux/GesMonth/_internal/assets" "GesMonth-v${VERSION}-Linux/GesMonth/"
fi

# Copiar documentación para usuarios con reemplazo de versión
echo "Generando README con versión ${VERSION}..."
sed "s/{{VERSION}}/${VERSION}/g" LEER_PRIMERO-DISTRIBUCION.txt > "GesMonth-v${VERSION}-Linux/README.txt"
cp VERSION "GesMonth-v${VERSION}-Linux/GesMonth/"

# Copiar licencia
cp LICENSE "GesMonth-v${VERSION}-Linux/LICENSE.txt"

# Dar permisos de ejecución
chmod +x "GesMonth-v${VERSION}-Linux/GesMonth/GesMonth"

# Crear carpeta .data con archivos .db placeholder vacíos
echo "Creando estructura de datos..."
mkdir -p "GesMonth-v${VERSION}-Linux/GesMonth/.data"
touch "GesMonth-v${VERSION}-Linux/GesMonth/.data/gesmonth.db"
touch "GesMonth-v${VERSION}-Linux/GesMonth/.data/users.db"
# Permisos de solo lectura (la app los eliminará y creará nuevos al iniciar)
chmod 444 "GesMonth-v${VERSION}-Linux/GesMonth/.data/gesmonth.db"
chmod 444 "GesMonth-v${VERSION}-Linux/GesMonth/.data/users.db"

# Crear archivo tar.gz
echo "Comprimiendo..."
tar -czf "GesMonth-v${VERSION}-Linux.tar.gz" "GesMonth-v${VERSION}-Linux/"

if [ $? -eq 0 ]; then
    echo ""
    echo "============================================"
    echo "Paquete creado exitosamente!"
    echo "============================================"
    echo ""
    echo "Archivo: GesMonth-v${VERSION}-Linux.tar.gz"
    echo ""
    echo "Este archivo está listo para distribuir."
    echo "Los usuarios solo necesitan:"
    echo "1. Descomprimir el tar.gz"
    echo "2. Entrar a la carpeta GesMonth/"
    echo "3. Ejecutar ./GesMonth"
    echo ""
else
    echo ""
    echo "ERROR: No se pudo crear el archivo comprimido"
    exit 1
fi

echo "Carpeta temporal: GesMonth-v${VERSION}-Linux/"
