"""
Splash Screen animado con logo
"""
from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QGraphicsBlurEffect
from PyQt6.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve, QParallelAnimationGroup, pyqtProperty, QRectF, QPointF
from PyQt6.QtGui import QPainter, QPixmap, QPainterPath, QLinearGradient, QRadialGradient, QColor, QTransform
import os
import sys
import math
import random
from utils import get_resource_path
from .responsive import UIScale


class SplashScreen(QWidget):
    """Pantalla de splash con animación del logo"""
    
    def __init__(self, tema='light', fullscreen=False):
        super().__init__()
        self.tema = tema
        self.fullscreen = fullscreen
        self._logo_scale = 0.66  # Escala inicial (1/3 más pequeño)
        self._title_scale = 0.66
        self._anim_time = 0  # Tiempo de animación para el fondo
        self._init_lava_bubbles()  # Inicializar burbujas de lava
        self._init_ui()
        self._start_animation()
    
    def _init_lava_bubbles(self):
        """Inicializa las burbujas tipo lámpara de lava"""
        self.bubbles = []
        # Crear 20-30 burbujas con posiciones y velocidades aleatorias
        num_bubbles = random.randint(20, 30)
        for _ in range(num_bubbles):
            bubble = {
                'x': random.uniform(0.0, 1.0),  # Posición X (0-1) - cubrir toda la pantalla
                'y': random.uniform(0.0, 1.0),  # Posición Y (0-1) - cubrir toda la pantalla
                'radius': random.uniform(110, 180),  # Radio de la burbuja (más uniforme)
                'speed_x': random.uniform(-0.5, 0.5),  # Velocidad horizontal (aumentada)
                'speed_y': random.uniform(-0.4, 0.4),  # Velocidad vertical (aumentada)
                'phase': random.uniform(0, 2 * math.pi)  # Fase de oscilación
            }
            self.bubbles.append(bubble)
    
    # Propiedades para animar la escala
    @pyqtProperty(float)
    def logo_scale(self):
        return self._logo_scale
    
    @logo_scale.setter
    def logo_scale(self, value):
        self._logo_scale = value
        self._update_logo_transform()
    
    @pyqtProperty(float)
    def title_scale(self):
        return self._title_scale
    
    @title_scale.setter
    def title_scale(self, value):
        self._title_scale = value
        self._update_title_transform()
    
    def _update_logo_transform(self):
        """Actualiza el logo segun la escala animada"""
        # Solo aplicar si tenemos un pixmap base
        if hasattr(self, "_base_logo_pixmap"):
            base = self._base_logo_pixmap
            size = base.size()
            new_w = max(1, int(size.width() * self._logo_scale))
            new_h = max(1, int(size.height() * self._logo_scale))
            scaled = base.scaled(
                new_w,
                new_h,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )
            self.logo_label.setPixmap(scaled)
    
    def _update_title_transform(self):
        """Actualiza el estilo del título segun la escala animada"""
        # Usar tamaño base responsivo si existe, sino usar valor por defecto
        base_font_size = getattr(self, 'base_font_size', 64)
        font_size = max(1, int(base_font_size * self._title_scale))

        if self.tema == 'dark':
            title_style = f"""
                font-size: {font_size}px;
                font-weight: bold;
                color: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #60a5fa,
                    stop:0.5 #3b82f6,
                    stop:1 #2563eb);
                letter-spacing: 8px;
            """
        else:
            title_style = f"""
                font-size: {font_size}px;
                font-weight: bold;
                color: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #3b82f6,
                    stop:0.5 #2563eb,
                    stop:1 #1d4ed8);
                letter-spacing: 8px;
            """

        self.title_label.setStyleSheet(title_style)
        
    def _init_ui(self):
        """Inicializa la interfaz"""
        # Configurar ventana para que esté por encima de todo
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint | 
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.SplashScreen
        )
        
        # Obtener tamaño de la pantalla
        screen = self.screen()
        
        if self.fullscreen:
            # Modo pantalla completa: cubrir toda la pantalla
            screen_geometry = screen.geometry()
            width = screen_geometry.width()
            height = screen_geometry.height()
            x = screen_geometry.x()
            y = screen_geometry.y()
        else:
            # Modo ventana: mismo tamaño que la ventana principal (1200x700) y centrado
            screen_geometry = screen.availableGeometry()
            width = 1200
            height = 700
            # Centrar en la pantalla
            x = screen_geometry.x() + (screen_geometry.width() - width) // 2
            y = screen_geometry.y() + (screen_geometry.height() - height) // 2
        
        self.setGeometry(x, y, width, height)
        self.setFixedSize(width, height)
        
        # Calcular tamaños responsivos basados en el tamaño de la ventana
        self.logo_size = min(width, height) // 4  # Logo 25% del lado más pequeño
        self.base_font_size = min(width, height) // 15  # Título proporcional
        
        # Layout principal
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Logo
        self.logo_label = QLabel()
        self.logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Cargar imagen del logo
        logo_path = get_resource_path(os.path.join('assets', 'icons', 'LOGO.png'))
        
        if os.path.exists(logo_path):
            pixmap = QPixmap(logo_path)
            # Guardar pixmap base con tamaño responsivo
            self._base_logo_pixmap = pixmap.scaled(
                self.logo_size,
                self.logo_size,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )
            # Aplicar escala inicial (~1/3 mas pequeño)
            self._update_logo_transform()
        else:
            # Fallback al texto si no hay logo
            self.logo_label.setText("LOGO")
            fallback_size = self.logo_size // 2
            self.logo_label.setStyleSheet(f"font-size: {fallback_size}px;")
        
        layout.addWidget(self.logo_label, alignment=Qt.AlignmentFlag.AlignHCenter)
        
        # Espaciado proporcional entre logo y título
        spacing = height // 15
        layout.addSpacing(spacing)
        
        # Título principal
        self.title_label = QLabel("GesMonth")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Estilo del título según tema y escala inicial
        self._update_title_transform()
        layout.addWidget(self.title_label)
        
    def paintEvent(self, event):
        """Dibuja el fondo con efecto tipo lámpara de lava"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        rect = self.rect()
        w = rect.width()
        h = rect.height()

        # Fondo base degradado según tema
        if self.tema == 'dark':
            bg_gradient = QLinearGradient(0, 0, 0, h)
            bg_gradient.setColorAt(0.0, QColor(15, 23, 42))  # #0f172a
            bg_gradient.setColorAt(1.0, QColor(30, 41, 59))  # #1e293b
        else:
            bg_gradient = QLinearGradient(0, 0, 0, h)
            bg_gradient.setColorAt(0.0, QColor(239, 246, 255))  # #eff6ff
            bg_gradient.setColorAt(1.0, QColor(219, 234, 254))  # #dbeafe

        painter.fillRect(rect, bg_gradient)

        # Actualizar y dibujar burbujas tipo lava lamp
        for bubble in self.bubbles:
            # Actualizar posición con movimiento suave
            bubble['x'] += bubble['speed_x'] * 0.001
            bubble['y'] += bubble['speed_y'] * 0.001
            
            # Agregar oscilación sinusoidal
            oscillation_x = math.sin(self._anim_time * 0.002 + bubble['phase']) * 0.0005
            oscillation_y = math.cos(self._anim_time * 0.0015 + bubble['phase']) * 0.0005
            bubble['x'] += oscillation_x
            bubble['y'] += oscillation_y
            
            # Rebotar en los bordes
            if bubble['x'] < 0 or bubble['x'] > 1:
                bubble['speed_x'] *= -1
                bubble['x'] = max(0, min(1, bubble['x']))
            if bubble['y'] < 0 or bubble['y'] > 1:
                bubble['speed_y'] *= -1
                bubble['y'] = max(0, min(1, bubble['y']))
            
            # Calcular posición en píxeles
            pos_x = bubble['x'] * w
            pos_y = bubble['y'] * h
            
            # Crear gradiente radial para la burbuja
            gradient = QRadialGradient(QPointF(pos_x, pos_y), bubble['radius'])
            
            if self.tema == 'dark':
                # Colores azules oscuros con transparencia
                gradient.setColorAt(0.0, QColor(59, 130, 246, 60))   # #3b82f6
                gradient.setColorAt(0.5, QColor(37, 99, 235, 30))    # #2563eb
                gradient.setColorAt(1.0, QColor(29, 78, 216, 0))     # #1d4ed8
            else:
                # Colores azules claros con transparencia
                gradient.setColorAt(0.0, QColor(147, 197, 253, 80))  # #93c5fd
                gradient.setColorAt(0.5, QColor(96, 165, 250, 40))   # #60a5fa
                gradient.setColorAt(1.0, QColor(59, 130, 246, 0))    # #3b82f6
            
            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(gradient)
            painter.drawEllipse(QPointF(pos_x, pos_y), bubble['radius'], bubble['radius'])
        
        # Incrementar tiempo de animación
        self._anim_time += 1

    def _start_animation(self):
        """Configura e inicia una animacion con escala (1/3 -> 1) y blur (20 -> 0)"""
        duration = 4000  # Duración de la animación en ms (4 segundos para cubrir todo el splash)

        # Efectos de blur iniciales (20px), aplicados al logo y al título
        self.logo_blur = QGraphicsBlurEffect(self)
        self.logo_blur.setBlurRadius(20.0)
        self.logo_label.setGraphicsEffect(self.logo_blur)

        self.title_blur = QGraphicsBlurEffect(self)
        self.title_blur.setBlurRadius(20.0)
        self.title_label.setGraphicsEffect(self.title_blur)

        # Asegurar escala inicial (aprox. 1/3)
        self._logo_scale = 0.66
        self._title_scale = 0.66
        self._update_logo_transform()
        self._update_title_transform()

        # Animacion de escala del logo (0.66 -> 1.0)
        self.logo_scale_anim = QPropertyAnimation(self, b"logo_scale", self)
        self.logo_scale_anim.setDuration(duration)
        self.logo_scale_anim.setStartValue(0.66)
        self.logo_scale_anim.setEndValue(1.0)
        self.logo_scale_anim.setEasingCurve(QEasingCurve.Type.OutCubic)

        # Animacion de escala del titulo (0.66 -> 1.0)
        self.title_scale_anim = QPropertyAnimation(self, b"title_scale", self)
        self.title_scale_anim.setDuration(duration)
        self.title_scale_anim.setStartValue(0.66)
        self.title_scale_anim.setEndValue(1.0)
        self.title_scale_anim.setEasingCurve(QEasingCurve.Type.OutCubic)

        # Animacion de blur del logo (20 -> 0)
        self.logo_blur_anim = QPropertyAnimation(self.logo_blur, b"blurRadius", self)
        self.logo_blur_anim.setDuration(duration)
        self.logo_blur_anim.setStartValue(20.0)
        self.logo_blur_anim.setEndValue(0.0)
        self.logo_blur_anim.setEasingCurve(QEasingCurve.Type.OutCubic)

        # Animacion de blur del titulo (20 -> 0)
        self.title_blur_anim = QPropertyAnimation(self.title_blur, b"blurRadius", self)
        self.title_blur_anim.setDuration(duration)
        self.title_blur_anim.setStartValue(20.0)
        self.title_blur_anim.setEndValue(0.0)
        self.title_blur_anim.setEasingCurve(QEasingCurve.Type.OutCubic)

        # Grupo de animaciones en paralelo para que todo se sienta sincronizado
        self.animation_group = QParallelAnimationGroup(self)
        self.animation_group.addAnimation(self.logo_scale_anim)
        self.animation_group.addAnimation(self.title_scale_anim)
        self.animation_group.addAnimation(self.logo_blur_anim)
        self.animation_group.addAnimation(self.title_blur_anim)
        self.animation_group.start()

        # Timer para refrescar el fondo animado (lámpara de lava)
        self.glow_timer = QTimer(self)
        self.glow_timer.timeout.connect(self.update)
        self.glow_timer.start(30)  # 30ms para animación más fluida

    def finish(self):
        """Cierra la pantalla de splash con fade out"""
        # Evitar múltiples llamadas
        if hasattr(self, '_finishing') and self._finishing:
            return
        
        self._finishing = True
        
        # Detener timer del fondo
        if hasattr(self, "glow_timer") and self.glow_timer.isActive():
            self.glow_timer.stop()
        
        # Detener animaciones en curso
        if hasattr(self, "animation_group") and self.animation_group.state() == QParallelAnimationGroup.State.Running:
            self.animation_group.stop()

        # Animación de fade out
        self.fade_out = QPropertyAnimation(self, b"windowOpacity")
        self.fade_out.setDuration(400)
        self.fade_out.setStartValue(1.0)
        self.fade_out.setEndValue(0.0)
        self.fade_out.setEasingCurve(QEasingCurve.Type.InOutQuad)
        # NO cerrar automáticamente, dejar que main.py lo maneje
        self.fade_out.start()
