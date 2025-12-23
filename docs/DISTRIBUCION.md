# Guía Rápida de Distribución - GesMonth v1.0.1

Esta guía te ayuda a crear paquetes de distribución de GesMonth para usuarios finales.

## Proceso Completo

### 1. Preparación (Una sola vez)

```bash
# Instalar dependencias incluyendo PyInstaller
./install.sh  # Linux/Mac
install.bat   # Windows
```

### 2. Compilación

Genera el ejecutable standalone:

```bash
# Linux/Mac
./build.sh

# Windows
build.bat
```

**Resultado**: Ejecutable en carpeta `dist/`
- Windows: `dist\GesMonth.exe`
- Linux: `dist/GesMonth`

**Tiempo estimado**: 3-5 minutos

### 3. Empaquetado para Distribución

Crea el paquete comprimido listo para distribuir:

```bash
# Linux/Mac
./package.sh

# Windows
package.bat
```

**Resultado**: Archivo comprimido listo para distribuir
- Windows: `GesMonth-v1.0.0-Windows.zip`
- Linux: `GesMonth-v1.0.0-Linux.tar.gz`

**Contenido del paquete**:
- Ejecutable (GesMonth.exe o GesMonth)
- Carpeta assets/ con estilos
- LEER_PRIMERO.txt (manual de usuario)
- VERSION
- LICENSE.txt

### 4. Distribución

**Opción A - Descarga directa**:
1. Sube el archivo .zip o .tar.gz a tu hosting/servidor
2. Comparte el enlace de descarga

**Opción B - GitHub Release**:
1. Crea un nuevo Release en GitHub
2. Adjunta los archivos como assets
3. Etiqueta con `v1.0.0`

**Opción C - Google Drive / Dropbox**:
1. Sube el archivo
2. Genera enlace público
3. Comparte con usuarios

## Checklist de Distribución

Antes de distribuir, verifica:

- [ ] Compilación exitosa sin errores
- [ ] Ejecutable probado en máquina limpia
- [ ] Carpeta `assets` incluida
- [ ] LEER_PRIMERO.txt presente
- [ ] LICENSE.txt incluido
- [ ] VERSION correcta (1.0.0)
- [ ] Tamaño del archivo razonable (~60 MB comprimido)
- [ ] Nombre del archivo con versión correcta

## Instrucciones para Usuarios Finales

### Windows
1. Descargar `GesMonth-v1.0.0-Windows.zip`
2. Descomprimir en cualquier carpeta
3. Doble clic en `GesMonth.exe`
4. Leer `LEER_PRIMERO.txt` para más información

### Linux
1. Descargar `GesMonth-v1.0.0-Linux.tar.gz`
2. Descomprimir: `tar -xzf GesMonth-v1.0.0-Linux.tar.gz`
3. Entrar a la carpeta: `cd GesMonth-v1.0.0-Linux`
4. Ejecutar: `./GesMonth`
5. Leer `LEER_PRIMERO.txt` para más información

## Comandos Rápidos

### Proceso completo de compilación y empaquetado:

**Windows**:
```cmd
build.bat && package.bat
```

**Linux/Mac**:
```bash
./build.sh && ./package.sh
```

## Estructura del Paquete Final

```
GesMonth-v1.0.0-Windows.zip
└── GesMonth-v1.0.0-Windows/
    ├── GesMonth.exe          # Ejecutable principal
    ├── assets/               # Recursos
    │   └── styles/
    │       └── main.qss
    ├── LEER_PRIMERO.txt     # Manual de usuario
    ├── LICENSE.txt          # Licencia
    └── VERSION              # Versión (1.0.0)
```

## Solución de Problemas

### El build falla
- Verifica que el venv esté activado
- Reinstala PyInstaller: `pip install --upgrade pyinstaller`
- Revisa logs en `build/gesmonth/`

### El paquete es muy grande
- Normal: ~150-200 MB sin comprimir, ~60 MB comprimido
- Incluye Python runtime completo + PyQt6
- No se puede reducir significativamente

### El ejecutable no funciona en otra máquina
- Asegúrate de incluir la carpeta `assets`
- Verifica que sea la arquitectura correcta (64-bit)
- En Linux, verifica permisos: `chmod +x GesMonth`

## Notas Importantes

1. **No incluir la base de datos**: `gesmonth.db` se crea automáticamente
2. **Assets obligatorios**: La carpeta `assets/` debe estar junto al ejecutable
3. **Compilación por plataforma**: Compila en Windows para Windows, Linux para Linux
4. **Testing**: Siempre prueba el ejecutable en una máquina limpia sin Python

## 🔄 Actualizar a Nueva Versión

Cuando lances v1.1.0 o superior:

1. Actualiza `VERSION` con el nuevo número
2. Actualiza `CHANGELOG.md` con los cambios
3. Recompila: `./build.sh`
4. Empaqueta: `./package.sh`
5. Distribuye con nuevo nombre: `GesMonth-v1.1.0-Windows.zip`

## 🆘 Soporte

Para problemas durante la compilación o distribución:
- Consulta `BUILD.md` para detalles técnicos
- Revisa logs de PyInstaller
- Abre un issue en el repositorio

---

**¿Listo para distribuir?**

Ejecuta en orden:
1. `./build.sh` (compilar)
2. `./package.sh` (empaquetar)
3. ¡Distribuye el archivo .zip/.tar.gz generado!

---

GesMonth v1.0.1 - Desarrollado por Dilan Acuña
