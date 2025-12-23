"""
Ventana principal de la aplicación con navegación lateral
"""

import os
from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QPushButton, QStackedWidget, QLabel, QFrame)
from PyQt6.QtCore import Qt, QSize, QTimer, QDateTime, QLocale
from PyQt6.QtGui import QIcon

from .dashboard_view import DashboardView
from .clientes_view import ClientesView
from .pagos_view import PagosView
from .cuotas_view import CuotasView
from .reportes_view import ReportesView
from .configuracion_view import ConfiguracionView


class MainWindow(QMainWindow):
    """Ventana principal con sidebar de navegación"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("GesMonth - Gestión de Pagos Mensuales")
        self.setMinimumSize(1200, 700)
        
        # Establecer icono de la ventana
        icon_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'assets', 'icons', 'LOGO.png')
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
        
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principal horizontal
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Crear sidebar
        self.sidebar = self._create_sidebar()
        main_layout.addWidget(self.sidebar)
        
        # Crear contenedor para el área de contenido con timestamp
        content_container = QWidget()
        content_layout = QVBoxLayout(content_container)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)
        
        # Crear área de contenido con vistas
        self.stacked_widget = QStackedWidget()
        content_layout.addWidget(self.stacked_widget)
        
        # Agregar timestamp al fondo
        self.timestamp_label = QLabel()
        self.timestamp_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.timestamp_label.setStyleSheet("""
            QLabel {
                background: rgba(15, 23, 42, 0.8);
                color: #94a3b8;
                font-size: 12px;
                font-weight: 500;
                padding: 8px 20px;
                border-top: 1px solid rgba(148, 163, 184, 0.2);
            }
        """)
        content_layout.addWidget(self.timestamp_label)
        
        main_layout.addWidget(content_container)
        
        # Configurar timer para actualizar timestamp
        self._update_timestamp()
        self.timer = QTimer()
        self.timer.timeout.connect(self._update_timestamp)
        self.timer.start(1000)  # Actualizar cada segundo
        
        # Agregar vistas
        self.dashboard_view = DashboardView()
        self.cuotas_view = CuotasView()
        self.clientes_view = ClientesView()
        self.reportes_view = ReportesView()
        self.configuracion_view = ConfiguracionView()
        
        self.stacked_widget.addWidget(self.dashboard_view)
        self.stacked_widget.addWidget(self.cuotas_view)
        self.stacked_widget.addWidget(self.clientes_view)
        self.stacked_widget.addWidget(self.reportes_view)
        self.stacked_widget.addWidget(self.configuracion_view)
        
        # Mostrar dashboard por defecto
        self.stacked_widget.setCurrentIndex(0)
        
        # Iniciar en pantalla completa después de configurar todo
        self.showFullScreen()
    
    def _create_sidebar(self) -> QWidget:
        """Crea el sidebar de navegación"""
        sidebar = QFrame()
        sidebar.setObjectName("sidebar")
        sidebar.setFixedWidth(250)
        
        layout = QVBoxLayout(sidebar)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Botones de navegación
        self.nav_buttons = []
        
        nav_items = [
            ("Dashboard", 0),
            ("Cuotas", 1),
            ("Clientes", 2),
            ("Reportes", 3),
            ("Configuración", 4)
        ]
        
        for text, index in nav_items:
            btn = QPushButton(text)
            btn.setObjectName("navButton")
            btn.setMinimumHeight(70)
            btn.setStyleSheet("font-size: 18px;")
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.clicked.connect(lambda checked, idx=index: self._change_view(idx))
            layout.addWidget(btn)
            self.nav_buttons.append(btn)
        
        # Espacio flexible al final
        layout.addStretch()
        
        # Marcar primer botón como activo
        self.nav_buttons[0].setProperty("active", True)
        
        return sidebar
    
    def _change_view(self, index: int):
        """Cambia la vista activa"""
        self.stacked_widget.setCurrentIndex(index)
        
        # Actualizar botones activos
        for i, btn in enumerate(self.nav_buttons):
            btn.setProperty("active", i == index)
            btn.style().unpolish(btn)
            btn.style().polish(btn)
        
        # Refrescar datos en las vistas
        if index == 0:  # Dashboard
            self.dashboard_view.refresh_data()
        elif index == 1:  # Cuotas
            self.clientes_view.refresh_data()
        elif index == 2:  # Clientes
            self.cuotas_view.refresh_data()
    
    def toggle_fullscreen(self, enable: bool):
        """Alterna el modo de pantalla completa"""
        if enable:
            self.showFullScreen()
        else:
            self.showNormal()
    
    def _update_timestamp(self):
        """Actualiza el timestamp con la fecha y hora actual"""
        current_datetime = QDateTime.currentDateTime()
        
        # Usar locale español
        locale = QLocale(QLocale.Language.Spanish, QLocale.Country.Colombia)
        
        # Formatear fecha y hora en español
        fecha = locale.toString(current_datetime, "dddd, dd 'de' MMMM 'de' yyyy")
        hora = current_datetime.toString("hh:mm:ss")
        
        # Capitalizar primera letra
        fecha = fecha[0].upper() + fecha[1:]
        
        self.timestamp_label.setText(f"{fecha}  •  {hora}")
