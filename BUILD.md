# Guía de Compilación - GesMonth v1.0.0

Esta guía explica cómo compilar GesMonth en un ejecutable standalone usando PyInstaller.

## 📋 Requisitos Previos

- Python 3.8 o superior instalado
- Entorno virtual configurado (ejecutar `install.bat` o `install.sh` primero)
- PyInstaller 6.3.0 (se instala automáticamente con los scripts)

## 🔨 Compilación en Windows

### Método Automático (Recomendado)

1. Ejecuta el script de compilación:
   ```cmd
   build.bat
   ```

2. El script realizará automáticamente:
   - Activación del entorno virtual
   - Instalación de PyInstaller (si no está instalado)
   - Limpieza de compilaciones anteriores
   - Compilación del ejecutable
   - Empaquetado de todos los recursos

3. El ejecutable estará en: `dist\GesMonth.exe`

### Método Manual

1. Activa el entorno virtual:
   ```cmd
   venv\Scripts\activate
   ```

2. Instala PyInstaller:
   ```cmd
   pip install pyinstaller==6.3.0
   ```

3. Compila con el spec file:
   ```cmd
   pyinstaller --clean --noconfirm gesmonth.spec
   ```

## 🐧 Compilación en Linux/Mac

### Método Automático (Recomendado)

1. Ejecuta el script de compilación:
   ```bash
   ./build.sh
   ```

2. El ejecutable estará en: `dist/GesMonth`

### Método Manual

1. Activa el entorno virtual:
   ```bash
   source venv/bin/activate
   ```

2. Instala PyInstaller:
   ```bash
   pip install pyinstaller==6.3.0
   ```

3. Compila con el spec file:
   ```bash
   pyinstaller --clean --noconfirm gesmonth.spec
   ```

## 📦 Estructura del Ejecutable

Después de la compilación, la carpeta `dist` contendrá:

```
dist/
├── GesMonth.exe (Windows) o GesMonth (Linux/Mac)
└── assets/
    └── styles/
        └── main.qss
```

## 🚀 Distribución

### Para Usuarios Finales

1. **Copia toda la carpeta `dist`**
   - No solo el .exe, sino toda la carpeta con sus contenidos
   - La carpeta `assets` debe estar junto al ejecutable

2. **Renombra la carpeta (opcional)**
   - Puedes renombrar `dist` a `GesMonth`

3. **Comprime la carpeta**
   - Crea un archivo ZIP: `GesMonth-v1.0.0-Windows.zip`
   - Los usuarios solo necesitan descomprimir y ejecutar

### Ejemplo de Estructura para Distribución

```
GesMonth-v1.0.0/
├── GesMonth.exe
├── assets/
│   └── styles/
│       └── main.qss
├── README.txt
└── LICENSE.txt
```

## 🔧 Optimizaciones del Spec File

El archivo `gesmonth.spec` incluye:

### Archivos Incluidos
- `assets/`: Carpeta de estilos y recursos
- `VERSION`: Archivo de versión
- Todos los módulos de la aplicación

### Módulos Ocultos (Hidden Imports)
- PyQt6 (Core, Gui, Widgets)
- pandas, openpyxl
- Todos los módulos de database, ui, controllers

### Módulos Excluidos (para reducir tamaño)
- matplotlib
- scipy
- numpy
- tkinter
- PIL

### Opciones de Compilación
- `console=False`: Sin ventana de consola
- `upx=True`: Compresión UPX para reducir tamaño
- `onefile=True`: Todo en un solo ejecutable

## 📊 Tamaño del Ejecutable

- **Sin comprimir**: ~150-200 MB
- **Con UPX**: ~80-120 MB
- **Comprimido (ZIP)**: ~40-60 MB

El tamaño incluye:
- Python runtime
- PyQt6 framework completo
- SQLite
- Librerías adicionales

## ⚠️ Problemas Comunes

### Error: "PyInstaller not found"
**Solución**: Instala PyInstaller manualmente
```bash
pip install pyinstaller==6.3.0
```

### Error: "Failed to execute script"
**Causas posibles**:
- Falta la carpeta `assets`
- Archivo QSS no encontrado
- Permisos insuficientes

**Solución**: Asegúrate de que la carpeta `assets` esté junto al ejecutable

### Ejecutable muy grande
**Solución**: Verifica que los módulos excluidos estén en el spec:
```python
excludes=['matplotlib', 'scipy', 'numpy', 'tkinter']
```

### Antivirus marca el ejecutable como amenaza
**Normal**: PyInstaller empaqueta Python, lo que algunos antivirus detectan como sospechoso
**Solución**: 
- Agrega el ejecutable a la lista blanca del antivirus
- Firma digitalmente el ejecutable (para distribución comercial)

## 🔐 Firma Digital (Opcional)

Para distribución comercial, se recomienda firmar el ejecutable:

### Windows
```cmd
signtool sign /f certificado.pfx /p password /t http://timestamp.digicert.com dist\GesMonth.exe
```

### Requisitos
- Certificado de firma de código (.pfx)
- Windows SDK instalado

## 📝 Notas Importantes

1. **Base de Datos**: No incluir `gesmonth.db` en el ejecutable
   - La BD se crea automáticamente en la primera ejecución
   - Cada usuario tendrá su propia base de datos

2. **Actualizaciones**: Para nuevas versiones:
   - Actualiza el archivo `VERSION`
   - Recompila con el spec file
   - Distribuye la nueva versión

3. **Testing**: Siempre prueba el ejecutable en una máquina limpia:
   - Sin Python instalado
   - Sin dependencias previas
   - Sistema operativo limpio o VM

4. **Compatibilidad**:
   - Windows: 7, 8, 10, 11 (64-bit)
   - Linux: Ubuntu 18.04+, Debian 10+, Fedora 30+
   - Mac: macOS 10.14+

## 🎯 Checklist de Distribución

- [ ] Compilación exitosa sin errores
- [ ] Ejecutable probado en máquina limpia
- [ ] Carpeta `assets` incluida
- [ ] README para usuarios finales
- [ ] Archivo ZIP comprimido
- [ ] Versión correcta en el nombre del archivo
- [ ] CHANGELOG actualizado
- [ ] Documentación incluida

## 🆘 Soporte

Si encuentras problemas durante la compilación:

1. Revisa los logs de PyInstaller en `build\gesmonth\`
2. Verifica que todas las dependencias estén instaladas
3. Consulta la documentación oficial de PyInstaller: https://pyinstaller.org/

---

**GesMonth v1.0.0** - Sistema de Gestión de Pagos Mensuales
