"""
GesMonth - Sistema de Gestión de Pagos Mensuales
Punto de entrada de la aplicación
"""

# Sys: Argumentos de línea de comandos y salida del programa
import sys  # sys: acceso a argumentos y manejo de salida de la aplicación

# OS: Operaciones con el sistema de archivos
import os  # os: manejo de rutas y entorno del sistema operativo

# PyQt6 Widgets: Componentes gráficos principales
from PyQt6.QtWidgets import QApplication  # QApplication: aplicación Qt principal

# PyQt6 Core: Funcionalidades centrales de Qt
from PyQt6.QtCore import Qt, QTimer  # Qt: constantes globales, QTimer: temporizadores

# PyQt6 GUI: Elementos gráficos
from PyQt6.QtGui import QIcon  # QIcon: iconos de la aplicación

# UI: Ventana principal de la aplicación
from ui.main_window import MainWindow  # MainWindow: ventana principal con navegación

# Database: Conexión y creación de base de datos
from database.connection import DatabaseConnection  # DatabaseConnection: inicialización de BD


def main():
    """Función principal de la aplicación"""
    # Habilitar escalado de alta DPI
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )
    
    # Crear aplicación
    app = QApplication(sys.argv)

    # Inicializar sistema de escala responsive (debe hacerse antes de crear widgets)
    from ui.responsive import UIScale
    UIScale.init(app)
    app.setApplicationName("GesMonth")
    app.setOrganizationName("GesMonth")
    
    # Obtener el directorio base (funciona tanto en desarrollo como en ejecutable)
    if getattr(sys, 'frozen', False):
        # Si está ejecutándose como ejecutable de PyInstaller
        base_path = os.path.dirname(sys.executable)
    else:
        # Si está ejecutándose como script Python
        base_path = os.path.dirname(__file__)
    
    # Establecer icono de la aplicación
    icon_path = os.path.join(base_path, 'assets', 'icons', 'LOGO.png')
    if os.path.exists(icon_path):
        app.setWindowIcon(QIcon(icon_path))
    
    # Inicializar bases de datos
    try:
        db = DatabaseConnection()
        print("Base de datos inicializada correctamente")
        
        # Inicializar base de datos de usuarios
        from database.user_connection import UserDatabaseConnection
        user_db = UserDatabaseConnection()
        print("Base de datos de usuarios inicializada correctamente")
    except Exception as e:
        print(f"Error al inicializar las bases de datos: {e}")
        return 1
    
    # Crear log_controller para el sistema
    from controllers.log_controller import LogController
    log_controller = LogController()
    
    # Mostrar pantalla de login
    from ui.login_view import LoginView
    login_window = LoginView(log_controller=log_controller)
    
    usuario_autenticado = None
    tema_seleccionado = 'light'  # Por defecto tema claro
    
    # Si el login es exitoso, obtener el usuario y el tema
    def on_login_exitoso(usuario, tema):
        nonlocal usuario_autenticado, tema_seleccionado
        usuario_autenticado = usuario
        tema_seleccionado = tema
    
    login_window.login_exitoso.connect(on_login_exitoso)
    
    # Ejecutar dialog de login
    if login_window.exec() != login_window.DialogCode.Accepted or usuario_autenticado is None:
        print("Login cancelado o fallido")
        db.close()
        return 0
    
    # PRIMERO: Determinar si debe ser pantalla completa
    from controllers.config_controller import ConfigController
    config = ConfigController()
    fullscreen_enabled = config.get_fullscreen()
    
    # Mostrar splash screen con el tamaño correcto
    from ui.splash_screen import SplashScreen
    splash = SplashScreen(tema=tema_seleccionado, fullscreen=fullscreen_enabled)
    splash.show()
    
    # Procesar eventos para que el splash aparezca de inmediato
    app.processEvents()
    
    # SEGUNDO: Crear la ventana principal completa (oculta) mientras el splash está visible
    print("Cargando ventana principal...")
    window = MainWindow(app, usuario_autenticado)
    window.apply_theme(tema_seleccionado)
    # NO mostrar todavía - dejar que termine el splash
    
    # Función para hacer transición del splash al dashboard
    def transicion_splash_a_dashboard():
        # Iniciar fade out del splash
        splash.finish()
        
        # Esperar un momento y mostrar ventana principal en el centro
        def mostrar_ventana():
            # Centrar la ventana en la pantalla
            screen = app.primaryScreen()
            screen_geometry = screen.availableGeometry()
            window_geometry = window.frameGeometry()
            center_point = screen_geometry.center()
            window_geometry.moveCenter(center_point)
            window.move(window_geometry.topLeft())
            
            # Mostrar ventana
            window.show()
            
            # Cerrar el splash después de que termine el fade out
            def limpiar_splash():
                splash.close()
                splash.deleteLater()
            
            QTimer.singleShot(500, limpiar_splash)
        
        QTimer.singleShot(100, mostrar_ventana)
    
    # Esperar 5 segundos totales (4 de animación + 1 de pausa) antes de la transición
    QTimer.singleShot(5000, transicion_splash_a_dashboard)
    
    # Ejecutar aplicación
    exit_code = app.exec()
    
    # Cerrar conexiones a bases de datos
    db.close()
    
    return exit_code


if __name__ == '__main__':
    sys.exit(main())
