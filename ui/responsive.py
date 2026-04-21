"""
Sistema de UI Responsive para GesMonth.

Provee tres utilidades principales:

  UIScale  — Factor de escala calculado a partir del DPI lógico de la
             pantalla primaria. Se inicializa UNA vez en main() con
             UIScale.init(app).  Todos los helpers de tamaño lo usan.

  Sp       — Constantes de espaciado en grilla de 8 pt (XS=4, SM=8,
             MD=12, LG=16, XL=24, XXL=32), escaladas automáticamente
             con UIScale.  Úsalas en lugar de números mágicos.

  BaseView — Clase base para vistas principales.  Expone header_layout
             (título + acciones) y content_layout (área expansible).

Helpers de QSizePolicy:
  expanding()       — Expanding / Expanding
  h_expanding()     — Expanding / Preferred
  v_expanding()     — Preferred  / Expanding
  fixed_size()      — Fixed / Fixed

Uso típico
----------
# main.py
UIScale.init(app)

# cualquier vista
from ui.responsive import Sp, UIScale, expanding, BaseView

class MiVista(BaseView):
    def __init__(self):
        super().__init__()
        self.set_title("Mi Vista")
        btn = QPushButton("Acción")
        self.add_header_action(btn)
        table = QTableWidget()
        table.setSizePolicy(expanding())
        self.content_layout.addWidget(table)
"""

from __future__ import annotations

from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QSizePolicy
from PyQt6.QtCore import Qt


# ──────────────────────────────────────────────────────────────────────────────
# UIScale
# ──────────────────────────────────────────────────────────────────────────────

class UIScale:
    """
    Calcula un factor de escala único basado en el DPI lógico de la pantalla.

    Diseñado con 96 DPI como referencia (factor = 1.0).
    En pantallas HiDPI (192 DPI) factor = 2.0, lo que duplica
    los valores mínimos fijos.

    Qt 6 ya escala los píxeles de renderizado automáticamente con
    setHighDpiScaleFactorRoundingPolicy; UIScale se usa para escalar
    valores que no gestiona Qt de forma automática:
      - anchos/altos fijos del sidebar
      - setMinimumSize de la ventana principal
      - márgenes y espaciados calculados en tiempo de ejecución

    Llamar UIScale.init(app) ANTES de crear cualquier widget.
    """

    _factor: float = 1.0

    @classmethod
    def init(cls, app: QApplication) -> None:
        """Inicializa el factor de escala a partir del DPI lógico."""
        screen = app.primaryScreen()
        if screen is None:
            return
        logical_dpi = screen.logicalDotsPerInch()
        # Clampeado: evita escalar demasiado en monitores con DPI mal reportado
        cls._factor = max(0.75, min(logical_dpi / 96.0, 2.5))

    @classmethod
    def factor(cls) -> float:
        """Factor de escala actual (1.0 == 96 DPI)."""
        return cls._factor

    @classmethod
    def px(cls, value: int) -> int:
        """Convierte píxeles lógicos a píxeles físicos escalados."""
        return round(value * cls._factor)

    # ── Valores predefinidos usados en toda la app ─────────────────────────

    @classmethod
    def sidebar_width(cls) -> int:
        """Ancho del sidebar en modo expandido."""
        return cls.px(250)

    @classmethod
    def sidebar_compact_width(cls) -> int:
        """Ancho del sidebar en modo compacto (solo iconos)."""
        return cls.px(64)

    @classmethod
    def initial_window_size(cls) -> tuple[int, int]:
        """
        Tamaño inicial sugerido para la ventana principal.
        Ocupa ~80% del área disponible de la pantalla, sin excederla.
        """
        screen = QApplication.primaryScreen()
        if screen:
            geom = screen.availableGeometry()
            w = max(cls.px(1200), round(geom.width() * 0.80))
            h = max(cls.px(700), round(geom.height() * 0.85))
            return (min(w, geom.width()), min(h, geom.height()))
        return (cls.px(1280), cls.px(760))


# ──────────────────────────────────────────────────────────────────────────────
# Sp — Sistema de espaciado en grilla de 8 pt
# ──────────────────────────────────────────────────────────────────────────────

class Sp:
    """
    Constantes de espaciado en grilla de 8 pt, escaladas con UIScale.

    Valores base (px lógicos):
        XS = 4   SM = 8   MD = 12   LG = 16   XL = 24   XXL = 32

    Ejemplo de uso:
        layout.setSpacing(Sp.lg())
        layout.setContentsMargins(Sp.xl(), Sp.xl(), Sp.xl(), Sp.xl())
    """

    XS: int = 4
    SM: int = 8
    MD: int = 12
    LG: int = 16
    XL: int = 24
    XXL: int = 32

    @classmethod
    def xs(cls) -> int:
        return UIScale.px(cls.XS)

    @classmethod
    def sm(cls) -> int:
        return UIScale.px(cls.SM)

    @classmethod
    def md(cls) -> int:
        return UIScale.px(cls.MD)

    @classmethod
    def lg(cls) -> int:
        return UIScale.px(cls.LG)

    @classmethod
    def xl(cls) -> int:
        return UIScale.px(cls.XL)

    @classmethod
    def xxl(cls) -> int:
        return UIScale.px(cls.XXL)


# ──────────────────────────────────────────────────────────────────────────────
# Helpers de QSizePolicy
# ──────────────────────────────────────────────────────────────────────────────

def expanding() -> QSizePolicy:
    """El widget se expande en ambos ejes (Expanding / Expanding)."""
    return QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)


def h_expanding() -> QSizePolicy:
    """El widget se expande horizontalmente; altura preferida (Expanding / Preferred)."""
    return QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)


def v_expanding() -> QSizePolicy:
    """El widget se expande verticalmente; ancho preferido (Preferred / Expanding)."""
    return QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)


def fixed_size() -> QSizePolicy:
    """El widget mantiene su tamaño sugerido en ambos ejes (Fixed / Fixed)."""
    return QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)


# ──────────────────────────────────────────────────────────────────────────────
# BaseView — Vista base con header + content estructurado
# ──────────────────────────────────────────────────────────────────────────────

class BaseView(QWidget):
    """
    Clase base para todas las vistas principales de GesMonth.

    Estructura:
        ┌──────────────────────────────────────────┐
        │  header_layout  [título]   [acciones →]  │  ← altura mínima
        ├──────────────────────────────────────────┤
        │                                          │
        │  content_layout          (stretch = 1)   │  ← ocupa el resto
        │                                          │
        └──────────────────────────────────────────┘

    Uso básico
    ----------
    class MiVista(BaseView):
        def __init__(self):
            super().__init__()
            self.set_title("Mi Vista")

            btn = QPushButton("Nueva entrada")
            self.add_header_action(btn)

            table = QTableWidget()
            table.setSizePolicy(expanding())
            self.content_layout.addWidget(table)

    Propiedades públicas
    --------------------
    header_layout  : QHBoxLayout — fila superior (título + botones de acción)
    content_layout : QVBoxLayout — área principal, stretch=1
    """

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setSizePolicy(expanding())

        # ── Layout raíz ────────────────────────────────────────────────────
        self._root = QVBoxLayout(self)
        m = Sp.xl()
        self._root.setContentsMargins(m, m, m, m)
        self._root.setSpacing(Sp.lg())

        # ── Fila de cabecera ────────────────────────────────────────────────
        _header_widget = QWidget()
        _header_widget.setSizePolicy(
            QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Maximum)
        )
        self.header_layout = QHBoxLayout(_header_widget)
        self.header_layout.setContentsMargins(UIScale.px(0), UIScale.px(0), UIScale.px(0), UIScale.px(0))
        self.header_layout.setSpacing(Sp.md())
        self._root.addWidget(_header_widget)

        # ── Área de contenido ───────────────────────────────────────────────
        _content_widget = QWidget()
        _content_widget.setSizePolicy(expanding())
        self.content_layout = QVBoxLayout(_content_widget)
        self.content_layout.setContentsMargins(UIScale.px(0), UIScale.px(0), UIScale.px(0), UIScale.px(0))
        self.content_layout.setSpacing(Sp.lg())
        self._root.addWidget(_content_widget, stretch=1)

    # ── API pública ─────────────────────────────────────────────────────────

    def set_title(self, text: str) -> QLabel:
        """
        Agrega el título a la izquierda del header.
        Devuelve el QLabel para personalización adicional.
        """
        lbl = QLabel(text)
        lbl.setObjectName("pageTitle")
        self.header_layout.insertWidget(0, lbl)
        return lbl

    def add_header_action(self, widget: QWidget) -> None:
        """
        Agrega un widget al extremo derecho del header.
        Inserta un stretch antes del widget si no existe ya.
        """
        has_stretch = any(
            self.header_layout.itemAt(i).spacerItem() is not None
            for i in range(self.header_layout.count())
        )
        if not has_stretch:
            self.header_layout.addStretch()
        self.header_layout.addWidget(widget)
