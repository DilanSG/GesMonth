"""
Ventana principal de la aplicación con navegación lateral
"""

# OS: Operaciones con rutas de archivos
import os  # os: construcción de rutas para iconos y recursos

# PyQt6 Widgets: Componentes gráficos de la interfaz
from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QPushButton, QStackedWidget, QLabel, QFrame, QApplication)
# QMainWindow: ventana principal, QWidget: widget base, QVBoxLayout/QHBoxLayout: layouts verticales/horizontales
# QPushButton: botones, QStackedWidget: pila de vistas, QLabel: etiquetas de texto
# QFrame: marco contenedor, QApplication: aplicación Qt

# PyQt6 Core: Funcionalidades centrales de Qt
from PyQt6.QtCore import Qt, QSize, QTimer, QDateTime, QLocale
# Qt: constantes globales, QSize: tamaños, QTimer: temporizadores
# QDateTime: fecha/hora, QLocale: localización

# PyQt6 GUI: Elementos gráficos y renderizado
from PyQt6.QtGui import QIcon, QPixmap, QPainter
# QIcon: iconos, QPixmap: imágenes, QPainter: dibujado personalizado

# PyQt6 SVG: Renderizado de archivos SVG
from PyQt6.QtSvg import QSvgRenderer  # QSvgRenderer: carga y renderiza imágenes SVG

# Utils: Utilidades de rutas
from utils import get_resource_path  # get_resource_path: rutas correctas de recursos

# Responsive: Sistema de escalado y espaciado adaptable
from .responsive import UIScale, Sp, expanding


# Views: Vistas de la aplicación
from .home_view import HomeView  # HomeView: vista de inicio/dashboard
from .clientes_view import ClientesView  # ClientesView: gestión de clientes
from .cuotas_view import CuotasView
from .reportes_view import ReportesView
from .configuracion_view import ConfiguracionView
from controllers.theme_controller import ThemeController
from controllers.log_controller import LogController


class MainWindow(QMainWindow):
    """Ventana principal con sidebar de navegación"""
    
    def __init__(self, app, usuario):
        super().__init__()
        self.app = app
        self.usuario_actual = usuario  # Usuario autenticado
        self.theme_controller = ThemeController()
        
        self.setWindowTitle("GesMonth - Gestión de Pagos Mensuales")
        self.setMinimumSize(UIScale.px(960), UIScale.px(640))

        # Estado del sidebar para comportamiento responsive
        self._sidebar_compact = False
        
        # Guardar tema actual (sin aplicar todavía)
        self.current_theme = self.theme_controller.get_current_theme()
        
        # Establecer icono de la ventana
        icon_path = get_resource_path(os.path.join('assets', 'icons', 'LOGO.png'))
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
        
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principal horizontal
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(UIScale.px(0), UIScale.px(0), UIScale.px(0), UIScale.px(0))
        main_layout.setSpacing(UIScale.px(0))
        
        # Crear sidebar
        self.sidebar = self._create_sidebar()
        main_layout.addWidget(self.sidebar)
        
        # Crear contenedor para el área de contenido con timestamp
        content_container = QWidget()
        content_layout = QVBoxLayout(content_container)
        content_layout.setContentsMargins(UIScale.px(0), UIScale.px(0), UIScale.px(0), UIScale.px(0))
        content_layout.setSpacing(UIScale.px(0))
        
        # Crear área de contenido con vistas
        self.stacked_widget = QStackedWidget()
        content_layout.addWidget(self.stacked_widget)
        
        # Footer con timestamp y versión
        footer_layout = QHBoxLayout()
        footer_layout.setContentsMargins(UIScale.px(10), UIScale.px(5), UIScale.px(10), UIScale.px(5))
        
        # Timestamp centrado
        self.timestamp_label = QLabel()
        self.timestamp_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        footer_layout.addStretch()
        footer_layout.addWidget(self.timestamp_label)
        footer_layout.addStretch()
        
        # Versión a la derecha
        self.version_label = QLabel()
        self.version_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        footer_layout.addWidget(self.version_label)
        
        # Widget contenedor del footer
        footer_widget = QWidget()
        footer_widget.setLayout(footer_layout)
        content_layout.addWidget(footer_widget)
        
        main_layout.addWidget(content_container)
        
        # Cargar y mostrar versión desde archivo VERSION
        self._load_version()
        
        # Configurar timer para actualizar timestamp en tiempo real
        # El timestamp se muestra en el footer y se actualiza cada segundo
        self._update_timestamp()  # Primera actualización inmediata
        self.timer = QTimer()  # Timer de Qt para ejecución periódica
        self.timer.timeout.connect(self._update_timestamp)  # Conectar señal timeout a método
        self.timer.start(1000)  # Disparar cada 1000ms (1 segundo)
        
        # Instanciar todas las vistas de la aplicación
        # Patrón: cada vista es un QWidget que maneja una sección específica
        self.home_view = HomeView()  # Dashboard con estadísticas
        self.cuotas_view = CuotasView(usuario_actual=usuario)  # Control de cuotas mensuales
        self.clientes_view = ClientesView()  # CRUD de clientes
        self.reportes_view = ReportesView()  # Generación de reportes
        self.configuracion_view = ConfiguracionView(usuario)  # Configuración y administración
        
        # Configurar sistema de logs para la vista de clientes
        # Inyección de dependencias: log_controller y usuario_actual
        # Esto permite que el controlador de clientes registre acciones en el log
        log_controller = LogController()
        self.clientes_view.controller.set_log_controller(log_controller)
        self.clientes_view.controller.set_usuario_actual(usuario)
        
        self.stacked_widget.addWidget(self.home_view)
        self.stacked_widget.addWidget(self.cuotas_view)
        self.stacked_widget.addWidget(self.clientes_view)
        self.stacked_widget.addWidget(self.reportes_view)
        self.stacked_widget.addWidget(self.configuracion_view)
        
        # Mostrar home por defecto
        self.stacked_widget.setCurrentIndex(0)
        
        # Aplicar tema DESPUÉS de crear todos los widgets
        self.apply_theme(self.current_theme)
        
        # Aplicar configuración de pantalla completa guardada con delay
        # para asegurar que la ventana esté completamente inicializada
        saved_fullscreen = self.theme_controller.config_controller.get_fullscreen()
        if saved_fullscreen:
            QTimer.singleShot(300, self.showFullScreen)
    

    
    def _create_sidebar(self) -> QWidget:
        """Crea el sidebar de navegación"""
        sidebar = QFrame()
        sidebar.setObjectName("sidebar")
        sidebar.setFixedWidth(UIScale.sidebar_width())
        
        layout = QVBoxLayout(sidebar)
        layout.setContentsMargins(UIScale.px(0), UIScale.px(0), UIScale.px(0), UIScale.px(0))
        layout.setSpacing(UIScale.px(0))
        
        # Información del usuario en la parte superior
        user_frame = QFrame()
        user_frame.setObjectName("userInfoFrame")
        user_frame.setMinimumHeight(UIScale.px(110))
        
        # Detectar tema actual
        is_dark = self.current_theme == "dark"
        
        # Estilo del frame según tema
        if is_dark:
            user_frame.setStyleSheet("""
                #userInfoFrame {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                        stop:0 rgba(30, 41, 59, 0.5),
                        stop:1 rgba(15, 23, 42, 0.5));
                    border-bottom: 2px solid rgba(59, 130, 246, 0.3);
                    border-radius: 0px;
                }
            """)
        else:
            user_frame.setStyleSheet("""
                #userInfoFrame {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                        stop:0 rgba(248, 250, 252, 0.9),
                        stop:1 rgba(241, 245, 249, 0.9));
                    border-bottom: 2px solid rgba(59, 130, 246, 0.2);
                    border-radius: 0px;
                }
            """)
        
        user_layout = QVBoxLayout(user_frame)
        user_layout.setContentsMargins(UIScale.px(20), UIScale.px(25), UIScale.px(20), UIScale.px(25))
        user_layout.setSpacing(UIScale.px(5))
        user_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Texto "Bienvenido"
        welcome_label = QLabel("Sesión iniciada como:")
        welcome_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        if is_dark:
            welcome_label.setStyleSheet("""
                font-size: 13px;
                color: #94a3b8;
                font-weight: 500;
                letter-spacing: 1px;
                text-transform: uppercase;
            """)
        else:
            welcome_label.setStyleSheet("""
                font-size: 13px;
                color: #64748b;
                font-weight: 600;
                letter-spacing: 1px;
                text-transform: uppercase;
            """)
        
        # Nombre del usuario
        user_name_label = QLabel(self.usuario_actual.nombre_completo)
        user_name_label.setObjectName("userName")
        user_name_label.setWordWrap(True)
        user_name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        if is_dark:
            user_name_label.setStyleSheet("""
                font-size: 20px;
                font-weight: 700;
                color: #ffffff;
                margin: 5px 0px;
            """)
        else:
            user_name_label.setStyleSheet("""
                font-size: 20px;
                font-weight: 700;
                color: #0f172a;
                margin: 5px 0px;
            """)
        
        user_layout.addWidget(welcome_label)
        user_layout.addWidget(user_name_label)
        
        layout.addWidget(user_frame)
        self._user_frame = user_frame  # referencia para colapso del sidebar
        
        # Botones de navegación
        self.nav_buttons = []
        
        nav_items = [
            ("Home", 0, "home.svg"),
            ("Cuotas", 1, "cuotas.svg"),
            ("Clientes", 2, "clientes.svg"),
            ("Reportes", 3, "reportes.svg")
        ]
        self._nav_items = nav_items  # referencia para colapso del sidebar
        
        for text, index, icon_file in nav_items:
            btn = QPushButton(f"  {text}")  # Espacio para el icono
            btn.setObjectName("navButton")
            btn.setMinimumHeight(UIScale.px(70))
            btn.setStyleSheet("font-size: 18px; text-align: left; padding-left: 20px;")
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.setToolTip(text)  # visible en modo compacto (solo iconos)
            btn.clicked.connect(lambda checked, idx=index: self._change_view(idx))
            
            # Cargar y aplicar icono SVG
            icon_path = get_resource_path(os.path.join("assets", "icons", icon_file))
            if os.path.exists(icon_path):
                with open(icon_path, 'r', encoding='utf-8') as f:
                    svg_content = f.read()
                    # Aplicar color según tema
                    if is_dark:
                        svg_content = svg_content.replace('stroke="currentColor"', 'stroke="#94a3b8"')
                    else:
                        svg_content = svg_content.replace('stroke="currentColor"', 'stroke="#64748b"')
                    
                    pixmap = QPixmap(32, 32)
                    pixmap.fill(Qt.GlobalColor.transparent)
                    painter = QPainter(pixmap)
                    renderer = QSvgRenderer(svg_content.encode())
                    renderer.render(painter)
                    painter.end()
                    
                    btn.setIcon(QIcon(pixmap))
                    btn.setIconSize(QSize(24, 24))
            
            layout.addWidget(btn)
            self.nav_buttons.append(btn)
        
        # Espacio flexible
        layout.addStretch()
        
        # ── Botones inferiores — modo expandido (HBox) ─────────────────────
        # En modo compacto se oculta este widget y se muestra _bottom_compact.
        self._bottom_full = QWidget()
        full_bl = QHBoxLayout(self._bottom_full)
        full_bl.setContentsMargins(UIScale.px(10), UIScale.px(5), UIScale.px(10), UIScale.px(20))
        full_bl.setSpacing(UIScale.px(8))

        cfg_f = self._make_action_btn(
            "configIconButton", "settings.svg",
            "#94a3b8" if is_dark else "#64748b",
            lambda: self._change_view(4), "Configuración",
            "rgba(100, 116, 139, 0.15)"
        )
        rst_f = self._make_action_btn(
            "restartIconButton", "logout-session.svg",
            "#60a5fa" if is_dark else "#3b82f6",
            self._reiniciar_app, "Cerrar sesión",
            "rgba(59, 130, 246, 0.2)"
        )
        lgt_f = self._make_action_btn(
            "logoutIconButton", "power-off.svg",
            "#f87171" if is_dark else "#dc2626",
            self._logout, "Cerrar programa",
            "rgba(220, 38, 38, 0.2)"
        )
        full_bl.addWidget(cfg_f)
        full_bl.addStretch()
        full_bl.addWidget(rst_f)
        full_bl.addStretch()
        full_bl.addWidget(lgt_f)

        # ── Botones inferiores — modo compacto (VBox, solo iconos) ──────────
        self._bottom_compact = QWidget()
        compact_bl = QVBoxLayout(self._bottom_compact)
        compact_bl.setContentsMargins(UIScale.px(8), UIScale.px(5), UIScale.px(8), UIScale.px(20))
        compact_bl.setSpacing(UIScale.px(6))
        compact_bl.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        cfg_c = self._make_action_btn(
            "configIconButton", "settings.svg",
            "#94a3b8" if is_dark else "#64748b",
            lambda: self._change_view(4), "Configuración",
            "rgba(100, 116, 139, 0.15)", size=40
        )
        rst_c = self._make_action_btn(
            "restartIconButton", "logout-session.svg",
            "#60a5fa" if is_dark else "#3b82f6",
            self._reiniciar_app, "Cerrar sesión",
            "rgba(59, 130, 246, 0.2)", size=40
        )
        lgt_c = self._make_action_btn(
            "logoutIconButton", "power-off.svg",
            "#f87171" if is_dark else "#dc2626",
            self._logout, "Cerrar programa",
            "rgba(220, 38, 38, 0.2)", size=40
        )
        compact_bl.addWidget(cfg_c)
        compact_bl.addWidget(rst_c)
        compact_bl.addWidget(lgt_c)
        self._bottom_compact.setVisible(False)  # oculto hasta que se colapse

        layout.addWidget(self._bottom_full)
        layout.addWidget(self._bottom_compact)
        
        # Marcar primer botón como activo
        self.nav_buttons[0].setProperty("active", True)
        
        return sidebar

    def _make_action_btn(
        self,
        obj_name: str,
        icon_file: str,
        icon_color: str,
        callback,
        tooltip: str,
        hover_color: str = "rgba(100, 116, 139, 0.15)",
        size: int = 48,
    ) -> "QPushButton":
        """
        Crea un botón de acción del sidebar con icono SVG.
        Extrae la lógica repetida de carga SVG y estilo.
        """
        btn = QPushButton()
        btn.setObjectName(obj_name)
        btn.setFixedSize(UIScale.px(size), UIScale.px(size))
        btn.setToolTip(tooltip)
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        btn.clicked.connect(callback)

        svg_path = get_resource_path(os.path.join("assets", "icons", icon_file))
        if os.path.exists(svg_path):
            with open(svg_path, 'r', encoding='utf-8') as f:
                svg_content = f.read()
            svg_content = svg_content.replace('stroke="currentColor"', f'stroke="{icon_color}"')
            svg_content = svg_content.replace('fill="#000000"', f'fill="{icon_color}"')

            pixmap = QPixmap(32, 32)
            pixmap.fill(Qt.GlobalColor.transparent)
            painter = QPainter(pixmap)
            renderer = QSvgRenderer(svg_content.encode())
            renderer.render(painter)
            painter.end()

            btn.setIcon(QIcon(pixmap))
            btn.setIconSize(QSize(UIScale.px(24), UIScale.px(24)))

        radius = UIScale.px(size) // 2
        btn.setStyleSheet(f"""
            QPushButton {{
                background: transparent;
                border: none;
                border-radius: {radius}px;
            }}
            QPushButton:hover {{
                background: {hover_color};
            }}
        """)
        return btn

    # ── Sidebar responsive ──────────────────────────────────────────────────

    def _update_sidebar_mode(self, compact: bool) -> None:
        """
        Alterna entre modo compacto (solo iconos, 64 px) y modo expandido
        (texto + iconos, 250 px) según el ancho de la ventana.

        Se llama desde resizeEvent; no hace nada si el estado no cambia.
        """
        if compact == self._sidebar_compact:
            return
        self._sidebar_compact = compact

        if compact:
            # Reducir ancho y ocultar elementos textuales
            self.sidebar.setFixedWidth(UIScale.sidebar_compact_width())
            self._user_frame.setVisible(False)
            for btn, (text, _, _) in zip(self.nav_buttons, self._nav_items):
                btn.setText("")
                btn.setMinimumHeight(UIScale.px(56))
                btn.setStyleSheet(
                    "font-size: 18px; text-align: center; padding: 0; padding-top: 4px;"
                )
            self._bottom_full.setVisible(False)
            self._bottom_compact.setVisible(True)
        else:
            # Restaurar modo expandido
            self.sidebar.setFixedWidth(UIScale.sidebar_width())
            self._user_frame.setVisible(True)
            for btn, (text, _, _) in zip(self.nav_buttons, self._nav_items):
                btn.setText(f"  {text}")
                btn.setMinimumHeight(UIScale.px(70))
                btn.setStyleSheet(
                    "font-size: 18px; text-align: left; padding-left: 20px;"
                )
            self._bottom_full.setVisible(True)
            self._bottom_compact.setVisible(False)

    def resizeEvent(self, event) -> None:
        """Colapsa el sidebar automáticamente en ventanas estrechas (< 960 px)."""
        super().resizeEvent(event)
        self._update_sidebar_mode(event.size().width() < UIScale.px(960))

    def _reiniciar_app(self):
        """Reinicia la aplicación"""
        import sys
        python = sys.executable
        script = sys.argv[0]
        
        # Cerrar la aplicación actual
        QApplication.quit()
        
        # Reiniciar con el mismo script
        os.execl(python, python, script)
    
    def _logout(self):
        """Cerrar sesión y volver al login"""
        from controllers.auth_controller import AuthController
        auth = AuthController()
        auth.logout()
        
        # Cerrar ventana actual y terminar aplicación
        self.close()
        QApplication.instance().quit()
    
    def _change_view(self, index: int):
        """Cambia la vista activa"""
        self.stacked_widget.setCurrentIndex(index)
        
        # Actualizar botones activos
        for i, btn in enumerate(self.nav_buttons):
            btn.setProperty("active", i == index)
            btn.style().unpolish(btn)
            btn.style().polish(btn)
        
        # Actualizar estilos de la vista cuando se accede a ella (lazy loading)
        if index == 0 and hasattr(self, 'home_view') and self.home_view:
            # Home
            self.home_view._actualizar_estilos_tarjetas()
        elif index == 3 and hasattr(self, 'reportes_view') and self.reportes_view:
            # Reportes
            self.reportes_view._actualizar_estilos_contenedores()
        elif index == 4 and hasattr(self, 'configuracion_view') and self.configuracion_view:
            # Configuración
            self.configuracion_view._actualizar_estilos_tema()
        
        # Refrescar datos de vistas relacionadas
            btn.style().polish(btn)
        
        # Refrescar datos en las vistas
        if index == 0:  # Home
            self.home_view.refresh_data()
        elif index == 1:  # Cuotas
            self.clientes_view.refresh_data()
        elif index == 2:  # Clientes
            self.cuotas_view.refresh_data()
    

    
    def toggle_fullscreen(self, enable: bool):
        """Alterna el modo de pantalla completa"""
        if enable:
            self.showFullScreen()
        else:
            # En Linux, usar setWindowState para asegurar la salida correcta de fullscreen
            self.setWindowState(self.windowState() & ~Qt.WindowState.WindowFullScreen)
            self.showNormal()
            QTimer.singleShot(10, lambda: self.setWindowState(Qt.WindowState.WindowNoState))
    
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
    
    def _load_version(self):
        """Carga la versión desde el archivo VERSION"""
        try:
            # Obtener ruta del archivo VERSION
            version_path = get_resource_path('VERSION')
            
            if os.path.exists(version_path):
                with open(version_path, 'r', encoding='utf-8') as f:
                    version = f.read().strip()
                    self.version_label.setText(f"v{version}")
            else:
                self.version_label.setText("v?.?.?")
        except Exception as e:
            print(f"Error al cargar versión: {e}")
            self.version_label.setText("v?.?.?")
    
    def apply_theme(self, theme: str):
        """
        Aplica un tema a toda la aplicación de forma optimizada
        
        Args:
            theme: 'dark' o 'light'
        """
        self.current_theme = theme
        stylesheet = self.theme_controller.get_theme_stylesheet(theme)
        if stylesheet:
            # Aplicar stylesheet global primero (instantáneo)
            self.app.setStyleSheet(stylesheet)
            
            # Actualizar timestamp inmediatamente
            if theme == 'dark':
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
            else:  # light
                self.timestamp_label.setStyleSheet("""
                    QLabel {
                        background: rgba(248, 249, 250, 0.95);
                        color: #64748b;
                        font-size: 12px;
                        font-weight: 500;
                        padding: 8px 20px;
                        border-top: 1px solid rgba(203, 213, 225, 0.4);
                    }
                """)
            
            # Recrear el sidebar para actualizar los estilos responsivos (diferido)
            if hasattr(self, 'sidebar'):
                # Guardar el índice del botón activo actual
                active_index = 0
                for i, btn in enumerate(self.nav_buttons):
                    if btn.property("active"):
                        active_index = i
                        break
                
                # Eliminar el sidebar actual
                old_sidebar = self.sidebar
                layout = self.centralWidget().layout()
                layout.removeWidget(old_sidebar)
                old_sidebar.deleteLater()
                
                # Crear nuevo sidebar con el tema actualizado
                self.sidebar = self._create_sidebar()
                layout.insertWidget(0, self.sidebar)
                
                # Restaurar el botón activo
                if active_index < len(self.nav_buttons):
                    self.nav_buttons[active_index].setProperty("active", True)
            
            # Actualizar vistas solo si están visibles (lazy loading)
            # Home
            if hasattr(self, 'home_view') and self.home_view and self.stacked_widget.currentWidget() == self.home_view:
                self.home_view._actualizar_estilos_tarjetas()
                self.home_view.refresh_data()
            
            # Reportes
            if hasattr(self, 'reportes_view') and self.reportes_view and self.stacked_widget.currentWidget() == self.reportes_view:
                self.reportes_view._actualizar_estilos_contenedores()
                self.reportes_view._actualizar_estadisticas()
            
            # Actualizar estilos de configuración si está visible
            if hasattr(self, 'configuracion_view') and self.configuracion_view:
                self.configuracion_view._actualizar_estilos_tema()
            
            # Actualizar estilos de cuotas si está visible
            if hasattr(self, 'cuotas_view') and self.cuotas_view:
                self.cuotas_view.refresh_data()
    
    def change_theme(self, theme: str):
        """
        Cambia el tema de la aplicación
        
        Args:
            theme: 'dark' o 'light'
        """
        if self.theme_controller.set_theme(theme):
            self.apply_theme(theme)
            return True
        return False
