"""
Módulo de interfaces de usuario
"""

from .main_window import MainWindow
from .dashboard_view import DashboardView
from .clientes_view import ClientesView
from .pagos_view import PagosView
from .cuotas_view import CuotasView
from .reportes_view import ReportesView
from .configuracion_view import ConfiguracionView

__all__ = [
    'MainWindow',
    'DashboardView',
    'ClientesView',
    'PagosView',
    'CuotasView',
    'ReportesView',
    'ConfiguracionView'
]
