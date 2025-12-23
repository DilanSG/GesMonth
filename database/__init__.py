"""
Módulo de base de datos
Gestiona la conexión y operaciones con SQLite
"""

from .connection import DatabaseConnection
from .models import Cliente, Pago, MetodoPago, CuotaMensual

__all__ = ['DatabaseConnection', 'Cliente', 'Pago', 'MetodoPago', 'CuotaMensual']
