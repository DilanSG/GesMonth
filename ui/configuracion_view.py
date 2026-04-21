"""
Vista de configuración
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QTableWidget, QTableWidgetItem, QDialog, QLineEdit, QHeaderView, QTabWidget, QCheckBox, QFrame, QSpinBox, QSizePolicy, QFileDialog, QComboBox, QScrollArea, QColorDialog)
from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve, pyqtProperty, QTimer
from PyQt6.QtGui import QColor, QPainter, QBrush, QPen
from .responsive import UIScale
from database.models import MetodoPago
from controllers.config_controller import ConfigController
from controllers.reporte_controller import ReporteController


class ToggleSwitch(QCheckBox):
    """Toggle switch personalizado para cambiar entre temas"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(UIScale.px(60), UIScale.px(30))
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


class ConfiguracionView(QWidget):
    """Vista de configuración del sistema"""
    
    def __init__(self, usuario=None):
        super().__init__()
        self.usuario_actual = usuario
        self.config_controller = ConfigController()
        self.reporte_controller = ReporteController()
        
        # Timer para debounce del toggle de fullscreen
        self._fullscreen_change_timer = QTimer()
        self._fullscreen_change_timer.setSingleShot(True)
        self._fullscreen_change_timer.setInterval(100)  # 100ms de delay
        self._fullscreen_change_timer.timeout.connect(self._apply_fullscreen_change)
        self._pending_fullscreen_state = None
        
        self._init_ui()
    
    def showEvent(self, event):
        """Se ejecuta cuando la vista se muestra"""
        super().showEvent(event)
        
        # Sincronizar estado de fullscreen con la BD al mostrar la vista
        main_window = self.window()
        is_fullscreen = main_window.isFullScreen()
        saved_fullscreen = self.config_controller.get_fullscreen()
        
        # Re-aplicar el estado guardado si hay discrepancia
        if saved_fullscreen and not is_fullscreen:
            main_window.showFullScreen()
        elif not saved_fullscreen and is_fullscreen:
            main_window.showNormal()
        
        self._actualizar_estilos_tema()
        self._sincronizar_tema_selector()
        self._sincronizar_fullscreen_toggle()
    
    def _sincronizar_fullscreen_toggle(self):
        """Sincroniza el toggle de fullscreen con el estado guardado en BD"""
        if not hasattr(self, 'toggle_fullscreen'):
            return
        
        saved_fullscreen = self.config_controller.get_fullscreen()
        toggle_checked = self.toggle_fullscreen.isChecked()
        
        # Desconectar temporalmente la señal para evitar loops
        try:
            self.toggle_fullscreen.stateChanged.disconnect(self._toggle_fullscreen)
        except:
            pass
        
        # Actualizar si hay diferencia
        if toggle_checked != saved_fullscreen:
            self.toggle_fullscreen.setChecked(saved_fullscreen)
            
            # Actualizar posición del círculo del toggle
            correct_position = 33 if saved_fullscreen else 3
            if hasattr(self.toggle_fullscreen, '_circle_position'):
                self.toggle_fullscreen._circle_position = correct_position
            self.toggle_fullscreen.repaint()
        
        # Reconectar la señal
        self.toggle_fullscreen.stateChanged.connect(self._toggle_fullscreen)
    
    def _sincronizar_tema_selector(self):
        """Sincroniza el selector de tema con el tema actual de la aplicación"""
        if not hasattr(self, 'toggle_theme'):
            return
        
        # Leer el tema actual desde la ventana principal
        main_window = self.window()
        if hasattr(main_window, 'current_theme'):
            current_theme = main_window.current_theme
        else:
            current_theme = self.config_controller.get_theme()
        
        # Desconectar temporalmente la señal para evitar cambios no deseados
        try:
            self.toggle_theme.stateChanged.disconnect()
        except:
            pass
        
        # Actualizar el estado según el tema actual
        # True = modo oscuro, False = modo claro
        should_be_checked = current_theme == 'dark'
        self.toggle_theme.setChecked(should_be_checked)
        
        # Forzar la posición correcta del círculo sin animación
        correct_position = 33 if should_be_checked else 3
        self.toggle_theme._circle_position = correct_position
        self.toggle_theme.update()  # Forzar repintado
        self.toggle_theme._circle_position = correct_position
        self.toggle_theme.update()
        
        # Reconectar la señal
        self.toggle_theme.stateChanged.connect(self._cambiar_tema_toggle)
    
    def _actualizar_estilos_tema(self):
        """Actualiza los estilos según el tema actual"""
        # Detectar tema actual
        main_window = self.window()
        is_dark = True
        if hasattr(main_window, 'current_theme'):
            is_dark = main_window.current_theme == 'dark'
        
        # Actualizar etiquetas de secciones
        if hasattr(self, 'labels_secciones'):
            for label in self.labels_secciones:
                if is_dark:
                    label.setStyleSheet("font-size: 19px; font-weight: bold; margin-top: 20px; margin-bottom: 10px; color: #e0e7ff;")
                else:
                    label.setStyleSheet("font-size: 19px; font-weight: bold; margin-top: 20px; margin-bottom: 10px; color: #0f172a;")
        
        # Actualizar etiquetas de texto
        if hasattr(self, 'labels_texto'):
            for label in self.labels_texto:
                if is_dark:
                    label.setStyleSheet("font-size: 16px; color: #cbd5e1;")
                else:
                    label.setStyleSheet("font-size: 16px; color: #1e293b; font-weight: 600;")
        
        # Mantener estilo personalizado para descripciones de secciones
        if hasattr(self, 'labels_secciones_desc'):
            for label in self.labels_secciones_desc:
                if is_dark:
                    label.setStyleSheet("""
                        font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
                        font-size: 12px;
                        color: #8b98a8;
                        font-weight: 300;
                        font-style: italic;
                        letter-spacing: 0.5px;
                        padding: 0px;
                        padding-left: 5px;
                        margin: 0px;
                    """)
                else:
                    label.setStyleSheet("""
                        font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
                        font-size: 12px;
                        color: #6b7280;
                        font-weight: 300;
                        font-style: italic;
                        letter-spacing: 0.5px;
                        padding: 0px;
                        padding-left: 5px;
                        margin: 0px;
                    """)
        
        # Mantener estilo personalizado para descripciones de acciones
        if hasattr(self, 'labels_acciones_desc'):
            for label in self.labels_acciones_desc:
                if is_dark:
                    label.setStyleSheet("""
                        font-size: 12px;
                        color: #94a3b8;
                        font-weight: 400;
                        padding-left: 10px;
                    """)
                else:
                    label.setStyleSheet("""
                        font-size: 12px;
                        color: #6b7280;
                        font-weight: 400;
                        padding-left: 10px;
                    """)
        
        # Actualizar botones según tema
        if hasattr(self, 'backup_buttons'):
            for btn in self.backup_buttons:
                # Obtener el tipo de botón desde el nombre o texto
                texto = btn.text().lower()
                
                # Determinar el tipo de botón
                if 'limpieza' in texto or 'limpiar' in texto:
                    color_tipo = 'warning'
                elif 'reiniciar' in texto and 'db' in texto:
                    color_tipo = 'danger'
                else:
                    color_tipo = 'default'
                
                # Aplicar estilos según tema
                if color_tipo == "warning":
                    if is_dark:
                        btn.setStyleSheet("""
                            QPushButton {
                                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                    stop:0 rgba(251, 191, 36, 0.25),
                                    stop:1 rgba(251, 191, 36, 0.15));
                                border: 1px solid rgba(251, 191, 36, 0.4);
                                border-radius: 10px;
                                color: #fbbf24;
                                font-size: 13px;
                                font-weight: 600;
                                padding: 10px 20px;
                            }
                            QPushButton:hover {
                                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                    stop:0 rgba(251, 191, 36, 0.35),
                                    stop:1 rgba(251, 191, 36, 0.25));
                                border: 1px solid rgba(251, 191, 36, 0.6);
                            }
                            QPushButton:pressed {
                                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                    stop:0 rgba(251, 191, 36, 0.4),
                                    stop:1 rgba(251, 191, 36, 0.3));
                            }
                        """)
                    else:
                        btn.setStyleSheet("""
                            QPushButton {
                                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                    stop:0 rgba(251, 191, 36, 0.75),
                                    stop:1 rgba(251, 191, 36, 0.6));
                                border: 2px solid rgba(161, 98, 7, 0.9);
                                border-radius: 10px;
                                color: #a16207;
                                font-size: 13px;
                                font-weight: 700;
                                padding: 10px 20px;
                            }
                            QPushButton:hover {
                                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                    stop:0 rgba(251, 191, 36, 0.85),
                                    stop:1 rgba(251, 191, 36, 0.7));
                                border: 2px solid rgba(161, 98, 7, 1.0);
                            }
                            QPushButton:pressed {
                                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                    stop:0 rgba(251, 191, 36, 0.95),
                                    stop:1 rgba(251, 191, 36, 0.8));
                            }
                        """)
                elif color_tipo == "danger":
                    if is_dark:
                        btn.setStyleSheet("""
                            QPushButton {
                                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                    stop:0 rgba(239, 68, 68, 0.25),
                                    stop:1 rgba(239, 68, 68, 0.15));
                                border: 1px solid rgba(252, 165, 165, 0.4);
                                border-radius: 10px;
                                color: #fca5a5;
                                font-size: 13px;
                                font-weight: 600;
                                padding: 10px 20px;
                            }
                            QPushButton:hover {
                                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                    stop:0 rgba(239, 68, 68, 0.35),
                                    stop:1 rgba(239, 68, 68, 0.25));
                                border: 1px solid rgba(252, 165, 165, 0.6);
                            }
                            QPushButton:pressed {
                                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                    stop:0 rgba(239, 68, 68, 0.4),
                                    stop:1 rgba(239, 68, 68, 0.3));
                            }
                        """)
                    else:
                        btn.setStyleSheet("""
                            QPushButton {
                                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                    stop:0 rgba(239, 68, 68, 0.75),
                                    stop:1 rgba(239, 68, 68, 0.6));
                                border: 2px solid rgba(185, 28, 28, 0.9);
                                border-radius: 10px;
                                color: #b91c1c;
                                font-size: 13px;
                                font-weight: 700;
                                padding: 10px 20px;
                            }
                            QPushButton:hover {
                                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                    stop:0 rgba(239, 68, 68, 0.85),
                                    stop:1 rgba(239, 68, 68, 0.7));
                                border: 2px solid rgba(185, 28, 28, 1.0);
                            }
                            QPushButton:pressed {
                                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                    stop:0 rgba(239, 68, 68, 0.95),
                                    stop:1 rgba(239, 68, 68, 0.8));
                            }
                        """)
                else:  # default
                    if is_dark:
                        btn.setStyleSheet("""
                            QPushButton {
                                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                    stop:0 rgba(59, 130, 246, 0.4),
                                    stop:1 rgba(59, 130, 246, 0.3));
                                border: 1px solid rgba(147, 197, 253, 0.6);
                                border-radius: 10px;
                                color: #93c5fd;
                                font-size: 13px;
                                font-weight: 600;
                                padding: 10px 20px;
                            }
                            QPushButton:hover {
                                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                    stop:0 rgba(59, 130, 246, 0.5),
                                    stop:1 rgba(59, 130, 246, 0.4));
                                border: 1px solid rgba(147, 197, 253, 0.8);
                            }
                            QPushButton:pressed {
                                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                    stop:0 rgba(59, 130, 246, 0.6),
                                    stop:1 rgba(59, 130, 246, 0.5));
                            }
                        """)
                    else:
                        btn.setStyleSheet("""
                            QPushButton {
                                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                    stop:0 #60a5fa,
                                    stop:1 #3b82f6);
                                border: 2px solid #2563eb;
                                border-radius: 10px;
                                color: white;
                                font-size: 13px;
                                font-weight: 700;
                                padding: 10px 20px;
                            }
                            QPushButton:hover {
                                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                    stop:0 #3b82f6,
                                    stop:1 #2563eb);
                                border: 2px solid #1d4ed8;
                            }
                            QPushButton:pressed {
                                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                    stop:0 #2563eb,
                                    stop:1 #1d4ed8);
                            }
                        """)
        
        # Actualizar título de mantenimiento
        if hasattr(self, 'maintenance_title'):
            if is_dark:
                self.maintenance_title.setStyleSheet("font-size: 18px; font-weight: 600; margin-top: 30px; color: #cbd5e1;")
            else:
                self.maintenance_title.setStyleSheet("font-size: 18px; font-weight: 700; margin-top: 30px; color: #0f172a;")
        
        # Actualizar etiquetas de mantenimiento
        if hasattr(self, 'maintenance_labels'):
            for label in self.maintenance_labels:
                if is_dark:
                    label.setStyleSheet("font-size: 14px; color: #64748b; margin-top: 30px;")
                else:
                    label.setStyleSheet("font-size: 14px; color: #475569; font-weight: 600; margin-top: 30px;")
        
        # Actualizar footer
        if hasattr(self, 'footer_labels'):
            for label_type, label in self.footer_labels.items():
                if label_type == 'app_name':
                    if is_dark:
                        label.setStyleSheet("font-size: 18px; font-weight: bold; color: #94a3b8;")
                    else:
                        label.setStyleSheet("font-size: 18px; font-weight: bold; color: #1e293b;")
                elif label_type == 'description':
                    if is_dark:
                        label.setStyleSheet("font-size: 11px; color: #94a3b8;")
                    else:
                        label.setStyleSheet("font-size: 11px; color: #475569; font-weight: 600;")
                else:  # version y developer
                    if is_dark:
                        label.setStyleSheet("font-size: 11px; color: #94a3b8;")
                    else:
                        label.setStyleSheet("font-size: 11px; color: #64748b; font-weight: 600;")
        
        # El footer_container ya no existe, se eliminó para usar layout simple
    
    def _init_ui(self):
        """Inicializa la interfaz"""
        # Layout principal sin padding (el scroll tendrá el padding)
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(UIScale.px(0), UIScale.px(0), UIScale.px(0), UIScale.px(0))
        main_layout.setSpacing(UIScale.px(0))
        
        # Contenedor con scroll
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll.setStyleSheet("""
            QScrollArea {
                background: transparent;
                border: none;
            }
        """)
        
        # Widget contenedor del scroll
        scroll_widget = QWidget()
        scroll_widget.setStyleSheet("""
            QWidget {
                background: transparent;
            }
        """)
        scroll_layout = QVBoxLayout(scroll_widget)
        scroll_layout.setContentsMargins(UIScale.px(30), UIScale.px(30), UIScale.px(30), UIScale.px(30))
        scroll_layout.setSpacing(UIScale.px(20))
        
        # Header con título
        header_layout = QHBoxLayout()
        header_layout.setSpacing(UIScale.px(15))
        
        title = QLabel("Configuración")
        title.setObjectName("pageTitle")
        header_layout.addWidget(title)
        
        scroll_layout.addLayout(header_layout)
        
        # Tabs para diferentes secciones
        tabs = QTabWidget()
        # No establecer altura mínima para que ocupe todo el espacio disponible
        
        # Tab de información general
        info_tab = self._crear_tab_info()
        tabs.addTab(info_tab, "General")
        
        # Tab de configuración de pagos
        pagos_tab = self._crear_tab_pagos()
        tabs.addTab(pagos_tab, "Configuracion para Pagos")
        
        # Tab de usuarios (solo para superadmin)
        if self.usuario_actual and self.usuario_actual.es_superadmin:
            usuarios_tab = self._crear_tab_usuarios()
            tabs.addTab(usuarios_tab, "Gestión de Usuarios")
        
        # Tab de historial de cambios (para admins y superadmin)
        if self.usuario_actual and (self.usuario_actual.rol in ['admin', 'superadmin']):
            historial_tab = self._crear_tab_historial()
            tabs.addTab(historial_tab, "Historial de Cambios")
        
        scroll_layout.addWidget(tabs)  

        scroll.setWidget(scroll_widget)
        main_layout.addWidget(scroll)
    
    def _agregar_seccion_titulo(self, layout: QVBoxLayout, titulo: str, descripcion: str = ""):
        """Agrega un encabezado de sección con título y descripción"""
        section_layout = QVBoxLayout()
        section_layout.setSpacing(UIScale.px(2))
        section_layout.setContentsMargins(UIScale.px(0), UIScale.px(30), UIScale.px(0), UIScale.px(25))
        
        # Título
        title_label = QLabel(titulo)
        title_label.setStyleSheet("""
            font-size: 22px;
            font-weight: 700;
            color: #cbd5e1;
            padding: 0px;
            margin: 0px;
        """)
        self.labels_secciones.append(title_label)
        section_layout.addWidget(title_label)
        
        # Descripción debajo del título con indentación
        if descripcion:
            desc_label = QLabel(descripcion)
            desc_label.setStyleSheet("""
                font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
                font-size: 12px;
                color: #8b98a8;
                font-weight: 300;
                font-style: italic;
                letter-spacing: 0.5px;
                padding: 0px;
                padding-left: 10px;
                margin: 0px;
            """)
            desc_label.setWordWrap(False)
            self.labels_secciones_desc.append(desc_label)
            section_layout.addWidget(desc_label)
        
        layout.addLayout(section_layout)
    
    def _crear_fila_configuracion(self, label: str, descripcion: str = "") -> QVBoxLayout:
        """Crea una fila de configuración con label y descripción"""
        container = QVBoxLayout()
        container.setSpacing(UIScale.px(8))
        container.setContentsMargins(UIScale.px(0), UIScale.px(10), UIScale.px(0), UIScale.px(10))
        
        if label:
            label_widget = QLabel(label)
            label_widget.setStyleSheet("font-size: 15px; font-weight: 700; color: #f1f5f9; margin-bottom: 2px;")
            self.labels_texto.append(label_widget)
            container.addWidget(label_widget)
        
        if descripcion:
            desc_widget = QLabel(descripcion)
            desc_widget.setStyleSheet("font-size: 12px; color: #64748b; font-weight: 400; margin-bottom: 6px;")
            desc_widget.setWordWrap(True)
            self.labels_texto.append(desc_widget)
            container.addWidget(desc_widget)
        
        # Crear y almacenar el row horizontal como atributo del container
        row = QHBoxLayout()
        row.setSpacing(UIScale.px(15))
        row.setContentsMargins(UIScale.px(0), UIScale.px(5), UIScale.px(0), UIScale.px(0))
        container.addLayout(row)
        
        # Guardar referencia al row para poder acceder después
        container.row_layout = row
        
        return container
    
    def _crear_accion_con_boton(self, titulo: str, descripcion: str, texto_boton: str, 
                                  callback, color_boton: str = "default") -> QVBoxLayout:
        """Crea una acción con título, descripción y botón """
        container = QVBoxLayout()
        container.setSpacing(UIScale.px(2))
        container.setContentsMargins(UIScale.px(0), UIScale.px(0), UIScale.px(0), UIScale.px(0))
        
        # Título
        title_label = QLabel(titulo)
        title_label.setStyleSheet("font-size: 15px; font-weight: 700; color: #f1f5f9;")
        self.labels_texto.append(title_label)
        container.addWidget(title_label)
        
        # Descripción pegada al título con pequeña indentación
        desc_label = QLabel(descripcion)
        desc_label.setStyleSheet("""
            font-size: 12   px;
            color: #94a3b8;
            font-weight: 400;
            padding-left: 10px;
        """)
        desc_label.setWordWrap(True)
        self.labels_acciones_desc.append(desc_label)
        container.addWidget(desc_label)
        
        container.addSpacing(8)
        
        # Botón
        btn = QPushButton(texto_boton)
        btn.setMinimumHeight(UIScale.px(40))
        btn.setMaximumWidth(UIScale.px(200))
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        
        # Detectar tema actual
        main_window = self.window()
        is_dark = True
        if hasattr(main_window, 'current_theme'):
            is_dark = main_window.current_theme == 'dark'
        
        # Estilos glassmorphism según tipo de botón y tema
        if color_boton == "success":
            if is_dark:
                btn.setStyleSheet("""
                    QPushButton {
                        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                            stop:0 rgba(34, 197, 94, 0.25),
                            stop:1 rgba(34, 197, 94, 0.15));
                        border: 1px solid rgba(110, 231, 183, 0.4);
                        border-radius: 10px;
                        color: #6ee7b7;
                        font-size: 13px;
                        font-weight: 600;
                        padding: 10px 20px;
                    }
                    QPushButton:hover {
                        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                            stop:0 rgba(34, 197, 94, 0.35),
                            stop:1 rgba(34, 197, 94, 0.25));
                        border: 1px solid rgba(110, 231, 183, 0.6);
                    }
                    QPushButton:pressed {
                        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                            stop:0 rgba(34, 197, 94, 0.4),
                            stop:1 rgba(34, 197, 94, 0.3));
                    }
                """)
            else:
                btn.setStyleSheet("""
                    QPushButton {
                        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                            stop:0 rgba(34, 197, 94, 0.75),
                            stop:1 rgba(34, 197, 94, 0.6));
                        border: 2px solid rgba(21, 128, 61, 0.9);
                        border-radius: 10px;
                        color: #15803d;
                        font-size: 13px;
                        font-weight: 700;
                        padding: 10px 20px;
                    }
                    QPushButton:hover {
                        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                            stop:0 rgba(34, 197, 94, 0.85),
                            stop:1 rgba(34, 197, 94, 0.7));
                        border: 2px solid rgba(21, 128, 61, 1.0);
                    }
                    QPushButton:pressed {
                        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                            stop:0 rgba(34, 197, 94, 0.95),
                            stop:1 rgba(34, 197, 94, 0.8));
                    }
                """)
        elif color_boton == "warning":
            if is_dark:
                btn.setStyleSheet("""
                    QPushButton {
                        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                            stop:0 rgba(251, 191, 36, 0.25),
                            stop:1 rgba(251, 191, 36, 0.15));
                        border: 1px solid rgba(251, 191, 36, 0.4);
                        border-radius: 10px;
                        color: #fbbf24;
                        font-size: 13px;
                        font-weight: 600;
                        padding: 10px 20px;
                    }
                    QPushButton:hover {
                        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                            stop:0 rgba(251, 191, 36, 0.35),
                            stop:1 rgba(251, 191, 36, 0.25));
                        border: 1px solid rgba(251, 191, 36, 0.6);
                    }
                    QPushButton:pressed {
                        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                            stop:0 rgba(251, 191, 36, 0.4),
                            stop:1 rgba(251, 191, 36, 0.3));
                    }
                """)
            else:
                btn.setStyleSheet("""
                    QPushButton {
                        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                            stop:0 rgba(251, 191, 36, 0.75),
                            stop:1 rgba(251, 191, 36, 0.6));
                        border: 2px solid rgba(161, 98, 7, 0.9);
                        border-radius: 10px;
                        color: #a16207;
                        font-size: 13px;
                        font-weight: 700;
                        padding: 10px 20px;
                    }
                    QPushButton:hover {
                        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                            stop:0 rgba(251, 191, 36, 0.85),
                            stop:1 rgba(251, 191, 36, 0.7));
                        border: 2px solid rgba(161, 98, 7, 1.0);
                    }
                    QPushButton:pressed {
                        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                            stop:0 rgba(251, 191, 36, 0.95),
                            stop:1 rgba(251, 191, 36, 0.8));
                    }
                """)
        elif color_boton == "danger":
            if is_dark:
                btn.setStyleSheet("""
                    QPushButton {
                        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                            stop:0 rgba(239, 68, 68, 0.25),
                            stop:1 rgba(239, 68, 68, 0.15));
                        border: 1px solid rgba(252, 165, 165, 0.4);
                        border-radius: 10px;
                        color: #fca5a5;
                        font-size: 13px;
                        font-weight: 600;
                        padding: 10px 20px;
                    }
                    QPushButton:hover {
                        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                            stop:0 rgba(239, 68, 68, 0.35),
                            stop:1 rgba(239, 68, 68, 0.25));
                        border: 1px solid rgba(252, 165, 165, 0.6);
                    }
                    QPushButton:pressed {
                        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                            stop:0 rgba(239, 68, 68, 0.4),
                            stop:1 rgba(239, 68, 68, 0.3));
                    }
                """)
            else:
                btn.setStyleSheet("""
                    QPushButton {
                        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                            stop:0 rgba(239, 68, 68, 0.75),
                            stop:1 rgba(239, 68, 68, 0.6));
                        border: 2px solid rgba(185, 28, 28, 0.9);
                        border-radius: 10px;
                        color: #b91c1c;
                        font-size: 13px;
                        font-weight: 700;
                        padding: 10px 20px;
                    }
                    QPushButton:hover {
                        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                            stop:0 rgba(239, 68, 68, 0.85),
                            stop:1 rgba(239, 68, 68, 0.7));
                        border: 2px solid rgba(185, 28, 28, 1.0);
                    }
                    QPushButton:pressed {
                        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                            stop:0 rgba(239, 68, 68, 0.95),
                            stop:1 rgba(239, 68, 68, 0.8));
                    }
                """)
        else:  # default
            if is_dark:
                btn.setStyleSheet("""
                    QPushButton {
                        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                            stop:0 rgba(59, 130, 246, 0.25),
                            stop:1 rgba(59, 130, 246, 0.15));
                        border: 1px solid rgba(147, 197, 253, 0.4);
                        border-radius: 10px;
                        color: #93c5fd;
                        font-size: 13px;
                        font-weight: 600;
                        padding: 10px 20px;
                    }
                    QPushButton:hover {
                        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                            stop:0 rgba(59, 130, 246, 0.35),
                            stop:1 rgba(59, 130, 246, 0.25));
                        border: 1px solid rgba(147, 197, 253, 0.6);
                    }
                    QPushButton:pressed {
                        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                            stop:0 rgba(59, 130, 246, 0.4),
                            stop:1 rgba(59, 130, 246, 0.3));
                    }
                """)
            else:
                btn.setStyleSheet("""
                    QPushButton {
                        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                            stop:0 rgba(59, 130, 246, 0.75),
                            stop:1 rgba(59, 130, 246, 0.6));
                        border: 2px solid rgba(29, 78, 216, 0.9);
                        border-radius: 10px;
                        color: #1d4ed8;
                        font-size: 13px;
                        font-weight: 700;
                        padding: 10px 20px;
                    }
                    QPushButton:hover {
                        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                            stop:0 rgba(59, 130, 246, 0.85),
                            stop:1 rgba(59, 130, 246, 0.7));
                        border: 2px solid rgba(29, 78, 216, 1.0);
                    }
                    QPushButton:pressed {
                        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                            stop:0 rgba(59, 130, 246, 0.95),
                            stop:1 rgba(59, 130, 246, 0.8));
                    }
                """)
        
        btn.clicked.connect(callback)
        self.backup_buttons.append(btn)
        container.addWidget(btn, alignment=Qt.AlignmentFlag.AlignLeft)
        
        return container
    
    def _agregar_separador(self, layout: QVBoxLayout):
        """Agrega un separador horizontal """
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setStyleSheet("""
            QFrame {
                background: rgba(148, 163, 184, 0.15);
                max-height: 1px;
                margin: 30px 0px 10px 0px;
            }
        """)
        layout.addWidget(separator)
    
    def _crear_tab_info(self) -> QWidget:
        """Crea el tab de información general"""
        widget = QWidget()
        main_layout = QVBoxLayout(widget)
        main_layout.setContentsMargins(UIScale.px(0), UIScale.px(0), UIScale.px(0), UIScale.px(0))
        main_layout.setSpacing(UIScale.px(0))
        
        # Crear scroll area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll.setStyleSheet("""
            QScrollArea {
                background: transparent;
                border: none;
            }
        """)
        
        # Widget contenedor del scroll
        scroll_widget = QWidget()
        scroll_widget.setStyleSheet("""
            QWidget {
                background: transparent;
            }
        """)
        layout = QVBoxLayout(scroll_widget)
        layout.setContentsMargins(UIScale.px(40), UIScale.px(30), UIScale.px(40), UIScale.px(30))
        layout.setSpacing(UIScale.px(0))
        
        # Inicializar listas para referencias
        self.labels_secciones = []
        self.labels_texto = []
        self.labels_secciones_desc = []  # Descripciones de secciones con estilo personalizado
        self.labels_acciones_desc = []  # Descripciones de acciones con estilo personalizado
        self.backup_buttons = []
        self.maintenance_labels = []
        
        # ==================== APARIENCIA ====================
        self._agregar_seccion_titulo(
            layout,
            "Apariencia",
            "Personaliza la interfaz de la aplicación"
        )
        
        # Selector de tema
        tema_label = QLabel(" Tema")
        tema_label.setStyleSheet("font-size: 15px; font-weight: 700; color: #f1f5f9; margin-top: 10px;")
        self.labels_texto.append(tema_label)
        layout.addWidget(tema_label)
        
        tema_desc = QLabel("Cambia entre modo claro y oscuro")
        tema_desc.setStyleSheet("""
            font-size: 12px;
            color: #94a3b8;
            font-weight: 400;
            padding-left: 10px;
            margin-bottom: 6px;
        """)
        tema_desc.setWordWrap(True)
        self.labels_acciones_desc.append(tema_desc)
        layout.addWidget(tema_desc)
        
        # Container para el toggle
        tema_container = QHBoxLayout()
        tema_container.setContentsMargins(UIScale.px(5), UIScale.px(10), UIScale.px(0), UIScale.px(10))
        tema_container.setSpacing(UIScale.px(15))
        
        # Label "Modo Claro"
        label_claro = QLabel("Modo Claro")
        label_claro.setStyleSheet("font-size: 14px; color: #94a3b8; font-weight: 500;")
        self.labels_acciones_desc.append(label_claro)
        tema_container.addWidget(label_claro)
        
        # Toggle Switch
        self.toggle_theme = ToggleSwitch()
        self.toggle_theme.setCursor(Qt.CursorShape.PointingHandCursor)
        self.toggle_theme.setToolTip("Cambiar entre modo claro y oscuro")
        
        # El tema se sincronizará en showEvent
        self.toggle_theme.setChecked(True)  # Default: modo oscuro
        
        self.toggle_theme.stateChanged.connect(self._cambiar_tema_toggle)
        tema_container.addWidget(self.toggle_theme)
        
        # Label "Modo Oscuro"
        label_oscuro = QLabel("Modo Oscuro")
        label_oscuro.setStyleSheet("font-size: 14px; color: #94a3b8; font-weight: 500;")
        self.labels_acciones_desc.append(label_oscuro)
        tema_container.addWidget(label_oscuro)
        
        tema_container.addStretch()
        
        layout.addLayout(tema_container)
        layout.addSpacing(20)
        
        # Selector de pantalla completa
        fullscreen_label = QLabel(" Pantalla Completa")
        fullscreen_label.setStyleSheet("font-size: 15px; font-weight: 700; color: #f1f5f9; margin-top: 10px;")
        self.labels_texto.append(fullscreen_label)
        layout.addWidget(fullscreen_label)
        
        fullscreen_desc = QLabel("Alterna entre modo ventana y pantalla completa")
        fullscreen_desc.setStyleSheet("""
            font-size: 12px;
            color: #94a3b8;
            font-weight: 400;
            padding-left: 10px;
            margin-bottom: 6px;
        """)
        fullscreen_desc.setWordWrap(True)
        self.labels_acciones_desc.append(fullscreen_desc)
        layout.addWidget(fullscreen_desc)
        
        # Container para el toggle
        fullscreen_container = QHBoxLayout()
        fullscreen_container.setContentsMargins(UIScale.px(5), UIScale.px(10), UIScale.px(0), UIScale.px(10))
        fullscreen_container.setSpacing(UIScale.px(15))
        
        # Label "Ventana"
        label_ventana = QLabel("Ventana")
        label_ventana.setStyleSheet("font-size: 14px; color: #94a3b8; font-weight: 500;")
        self.labels_acciones_desc.append(label_ventana)
        fullscreen_container.addWidget(label_ventana)
        
        # Toggle Switch
        self.toggle_fullscreen = ToggleSwitch()
        self.toggle_fullscreen.setCursor(Qt.CursorShape.PointingHandCursor)
        self.toggle_fullscreen.setToolTip("Cambiar entre ventana y pantalla completa")
        
        # Bloquear señales durante la inicialización para evitar disparos prematuros
        self.toggle_fullscreen.blockSignals(True)
        
        # Cargar configuración guardada
        saved_fullscreen = self.config_controller.get_fullscreen()
        self.toggle_fullscreen.setChecked(saved_fullscreen)
        
        # Forzar la posición inicial del círculo sin animación
        initial_position = 33 if saved_fullscreen else 3
        if hasattr(self.toggle_fullscreen, '_circle_position'):
            self.toggle_fullscreen._circle_position = initial_position
        
        # Desbloquear señales y conectar después de la inicialización
        self.toggle_fullscreen.blockSignals(False)
        self.toggle_fullscreen.stateChanged.connect(self._toggle_fullscreen)
        
        fullscreen_container.addWidget(self.toggle_fullscreen)
        
        # Label "Pantalla Completa"
        label_fullscreen = QLabel("Pantalla Completa")
        label_fullscreen.setStyleSheet("font-size: 14px; color: #94a3b8; font-weight: 500;")
        self.labels_acciones_desc.append(label_fullscreen)
        fullscreen_container.addWidget(label_fullscreen)
        
        fullscreen_container.addStretch()
        
        layout.addLayout(fullscreen_container)
        
        # Separador
        self._agregar_separador(layout)
        
        # ==================== RESPALDOS Y EXPORTACIONES ====================
        self._agregar_seccion_titulo(
            layout,
            "Respaldos y Exportaciones",
            "Gestiona copias de seguridad y exporta datos"
        )
        
        # Botón crear respaldo
        backup_layout = self._crear_accion_con_boton(
            "Base de Datos",
            "Crea una copia de seguridad completa de tu base de datos",
            "Crear Respaldo",
            self._create_backup
        )
        backup_layout.setContentsMargins(UIScale.px(5), UIScale.px(0), UIScale.px(0), UIScale.px(0))
        layout.addLayout(backup_layout)
        layout.addSpacing(25)
        
        # Exportar clientes
        export_clientes_layout = self._crear_accion_con_boton(
            "Lista de Clientes",
            "Exporta todos los clientes a un archivo Excel editable",
            "Exportar",
            self._export_clientes
        )
        export_clientes_layout.setContentsMargins(UIScale.px(5), UIScale.px(0), UIScale.px(0), UIScale.px(0))
        layout.addLayout(export_clientes_layout)
        layout.addSpacing(25)
        
        # Importar clientes
        import_clientes_layout = self._crear_accion_con_boton(
            "Importar Clientes",
            "Carga o actualiza clientes desde un archivo Excel",
            "Seleccionar Archivo",
            self._import_clientes,
        )
        import_clientes_layout.setContentsMargins(UIScale.px(5), UIScale.px(0), UIScale.px(0), UIScale.px(0))
        layout.addLayout(import_clientes_layout)
        layout.addSpacing(25)
        
        # Exportar pagos
        export_pagos_layout = self._crear_accion_con_boton(
            "Historial de Pagos",
            "Exporta el registro completo de pagos a Excel",
            "Exportar",
            self._export_pagos
        )
        export_pagos_layout.setContentsMargins(UIScale.px(5), UIScale.px(0), UIScale.px(0), UIScale.px(0))
        layout.addLayout(export_pagos_layout)
        layout.addSpacing(25)
        
        # Exportar mora
        export_mora_layout = self._crear_accion_con_boton(
            "Clientes en Mora",
            "Exporta la lista de clientes con pagos pendientes",
            "Exportar",
            self._export_mora
        )
        export_mora_layout.setContentsMargins(UIScale.px(5), UIScale.px(0), UIScale.px(0), UIScale.px(0))
        layout.addLayout(export_mora_layout)
        layout.addSpacing(25)
        
        # Descargar logs del sistema
        logs_layout = self._crear_accion_con_boton(
            "Descargar Logs del Sistema",
            "Exporta el historial de acciones del sistema a un archivo CSV",
            "Descargar Logs",
            self._descargar_logs,
            color_boton="default"
        )
        logs_layout.setContentsMargins(UIScale.px(5), UIScale.px(0), UIScale.px(0), UIScale.px(0))
        layout.addLayout(logs_layout)
        layout.addSpacing(25)
        
        # Separador
        self._agregar_separador(layout)
        
        # ==================== ZONA PELIGROSA ====================
        self._agregar_seccion_titulo(
            layout,
            "Zona Peligrosa",
            "Las siguientes acciones son irreversibles y son responsabilidad del usuario los resultados de su uso."
        )
        
        # Reiniciar base de datos
        reset_layout = self._crear_accion_con_boton(
            "Reiniciar Base de Datos",
            "Elimina TODOS los datos y restaura la base de datos a su estado inicial",
            "Reiniciar DB",
            self._reset_database,
            color_boton="danger"
        )
        reset_layout.setContentsMargins(UIScale.px(5), UIScale.px(0), UIScale.px(0), UIScale.px(0))
        layout.addLayout(reset_layout)
        
        # Espacio antes del footer
        layout.addSpacing(60)
        
        # ==================== INFORMACIÓN DE LA APLICACIÓN ====================
        info_layout = QHBoxLayout()
        
        info_content = QVBoxLayout()
        info_content.setSpacing(UIScale.px(6))
        
        # Diccionario para almacenar las etiquetas del footer
        self.footer_labels = {}
        
        # Nombre de la aplicación
        app_name = QLabel("GesMonth")
        app_name.setStyleSheet("font-size: 18px; font-weight: bold; color: #94a3b8;")
        app_name.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.footer_labels['app_name'] = app_name
        info_content.addWidget(app_name)
        
        # Descripción
        description = QLabel("Sistema de Gestión de Pagos Mensuales")
        description.setStyleSheet("font-size: 11px; color: #94a3b8;")
        description.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.footer_labels['description'] = description
        info_content.addWidget(description)
        
        # Versión y desarrollador en layout horizontal
        details_layout = QHBoxLayout()
        details_layout.setSpacing(UIScale.px(15))
        
        # Versión
        try:
            import os
            version_file = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'VERSION')
            with open(version_file, 'r', encoding='utf-8') as f:
                version_text = f.read().strip()
        except:
            version_text = "1.0.1"
        
        version = QLabel(f"v{version_text}")
        version.setStyleSheet("font-size: 11px; color: #94a3b8;")
        self.footer_labels['version'] = version
        details_layout.addWidget(version)
        
        developer = QLabel("By: Dilan Acuña")
        developer.setStyleSheet("font-size: 11px; color: #94a3b8;")
        self.footer_labels['developer'] = developer
        details_layout.addWidget(developer)
        
        info_content.addLayout(details_layout)
        
        info_layout.addLayout(info_content)
        info_layout.addStretch()
        
        layout.addLayout(info_layout)
        
        # Espacio al final
        layout.addStretch()
        
        # Configurar el scroll
        scroll.setWidget(scroll_widget)
        main_layout.addWidget(scroll)
        
        return widget
    
    def _crear_tab_pagos(self) -> QWidget:
        """Crea el tab de configuración de pagos"""
        widget = QWidget()
        main_layout = QVBoxLayout(widget)
        main_layout.setContentsMargins(UIScale.px(0), UIScale.px(0), UIScale.px(0), UIScale.px(0))
        main_layout.setSpacing(UIScale.px(0))
        
        # Crear scroll area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll.setStyleSheet("""
            QScrollArea {
                background: transparent;
                border: none;
            }
        """)
        
        # Widget contenedor del scroll
        scroll_widget = QWidget()
        scroll_widget.setStyleSheet("""
            QWidget {
                background: transparent;
            }
        """)
        layout = QVBoxLayout(scroll_widget)
        layout.setContentsMargins(UIScale.px(20), UIScale.px(20), UIScale.px(20), UIScale.px(20))
        layout.setSpacing(UIScale.px(25))
        
        # ===== SECCION 1: AÑOS DE FACTURACION =====
        anos_title = QLabel("Años de Facturacion")
        anos_title.setStyleSheet("font-size: 16px; font-weight: bold; color: #60a5fa;")
        layout.addWidget(anos_title)
        
        anos_desc = QLabel("Seleccione los años que se mostrarán en el control de cuotas")
        anos_desc.setStyleSheet("font-size: 12px; color: #94a3b8;")
        layout.addWidget(anos_desc)
        
        # Selector de años
        anos_layout = QHBoxLayout()
        anos_layout.setSpacing(UIScale.px(15))
        
        # Año inicial
        label_inicio = QLabel("Primer Año:")
        label_inicio.setStyleSheet("font-size: 13px;")
        anos_layout.addWidget(label_inicio)
        
        self.spin_ano_inicio = QSpinBox()
        self.spin_ano_inicio.setMinimum(2020)
        self.spin_ano_inicio.setMaximum(2050)
        self.spin_ano_inicio.setValue(2025)
        self.spin_ano_inicio.setMinimumHeight(UIScale.px(40))
        self.spin_ano_inicio.setMinimumWidth(UIScale.px(100))
        self.spin_ano_inicio.setStyleSheet("font-size: 14px; padding: 5px;")
        anos_layout.addWidget(self.spin_ano_inicio)
        
        # Año final
        label_fin = QLabel("Segundo Año:")
        label_fin.setStyleSheet("font-size: 13px;")
        anos_layout.addWidget(label_fin)
        
        self.spin_ano_fin = QSpinBox()
        self.spin_ano_fin.setMinimum(2020)
        self.spin_ano_fin.setMaximum(2050)
        self.spin_ano_fin.setValue(2026)
        self.spin_ano_fin.setMinimumHeight(UIScale.px(40))
        self.spin_ano_fin.setMinimumWidth(UIScale.px(100))
        self.spin_ano_fin.setStyleSheet("font-size: 14px; padding: 5px;")
        anos_layout.addWidget(self.spin_ano_fin)
        
        anos_layout.addStretch()
        
        btn_guardar_anos = QPushButton("Guardar Años")
        btn_guardar_anos.setMinimumHeight(UIScale.px(40))
        btn_guardar_anos.setMinimumWidth(UIScale.px(130))
        btn_guardar_anos.setCursor(Qt.CursorShape.PointingHandCursor)
        
        # Detectar tema actual
        main_window = self.window()
        is_dark = True
        if hasattr(main_window, 'current_theme'):
            is_dark = main_window.current_theme == 'dark'
        
        if is_dark:
            btn_guardar_anos.setStyleSheet("""
                QPushButton {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 rgba(59, 130, 246, 0.4),
                        stop:1 rgba(59, 130, 246, 0.3));
                    border: 1px solid rgba(147, 197, 253, 0.6);
                    border-radius: 10px;
                    color: #93c5fd;
                    font-size: 13px;
                    font-weight: 600;
                    padding: 10px 20px;
                }
                QPushButton:hover {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 rgba(59, 130, 246, 0.5),
                        stop:1 rgba(59, 130, 246, 0.4));
                    border: 1px solid rgba(147, 197, 253, 0.8);
                }
                QPushButton:pressed {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 rgba(59, 130, 246, 0.6),
                        stop:1 rgba(59, 130, 246, 0.5));
                }
            """)
        else:
            btn_guardar_anos.setStyleSheet("""
                QPushButton {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 #60a5fa,
                        stop:1 #3b82f6);
                    border: 2px solid #2563eb;
                    border-radius: 10px;
                    color: white;
                    font-size: 13px;
                    font-weight: 700;
                    padding: 10px 20px;
                }
                QPushButton:hover {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 #3b82f6,
                        stop:1 #2563eb);
                    border: 2px solid #1d4ed8;
                }
                QPushButton:pressed {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 #2563eb,
                        stop:1 #1d4ed8);
                }
            """)
        
        btn_guardar_anos.clicked.connect(self._guardar_anos)
        self.backup_buttons.append(btn_guardar_anos)
        anos_layout.addWidget(btn_guardar_anos)
        
        layout.addLayout(anos_layout)
        
        # Cargar años actuales
        anos_list = self.config_controller.get_billing_years()
        if len(anos_list) >= 1:
            self.spin_ano_inicio.setValue(anos_list[0])
        if len(anos_list) >= 2:
            self.spin_ano_fin.setValue(anos_list[1])
        
        # Separador visual
        layout.addSpacing(20)
        separador = QLabel("")
        separador.setStyleSheet("border-top: 1px solid rgba(148, 163, 184, 0.2);")
        separador.setMaximumHeight(UIScale.px(1))
        layout.addWidget(separador)
        layout.addSpacing(20)
        
        # ===== SECCION 2: METODOS DE PAGO =====
        metodos_header = QHBoxLayout()
        
        metodos_title = QLabel("Metodos de Pago")
        metodos_title.setStyleSheet("font-size: 16px; font-weight: bold; color: #60a5fa;")
        metodos_header.addWidget(metodos_title)
        metodos_header.addStretch()
        
        btn_add = QPushButton("Agregar ")
        btn_add.setMinimumHeight(UIScale.px(40))
        btn_add.setMaximumWidth(UIScale.px(200))
        btn_add.setCursor(Qt.CursorShape.PointingHandCursor)
        
        # Detectar tema actual
        if is_dark:
            btn_add.setStyleSheet("""
                QPushButton {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 rgba(59, 130, 246, 0.4),
                        stop:1 rgba(59, 130, 246, 0.3));
                    border: 1px solid rgba(147, 197, 253, 0.6);
                    border-radius: 10px;
                    color: #93c5fd;
                    font-size: 13px;
                    font-weight: 600;
                    padding: 10px 20px;
                }
                QPushButton:hover {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 rgba(59, 130, 246, 0.5),
                        stop:1 rgba(59, 130, 246, 0.4));
                    border: 1px solid rgba(147, 197, 253, 0.8);
                }
                QPushButton:pressed {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 rgba(59, 130, 246, 0.6),
                        stop:1 rgba(59, 130, 246, 0.5));
                }
            """)
        else:
            btn_add.setStyleSheet("""
                QPushButton {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 #60a5fa,
                        stop:1 #3b82f6);
                    border: 2px solid #2563eb;
                    border-radius: 10px;
                    color: white;
                    font-size: 13px;
                    font-weight: 700;
                    padding: 10px 20px;
                }
                QPushButton:hover {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 #3b82f6,
                        stop:1 #2563eb);
                    border: 2px solid #1d4ed8;
                }
                QPushButton:pressed {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 #2563eb,
                        stop:1 #1d4ed8);
                }
            """)
        
        btn_add.clicked.connect(self._agregar_metodo_pago)
        self.backup_buttons.append(btn_add)
        metodos_header.addWidget(btn_add)
        
        layout.addLayout(metodos_header)
        
        # Tabla de métodos de pago
        self.tabla_metodos = QTableWidget()
        self.tabla_metodos.setColumnCount(2)
        self.tabla_metodos.setHorizontalHeaderLabels(['Metodo de Pago', 'Acciones'])
        
        header = self.tabla_metodos.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)  # Metodo de Pago
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Fixed)  # Acciones
        
        self.tabla_metodos.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.tabla_metodos.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.tabla_metodos.setAlternatingRowColors(True)
        self.tabla_metodos.verticalHeader().setVisible(False)
        self.tabla_metodos.setColumnWidth(1, 90)
        self.tabla_metodos.setMinimumHeight(UIScale.px(300))  # Altura mínima para que se vean varios métodos
        
        layout.addWidget(self.tabla_metodos)
        
        # Espacio al final
        layout.addSpacing(20)
        
        # Configurar el scroll
        scroll.setWidget(scroll_widget)
        main_layout.addWidget(scroll)
        
        # Cargar datos
        self._cargar_metodos_pago()
        
        return widget
    
    def _crear_tab_usuarios(self) -> QWidget:
        """Crea el tab de gestión de usuarios (solo para superadmin)"""
        from .usuarios_management import UsuariosManagement
        return UsuariosManagement(self.usuario_actual)
    
    def _crear_tab_historial(self) -> QWidget:
        """Crea el tab de historial de cambios (para admins y superadmin)"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(UIScale.px(30), UIScale.px(30), UIScale.px(30), UIScale.px(30))
        layout.setSpacing(UIScale.px(20))
        
        # Título y descripción
        title = QLabel("Historial de Cambios del Sistema")
        title.setStyleSheet("font-size: 18px; font-weight: bold; color: #60a5fa;")
        layout.addWidget(title)
        
        desc = QLabel("Registro completo de todas las acciones realizadas en el sistema")
        desc.setStyleSheet("font-size: 13px; color: #94a3b8;")
        desc.setWordWrap(True)
        layout.addWidget(desc)
        
        # Barra de botones
        buttons_layout = QHBoxLayout()
        buttons_layout.addStretch()
        
        # Botón para borrar logs (solo para superadmin)
        if self.usuario_actual and self.usuario_actual.es_superadmin:
            btn_borrar = QPushButton(" Borrar Logs")
            btn_borrar.setMinimumHeight(UIScale.px(35))
            btn_borrar.setCursor(Qt.CursorShape.PointingHandCursor)
            btn_borrar.setStyleSheet("""
                QPushButton {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                        stop:0 rgba(239, 68, 68, 0.9),
                        stop:1 rgba(220, 38, 38, 0.9));
                    border: 1px solid rgba(239, 68, 68, 0.6);
                    border-radius: 8px;
                    color: white;
                    font-size: 13px;
                    font-weight: bold;
                    padding: 0 20px;
                }
                QPushButton:hover {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                        stop:0 rgba(239, 68, 68, 1.0),
                        stop:1 rgba(220, 38, 38, 1.0));
                }
            """)
            btn_borrar.clicked.connect(self._borrar_logs)
            buttons_layout.addWidget(btn_borrar)
        
        # Botón para refrescar
        btn_refresh = QPushButton(" Actualizar")
        btn_refresh.setMinimumHeight(UIScale.px(35))
        btn_refresh.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_refresh.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(59, 130, 246, 0.9),
                    stop:1 rgba(37, 99, 235, 0.9));
                border: 1px solid rgba(59, 130, 246, 0.6);
                border-radius: 8px;
                color: white;
                font-size: 13px;
                font-weight: bold;
                padding: 0 20px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(59, 130, 246, 1.0),
                    stop:1 rgba(37, 99, 235, 1.0));
            }
        """)
        btn_refresh.clicked.connect(self._cargar_historial)
        buttons_layout.addWidget(btn_refresh)
        
        layout.addLayout(buttons_layout)
        
        # Tabla de logs
        self.tabla_historial = QTableWidget()
        self.tabla_historial.setColumnCount(5)
        self.tabla_historial.setHorizontalHeaderLabels(['Fecha y Hora', 'Usuario', 'Acción', 'Detalles', 'ID'])
        
        # Configurar ancho de columnas
        header = self.tabla_historial.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)  # Fecha
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)  # Usuario
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)  # Acción
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)  # Detalles
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)  # ID
        
        # Configuración visual
        self.tabla_historial.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.tabla_historial.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.tabla_historial.setAlternatingRowColors(True)
        self.tabla_historial.setShowGrid(False)
        self.tabla_historial.verticalHeader().setVisible(False)
        self.tabla_historial.setMinimumHeight(UIScale.px(400))
        
        # Habilitar word wrap para que el texto se expanda en múltiples líneas
        self.tabla_historial.setWordWrap(True)
        self.tabla_historial.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        
        layout.addWidget(self.tabla_historial)
        
        # Cargar datos inicialmente
        self._cargar_historial()
        
        return tab
    
    def _cargar_historial(self):
        """Carga todos los logs en la tabla"""
        from database.models import LogSistema
        from controllers.log_controller import LogController
        
        log_ctrl = LogController()
        logs = log_ctrl.obtener_logs(limite=1000)  # Últimos 1000 logs
        
        self.tabla_historial.setRowCount(len(logs))
        
        for row, log in enumerate(logs):
            # Fecha y hora
            fecha_item = QTableWidgetItem(log['fecha_hora'])
            fecha_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.tabla_historial.setItem(row, 0, fecha_item)
            
            # Usuario
            usuario_item = QTableWidgetItem(log['usuario_nombre'])
            usuario_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.tabla_historial.setItem(row, 1, usuario_item)
            
            # Acción
            accion_item = QTableWidgetItem(log['accion'])
            accion_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            
            # Colorear según tipo de acción
            if 'Crear' in log['accion'] or 'Registrar' in log['accion']:
                accion_item.setForeground(QColor(34, 197, 94))  # Verde
            elif 'Eliminar' in log['accion']:
                accion_item.setForeground(QColor(239, 68, 68))  # Rojo
            elif 'Editar' in log['accion'] or 'Actualizar' in log['accion'] or 'Cambiar' in log['accion']:
                accion_item.setForeground(QColor(59, 130, 246))  # Azul
            elif 'Impago' in log['accion']:
                accion_item.setForeground(QColor(234, 179, 8))  # Amarillo
            
            self.tabla_historial.setItem(row, 2, accion_item)
            
            # Detalles (con word wrap habilitado)
            detalles_item = QTableWidgetItem(log['detalles'])
            detalles_item.setTextAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
            self.tabla_historial.setItem(row, 3, detalles_item)
            
            # ID
            id_item = QTableWidgetItem(str(log['id']))
            id_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.tabla_historial.setItem(row, 4, id_item)
        
        # Ajustar altura de filas al contenido después de cargar todos los datos
        self.tabla_historial.resizeRowsToContents()
    
    def _borrar_logs(self):
        """Borra todos los logs del sistema (solo superadmin)"""
        # Verificar que sea superadmin
        if not self.usuario_actual or not self.usuario_actual.es_superadmin:
            dialog = ConfirmacionDialog(
                self,
                "Acceso Denegado",
                "Solo el superadministrador puede borrar logs",
                tipo="error"
            )
            dialog.exec()
            return
        
        # Diálogo de confirmación con advertencia fuerte
        dialog = ConfirmacionDialog(
            self,
            "Confirmar Borrado de Logs",
            "¿Está seguro de que desea borrar TODOS los logs del sistema?\n\n"
            "Esta acción es IRREVERSIBLE y eliminará permanentemente:\n\n"
            "• Todo el historial de acciones\n"
            "• Registros de cambios de usuarios\n"
            "• Auditoría del sistema\n\n"
            "  ADVERTENCIA: Se perderá toda la trazabilidad del sistema",
            tipo="warning"
        )
        
        if dialog.exec() == QDialog.DialogCode.Accepted:
            try:
                from controllers.log_controller import LogController
                
                log_ctrl = LogController()
                cantidad_borrada = log_ctrl.borrar_todos_logs()
                
                # Registrar la acción de borrado en un nuevo log
                log_ctrl.registrar_log(
                    usuario_id=self.usuario_actual.id,
                    usuario_nombre=self.usuario_actual.nombre_completo,
                    accion="Borrar Logs del Sistema",
                    detalles=f"Se eliminaron {cantidad_borrada} registros del historial"
                )
                
                # Recargar la tabla
                self._cargar_historial()
                
                # Mensaje de éxito
                dialog_success = ConfirmacionDialog(
                    self,
                    "Logs Borrados",
                    f"Se eliminaron exitosamente {cantidad_borrada} registros del historial",
                    tipo="success"
                )
                dialog_success.exec()
                
            except Exception as e:
                # Mensaje de error
                dialog_error = ConfirmacionDialog(
                    self,
                    "Error",
                    f"No se pudieron borrar los logs: {str(e)}",
                    tipo="error"
                )
                dialog_error.exec()
    
    def _guardar_anos(self):
        """Guarda los años de facturacion"""
        ano_1 = self.spin_ano_inicio.value()
        ano_2 = self.spin_ano_fin.value()
        
        # Guardar los 2 años específicos (ordenados)
        try:
            anos_formatted = self.config_controller.set_billing_years(ano_1, ano_2)
            dialog = ConfirmacionDialog(
                self,
                "Éxito",
                f"Años actualizados: {anos_formatted}\n\nActualice la vista de Cuotas para ver los cambios.",
                tipo="success"
            )
            dialog.exec()
        except Exception as e:
            dialog = ConfirmacionDialog(
                self,
                "Error",
                f"No se pudo guardar: {str(e)}",
                tipo="error"
            )
            dialog.exec()
    
    def _cargar_metodos_pago(self):
        """Carga los métodos de pago en la tabla"""
        metodos = MetodoPago.obtener_todos()
        self.tabla_metodos.setRowCount(len(metodos))
        
        for row, metodo in enumerate(metodos):
            # Nombre del método con su color
            nombre_widget = QWidget()
            nombre_layout = QHBoxLayout(nombre_widget)
            nombre_layout.setContentsMargins(UIScale.px(8), UIScale.px(4), UIScale.px(8), UIScale.px(4))
            nombre_layout.setSpacing(UIScale.px(10))
            
            # Nombre del método con color aplicado al texto
            nombre_label = QLabel(metodo.nombre)
            nombre_label.setStyleSheet(f"font-size: 14px; color: {metodo.color}; font-weight: 700;")
            nombre_layout.addWidget(nombre_label)
            nombre_layout.addStretch()
            
            self.tabla_metodos.setCellWidget(row, 0, nombre_widget)
            
            # Botones de acción con iconos compactos
            actions_widget = QWidget()
            actions_layout = QHBoxLayout(actions_widget)
            actions_layout.setContentsMargins(UIScale.px(0), UIScale.px(0), UIScale.px(0), UIScale.px(0))
            actions_layout.setSpacing(UIScale.px(6))
            actions_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
            
            # Botón Editar (icono)
            btn_edit = QPushButton("✏️")
            btn_edit.setFixedSize(UIScale.px(26), UIScale.px(26))
            btn_edit.setToolTip("Editar método de pago")
            btn_edit.setStyleSheet("""
                QPushButton {
                    background: rgba(96, 165, 250, 0.2);
                    border: 1px solid rgba(96, 165, 250, 0.5);
                    border-radius: 13px;
                    color: #60a5fa;
                    font-size: 14px;
                    padding: 0;
                }
                QPushButton:hover {
                    background: rgba(96, 165, 250, 0.4);
                    border: 1px solid rgba(96, 165, 250, 0.8);
                }
            """)
            btn_edit.setCursor(Qt.CursorShape.PointingHandCursor)
            btn_edit.clicked.connect(lambda checked, m=metodo: self._editar_metodo_pago(m))
            
            # Botón Eliminar (icono)
            btn_delete = QPushButton("🗑️")
            btn_delete.setFixedSize(UIScale.px(26), UIScale.px(26))
            btn_delete.setToolTip("Eliminar método de pago")
            btn_delete.setStyleSheet("""
                QPushButton {
                    background: rgba(239, 68, 68, 0.2);
                    border: 1px solid rgba(239, 68, 68, 0.5);
                    border-radius: 13px;
                    color: #ef4444;
                    font-size: 14px;
                    padding: 0;
                }
                QPushButton:hover {
                    background: rgba(239, 68, 68, 0.4);
                    border: 1px solid rgba(239, 68, 68, 0.8);
                }
            """)
            btn_delete.setCursor(Qt.CursorShape.PointingHandCursor)
            btn_delete.clicked.connect(lambda checked, mid=metodo.id: self._eliminar_metodo_pago(mid))
            
            actions_layout.addWidget(btn_edit)
            actions_layout.addWidget(btn_delete)
            
            self.tabla_metodos.setCellWidget(row, 1, actions_widget)
            self.tabla_metodos.setRowHeight(row, 58)
    
    def _agregar_metodo_pago(self):
        """Muestra el diálogo para agregar método de pago"""
        dialog = MetodoPagoDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            nombre = dialog.get_nombre()
            color = dialog.get_color()
            if nombre:
                try:
                    metodo_id = MetodoPago.crear(nombre, color)
                    
                    # Registrar log
                    if hasattr(self, 'usuario_actual') and self.usuario_actual:
                        from controllers.log_controller import LogController
                        log_ctrl = LogController()
                        log_ctrl.registrar_log(
                            usuario_id=self.usuario_actual.id if hasattr(self.usuario_actual, 'id') else None,
                            usuario_nombre=self.usuario_actual.username if hasattr(self.usuario_actual, 'username') else self.usuario_actual.nombre_completo if hasattr(self.usuario_actual, 'nombre_completo') else "Usuario",
                            accion='Crear Método de Pago',
                            detalles=f'Nuevo método de pago creado llamado {nombre}'
                        )
                    
                    dialog_success = ConfirmacionDialog(
                        self,
                        "Éxito",
                        "Método de pago agregado correctamente",
                        tipo="success"
                    )
                    dialog_success.exec()
                    self._cargar_metodos_pago()
                except Exception as e:
                    dialog_error = ConfirmacionDialog(
                        self,
                        "Error",
                        f"No se pudo agregar el método: {str(e)}",
                        tipo="error"
                    )
                    dialog_error.exec()
    
    def _editar_metodo_pago(self, metodo: MetodoPago):
        """Muestra el diálogo para editar método de pago"""
        dialog = MetodoPagoDialog(self, metodo)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            nombre = dialog.get_nombre()
            color = dialog.get_color()
            if nombre:
                try:
                    MetodoPago.actualizar(metodo.id, nombre, True, color)
                    
                    # Registrar log
                    if hasattr(self, 'usuario_actual') and self.usuario_actual:
                        from controllers.log_controller import LogController
                        log_ctrl = LogController()
                        
                        # Solo registrar si cambió el nombre
                        if metodo.nombre != nombre:
                            detalles = f'Método de pago anterior: {metodo.nombre} | Método de pago nuevo: {nombre}'
                            
                            log_ctrl.registrar_log(
                                usuario_id=self.usuario_actual.id if hasattr(self.usuario_actual, 'id') else None,
                                usuario_nombre=self.usuario_actual.username if hasattr(self.usuario_actual, 'username') else self.usuario_actual.nombre_completo if hasattr(self.usuario_actual, 'nombre_completo') else "Usuario",
                                accion='Editar Método de Pago',
                                detalles=detalles
                            )
                    
                    dialog_success = ConfirmacionDialog(
                        self,
                        "Éxito",
                        "Método de pago actualizado correctamente",
                        tipo="success"
                    )
                    dialog_success.exec()
                    self._cargar_metodos_pago()
                except Exception as e:
                    dialog_error = ConfirmacionDialog(
                        self,
                        "Error",
                        f"No se pudo actualizar el método: {str(e)}",
                        tipo="error"
                    )
                    dialog_error.exec()
    
    def _eliminar_metodo_pago(self, metodo_id: int):
        """Elimina un método de pago"""
        # Obtener info del método antes de eliminar
        metodo_info = None
        try:
            from database.connection import DatabaseConnection
            db = DatabaseConnection()
            cursor = db.get_connection().cursor()
            cursor.execute('SELECT nombre, color FROM metodos_pago WHERE id = ?', (metodo_id,))
            row = cursor.fetchone()
            if row:
                metodo_info = {'nombre': row['nombre'], 'color': row['color']}
        except:
            pass
        
        dialog = ConfirmacionDialog(
            self,
            "Confirmar eliminación",
            "¿Está seguro de eliminar este método de pago?",
            tipo="question"
        )
        
        if dialog.exec() == QDialog.DialogCode.Accepted:
            try:
                MetodoPago.eliminar(metodo_id)
                
                # Registrar log
                if hasattr(self, 'usuario_actual') and self.usuario_actual:
                    from controllers.log_controller import LogController
                    log_ctrl = LogController()
                    detalles = f'Método de pago eliminado: {metodo_info["nombre"]}' if metodo_info else "Método de pago eliminado"
                    
                    log_ctrl.registrar_log(
                        usuario_id=self.usuario_actual.id if hasattr(self.usuario_actual, 'id') else None,
                        usuario_nombre=self.usuario_actual.username if hasattr(self.usuario_actual, 'username') else self.usuario_actual.nombre_completo if hasattr(self.usuario_actual, 'nombre_completo') else "Usuario",
                        accion='Eliminar Método de Pago',
                        detalles=detalles
                    )
                
                dialog_success = ConfirmacionDialog(
                    self,
                    "Éxito",
                    "Método de pago eliminado correctamente",
                    tipo="success"
                )
                dialog_success.exec()
                self._cargar_metodos_pago()
            except Exception as e:
                dialog_error = ConfirmacionDialog(
                    self,
                    "Error",
                    f"No se pudo eliminar el método: {str(e)}",
                    tipo="error"
                )
                dialog_error.exec()
    
    def _toggle_fullscreen(self, state):
        """Alterna el modo de pantalla completa (con debounce)"""
        self._pending_fullscreen_state = bool(state)
        
        # Reiniciar timer: espera 100ms antes de aplicar el cambio
        # Esto evita múltiples eventos rápidos del toggle
        self._fullscreen_change_timer.stop()
        self._fullscreen_change_timer.start()
    
    def _apply_fullscreen_change(self):
        """Aplica el cambio de fullscreen después del debounce"""
        if self._pending_fullscreen_state is None:
            return
        
        is_enabled = self._pending_fullscreen_state
        main_window = self.window()
        
        # Cambiar el estado de la ventana
        if hasattr(main_window, 'toggle_fullscreen'):
            main_window.toggle_fullscreen(is_enabled)
        
        # Guardar en BD
        self.config_controller.set_fullscreen(is_enabled)
        self._pending_fullscreen_state = None
    
    def _cambiar_tema(self, tema_texto: str):
        """Cambia el tema de la aplicación"""
        # Convertir texto a código de tema
        theme = 'dark' if tema_texto == 'Modo Oscuro' else 'light'
        
        # Obtener ventana principal
        main_window = self.window()
        if hasattr(main_window, 'change_theme'):
            if main_window.change_theme(theme):
                dialog = ConfirmacionDialog(
                    self,
                    "Tema Actualizado",
                    f"El tema se ha cambiado a {tema_texto}",
                    tipo="success"
                )
                dialog.exec()
            else:
                dialog = ConfirmacionDialog(
                    self,
                    "Error",
                    "No se pudo cambiar el tema",
                    tipo="error"
                )
                dialog.exec()
    
    def _cambiar_tema_toggle(self, state):
        """Cambia el tema usando el toggle switch"""
        # True = modo oscuro, False = modo claro
        theme = 'dark' if state else 'light'
        
        # Obtener ventana principal
        main_window = self.window()
        if hasattr(main_window, 'change_theme'):
            main_window.change_theme(theme)
    
    def _create_backup(self):
        """Crea un respaldo de la base de datos"""
        try:
            backup_path = self.config_controller.create_backup()
            dialog = ConfirmacionDialog(
                self,
                "Éxito",
                f"Respaldo creado exitosamente:\n{backup_path}",
                tipo="success"
            )
            dialog.exec()
        except Exception as e:
            dialog = ConfirmacionDialog(
                self,
                "Error",
                f"No se pudo crear el respaldo:\n{str(e)}",
                tipo="error"
            )
            dialog.exec()
    
    def _export_clientes(self):
        """Exporta la lista de clientes"""
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Guardar reporte",
            "reporte_clientes.xlsx",
            "Excel Files (*.xlsx)"
        )
        
        if file_path:
            if self.reporte_controller.exportar_clientes(file_path):
                dialog = ConfirmacionDialog(
                    self,
                    "Éxito",
                    f"Reporte guardado en:\n{file_path}",
                    tipo="success"
                )
                dialog.exec()
            else:
                dialog = ConfirmacionDialog(
                    self,
                    "Error",
                    "No se pudo generar el reporte",
                    tipo="error"
                )
                dialog.exec()
    
    def _import_clientes(self):
        """Importa clientes desde un archivo Excel"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Seleccionar archivo de clientes",
            "",
            "Excel Files (*.xlsx *.xls)"
        )
        
        if file_path:
            exito, mensaje, insertados, actualizados = self.reporte_controller.importar_clientes(file_path)
            
            if exito:
                tipo = "success" if insertados + actualizados > 0 else "info"
                dialog = ConfirmacionDialog(
                    self,
                    "Importación Completada",
                    mensaje,
                    tipo=tipo
                )
                dialog.exec()
                
                # Recargar vista si se modificaron datos
                if insertados + actualizados > 0:
                    # Notificar a la ventana principal para refrescar vistas
                    if hasattr(self.window(), 'refresh_all_views'):
                        self.window().refresh_all_views()
            else:
                dialog = ConfirmacionDialog(
                    self,
                    "Error al Importar",
                    mensaje,
                    tipo="error"
                )
                dialog.exec()
    
    def _export_pagos(self):
        """Exporta el historial de pagos"""
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Guardar reporte",
            "reporte_pagos.xlsx",
            "Excel Files (*.xlsx)"
        )
        
        if file_path:
            if self.reporte_controller.exportar_pagos(file_path):
                dialog = ConfirmacionDialog(
                    self,
                    "Éxito",
                    f"Reporte guardado en:\n{file_path}",
                    tipo="success"
                )
                dialog.exec()
            else:
                dialog = ConfirmacionDialog(
                    self,
                    "Error",
                    "No se pudo generar el reporte",
                    tipo="error"
                )
                dialog.exec()
    
    def _export_mora(self):
        """Exporta clientes en mora"""
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Guardar reporte",
            "reporte_mora.xlsx",
            "Excel Files (*.xlsx)"
        )
        
        if file_path:
            if self.reporte_controller.exportar_mora(file_path):
                dialog = ConfirmacionDialog(
                    self,
                    "Éxito",
                    f"Reporte guardado en:\n{file_path}",
                    tipo="success"
                )
                dialog.exec()
            else:
                dialog = ConfirmacionDialog(
                    self,
                    "Error",
                    "No se pudo generar el reporte",
                    tipo="error"
                )
                dialog.exec()
    
    def _descargar_logs(self):
        """Descarga los logs del sistema a un archivo CSV"""
        from PyQt6.QtWidgets import QFileDialog
        from controllers.log_controller import LogController
        from datetime import datetime
        import os
        
        # Determinar carpeta por defecto
        try:
            from utils import get_data_path
            default_dir = os.path.dirname(get_data_path(''))
        except:
            default_dir = os.path.expanduser("~")
        
        # Nombre de archivo con fecha y hora
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        default_filename = f"logs_gesmonth_{timestamp}.csv"
        default_path = os.path.join(default_dir, default_filename)
        
        # Diálogo para guardar archivo
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Guardar Logs del Sistema",
            default_path,
            "Archivos CSV (*.csv);;Todos los archivos (*.*)"
        )
        
        if file_path:
            try:
                log_controller = LogController()
                
                # Exportar todos los logs
                exito = log_controller.exportar_logs_csv(file_path)
                
                if exito:
                    # Obtener estadísticas
                    stats = log_controller.obtener_estadisticas()
                    total_logs = stats.get('total_logs', 0)
                    
                    dialog_success = ConfirmacionDialog(
                        self,
                        "Éxito",
                        f"Logs exportados correctamente.\n\n"
                        f"Total de registros: {total_logs}\n"
                        f"Archivo guardado en:\n{file_path}",
                        tipo="success"
                    )
                    dialog_success.exec()
                else:
                    dialog_error = ConfirmacionDialog(
                        self,
                        "Error",
                        "No se pudieron exportar los logs.\n"
                        "Es posible que no haya registros disponibles.",
                        tipo="error"
                    )
                    dialog_error.exec()
            except Exception as e:
                dialog_error = ConfirmacionDialog(
                    self,
                    "Error",
                    f"Error al exportar logs:\n{str(e)}",
                    tipo="error"
                )
                dialog_error.exec()
    
    def _reset_database(self):
        """Reinicia la base de datos con múltiples advertencias"""
        # Primera advertencia
        dialog1 = ConfirmacionDialog(
            self,
            "⚠️ ADVERTENCIA CRÍTICA",
            "Está a punto de ELIMINAR TODA LA INFORMACIÓN de la base de datos.\n\n"
            "Esto incluye:\n"
            "• Todos los clientes registrados\n"
            "• Todo el historial de cuotas\n"
            "• Todos los pagos registrados\n"
            "• Todas las configuraciones personalizadas\n\n"
            "Esta acción NO se puede deshacer.\n\n"
            "¿Está COMPLETAMENTE SEGURO de continuar?",
            tipo="warning"
        )
        
        if dialog1.exec() != QDialog.DialogCode.Accepted:
            return
        
        # Segunda confirmación
        dialog2 = ConfirmacionDialog(
            self,
            "⛔ ÚLTIMA ADVERTENCIA",
            "SE PERDERÁN TODOS LOS DATOS PERMANENTEMENTE.\n\n"
            "Le recomendamos crear un respaldo antes de continuar.\n\n"
            "¿Desea crear un respaldo ahora?",
            tipo="question"
        )
        
        if dialog2.exec() == QDialog.DialogCode.Accepted:
            # Usuario quiere crear respaldo primero
            try:
                backup_path = self.config_controller.create_backup()
                dialog_backup = ConfirmacionDialog(
                    self,
                    "Respaldo Creado",
                    f"Respaldo guardado en:\n{backup_path}\n\n"
                    "¿Desea continuar con el reinicio de la base de datos?",
                    tipo="question"
                )
                if dialog_backup.exec() != QDialog.DialogCode.Accepted:
                    return
            except Exception as e:
                dialog_error = ConfirmacionDialog(
                    self,
                    "Error al Crear Respaldo",
                    f"No se pudo crear el respaldo:\n{str(e)}\n\n"
                    "¿Desea continuar de todas formas?",
                    tipo="error"
                )
                if dialog_error.exec() != QDialog.DialogCode.Accepted:
                    return
        
        # Confirmación final con texto de verificación
        dialog3 = ConfirmacionDialog(
            self,
            "🔴 CONFIRMACIÓN FINAL",
            "Para confirmar el reinicio de la base de datos,\n"
            "debe estar absolutamente seguro.\n\n"
            "Se eliminarán TODOS los datos del sistema.\n\n"
            "Esta es su última oportunidad para cancelar.",
            tipo="error"
        )
        
        if dialog3.exec() == QDialog.DialogCode.Accepted:
            try:
                # Reiniciar la base de datos
                import os
                import sys
                from database.connection import DatabaseConnection
                
                db = DatabaseConnection()
                db_path = db._db_path  # Acceder al atributo privado
                
                # Cerrar conexión
                if db._connection:
                    db._connection.close()
                    DatabaseConnection._connection = None
                    DatabaseConnection._instance = None
                
                # Eliminar archivo de base de datos
                if os.path.exists(db_path):
                    os.remove(db_path)
                
                # Reinicializar
                DatabaseConnection._instance = None
                db = DatabaseConnection()
                
                dialog_success = ConfirmacionDialog(
                    self,
                    "Base de Datos Reiniciada",
                    "La base de datos ha sido reiniciada exitosamente.\n\n"
                    "El sistema se reiniciará ahora.",
                    tipo="success"
                )
                dialog_success.exec()
                
                # Reiniciar la aplicación
                from PyQt6.QtWidgets import QApplication
                QApplication.quit()
                os.execl(sys.executable, sys.executable, *sys.argv)
                
            except Exception as e:
                dialog
                _error = ConfirmacionDialog(
                    self,
                    "Error Crítico",
                    f"Error al reiniciar la base de datos:\n{str(e)}",
                    tipo="error"
                )
                dialog_error.exec()


class ConfirmacionDialog(QDialog):
    """Diálogo de confirmación personalizado con estilo consistente"""
    
    def __init__(self, parent, titulo: str, mensaje: str, tipo: str = "info"):
        super().__init__(parent)
        self.titulo = titulo
        self.mensaje = mensaje
        self.tipo = tipo  # "success", "error", "warning", "question", "info"
        self.setWindowTitle(titulo)
        self.setMinimumWidth(UIScale.px(450))
        self._init_ui()
    
    def _init_ui(self):
        """Inicializa la interfaz del diálogo"""
        layout = QVBoxLayout(self)
        layout.setSpacing(UIScale.px(20))
        layout.setContentsMargins(UIScale.px(30), UIScale.px(30), UIScale.px(30), UIScale.px(30))
        
        # Detectar tema actual desde la ventana principal
        main_window = self.parent()
        if main_window:
            main_window = main_window.window()
        is_dark = True
        if main_window and hasattr(main_window, 'current_theme'):
            is_dark = main_window.current_theme == 'dark'
        
        # Título con color según tipo
        titulo = QLabel(self.titulo)
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        titulo.setWordWrap(True)
        
        colores = {
            "success": "#22c55e",
            "error": "#ef4444",
            "warning": "#eab308",
            "question": "#3b82f6",
            "info": "#cbd5e1"
        }
        color = colores.get(self.tipo, "#cbd5e1")
        
        titulo.setStyleSheet(f"font-size: 20px; color: {color}; font-weight: 700;")
        layout.addWidget(titulo)
        
        layout.addSpacing(10)
        
        # Mensaje
        mensaje_label = QLabel(self.mensaje)
        if is_dark:
            mensaje_label.setStyleSheet("font-size: 14px; color: #cbd5e1; line-height: 1.5;")
        else:
            mensaje_label.setStyleSheet("font-size: 14px; color: #1e293b; font-weight: 600; line-height: 1.5;")
        mensaje_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        mensaje_label.setWordWrap(True)
        layout.addWidget(mensaje_label)
        
        layout.addSpacing(10)
        
        # Botones según el tipo
        if self.tipo == "question":
            # Dos botones: Sí y No
            btn_layout = QHBoxLayout()
            btn_layout.setSpacing(UIScale.px(15))
            
            btn_si = QPushButton("Sí")
            btn_si.setMinimumHeight(UIScale.px(40))
            btn_si.setCursor(Qt.CursorShape.PointingHandCursor)
            btn_si.setStyleSheet("""
                QPushButton {
                    background: rgba(34, 197, 94, 0.25);
                    color: #22c55e;
                    border: 2px solid #22c55e;
                    border-radius: 8px;
                    font-size: 14px;
                    font-weight: 600;
                }
                QPushButton:hover {
                    background: rgba(34, 197, 94, 0.35);
                }
            """)
            btn_si.clicked.connect(self.accept)
            btn_layout.addWidget(btn_si)
            
            btn_no = QPushButton("No")
            btn_no.setMinimumHeight(UIScale.px(40))
            btn_no.setCursor(Qt.CursorShape.PointingHandCursor)
            btn_no.setStyleSheet("""
                QPushButton {
                    background: rgba(71, 85, 105, 0.25);
                    color: #94a3b8;
                    border: 2px solid #475569;
                    border-radius: 8px;
                    font-size: 14px;
                    font-weight: 600;
                }
                QPushButton:hover {
                    background: rgba(71, 85, 105, 0.35);
                }
            """)
            btn_no.clicked.connect(self.reject)
            btn_layout.addWidget(btn_no)
            
            layout.addLayout(btn_layout)
        else:
            # Un solo botón: Aceptar
            btn_aceptar = QPushButton("Aceptar")
            btn_aceptar.setMinimumHeight(UIScale.px(40))
            btn_aceptar.setCursor(Qt.CursorShape.PointingHandCursor)
            
            if self.tipo == "success":
                estilo_btn = """
                    QPushButton {
                        background: rgba(34, 197, 94, 0.25);
                        color: #22c55e;
                        border: 2px solid #22c55e;
                        border-radius: 8px;
                        font-size: 14px;
                        font-weight: 600;
                    }
                    QPushButton:hover {
                        background: rgba(34, 197, 94, 0.35);
                    }
                """
            elif self.tipo == "error":
                estilo_btn = """
                    QPushButton {
                        background: rgba(239, 68, 68, 0.25);
                        color: #ef4444;
                        border: 2px solid #ef4444;
                        border-radius: 8px;
                        font-size: 14px;
                        font-weight: 600;
                    }
                    QPushButton:hover {
                        background: rgba(239, 68, 68, 0.35);
                    }
                """
            elif self.tipo == "warning":
                estilo_btn = """
                    QPushButton {
                        background: rgba(234, 179, 8, 0.25);
                        color: #eab308;
                        border: 2px solid #eab308;
                        border-radius: 8px;
                        font-size: 14px;
                        font-weight: 600;
                    }
                    QPushButton:hover {
                        background: rgba(234, 179, 8, 0.35);
                    }
                """
            else:  # info
                estilo_btn = """
                    QPushButton {
                        background: rgba(59, 130, 246, 0.25);
                        color: #3b82f6;
                        border: 2px solid #3b82f6;
                        border-radius: 8px;
                        font-size: 14px;
                        font-weight: 600;
                    }
                    QPushButton:hover {
                        background: rgba(59, 130, 246, 0.35);
                    }
                """
            
            btn_aceptar.setStyleSheet(estilo_btn)
            btn_aceptar.clicked.connect(self.accept)
            layout.addWidget(btn_aceptar)


class MetodoPagoDialog(QDialog):
    """Diálogo para agregar/editar métodos de pago"""
    
    def __init__(self, parent=None, metodo: MetodoPago = None):
        super().__init__(parent)
        self.metodo = metodo
        self.color_seleccionado = metodo.color if metodo else "#3b82f6"
        self.setWindowTitle("Editar Método de Pago" if metodo else "Agregar Método de Pago")
        self.setMinimumWidth(UIScale.px(450))
        self._init_ui()
    
    def _init_ui(self):
        """Inicializa la interfaz del diálogo"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(UIScale.px(30), UIScale.px(30), UIScale.px(30), UIScale.px(30))
        layout.setSpacing(UIScale.px(20))
        
        # Detectar tema actual desde la ventana principal
        main_window = self.parent()
        if main_window:
            main_window = main_window.window()
        self.is_dark = True
        if main_window and hasattr(main_window, 'current_theme'):
            self.is_dark = main_window.current_theme == 'dark'
        
        # Título
        titulo = QLabel("Editar Método de Pago" if self.metodo else "Agregar Método de Pago")
        if self.is_dark:
            titulo.setStyleSheet("font-size: 20px; color: #cbd5e1; font-weight: 700;")
        else:
            titulo.setStyleSheet("font-size: 20px; color: #1e293b; font-weight: 700;")
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(titulo)
        
        layout.addSpacing(10)
        
        # Campo nombre
        label = QLabel("Nombre del Método:")
        if self.is_dark:
            label.setStyleSheet("font-size: 14px; color: #94a3b8; font-weight: 500; margin-bottom: 5px;")
        else:
            label.setStyleSheet("font-size: 14px; color: #334155; font-weight: 600; margin-bottom: 5px;")
        layout.addWidget(label)
        
        self.input_nombre = QLineEdit()
        self.input_nombre.setPlaceholderText("Ej: Efectivo, Transferencia, Tarjeta...")
        self.input_nombre.setMinimumHeight(UIScale.px(40))
        
        if self.metodo:
            self.input_nombre.setText(self.metodo.nombre)
        
        layout.addWidget(self.input_nombre)
        
        layout.addSpacing(10)
        
        # Selector de color
        color_label = QLabel("Color del Método:")
        if self.is_dark:
            color_label.setStyleSheet("font-size: 14px; color: #94a3b8; font-weight: 500; margin-bottom: 5px;")
        else:
            color_label.setStyleSheet("font-size: 14px; color: #334155; font-weight: 600; margin-bottom: 5px;")
        layout.addWidget(color_label)
        
        color_row = QHBoxLayout()
        color_row.setSpacing(UIScale.px(12))
        
        # Botón para seleccionar color
        self.btn_color = QPushButton("Seleccionar Color")
        self.btn_color.setMinimumHeight(UIScale.px(40))
        self.btn_color.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_color.clicked.connect(self._seleccionar_color)
        self._actualizar_boton_color()
        
        color_row.addWidget(self.btn_color)
        
        # Vista previa del color
        self.color_preview = QFrame()
        self.color_preview.setFixedSize(UIScale.px(40), UIScale.px(40))
        self.color_preview.setStyleSheet(f"""
            QFrame {{
                background-color: {self.color_seleccionado};
                border: 2px solid {"#475569" if self.is_dark else "#cbd5e1"};
                border-radius: 8px;
            }}
        """)
        color_row.addWidget(self.color_preview)
        
        layout.addLayout(color_row)
        
        layout.addSpacing(10)
        
        # Botones con diseño mejorado
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(UIScale.px(15))
        
        btn_cancel = QPushButton("Cancelar")
        btn_cancel.setMinimumHeight(UIScale.px(45))
        btn_cancel.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_cancel.setStyleSheet("""
            QPushButton {
                background: rgba(71, 85, 105, 0.25);
                color: #94a3b8;
                border: 2px solid #475569;
                border-radius: 8px;
                font-size: 14px;
                font-weight: 600;
            }
            QPushButton:hover {
                background: rgba(71, 85, 105, 0.35);
            }
        """)
        btn_cancel.clicked.connect(self.reject)
        
        btn_save = QPushButton("Guardar")
        btn_save.setMinimumHeight(UIScale.px(45))
        btn_save.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_save.setStyleSheet("""
            QPushButton {
                background: rgba(34, 197, 94, 0.25);
                color: #22c55e;
                border: 2px solid #22c55e;
                border-radius: 8px;
                font-size: 14px;
                font-weight: 600;
            }
            QPushButton:hover {
                background: rgba(34, 197, 94, 0.35);
            }
        """)
        btn_save.clicked.connect(self._validate_and_accept)
        
        buttons_layout.addWidget(btn_cancel)
        buttons_layout.addWidget(btn_save)
        
        layout.addLayout(buttons_layout)
    
    def _seleccionar_color(self):
        """Abre el diálogo de selección de color"""
        color_inicial = QColor(self.color_seleccionado)
        color = QColorDialog.getColor(color_inicial, self, "Seleccionar Color del Método")
        
        if color.isValid():
            self.color_seleccionado = color.name()
            self._actualizar_boton_color()
            self.color_preview.setStyleSheet(f"""
                QFrame {{
                    background-color: {self.color_seleccionado};
                    border: 2px solid {"#475569" if self.is_dark else "#cbd5e1"};
                    border-radius: 8px;
                }}
            """)
    
    def _actualizar_boton_color(self):
        """Actualiza el estilo del botón de color"""
        self.btn_color.setStyleSheet(f"""
            QPushButton {{
                background: {self.color_seleccionado};
                color: {"white" if self._es_color_oscuro(self.color_seleccionado) else "black"};
                border: 2px solid {"#475569" if self.is_dark else "#cbd5e1"};
                border-radius: 8px;
                font-size: 13px;
                font-weight: 600;
            }}
            QPushButton:hover {{
                opacity: 0.9;
                border-color: {self.color_seleccionado};
            }}
        """)
    
    def _es_color_oscuro(self, hex_color: str) -> bool:
        """Determina si un color hexadecimal es oscuro"""
        hex_color = hex_color.lstrip('#')
        r, g, b = int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)
        luminance = (0.299 * r + 0.587 * g + 0.114 * b) / 255
        return luminance < 0.5
    
    def _validate_and_accept(self):
        """Valida los datos antes de aceptar"""
        if not self.input_nombre.text().strip():
            dialog = ConfirmacionDialog(
                self,
                "Error",
                "El nombre del método es obligatorio",
                tipo="warning"
            )
            dialog.exec()
            return
        
        self.accept()
    
    def get_nombre(self) -> str:
        """Retorna el nombre del método"""
        return self.input_nombre.text().strip()
    
    def get_color(self) -> str:
        """Retorna el color seleccionado"""
        return self.color_seleccionado
