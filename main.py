"""
GesMonth - Sistema de Gestión de Pagos Mensuales
Punto de entrada de la aplicación
"""

import sys
import os
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from ui.main_window import MainWindow
from database.connection import DatabaseConnection


def load_stylesheet(app: QApplication):
    """Carga el archivo de estilos QSS"""
    try:
        style_path = os.path.join(os.path.dirname(__file__), 'assets', 'styles', 'main.qss')
        with open(style_path, 'r', encoding='utf-8') as f:
            app.setStyleSheet(f.read())
    except Exception as e:
        print(f"Error al cargar estilos: {e}")


def main():
    """Función principal de la aplicación"""
    # Habilitar escalado de alta DPI
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )
    
    # Crear aplicación
    app = QApplication(sys.argv)
    app.setApplicationName("GesMonth")
    app.setOrganizationName("GesMonth")
    
    # Establecer icono de la aplicación
    icon_path = os.path.join(os.path.dirname(__file__), 'assets', 'icons', 'LOGO.png')
    if os.path.exists(icon_path):
        app.setWindowIcon(QIcon(icon_path))
    
    # Cargar estilos
    load_stylesheet(app)
    
    # Inicializar base de datos
    try:
        db = DatabaseConnection()
        print("Base de datos inicializada correctamente")
    except Exception as e:
        print(f"Error al inicializar la base de datos: {e}")
        return 1
    
    # Crear y mostrar ventana principal
    window = MainWindow()
    window.show()
    
    # Ejecutar aplicación
    exit_code = app.exec()
    
    # Cerrar conexión a base de datos
    db.close()
    
    return exit_code


if __name__ == '__main__':
    sys.exit(main())
