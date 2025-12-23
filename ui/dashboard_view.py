"""
Vista del Dashboard - Resumen general
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QFrame, QGridLayout)
from PyQt6.QtCore import Qt, QDateTime
from database.models import Pago, Cliente, CuotaMensual
from database.connection import DatabaseConnection


class DashboardView(QWidget):
    """Vista de dashboard con estadísticas generales"""
    
    def __init__(self):
        super().__init__()
        self._init_ui()
    
    def _init_ui(self):
        """Inicializa la interfaz del dashboard"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(30)
        
        # Título
        title = QLabel("Dashboard")
        title.setObjectName("pageTitle")
        layout.addWidget(title)
        
        # Grid de tarjetas principales (2x2)
        stats_grid = QGridLayout()
        stats_grid.setSpacing(20)
        stats_grid.setContentsMargins(0, 0, 0, 0)
        
        # Crear tarjetas principales
        self.card_total_clientes = self._create_stat_card("Total Clientes", "0", "#3b82f6")
        self.card_clientes_mora = self._create_stat_card("Clientes en Mora", "0", "#ef4444")
        self.card_clientes_dia = self._create_stat_card("Clientes al Día", "0", "#22c55e")
        self.card_total_año = self._create_stat_card("Total Año 2025", "$0", "#8b5cf6")
        
        stats_grid.addWidget(self.card_total_clientes, 0, 0)
        stats_grid.addWidget(self.card_clientes_mora, 0, 1)
        stats_grid.addWidget(self.card_clientes_dia, 1, 0)
        stats_grid.addWidget(self.card_total_año, 1, 1)
        
        # Hacer que las columnas tengan el mismo ancho
        stats_grid.setColumnStretch(0, 1)
        stats_grid.setColumnStretch(1, 1)
        
        layout.addLayout(stats_grid)
        
        # Tarjeta grande de total del mes actual
        self.card_total_mes = self._create_month_card()
        layout.addWidget(self.card_total_mes)
        
        # Espacio flexible
        layout.addStretch()
        
        # Información del programa en la parte inferior
        info_layout = self._create_info_footer()
        layout.addLayout(info_layout)
        
        # Cargar datos
        self.refresh_data()
    
    def _create_stat_card(self, title: str, value: str, color: str) -> QFrame:
        """Crea una tarjeta de estadística"""
        card = QFrame()
        card.setStyleSheet(f"""
            QFrame {{
                background: rgba(30, 41, 59, 0.5);
                border: 1px solid rgba(71, 85, 105, 0.5);
                border-radius: 12px;
            }}
            QLabel {{
                border: none;
                background: transparent;
            }}
        """)
        card.setMinimumHeight(130)
        
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(25, 25, 25, 25)
        card_layout.setSpacing(15)
        
        # Título
        title_label = QLabel(title)
        title_label.setStyleSheet("font-size: 14px; color: #94a3b8; font-weight: 500; border: none;")
        card_layout.addWidget(title_label)
        
        # Valor
        value_label = QLabel(value)
        value_label.setStyleSheet(f"font-size: 36px; color: {color}; font-weight: 700; border: none;")
        card_layout.addWidget(value_label)
        
        card_layout.addStretch()
        
        # Guardar referencia al label de valor
        card.value_label = value_label
        
        return card
    
    def _create_month_card(self) -> QFrame:
        """Crea la tarjeta grande del total del mes"""
        card = QFrame()
        card.setStyleSheet("""
            QFrame {
                background: rgba(59, 130, 246, 0.1);
                border: 1px solid rgba(59, 130, 246, 0.3);
                border-radius: 12px;
            }
            QLabel {
                border: none;
                background: transparent;
            }
        """)
        card.setMinimumHeight(100)
        card.setMaximumHeight(120)
        
        card_layout = QHBoxLayout(card)
        card_layout.setContentsMargins(30, 25, 30, 25)
        card_layout.setSpacing(20)
        
        # Columna izquierda: Etiqueta
        label_layout = QVBoxLayout()
        label_layout.setSpacing(5)
        
        month_label = QLabel()
        month_label.setObjectName("monthLabel")
        month_label.setStyleSheet("font-size: 16px; color: #94a3b8; font-weight: 500; border: none;")
        label_layout.addWidget(month_label)
        
        subtitle_label = QLabel("Recaudado en el mes")
        subtitle_label.setStyleSheet("font-size: 12px; color: #64748b; border: none;")
        label_layout.addWidget(subtitle_label)
        
        card_layout.addLayout(label_layout)
        
        card_layout.addStretch()
        
        # Columna derecha: Valor
        value_label = QLabel("$0")
        value_label.setStyleSheet("font-size: 42px; color: #3b82f6; font-weight: 700; border: none;")
        card_layout.addWidget(value_label)
        
        # Guardar referencias
        card.month_label = month_label
        card.value_label = value_label
        
        return card
    
    def _create_info_footer(self) -> QHBoxLayout:
        """Crea el footer con información del programa"""
        footer_layout = QHBoxLayout()
        footer_layout.setContentsMargins(0, 20, 0, 0)
        footer_layout.setSpacing(30)
        
        # Nombre de la aplicación
        app_name = QLabel("GesMonth")
        app_name.setStyleSheet("font-size: 18px; font-weight: 700; color: #94a3b8; border: none;")
        footer_layout.addWidget(app_name)
        
        # Separador
        separator1 = QLabel("•")
        separator1.setStyleSheet("font-size: 14px; color: #475569; border: none;")
        footer_layout.addWidget(separator1)
        
        # Versión
        version = QLabel("v1.0.1")
        version.setStyleSheet("font-size: 14px; color: #64748b; border: none;")
        footer_layout.addWidget(version)
        
        # Separador
        separator2 = QLabel("•")
        separator2.setStyleSheet("font-size: 14px; color: #475569; border: none;")
        footer_layout.addWidget(separator2)
        
        # Descripción
        description = QLabel("Sistema para gestión de cuotas mensuales")
        description.setStyleSheet("font-size: 14px; color: #64748b; border: none;")
        footer_layout.addWidget(description)
        
        footer_layout.addStretch()
        
        return footer_layout
    
    def refresh_data(self):
        """Actualiza las estadísticas del dashboard"""
        # Obtener fecha actual
        now = QDateTime.currentDateTime()
        año_actual = now.date().year()
        mes_actual = now.date().month()
        
        # Nombres de meses
        meses = ["", "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
                 "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
        
        # Total de clientes activos
        clientes = Cliente.obtener_todos()
        total_clientes = len([c for c in clientes if c.estado == 'activo'])
        
        # Clientes en mora (último registro en impago)
        clientes_mora = 0
        clientes_dia = 0
        
        for cliente in clientes:
            if cliente.estado == 'activo':
                # Obtener última cuota registrada del cliente
                cuotas = CuotaMensual.obtener_por_cliente(cliente.id)
                if cuotas:
                    ultima_cuota = cuotas[0]  # Ya viene ordenado descendente
                    if ultima_cuota.estado == 'impago':
                        clientes_mora += 1
                    elif ultima_cuota.estado in ['pagado', 'con_deuda']:
                        clientes_dia += 1
                else:
                    # Sin cuotas registradas, se considera al día
                    clientes_dia += 1
        
        # Total recaudado en el mes actual
        db = DatabaseConnection()
        conn = db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT COALESCE(SUM(monto), 0) as total
            FROM pagos
            WHERE mes_correspondiente = ?
        ''', (f"{año_actual}-{mes_actual:02d}",))
        
        total_mes = cursor.fetchone()['total']
        
        # Total recaudado en el año actual
        cursor.execute('''
            SELECT COALESCE(SUM(monto), 0) as total
            FROM pagos
            WHERE mes_correspondiente LIKE ?
        ''', (f"{año_actual}%",))
        
        total_año = cursor.fetchone()['total']
        
        # Actualizar tarjetas
        self.card_total_clientes.value_label.setText(str(total_clientes))
        self.card_clientes_mora.value_label.setText(str(clientes_mora))
        self.card_clientes_dia.value_label.setText(str(clientes_dia))
        self.card_total_año.value_label.setText(f"${total_año:,.0f}")
        
        # Actualizar tarjeta del mes
        self.card_total_mes.month_label.setText(f"{meses[mes_actual]} {año_actual}")
        self.card_total_mes.value_label.setText(f"${total_mes:,.0f}")
