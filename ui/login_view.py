"""
Vista de Login mejorada con toggle de tema
"""

# OS: Operaciones con rutas de archivos
import os  # os: construcción de rutas para imágenes del logo

# PyQt6 Widgets: Componentes gráficos de la interfaz
from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                             QLineEdit, QPushButton, QFrame, QApplication, QCheckBox)
# QDialog: ventana de diálogo, QVBoxLayout/QHBoxLayout: layouts, QLabel: etiquetas
# QLineEdit: campos de texto, QPushButton: botones, QFrame: marcos, QCheckBox: casillas

# PyQt6 Core: Funcionalidades centrales de Qt
from PyQt6.QtCore import Qt, pyqtSignal, QPropertyAnimation, QEasingCurve, pyqtProperty, QTimer
# Qt: constantes, pyqtSignal: señales personalizadas, QPropertyAnimation: animaciones
# QEasingCurve: curvas de animación, pyqtProperty: propiedades animables, QTimer: temporizadores

# PyQt6 GUI: Elementos gráficos y dibujado
from PyQt6.QtGui import QIcon, QPixmap, QPainter, QBrush, QColor
# QIcon: iconos, QPixmap: imágenes, QPainter: dibujado, QBrush: rellenos, QColor: colores

# Controllers: Lógica de negocio
from controllers.auth_controller import AuthController  # AuthController: autenticación de usuarios
from controllers.config_controller import ConfigController  # ConfigController: configuración de tema

# Utils: Utilidades de rutas
from utils import get_resource_path  # get_resource_path: rutas correctas de recursos

# Responsive: escalado DPI de tamaños fijos
from .responsive import UIScale


class ToggleSwitch(QCheckBox):
    """
    Toggle switch personalizado con animación suave para cambio de temas.
    
    Implementa un interruptor visual animado que reemplaza al checkbox estándar.
    Usa QPropertyAnimation para animar la posición del círculo interno.
    
    Componentes:
    - Fondo rectangular redondeado (cambia de color según estado)
    - Círculo blanco que se desliza (posición 3 a 33 px)
    - Animación con curva InOutCubic (suaviza inicio y fin)
    
    Estados:
    - Desactivado (False): círculo a la izquierda, fondo gris
    - Activado (True): círculo a la derecha, fondo azul
    """
    
    def __init__(self, parent=None, small=False):
        super().__init__(parent)
        self.small = small
        
        if small:
            # Toggle pequeño: mitad del tamaño
            self.setFixedSize(UIScale.px(30), UIScale.px(15))
            self._circle_position = 2  # Posición inicial del círculo (izquierda)
            self._circle_size = 11
            self._end_position = 17
        else:
            # Toggle normal
            self.setFixedSize(UIScale.px(60), UIScale.px(30))
            self._circle_position = 3
            self._circle_size = 24
            self._end_position = 33
            
        # Crear animación para la propiedad personalizada 'circle_position'
        self.animation = QPropertyAnimation(self, b"circle_position", self)
        self.animation.setEasingCurve(QEasingCurve.Type.InOutCubic)  # Curva suave
        self.animation.setDuration(200)  # Duración de 200ms
        self.stateChanged.connect(self.start_transition)  # Conectar cambio de estado con animación
        
    @pyqtProperty(int)
    def circle_position(self):
        """
        Propiedad personalizada que representa la posición X del círculo.
        
        Esta propiedad es animable por QPropertyAnimation.
        Al cambiar su valor, se dispara automáticamente update() para repintar.
        
        Returns:
            Posición X actual del círculo en píxeles (3 a 33)
        """
        return self._circle_position
    
    @circle_position.setter
    def circle_position(self, pos):
        """
        Setter de la posición del círculo.
        
        Actualiza la posición y fuerza un repintado del widget.
        Llamado automáticamente por QPropertyAnimation durante la animación.
        
        Args:
            pos: Nueva posición X del círculo en píxeles
        """
        self._circle_position = pos
        self.update()  # Forzar repintado con nueva posición
    
    def start_transition(self, value):
        """
        Inicia la animación del círculo al cambiar el estado del toggle.
        
        Animación:
        - De izquierda a derecha cuando se activa
        - De derecha a izquierda cuando se desactiva
        
        Args:
            value: Nuevo estado del checkbox (0=desactivado, 1=activado)
        """
        self.animation.stop()  # Detener animación previa si existe
        self.animation.setStartValue(self._circle_position)  # Desde posición actual
        if value:
            self.animation.setEndValue(self._end_position)  # Mover a la derecha
        else:
            if self.small:
                self.animation.setEndValue(2)  # Mover a la izquierda (pequeño)
            else:
                self.animation.setEndValue(3)  # Mover a la izquierda (normal)
        self.animation.start()  # Iniciar animación
    
    def mousePressEvent(self, event):
        """
        Maneja el click del mouse sobre el toggle.
        
        Sobreescribe el comportamiento por defecto del QCheckBox para:
        1. Alternar el estado manualmente
        2. Sincronizar la animación con el nuevo estado
        3. Evitar comportamientos duplicados del checkbox base
        
        Args:
            event: Evento de click del mouse
        """
        # Alternar el estado manualmente
        new_state = not self.isChecked()
        self.setChecked(new_state)
        
        # Forzar la animación de la posición inmediatamente
        self.animation.stop()
        self.animation.setStartValue(self._circle_position)
        target_position = self._end_position if new_state else (2 if self.small else 3)
        self.animation.setEndValue(target_position)
        self.animation.start()
        
        # No llamar a super() para evitar conflictos con el comportamiento del QCheckBox
        event.accept()
    
    def paintEvent(self, event):
        """
        Dibuja el toggle switch personalizado.
        
        Dibuja dos elementos:
        1. Fondo: rectángulo redondeado con color según estado
           - Gris (#cbd5e1) si está desactivado
           - Azul (#3b82f6) si está activado
        2. Círculo: círculo blanco que se mueve horizontalmente
           - Posición controlada por self._circle_position
        
        Args:
            event: Evento de pintado de Qt
        """
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)  # Suavizar bordes
        
        # Fondo del toggle con color según estado
        if self.isChecked():
            # Activado (tema oscuro) - azul
            brush_color = QColor(59, 130, 246)  # #3b82f6
        else:
            # Desactivado (tema claro) - gris
            brush_color = QColor(203, 213, 225)  # #cbd5e1
        
        painter.setBrush(QBrush(brush_color))
        painter.setPen(Qt.PenStyle.NoPen)  # Sin borde
        # Dibujar rectángulo redondeado (mitad de altura para bordes circulares)
        painter.drawRoundedRect(0, 0, self.width(), self.height(), self.height() / 2, self.height() / 2)
        
        # Círculo del toggle (siempre blanco)
        painter.setBrush(QBrush(QColor(255, 255, 255)))
        # Dibujar círculo en posición animada
        circle_offset = 2 if self.small else 3
        painter.drawEllipse(self._circle_position, circle_offset, self._circle_size, self._circle_size)


class LoginView(QDialog):
    """Ventana de login"""
    
    login_exitoso = pyqtSignal(object, str)  # Emite el usuario autenticado y el tema seleccionado
    
    def __init__(self, log_controller=None):
        super().__init__()
        self.auth_controller = AuthController(log_controller=log_controller)
        self.config_controller = ConfigController()
        
        # Cargar tema guardado desde configuración
        saved_theme = self.config_controller.get_theme()
        self.tema_oscuro = saved_theme == 'dark'
        
        # Cargar usuario recordado
        self.remembered_user = self._cargar_usuario_recordado()
        
        self._init_ui()
        
    def _init_ui(self):
        """Inicializa la interfaz"""
        self.setWindowTitle("GesMonth - Iniciar Sesión")
        self.setMinimumSize(UIScale.px(700), UIScale.px(850))  # Tamaño mínimo más grande para acomodar notificaciones
        self.resize(UIScale.px(700), UIScale.px(850))  # Tamaño inicial
        self.setModal(True)
        
        # Centrar la ventana en la pantalla
        from PyQt6.QtWidgets import QApplication
        screen = QApplication.primaryScreen().availableGeometry()
        window_geometry = self.frameGeometry()
        center_point = screen.center()
        window_geometry.moveCenter(center_point)
        self.move(window_geometry.topLeft())
        
        # Layout principal
        layout = QVBoxLayout(self)
        layout.setContentsMargins(UIScale.px(70), UIScale.px(50), UIScale.px(70), UIScale.px(40))
        layout.setSpacing(UIScale.px(25))
        
        # Logo/Título
        logo_layout = QVBoxLayout()
        logo_layout.setSpacing(UIScale.px(10))
        logo_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Agregar imagen del logo
        logo_path = get_resource_path(os.path.join('assets', 'icons', 'LOGO.png'))
        if os.path.exists(logo_path):
            self.logo_image = QLabel()
            pixmap = QPixmap(logo_path)
            # Escalar el logo a un tamaño más grande y profesional (100x100 px)
            scaled_pixmap = pixmap.scaled(100, 100, Qt.AspectRatioMode.KeepAspectRatio, 
                                         Qt.TransformationMode.SmoothTransformation)
            self.logo_image.setPixmap(scaled_pixmap)
            self.logo_image.setAlignment(Qt.AlignmentFlag.AlignCenter)
            logo_layout.addWidget(self.logo_image)
            logo_layout.addSpacing(8)
        
        self.app_name = QLabel("GesMonth")
        self.app_name.setObjectName("appName")
        self.app_name.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logo_layout.addWidget(self.app_name)
        
        self.subtitle = QLabel("Sistema para la Gestión de Pagos")
        self.subtitle.setObjectName("subtitle")
        self.subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logo_layout.addWidget(self.subtitle)
        
        layout.addLayout(logo_layout)
        layout.addSpacing(25)  # Más espacio antes del formulario
        
        # Frame del formulario
        self.form_frame = QFrame()
        self.form_frame.setObjectName("formFrame")
        
        # Permitir que el frame se expanda verticalmente según el contenido
        from PyQt6.QtWidgets import QSizePolicy
        form_size_policy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        self.form_frame.setSizePolicy(form_size_policy)
        
        form_layout = QVBoxLayout(self.form_frame)
        form_layout.setContentsMargins(UIScale.px(0), UIScale.px(0), UIScale.px(0), UIScale.px(0))  # Sin márgenes, el padding lo maneja CSS
        form_layout.setSpacing(UIScale.px(0))  # Sin espaciado automático, lo controlamos manualmente
        
        # Campo Usuario
        self.user_label = QLabel("Usuario")
        self.user_label.setObjectName("fieldLabel")
        form_layout.addWidget(self.user_label)
        form_layout.addSpacing(8)  # Espacio pequeño entre label e input
        
        self.input_username = QLineEdit()
        self.input_username.setObjectName("inputField")
        self.input_username.setPlaceholderText("Ingrese su usuario")
        self.input_username.setMinimumHeight(UIScale.px(55))
        
        # Autocompletar con usuario recordado
        if self.remembered_user:
            self.input_username.setText(self.remembered_user)
        
        form_layout.addWidget(self.input_username)
        form_layout.addSpacing(20)  # Espacio entre campos
        
        # Campo Contraseña
        self.password_label = QLabel("Contraseña")
        self.password_label.setObjectName("fieldLabel")
        form_layout.addWidget(self.password_label)
        form_layout.addSpacing(8)  # Espacio pequeño entre label e input
        
        self.input_password = QLineEdit()
        self.input_password.setObjectName("inputField")
        self.input_password.setPlaceholderText("Ingrese su contraseña")
        self.input_password.setEchoMode(QLineEdit.EchoMode.Password)
        self.input_password.setMinimumHeight(UIScale.px(55))
        
        # Conectar navegación entre campos
        self.input_username.returnPressed.connect(self.input_password.setFocus)
        self.input_password.returnPressed.connect(self._intentar_login)
        
        form_layout.addWidget(self.input_password)
        form_layout.addSpacing(15)  # Espacio antes del checkbox
        
        # "Recordar usuario" con toggle pequeño
        remember_layout = QHBoxLayout()
        remember_layout.setSpacing(UIScale.px(8))
        remember_layout.setContentsMargins(UIScale.px(0), UIScale.px(0), UIScale.px(0), UIScale.px(0))
        
        remember_label = QLabel("Recordar usuario")
        remember_label.setObjectName("rememberLabel")
        remember_label.setStyleSheet("font-size: 13px; font-weight: 500;")
        remember_layout.addWidget(remember_label)
        
        self.toggle_recordar = ToggleSwitch(small=True)
        self.toggle_recordar.setCursor(Qt.CursorShape.PointingHandCursor)
        
        # Marcar toggle si hay usuario recordado
        if self.remembered_user:
            self.toggle_recordar.setChecked(True)
            self.toggle_recordar._circle_position = 17 if self.toggle_recordar.small else 33
            self.toggle_recordar.update()
        
        remember_layout.addWidget(self.toggle_recordar)
        remember_layout.addStretch()
        
        form_layout.addLayout(remember_layout)
        form_layout.addSpacing(20)  # Espacio antes del error
        
        # Label de error (oculto inicialmente)
        from PyQt6.QtWidgets import QSizePolicy
        self.error_label = QLabel()
        self.error_label.setObjectName("errorLabel")
        self.error_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.error_label.setWordWrap(True)
        self.error_label.setMinimumHeight(UIScale.px(0))
        
        # Permitir que el label se expanda verticalmente según el contenido
        size_policy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        self.error_label.setSizePolicy(size_policy)
        self.error_label.hasHeightForWidth()
        
        self.error_label.hide()
        form_layout.addWidget(self.error_label)
        form_layout.addSpacing(25)  # Espacio antes del botón
        
        # Botón Login
        self.btn_login = QPushButton("Iniciar Sesión")
        self.btn_login.setObjectName("loginButton")
        self.btn_login.setMinimumHeight(UIScale.px(60))
        self.btn_login.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_login.clicked.connect(self._intentar_login)
        form_layout.addWidget(self.btn_login)
        
        layout.addWidget(self.form_frame, 0)  # stretch factor 0 = no comprimir
        
        layout.addSpacing(20)  # Espacio fijo antes del footer
        
        # Toggle de tema centrado con solo etiqueta "Tema Oscuro"
        footer_layout = QHBoxLayout()
        footer_layout.setSpacing(UIScale.px(10))
        footer_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Label "Tema Oscuro"
        self.dark_label = QLabel("Tema Oscuro")
        self.dark_label.setObjectName("themeLabel")
        footer_layout.addWidget(self.dark_label)
        
        # Toggle switch
        self.dark_mode_toggle = ToggleSwitch()
        self.dark_mode_toggle.setCursor(Qt.CursorShape.PointingHandCursor)
        self.dark_mode_toggle.stateChanged.connect(self._toggle_tema)
        footer_layout.addWidget(self.dark_mode_toggle)
        
        layout.addLayout(footer_layout)
        
        # Sincronizar toggle con tema guardado
        self.dark_mode_toggle.setChecked(self.tema_oscuro)
        self.dark_mode_toggle._circle_position = 33 if self.tema_oscuro else 3
        self.dark_mode_toggle.update()
        
        # Aplicar tema inicial
        self._aplicar_tema()
        
        # Focus inicial: si hay usuario recordado, focus en password, sino en username
        if self.remembered_user:
            self.input_password.setFocus()
        else:
            self.input_username.setFocus()
    
    def _toggle_tema(self):
        """Cambia entre tema claro y oscuro"""
        self.tema_oscuro = self.dark_mode_toggle.isChecked()
        self._aplicar_tema()
        
        # IMPORTANTE: Guardar el tema en la base de datos inmediatamente
        tema = 'dark' if self.tema_oscuro else 'light'
        self.config_controller.set_theme(tema)
    
    def _aplicar_tema(self):
        """Aplica el tema seleccionado"""
        if self.tema_oscuro:
            # Tema Oscuro
            self.setStyleSheet(f"""
                QDialog {{
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 #0f172a,
                        stop:1 #1e293b);
                }}
                QLabel#appName {{
                    font-size: 52px;
                    font-weight: bold;
                    color: #60a5fa;
                    letter-spacing: 4px;
                    text-align: center;
                }}
                QLabel#subtitle {{
                    font-size: 15px;
                    color: #94a3b8;
                    font-weight: 400;
                    letter-spacing: 0.5px;
                }}
                QFrame#formFrame {{
                    background: rgba(30, 41, 59, 0.6);
                    border: 2px solid rgba(96, 165, 250, 0.3);
                    border-radius: 20px;
                    padding: 40px;
                }}
                QLabel#fieldLabel {{
                    font-size: 13px;
                    color: #cbd5e1;
                    font-weight: 600;
                    letter-spacing: 0.3px;
                }}
                QLineEdit#inputField {{
                    background: rgba(15, 23, 42, 0.7);
                    border: 2px solid #475569;
                    border-radius: 12px;
                    padding: 0 20px;
                    font-size: 15px;
                    color: #e2e8f0;
                }}
                QLineEdit#inputField:focus {{
                    border-color: #60a5fa;
                    background: rgba(15, 23, 42, 0.95);
                    border-width: 2px;
                }}
                QLabel#errorLabel {{
                    color: #ef4444;
                    font-size: 13px;
                    font-weight: 500;
                    padding: 10px 15px;
                    background: rgba(239, 68, 68, 0.15);
                    border: 1px solid rgba(239, 68, 68, 0.4);
                    border-radius: 8px;
                }}
                QPushButton#loginButton {{
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                        stop:0 rgba(59, 130, 246, 0.9),
                        stop:1 rgba(96, 165, 250, 0.9));
                    border: none;
                    border-radius: 14px;
                    color: white;
                    font-size: 17px;
                    font-weight: 700;
                    letter-spacing: 1.5px;
                }}
                QPushButton#loginButton:hover {{
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                        stop:0 rgba(59, 130, 246, 1),
                        stop:1 rgba(96, 165, 250, 1));
                }}
                QPushButton#loginButton:pressed {{
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                        stop:0 rgba(37, 99, 235, 1),
                        stop:1 rgba(59, 130, 246, 1));
                }}
                QLabel#themeLabel {{
                    font-size: 13px;
                    color: #94a3b8;
                    font-weight: 500;
                }}
                QLabel#rememberLabel {{
                    font-size: 13px;
                    color: #cbd5e1;
                    font-weight: 500;
                }}
                QCheckBox#rememberCheckbox {{
                    font-size: 13px;
                    color: #cbd5e1;
                    font-weight: 500;
                    spacing: 8px;
                }}
                QCheckBox#rememberCheckbox::indicator {{
                    width: 20px;
                    height: 20px;
                    border-radius: 4px;
                    border: 2px solid #475569;
                    background: rgba(15, 23, 42, 0.9);
                }}
                QCheckBox#rememberCheckbox::indicator:hover {{
                    border-color: #3b82f6;
                }}
                QCheckBox#rememberCheckbox::indicator:checked {{
                    background: #3b82f6;
                    border-color: #3b82f6;
                    image: url(none);
                }}
                QCheckBox#rememberCheckbox::indicator:checked::after {{
                    content: "✓";
                }}
            """)
        else:
            # Tema Claro
            self.setStyleSheet(f"""
                QDialog {{
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 #f8fafc,
                        stop:1 #e2e8f0);
                }}
                QLabel#appName {{
                    font-size: 52px;
                    font-weight: bold;
                    color: #2563eb;
                    letter-spacing: 4px;
                    text-align: center;
                }}
                QLabel#subtitle {{
                    font-size: 15px;
                    color: #475569;
                    font-weight: 400;
                    letter-spacing: 0.5px;
                }}
                QFrame#formFrame {{
                    background: rgba(255, 255, 255, 0.98);
                    border: 2px solid rgba(59, 130, 246, 0.25);
                    border-radius: 20px;
                    padding: 40px;
                    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
                }}
                QLabel#fieldLabel {{
                    font-size: 13px;
                    color: #334155;
                    font-weight: 600;
                    letter-spacing: 0.3px;
                }}
                QLineEdit#inputField {{
                    background: #ffffff;
                    border: 2px solid #cbd5e1;
                    border-radius: 12px;
                    padding: 0 20px;
                    font-size: 15px;
                    color: #1e293b;
                }}
                QLineEdit#inputField:focus {{
                    border-color: #3b82f6;
                    background: #ffffff;
                    border-width: 2px;
                }}
                QLabel#errorLabel {{
                    color: #dc2626;
                    font-size: 13px;
                    font-weight: 500;
                    padding: 10px 15px;
                    background: rgba(239, 68, 68, 0.1);
                    border: 1px solid rgba(239, 68, 68, 0.3);
                    border-radius: 8px;
                }}
                QPushButton#loginButton {{
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                        stop:0 #3b82f6,
                        stop:1 #60a5fa);
                    border: none;
                    border-radius: 14px;
                    color: white;
                    font-size: 17px;
                    font-weight: 700;
                    letter-spacing: 1.5px;
                }}
                QPushButton#loginButton:hover {{
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                        stop:0 #2563eb,
                        stop:1 #3b82f6);
                }}
                QPushButton#loginButton:pressed {{
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                        stop:0 #1d4ed8,
                        stop:1 #2563eb);
                }}
                QLabel#themeLabel {{
                    font-size: 13px;
                    color: #475569;
                    font-weight: 500;
                }}
                QLabel#rememberLabel {{
                    font-size: 13px;
                    color: #334155;
                    font-weight: 600;
                }}
                QCheckBox#rememberCheckbox {{
                    font-size: 13px;
                    color: #334155;
                    font-weight: 600;
                    spacing: 8px;
                }}
                QCheckBox#rememberCheckbox::indicator {{
                    width: 20px;
                    height: 20px;
                    border-radius: 4px;
                    border: 2px solid #cbd5e1;
                    background: white;
                }}
                QCheckBox#rememberCheckbox::indicator:hover {{
                    border-color: #3b82f6;
                }}
                QCheckBox#rememberCheckbox::indicator:checked {{
                    background: #3b82f6;
                    border-color: #3b82f6;
                }}
            """)
    
    def _intentar_login(self):
        """Intenta hacer login"""
        username = self.input_username.text().strip()
        password = self.input_password.text()  # NO hacer strip en password - espacios pueden ser parte de la contraseña
        
        # Si hay username, intentar autenticar primero (para verificar bloqueo)
        # Esto previene que usuarios bloqueados vean "campos vacíos" al dejar password en blanco
        if username and not password:
            # Verificar si el usuario está bloqueado antes de mostrar "campos vacíos"
            exito, mensaje = self.auth_controller.login(username, "dummy_password_check")
            if "bloqueado" in mensaje.lower():
                # Usuario está bloqueado, mostrar ese mensaje en lugar de "campos vacíos"
                self._mostrar_error(f"{mensaje}", "blocked")
                return
        
        # Validación estricta de campos vacíos (solo si no está bloqueado)
        if not username or not password:
            self._mostrar_error("! Por favor complete todos los campos", "warning")
            return
        
        # Intentar autenticar
        exito, mensaje = self.auth_controller.login(username, password)
        
        if exito:
            # Login exitoso - guardar o eliminar usuario recordado según toggle
            if self.toggle_recordar.isChecked():
                self._guardar_usuario_recordado(username)
            else:
                self._eliminar_usuario_recordado()
            
            # Mostrar mensaje de éxito y esperar 0.5 segundos
            self._mostrar_error(f"✓ {mensaje}", "success")
            
            # Deshabilitar inputs para evitar interacción durante la espera
            self.input_username.setEnabled(False)
            self.input_password.setEnabled(False)
            self.btn_login.setEnabled(False)
            
            # Timer para esperar 0.5 segundos antes de continuar
            QTimer.singleShot(500, self._completar_login)
        else:
            # Login fallido - mapeo estricto de mensajes a tipos de error
            # Usar el mensaje exacto sin modificar para evitar inconsistencias
            mensaje_lower = mensaje.lower()
            
            if "no existe" in mensaje_lower or "inexistente" in mensaje_lower:
                # Error: Usuario no encontrado en base de datos
                self._mostrar_error(f"{mensaje}", "user_error")
                self.input_username.setFocus()
                self.input_username.selectAll()
                
            elif "contraseña" in mensaje_lower and "incorrecta" in mensaje_lower:
                # Error: Contraseña incorrecta
                self._mostrar_error(f"{mensaje}", "password_error")
                self.input_password.setFocus()
                self.input_password.selectAll()  # Seleccionar para facilitar reescribir
                
            elif "bloqueado" in mensaje_lower:
                # Error: Usuario bloqueado por múltiples intentos fallidos
                # NO limpiar password para evitar el problema de "campos vacíos" en siguiente intento
                self._mostrar_error(f"{mensaje}", "blocked")
                self.input_password.setFocus()
                self.input_password.selectAll()  # Seleccionar para que vea que está bloqueado
                
            elif "desactivado" in mensaje_lower or "inactivo" in mensaje_lower:
                # Error: Usuario existe pero está desactivado
                self._mostrar_error(f"{mensaje}", "inactive")
                self.input_password.clear()
                self.input_username.setFocus()
                
            else:
                # Error genérico (no debería llegar aquí si todo está bien configurado)
                self._mostrar_error(f"! {mensaje}", "error")
                self.input_password.setFocus()
    
    def _completar_login(self):
        """Completa el proceso de login después de mostrar el mensaje de éxito"""
        tema = 'dark' if self.tema_oscuro else 'light'
        self.login_exitoso.emit(self.auth_controller.usuario_actual, tema)
        self.accept()
    
    def _mostrar_error(self, mensaje: str, tipo: str = "error"):
        """
        Muestra un mensaje con estilo profesional
        
        Args:
            mensaje: Texto del mensaje a mostrar
            tipo: Tipo de mensaje (success, warning, user_error, password_error, blocked, inactive, error)
        """
        self.error_label.setText(mensaje)
        
        # Aplicar estilos según el tipo de mensaje
        if tipo == "success":
            self.error_label.setStyleSheet("""
                QLabel {
                    color: #10b981;
                    background-color: rgba(16, 185, 129, 0.1);
                    border: 2px solid #10b981;
                    border-radius: 8px;
                    padding: 10px 20px;
                    font-size: 14px;
                    font-weight: 600;
                    min-height: 20px;
                    max-height: none;
                }
            """)
        elif tipo == "warning":
            self.error_label.setStyleSheet("""
                QLabel {
                    color: #f59e0b;
                    background-color: rgba(245, 158, 11, 0.1);
                    border: 2px solid #f59e0b;
                    border-radius: 8px;
                    padding: 10px 20px;
                    font-size: 14px;
                    font-weight: 500;
                    min-height: 20px;
                    max-height: none;
                }
            """)
        elif tipo == "user_error":
            self.error_label.setStyleSheet("""
                QLabel {
                    color: #3b82f6;
                    background-color: rgba(59, 130, 246, 0.1);
                    border: 2px solid #3b82f6;
                    border-radius: 8px;
                    padding: 10px 20px;
                    font-size: 14px;
                    font-weight: 500;
                    min-height: 20px;
                    max-height: none;
                }
            """)
        elif tipo == "password_error":
            self.error_label.setStyleSheet("""
                QLabel {
                    color: #ef4444;
                    background-color: rgba(239, 68, 68, 0.1);
                    border: 2px solid #ef4444;
                    border-radius: 8px;
                    padding: 10px 20px;
                    font-size: 14px;
                    font-weight: 500;
                    min-height: 20px;
                    max-height: none;
                }
            """)
        elif tipo == "blocked":
            self.error_label.setStyleSheet("""
                QLabel {
                    color: #dc2626;
                    background-color: rgba(220, 38, 38, 0.1);
                    border: 2px solid #dc2626;
                    border-radius: 8px;
                    padding: 10px 20px;
                    font-size: 14px;
                    font-weight: 600;
                    min-height: 20px;
                    max-height: none;
                }
            """)
        elif tipo == "inactive":
            self.error_label.setStyleSheet("""
                QLabel {
                    color: #6b7280;
                    background-color: rgba(107, 114, 128, 0.1);
                    border: 2px solid #6b7280;
                    border-radius: 8px;
                    padding: 10px 20px;
                    font-size: 14px;
                    font-weight: 500;
                    min-height: 20px;
                    max-height: none;
                }
            """)
        else:  # error genérico
            self.error_label.setStyleSheet("""
                QLabel {
                    color: #ef4444;
                    background-color: rgba(239, 68, 68, 0.1);
                    border: 2px solid #ef4444;
                    border-radius: 8px;
                    padding: 10px 20px;
                    font-size: 14px;
                    font-weight: 500;
                    min-height: 20px;
                    max-height: none;
                }
            """)
        
        self.error_label.show()
        
        # Forzar que el label se ajuste al contenido
        self.error_label.adjustSize()
        self.error_label.updateGeometry()
        
        # Animación de shake (opcional)
        QApplication.beep()
    
    def closeEvent(self, event):
        """Maneja el evento de cierre del diálogo"""
        event.accept()
    
    def _cargar_usuario_recordado(self) -> str:
        """Carga el usuario recordado desde la configuración"""
        try:
            return self.config_controller.get_remembered_user()
        except:
            return ""
    
    def _guardar_usuario_recordado(self, username: str):
        """Guarda el usuario en la configuración"""
        try:
            self.config_controller.set_remembered_user(username)
        except Exception as e:
            print(f"Error al guardar usuario recordado: {e}")
    
    def _eliminar_usuario_recordado(self):
        """Elimina el usuario recordado de la configuración"""
        try:
            self.config_controller.clear_remembered_user()
        except Exception as e:
            print(f"Error al eliminar usuario recordado: {e}")
