# 🚀 Guía de Instalación Rápida - GesMonth

## Windows

### Opción 1: Instalación Automática (Recomendada)

1. **Doble clic** en `install.bat`
2. Espera a que se instalen todas las dependencias
3. **Doble clic** en `run.bat` para ejecutar la aplicación

### Opción 2: Instalación Manual

```cmd
# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar aplicación
python main.py
```

---

## Linux / Mac

### Opción 1: Instalación Automática (Recomendada)

```bash
# Dar permisos de ejecución
chmod +x install.sh run.sh

# Ejecutar instalador
./install.sh

# Ejecutar aplicación
./run.sh
```

### Opción 2: Instalación Manual

```bash
# Crear entorno virtual
python3 -m venv venv

# Activar entorno virtual
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar aplicación
python main.py
```

---

## ⚠️ Requisitos Previos

- **Python 3.8 o superior** instalado
- **pip** (gestor de paquetes de Python)
- Conexión a internet para descargar dependencias

### Verificar instalación de Python

Windows:
```cmd
python --version
```

Linux/Mac:
```bash
python3 --version
```

Si Python no está instalado, descárgalo desde: https://www.python.org/downloads/

---

## 📦 Dependencias del Proyecto

- **PyQt6**: Interfaz gráfica moderna
- **pandas**: Manipulación de datos
- **openpyxl**: Exportación a Excel

---

## 🎯 Primera Ejecución

1. Al ejecutar por primera vez, se creará automáticamente:
   - Base de datos `database.db`
   - Tablas necesarias (alumnos, pagos)

2. La aplicación se abrirá con:
   - Dashboard vacío
   - Todas las funcionalidades listas para usar

---

## 🆘 Solución de Problemas

### "Python no está instalado"
- Instala Python desde https://www.python.org/
- En Windows, marca "Add Python to PATH" durante la instalación

### "pip no encontrado"
Windows:
```cmd
python -m ensurepip --upgrade
```

Linux:
```bash
sudo apt install python3-pip
```

### "No se pueden instalar las dependencias"
- Verifica tu conexión a internet
- Actualiza pip: `python -m pip install --upgrade pip`
- Intenta instalar una por una:
  ```bash
  pip install PyQt6
  pip install pandas
  pip install openpyxl
  ```

### Error al ejecutar en Linux
- Asegúrate de dar permisos: `chmod +x run.sh`
- Instala dependencias del sistema:
  ```bash
  sudo apt install python3-pyqt6
  ```

---

## 📚 Documentación Completa

Para más información, consulta el archivo `README.md`

---

¡Listo para usar GesMonth! 🎉
