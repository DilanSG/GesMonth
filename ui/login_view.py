"""
Vista de Login mejorada con toggle de tema
"""
import os
from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                             QLineEdit, QPushButton, QFrame, QApplication, QCheckBox)
from PyQt6.QtCore import Qt, pyqtSignal, QPropertyAnimation, QEasingCurve, pyqtProperty
from PyQt6.QtGui import QIcon, QPixmap, QPainter, QBrush, QColor
from controllers.auth_controller import AuthController
from controllers.config_controller import ConfigController
from utils import get_resource_path


class ToggleSwitch(QCheckBox):
    """Toggle switch personalizado para cambiar entre temas"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(60, 30)
        self._circle_position = 3
        self.animation = QPropertyAnimation(self, b"circle_position", self)
        self.animation.setEasingCurve(QEasingCurve.Type.InOutCubic)
        self.animation.setDuration(200)
        self.stateChanged.connect(self.start_transition)
        
    @pyqtProperty(int)
    def circle_position(self):
        return self._circle_position
    
    @circle_position.setter
    def circle_position(self, pos):
        self._circle_position = pos
        self.update()
    
    def start_transition(self, value):
        self.animation.stop()
        self.animation.setStartValue(self._circle_position)
        if value:
            self.animation.setEndValue(33)
        else:
            self.animation.setEndValue(3)
        self.animation.start()
    
    def mousePressEvent(self, event):
        """Captura el click del mouse y alterna el estado manualmente"""
        # Alternar el estado manualmente
        new_state = not self.isChecked()
        self.setChecked(new_state)
        
        # Forzar la animación de la posición
        self.animation.stop()
        self.animation.setStartValue(self._circle_position)
        target_position = 33 if new_state else 3
        self.animation.setEndValue(target_position)
        self.animation.start()
        
        # No llamar a super() para evitar conflictos
        event.accept()
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Fondo del toggle
        if self.isChecked():
            # Activado (tema oscuro) - azul
            brush_color = QColor(59, 130, 246)  # #3b82f6
        else:
            # Desactivado (tema claro) - gris
            brush_color = QColor(203, 213, 225)  # #cbd5e1
        
        painter.setBrush(QBrush(brush_color))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(0, 0, self.width(), self.height(), self.height() / 2, self.height() / 2)
        
        # Círculo del toggle
        painter.setBrush(QBrush(QColor(255, 255, 255)))
        painter.drawEllipse(self._circle_position, 3, 24, 24)


class LoginView(QDialog):
    """Ventana de login"""
    
    login_exitoso = pyqtSignal(object, str)  # Emite el usuario autenticado y el tema seleccionado
    
    def __init__(self):
        super().__init__()
        self.auth_controller = AuthController()
        self.config_controller = ConfigController()
        
        # Cargar tema guardado desde configuración
        saved_theme = self.config_controller.get_theme()
        self.tema_oscuro = saved_theme == 'dark'
        
        self._init_ui()
        
    def _init_ui(self):
        """Inicializa la interfaz"""
        self.setWindowTitle("GesMonth - Iniciar Sesión")
        self.setFixedSize(650, 750)  # Ventana mucho más grande
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
        layout.setContentsMargins(60, 40, 60, 40)
        layout.setSpacing(20)
        
        # Logo/Título
        logo_layout = QVBoxLayout()
        logo_layout.setSpacing(8)
        logo_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Agregar imagen del logo
        logo_path = get_resource_path(os.path.join('assets', 'icons', 'LOGO.png'))
        if os.path.exists(logo_path):
            self.logo_image = QLabel()
            pixmap = QPixmap(logo_path)
            # Escalar el logo a un tamaño apropiado (90x90 px)
            scaled_pixmap = pixmap.scaled(90, 90, Qt.AspectRatioMode.KeepAspectRatio, 
                                         Qt.TransformationMode.SmoothTransformation)
            self.logo_image.setPixmap(scaled_pixmap)
            self.logo_image.setAlignment(Qt.AlignmentFlag.AlignCenter)
            logo_layout.addWidget(self.logo_image)
            logo_layout.addSpacing(5)
        
        self.app_name = QLabel("GesMonth")
        self.app_name.setObjectName("appName")
        self.app_name.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logo_layout.addWidget(self.app_name)
        
        self.subtitle = QLabel("Sistema para la Gestión de Pagos")
        self.subtitle.setObjectName("subtitle")
        self.subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logo_layout.addWidget(self.subtitle)
        
        layout.addLayout(logo_layout)
        layout.addSpacing(20)
        
        # Frame del formulario
        self.form_frame = QFrame()
        self.form_frame.setObjectName("formFrame")
        form_layout = QVBoxLayout(self.form_frame)
        form_layout.setContentsMargins(0, 0, 0, 0)  # Sin márgenes, el padding lo maneja CSS
        form_layout.setSpacing(0)  # Sin espaciado automático, lo controlamos manualmente
        
        # Campo Usuario
        self.user_label = QLabel("Usuario")
        self.user_label.setObjectName("fieldLabel")
        form_layout.addWidget(self.user_label)
        form_layout.addSpacing(8)  # Espacio pequeño entre label e input
        
        self.input_username = QLineEdit()
        self.input_username.setObjectName("inputField")
        self.input_username.setPlaceholderText("Ingrese su usuario")
        self.input_username.setMinimumHeight(55)
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
        self.input_password.setMinimumHeight(55)
        
        # Conectar navegación entre campos
        self.input_username.returnPressed.connect(self.input_password.setFocus)
        self.input_password.returnPressed.connect(self._intentar_login)
        
        form_layout.addWidget(self.input_password)
        form_layout.addSpacing(25)  # Espacio antes del error
        
        # Label de error (oculto inicialmente)
        self.error_label = QLabel()
        self.error_label.setObjectName("errorLabel")
        self.error_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.error_label.setWordWrap(True)
        self.error_label.setMinimumHeight(0)  # Altura 0 cuando está oculto
        self.error_label.setMaximumWidth(9999)  # Sin límite de ancho
        self.error_label.hide()
        form_layout.addWidget(self.error_label)
        form_layout.addSpacing(25)  # Espacio después del error
        
        # Botón Login
        self.btn_login = QPushButton("Iniciar Sesión")
        self.btn_login.setObjectName("loginButton")
        self.btn_login.setMinimumHeight(60)
        self.btn_login.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_login.clicked.connect(self._intentar_login)
        form_layout.addWidget(self.btn_login)
        
        layout.addWidget(self.form_frame)
        
        layout.addStretch()
        
        # Toggle de tema centrado con solo etiqueta "Tema Oscuro"
        footer_layout = QHBoxLayout()
        footer_layout.setSpacing(10)
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
        
        # Focus inicial
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
                    font-size: 48px;
                    font-weight: bold;
                    color: #3b82f6;
                    letter-spacing: 3px;
                }}
                QLabel#subtitle {{
                    font-size: 16px;
                    color: #94a3b8;
                    font-weight: 500;
                }}
                QFrame#formFrame {{
                    background: rgba(30, 41, 59, 0.85);
                    border: 2px solid rgba(59, 130, 246, 0.4);
                    border-radius: 16px;
                    padding: 30px;
                }}
                QLabel#fieldLabel {{
                    font-size: 14px;
                    color: #cbd5e1;
                    font-weight: 600;
                }}
                QLineEdit#inputField {{
                    background: rgba(15, 23, 42, 0.9);
                    border: 2px solid #475569;
                    border-radius: 10px;
                    padding: 0 20px;
                    font-size: 15px;
                    color: #e2e8f0;
                }}
                QLineEdit#inputField:focus {{
                    border-color: #3b82f6;
                    background: rgba(15, 23, 42, 1);
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
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 rgba(59, 130, 246, 0.95),
                        stop:1 rgba(59, 130, 246, 0.75));
                    border: 2px solid rgba(147, 197, 253, 0.6);
                    border-radius: 12px;
                    color: white;
                    font-size: 16px;
                    font-weight: 700;
                    letter-spacing: 1.5px;
                }}
                QPushButton#loginButton:hover {{
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 rgba(59, 130, 246, 1),
                        stop:1 rgba(59, 130, 246, 0.9));
                    border-color: rgba(147, 197, 253, 0.9);
                }}
                QPushButton#loginButton:pressed {{
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 rgba(37, 99, 235, 1),
                        stop:1 rgba(37, 99, 235, 0.95));
                }}
                QLabel#themeLabel {{
                    font-size: 13px;
                    color: #94a3b8;
                    font-weight: 500;
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
                    font-size: 48px;
                    font-weight: bold;
                    color: #2563eb;
                    letter-spacing: 3px;
                }}
                QLabel#subtitle {{
                    font-size: 16px;
                    color: #475569;
                    font-weight: 500;
                }}
                QFrame#formFrame {{
                    background: rgba(255, 255, 255, 0.95);
                    border: 2px solid rgba(59, 130, 246, 0.3);
                    border-radius: 16px;
                    padding: 30px;
                }}
                QLabel#fieldLabel {{
                    font-size: 14px;
                    color: #334155;
                    font-weight: 600;
                }}
                QLineEdit#inputField {{
                    background: white;
                    border: 2px solid #cbd5e1;
                    border-radius: 10px;
                    padding: 0 20px;
                    font-size: 15px;
                    color: #1e293b;
                }}
                QLineEdit#inputField:focus {{
                    border-color: #3b82f6;
                    background: #ffffff;
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
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 #3b82f6,
                        stop:1 #2563eb);
                    border: none;
                    border-radius: 12px;
                    color: white;
                    font-size: 16px;
                    font-weight: 700;
                    letter-spacing: 1.5px;
                }}
                QPushButton#loginButton:hover {{
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 #2563eb,
                        stop:1 #1d4ed8);
                }}
                QPushButton#loginButton:pressed {{
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 #1d4ed8,
                        stop:1 #1e40af);
                }}
                QLabel#themeLabel {{
                    font-size: 13px;
                    color: #475569;
                    font-weight: 500;
                }}
            """)
    
    def _intentar_login(self):
        """Intenta hacer login"""
        username = self.input_username.text().strip()
        password = self.input_password.text()
        
        if not username or not password:
            self._mostrar_error("Por favor complete todos los campos")
            return
        
        # Intentar autenticar
        exito, mensaje = self.auth_controller.login(username, password)
        
        if exito:
            # Login exitoso - emitir usuario y tema seleccionado
            tema = 'dark' if self.tema_oscuro else 'light'
            self.login_exitoso.emit(self.auth_controller.usuario_actual, tema)
            self.accept()
        else:
            # Login fallido
            self._mostrar_error(mensaje)
            self.input_password.clear()
            self.input_password.setFocus()
    
    def _mostrar_error(self, mensaje: str):
        """Muestra un mensaje de error"""
        self.error_label.setText(mensaje)
        self.error_label.show()
        
        # Animación de shake (opcional)
        QApplication.beep()
    
    def closeEvent(self, event):
        """Maneja el evento de cierre del diálogo"""
        event.accept()
