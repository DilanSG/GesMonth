"""
Vista de control de cuotas mensuales - Todos los clientes
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QPushButton, QComboBox, QMessageBox, QDialog,
                             QFormLayout, QLineEdit, QGridLayout, QScrollArea, QFrame,
                             QCheckBox, QDoubleSpinBox)
from PyQt6.QtCore import Qt, QSize, QDateTime
from PyQt6.QtGui import QIcon, QFont
from database.models import Cliente, CuotaMensual, MetodoPago, Pago
from controllers.config_controller import ConfigController
from ui.detalles_cuota_dialog import DetallesCuotaDialog


class CuotasView(QWidget):
    """Vista para control de cuotas mensuales - Muestra todos los clientes"""
    
    def __init__(self):
        super().__init__()
        self.config_controller = ConfigController()
        self.clientes_filtrados = []
        self._init_ui()
    
    def _init_ui(self):
        """Inicializa la interfaz"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)
        
        # Header: Título y barra de búsqueda
        header_layout = QVBoxLayout()
        header_layout.setSpacing(15)
        
        # Título
        title = QLabel("Control de Cuotas Mensuales")
        title.setObjectName("pageTitle")
        title.setStyleSheet("border: none;")
        header_layout.addWidget(title)
        
        # Barra de búsqueda
        search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("🔍 Buscar cliente por nombre o documento...")
        self.search_input.setMinimumHeight(45)
        self.search_input.textChanged.connect(self._filtrar_clientes)
        search_layout.addWidget(self.search_input)
        
        header_layout.addLayout(search_layout)
        layout.addLayout(header_layout)
        
        # Área de scroll para las tarjetas de clientes
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; background: transparent; }")
        
        self.clientes_container = QWidget()
        self.clientes_container.setStyleSheet("QWidget { background: transparent; }")
        self.clientes_layout = QVBoxLayout(self.clientes_container)
        self.clientes_layout.setSpacing(20)
        self.clientes_layout.setContentsMargins(0, 0, 0, 0)
        
        scroll.setWidget(self.clientes_container)
        layout.addWidget(scroll)
        
        # Cargar clientes
        self.refresh_data()
    
    def refresh_data(self):
        """Recarga todos los clientes"""
        clientes = Cliente.obtener_todos()
        self.clientes_filtrados = [c for c in clientes if c.estado == 'activo']
        self._mostrar_clientes()
    
    def _filtrar_clientes(self, texto):
        """Filtra clientes por texto de búsqueda"""
        texto = texto.lower().strip()
        clientes = Cliente.obtener_todos()
        
        if texto:
            self.clientes_filtrados = [
                c for c in clientes 
                if c.estado == 'activo' and (
                    texto in c.nombre.lower() or 
                    texto in c.documento.lower()
                )
            ]
        else:
            self.clientes_filtrados = [c for c in clientes if c.estado == 'activo']
        
        self._mostrar_clientes()
    
    def _obtener_años_configurados(self) -> list:
        """Obtiene los años configurados desde la base de datos"""
        return self.config_controller.get_billing_years()
    
    def _mostrar_clientes(self):
        """Muestra todas las tarjetas de clientes"""
        # Limpiar layout anterior
        while self.clientes_layout.count():
            child = self.clientes_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        
        if not self.clientes_filtrados:
            # Mensaje cuando no hay clientes
            no_data = QLabel("No hay clientes activos")
            no_data.setAlignment(Qt.AlignmentFlag.AlignCenter)
            no_data.setStyleSheet("font-size: 16px; color: #94a3b8; padding: 40px;")
            self.clientes_layout.addWidget(no_data)
            self.clientes_layout.addStretch()
            return
        
        # Crear tarjeta para cada cliente
        for cliente in self.clientes_filtrados:
            tarjeta = self._crear_tarjeta_cliente(cliente)
            self.clientes_layout.addWidget(tarjeta)
        
        self.clientes_layout.addStretch()
    
    def _crear_tarjeta_cliente(self, cliente: Cliente) -> QFrame:
        """Crea una tarjeta con la información y grid de cuotas del cliente"""
        tarjeta = QFrame()
        tarjeta.setObjectName("clientCard")
        tarjeta.setStyleSheet("""
            #clientCard {
                background: rgba(30, 41, 59, 0.5);
                border: 1px solid rgba(71, 85, 105, 0.5);
                border-radius: 12px;
                padding: 20px;
            }
            QLabel {
                border: none;
                background: transparent;
            }
        """)
        
        layout = QVBoxLayout(tarjeta)
        layout.setSpacing(15)
        
        # Header con info del cliente
        header = QHBoxLayout()
        
        # Nombre y documento
        info_layout = QVBoxLayout()
        nombre = QLabel(cliente.nombre)
        nombre.setStyleSheet("font-size: 20px; font-weight: 700; color: #e0e7ff; border: none;")
        info_layout.addWidget(nombre)
        
        documento = QLabel(cliente.documento)
        documento.setStyleSheet("font-size: 14px; color: #94a3b8; border: none;")
        info_layout.addWidget(documento)
        
        header.addLayout(info_layout)
        header.addStretch()
        
        # Valor de cuota
        cuota_label = QLabel(f"${cliente.valor_cuota:,.2f}/mes")
        cuota_label.setStyleSheet("""
            font-size: 22px;
            font-weight: 700;
            color: #3b82f6;
            background: rgba(59, 130, 246, 0.1);
            padding: 10px 20px;
            border-radius: 10px;
            border: 1px solid rgba(59, 130, 246, 0.3);
        """)
        header.addWidget(cuota_label)
        
        layout.addLayout(header)
        
        # Grids de años configurados
        años_layout = QVBoxLayout()
        años_layout.setSpacing(20)
        
        años_configurados = self._obtener_años_configurados()
        for año in años_configurados:
            año_widget = self._crear_grid_año(cliente, año)
            años_layout.addWidget(año_widget)
        
        layout.addLayout(años_layout)
        
        return tarjeta
    
    def _crear_grid_año(self, cliente: Cliente, año: int) -> QWidget:
        """Crea el grid de cuotas para un año"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(12)
        
        # Header del año
        header = QLabel(f"{año}")
        header.setStyleSheet("""
            font-size: 16px;
            font-weight: 600;
            color: #94a3b8;
            padding: 8px 12px;
            background: rgba(59, 130, 246, 0.1);
            border: 1px solid rgba(59, 130, 246, 0.2);
            border-radius: 8px;
        """)
        layout.addWidget(header)
        
        # Grid de meses
        grid = QGridLayout()
        grid.setSpacing(8)
        
        meses = [
            "Enero", "Febrero", "Marzo", "Abril",
            "Mayo", "Junio", "Julio", "Agosto",
            "Septiembre", "Octubre", "Noviembre", "Diciembre"
        ]
        
        for idx, nombre_mes in enumerate(meses):
            mes_widget = self._crear_celda_mes(cliente, año, idx + 1, nombre_mes)
            row = idx // 6
            col = idx % 6
            grid.addWidget(mes_widget, row, col)
        
        layout.addLayout(grid)
        
        return widget
    
    def _crear_celda_mes(self, cliente: Cliente, año: int, mes: int, nombre_mes: str) -> QFrame:
        """Crea una celda para un mes"""
        frame = QFrame()
        frame.setMinimumSize(140, 110)
        frame.setMaximumSize(180, 130)
        frame.setCursor(Qt.CursorShape.PointingHandCursor)
        
        # Obtener fecha actual del sistema
        hoy = QDateTime.currentDateTime()
        mes_actual = hoy.date().month()
        año_actual = hoy.date().year()
        es_mes_actual = (año == año_actual and mes == mes_actual)
        
        # Obtener estado de la cuota
        cuota = CuotaMensual.obtener_cuota(cliente.id, año, mes)
        
        # Verificar si el mes anterior tiene deuda (impago o con_deuda)
        mes_anterior = mes - 1 if mes > 1 else 12
        año_anterior = año if mes > 1 else año - 1
        cuota_anterior = CuotaMensual.obtener_cuota(cliente.id, año_anterior, mes_anterior)
        
        # Calcular deuda acumulada del mes anterior
        deuda_mes_anterior = 0
        fecha_inicio_mora_heredada = None
        
        if cuota_anterior:
            if cuota_anterior.estado == 'impago':
                # El mes anterior está impago, heredar su deuda
                deuda_mes_anterior = cuota_anterior.monto + (cuota_anterior.deuda_acumulada or 0)
                fecha_inicio_mora_heredada = cuota_anterior.fecha_inicio_mora
            elif cuota_anterior.estado == 'con_deuda':
                # El mes anterior tiene deuda, heredarla
                deuda_mes_anterior = cuota_anterior.deuda_acumulada or 0
                fecha_inicio_mora_heredada = cuota_anterior.fecha_inicio_mora
        
        # Determinar colores y contenido
        if cuota:
            if cuota.estado == 'pagado':
                color_fondo = "rgba(34, 197, 94, 0.25)"
                border_color = "rgba(34, 197, 94, 0.5)"
                color_texto = "#86efac"
                
                # Extraer hora de registro (formato: YYYY-MM-DD HH:MM:SS)
                try:
                    hora_registro = cuota.fecha_registro.split(' ')[1][:5] if cuota.fecha_registro else "N/A"
                except:
                    hora_registro = "N/A"
                
                # Calcular si se pagó deuda acumulada (verificar mes anterior)
                mes_ant = mes - 1 if mes > 1 else 12
                año_ant = año if mes > 1 else año - 1
                cuota_ant = CuotaMensual.obtener_cuota(cliente.id, año_ant, mes_ant)
                
                monto_mostrar = cuota.monto  # Por defecto, solo la cuota
                
                if cuota_ant:
                    # Verificar si había deuda previa
                    if cuota_ant.estado == 'impago':
                        deuda_previa = cuota_ant.monto + (cuota_ant.deuda_acumulada or 0)
                        monto_mostrar = cuota.monto + deuda_previa
                    elif cuota_ant.estado == 'con_deuda' and not cuota_ant.metodo_pago:
                        # Deuda heredada sin pagar
                        deuda_previa = cuota_ant.deuda_acumulada or 0
                        monto_mostrar = cuota.monto + deuda_previa
                
                linea1 = f"{cuota.metodo_pago or 'N/A'}"
                linea2 = f"{hora_registro}"
                linea3 = f"${monto_mostrar:,.0f}"
                font_size_1 = "11px"
                font_size_2 = "10px"
                font_size_3 = "13px"
                
            elif cuota.estado == 'con_deuda':
                # Verificar si se hizo un pago parcial (tiene método de pago) o es solo deuda heredada
                if cuota.metodo_pago:
                    # PAGO PARCIAL REALIZADO - Verde claro
                    color_fondo = "rgba(16, 185, 129, 0.25)"  # Verde esmeralda más claro
                    border_color = "rgba(16, 185, 129, 0.5)"
                    color_texto = "#6ee7b7"
                    
                    # Calcular deuda que había antes del pago
                    # La deuda_acumulada es lo que queda después del pago parcial
                    # Necesito calcular cuánto había antes del pago
                    
                    # Obtener deuda del mes anterior
                    mes_ant = mes - 1 if mes > 1 else 12
                    año_ant = año if mes > 1 else año - 1
                    cuota_ant = CuotaMensual.obtener_cuota(cliente.id, año_ant, mes_ant)
                    
                    deuda_previa = 0
                    if cuota_ant:
                        if cuota_ant.estado == 'impago':
                            deuda_previa = cuota_ant.monto + (cuota_ant.deuda_acumulada or 0)
                        elif cuota_ant.estado == 'con_deuda':
                            deuda_previa = cuota_ant.deuda_acumulada or 0
                    
                    # Deuda total antes del pago = cuota del mes + deuda previa
                    deuda_total_antes = cuota.monto + deuda_previa
                    deuda_restante = cuota.deuda_acumulada or 0
                    monto_pagado = deuda_total_antes - deuda_restante
                    
                    linea1 = f"Pago Parcial"
                    linea2 = f"Pagó: ${monto_pagado:,.0f} | Resta: ${deuda_restante:,.0f}"
                    # Mostrar método de pago y fecha de mora si existe
                    if cuota.fecha_inicio_mora:
                        linea3 = f"{cuota.metodo_pago} | Mora: {cuota.fecha_inicio_mora[:10]}"
                    else:
                        linea3 = f"{cuota.metodo_pago}"
                    font_size_1 = "11px"
                    font_size_2 = "9px"
                    font_size_3 = "8px"
                else:
                    # DEUDA HEREDADA SIN PAGAR - Amarillo
                    color_fondo = "rgba(234, 179, 8, 0.25)"
                    border_color = "rgba(234, 179, 8, 0.5)"
                    color_texto = "#fcd34d"
                    
                    deuda_total = cuota.monto + (cuota.deuda_acumulada or 0)
                    linea1 = f"Deuda Acumulada"
                    linea2 = f"Desde: {cuota.fecha_inicio_mora[:10] if cuota.fecha_inicio_mora else 'N/A'}"
                    linea3 = f"${deuda_total:,.0f}"
                    font_size_1 = "10px"
                    font_size_2 = "9px"
                    font_size_3 = "14px"
                
            else:  # impago
                color_fondo = "rgba(239, 68, 68, 0.25)"
                border_color = "rgba(239, 68, 68, 0.5)"
                color_texto = "#fca5a5"
                
                # Usar fecha_inicio_mora si existe, si no calcular con día de cobro
                if cuota.fecha_inicio_mora:
                    fecha_mora = cuota.fecha_inicio_mora[:10]
                else:
                    fecha_mora = f"{año}-{mes:02d}-{cliente.dia_cobro:02d}"
                
                linea1 = f"Mora desde"
                linea2 = fecha_mora
                linea3 = f"-${abs(cuota.monto):,.0f}"
                font_size_1 = "10px"
                font_size_2 = "10px"
                font_size_3 = "14px"
                
        elif deuda_mes_anterior > 0:
            # Mes sin registro pero con deuda del mes anterior - AMARILLO
            color_fondo = "rgba(234, 179, 8, 0.25)"
            border_color = "rgba(234, 179, 8, 0.5)"
            color_texto = "#fcd34d"
            
            deuda_total = cliente.valor_cuota + deuda_mes_anterior
            linea1 = f"Deuda Pendiente"
            linea2 = f"Desde: {fecha_inicio_mora_heredada[:10] if fecha_inicio_mora_heredada else 'N/A'}"
            linea3 = f"${deuda_total:,.0f}"
            font_size_1 = "10px"
            font_size_2 = "9px"
            font_size_3 = "14px"
            
        elif es_mes_actual:
            # Mes actual sin registro - destacado
            color_fondo = "rgba(255, 255, 255, 0.15)"
            border_color = "rgba(96, 165, 250, 0.7)"
            color_texto = "#ffffff"
            linea1 = "Mes Actual"
            linea2 = f"Vence: {cliente.dia_cobro:02d}"
            linea3 = f"${cliente.valor_cuota:,.0f}"
            font_size_1 = "11px"
            font_size_2 = "10px"
            font_size_3 = "14px"
        else:
            # Pendiente
            color_fondo = "rgba(71, 85, 105, 0.3)"
            border_color = "rgba(148, 163, 184, 0.3)"
            color_texto = "#94a3b8"
            linea1 = f"{año}-{mes:02d}-{cliente.dia_cobro:02d}"
            linea2 = ""
            linea3 = f"${cliente.valor_cuota:,.0f}"
            font_size_1 = "10px"
            font_size_2 = "10px"
            font_size_3 = "14px"
        
        frame.setStyleSheet(f"""
            QFrame {{
                background: {color_fondo};
                border: {'2px' if es_mes_actual else '1px'} solid {border_color};
                border-radius: 10px;
            }}
            QFrame:hover {{
                background: {color_fondo.replace('0.25', '0.35').replace('0.3', '0.4').replace('0.15', '0.25')};
                border: 2px solid {border_color};
            }}
        """)
        
        layout = QVBoxLayout(frame)
        layout.setContentsMargins(8, 6, 8, 6)
        layout.setSpacing(2)
        
        # Nombre del mes
        label_mes = QLabel(nombre_mes[:3].upper())
        label_mes.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label_mes.setStyleSheet(f"""
            font-size: 12px;
            font-weight: {'700' if es_mes_actual else '600'};
            color: {color_texto};
            letter-spacing: 1px;
        """)
        layout.addWidget(label_mes)
        
        # Línea 1
        label_linea1 = QLabel(linea1)
        label_linea1.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label_linea1.setStyleSheet(f"""
            font-size: {font_size_1};
            color: {color_texto};
            font-weight: 600;
        """)
        label_linea1.setWordWrap(True)
        layout.addWidget(label_linea1)
        
        # Línea 2 (si existe)
        if linea2:
            label_linea2 = QLabel(linea2)
            label_linea2.setAlignment(Qt.AlignmentFlag.AlignCenter)
            label_linea2.setStyleSheet(f"""
                font-size: {font_size_2};
                color: {color_texto};
                font-weight: 500;
            """)
            layout.addWidget(label_linea2)
        
        # Línea 3 (monto)
        label_linea3 = QLabel(linea3)
        label_linea3.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label_linea3.setStyleSheet(f"""
            font-size: {font_size_3};
            color: {color_texto};
            font-weight: 700;
        """)
        layout.addWidget(label_linea3)
        
        # Conectar click
        frame.mousePressEvent = lambda event: self._on_celda_click(cliente, año, mes, cuota)
        
        return frame
    
    def _on_celda_click(self, cliente: Cliente, año: int, mes: int, cuota):
        """Maneja el click en una celda de mes"""
        if cuota:
            # Si ya tiene cuota, mostrar diálogo detallado
            dialog = DetallesCuotaDialog(self, cliente, año, mes, cuota)
            if dialog.exec() == QDialog.DialogCode.Accepted:
                self._mostrar_clientes()
        else:
            # Mostrar diálogo para registrar pago o impago
            dialog = RegistroCuotaDialog(self, cliente, año, mes)
            if dialog.exec() == QDialog.DialogCode.Accepted:
                self._mostrar_clientes()


class RegistroCuotaDialog(QDialog):
    """Diálogo para registrar pago o impago de cuota"""
    
    def __init__(self, parent, cliente: Cliente, año: int, mes: int):
        super().__init__(parent)
        self.cliente = cliente
        self.año = año
        self.mes = mes
        
        # Detectar si es mes futuro
        hoy = QDateTime.currentDateTime()
        self.es_mes_futuro = (año > hoy.date().year()) or (año == hoy.date().year() and mes > hoy.date().month())
        
        self.setWindowTitle(f"Registrar Cuota - {cliente.nombre}")
        self.setMinimumWidth(400)
        self._init_ui()
    
    def _init_ui(self):
        """Inicializa la interfaz del diálogo"""
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)
        
        # Título con nombre del cliente
        titulo = QLabel(self.cliente.nombre)
        titulo.setStyleSheet("font-size: 20px; color: #cbd5e1; font-weight: 700;")
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(titulo)
        
        # Información del mes
        meses = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
                 "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
        
        mes_label = QLabel(f"{meses[self.mes - 1]} {self.año}")
        mes_label.setStyleSheet("font-size: 16px; color: #94a3b8; font-weight: 500;")
        mes_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(mes_label)
        
        layout.addSpacing(10)
        
        # Calcular deuda acumulada si existe
        cuota_actual = CuotaMensual.obtener_cuota(self.cliente.id, self.año, self.mes)
        
        # Si no hay cuota registrada, verificar deuda del mes anterior
        if not cuota_actual:
            mes_anterior = self.mes - 1 if self.mes > 1 else 12
            año_anterior = self.año if self.mes > 1 else self.año - 1
            cuota_anterior = CuotaMensual.obtener_cuota(self.cliente.id, año_anterior, mes_anterior)
            
            deuda_acumulada = 0
            if cuota_anterior:
                if cuota_anterior.estado == 'impago':
                    deuda_acumulada = cuota_anterior.monto + (cuota_anterior.deuda_acumulada or 0)
                elif cuota_anterior.estado == 'con_deuda':
                    deuda_acumulada = cuota_anterior.deuda_acumulada or 0
        else:
            deuda_acumulada = cuota_actual.deuda_acumulada if cuota_actual.deuda_acumulada else 0
        
        deuda_total = self.cliente.valor_cuota + deuda_acumulada
        
        # Mostrar información de forma limpia
        self._agregar_linea_info(layout, "Cuota del mes:", f"${self.cliente.valor_cuota:,.0f}")
        if deuda_acumulada > 0:
            self._agregar_linea_info(layout, "Deuda previa:", f"${deuda_acumulada:,.0f}")
            self._agregar_linea_info(layout, "Total a pagar:", f"${deuda_total:,.0f}", True)
        
        layout.addSpacing(10)
        
        # Opción de pago parcial - SIEMPRE mostrar para permitir pagos parciales
        parcial_container = QFrame()
        parcial_layout = QHBoxLayout(parcial_container)
        parcial_layout.setContentsMargins(0, 0, 0, 0)
        
        self.check_pago_parcial = QCheckBox("Pago Parcial")
        self.check_pago_parcial.setStyleSheet("font-size: 13px; color: #cbd5e1;")
        self.check_pago_parcial.toggled.connect(self._toggle_pago_parcial)
        parcial_layout.addWidget(self.check_pago_parcial)
        
        self.spin_monto_parcial = QDoubleSpinBox()
        self.spin_monto_parcial.setPrefix("$ ")
        self.spin_monto_parcial.setRange(0.01, deuda_total)
        self.spin_monto_parcial.setValue(deuda_total)
        self.spin_monto_parcial.setDecimals(2)
        self.spin_monto_parcial.setEnabled(False)
        self.spin_monto_parcial.setMinimumHeight(35)
        self.spin_monto_parcial.setStyleSheet("font-size: 14px;")
        parcial_layout.addWidget(self.spin_monto_parcial)
        
        layout.addWidget(parcial_container)
        
        layout.addSpacing(10)
        
        # Botones de acción
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(15)
        
        btn_pago = QPushButton("Registrar Pago")
        btn_pago.setMinimumHeight(40)
        btn_pago.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_pago.setStyleSheet("""
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
        btn_pago.clicked.connect(self._registrar_pago)
        
        btn_impago = QPushButton("Registrar Impago")
        btn_impago.setMinimumHeight(40)
        btn_impago.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_impago.setStyleSheet("""
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
        """)
        btn_impago.clicked.connect(self._registrar_impago)
        
        btn_layout.addWidget(btn_pago)
        btn_layout.addWidget(btn_impago)
        layout.addLayout(btn_layout)
    
    def _agregar_linea_info(self, layout: QVBoxLayout, label: str, valor: str, destacado: bool = False):
        """Agrega una línea de información al layout"""
        linea_layout = QHBoxLayout()
        linea_layout.setContentsMargins(0, 0, 0, 0)
        
        label_widget = QLabel(label)
        label_widget.setStyleSheet("font-size: 14px; color: #94a3b8;")
        linea_layout.addWidget(label_widget)
        
        linea_layout.addStretch()
        
        valor_widget = QLabel(valor)
        if destacado:
            valor_widget.setStyleSheet("font-size: 14px; color: #3b82f6; font-weight: 600;")
        else:
            valor_widget.setStyleSheet("font-size: 14px; color: #cbd5e1;")
        linea_layout.addWidget(valor_widget)
        
        layout.addLayout(linea_layout)
    
    def _toggle_pago_parcial(self, checked: bool):
        """Activa/desactiva el campo de monto parcial"""
        if self.spin_monto_parcial:
            self.spin_monto_parcial.setEnabled(checked)
    
    def _registrar_pago(self):
        """Registra el pago de la cuota"""
        # Validar si es mes futuro
        if self.es_mes_futuro:
            dialog = ConfirmacionDialog(
                self,
                "Pago Adelantado",
                f"Este es un mes futuro.\n\n"
                f"¿Desea registrar un ADELANTO de pago?\n\n"
                f"Monto: ${self.cliente.valor_cuota:,.2f}",
                tipo="question"
            )
            
            if dialog.exec() != QDialog.DialogCode.Accepted:
                return
        
        # Mostrar diálogo para seleccionar método de pago
        metodos = MetodoPago.obtener_todos()
        if not metodos:
            dialog = ConfirmacionDialog(
                self,
                "Error",
                "No hay métodos de pago configurados",
                tipo="error"
            )
            dialog.exec()
            return
        
        dialog = MetodoPagoSeleccionDialog(self, metodos)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            metodo = dialog.get_metodo()
            
            # Determinar deuda acumulada (de cuota existente o del mes anterior)
            cuota_actual = CuotaMensual.obtener_cuota(self.cliente.id, self.año, self.mes)
            
            if not cuota_actual:
                # No hay cuota registrada, verificar deuda del mes anterior
                mes_anterior = self.mes - 1 if self.mes > 1 else 12
                año_anterior = self.año if self.mes > 1 else self.año - 1
                cuota_anterior = CuotaMensual.obtener_cuota(self.cliente.id, año_anterior, mes_anterior)
                
                deuda_acumulada = 0
                fecha_inicio_mora = None
                
                if cuota_anterior:
                    if cuota_anterior.estado == 'impago':
                        deuda_acumulada = cuota_anterior.monto + (cuota_anterior.deuda_acumulada or 0)
                        fecha_inicio_mora = cuota_anterior.fecha_inicio_mora
                    elif cuota_anterior.estado == 'con_deuda':
                        # Si está con_deuda, significa que se pagó parcialmente pero AÚN queda deuda
                        # La deuda_acumulada ya incluye TODO lo que falta por pagar (cuota + deuda anterior)
                        deuda_acumulada = cuota_anterior.deuda_acumulada or 0
                        fecha_inicio_mora = cuota_anterior.fecha_inicio_mora
            else:
                deuda_acumulada = cuota_actual.deuda_acumulada if cuota_actual.deuda_acumulada else 0
                fecha_inicio_mora = cuota_actual.fecha_inicio_mora if hasattr(cuota_actual, 'fecha_inicio_mora') else None
            
            deuda_total = self.cliente.valor_cuota + deuda_acumulada
            
            # Si es pago parcial Y existen los widgets, usar el monto ingresado
            monto_pagado = None
            if self.check_pago_parcial and self.check_pago_parcial.isChecked():
                monto_pagado = self.spin_monto_parcial.value()
            
            # Registrar cuota como pagado (con monto opcional y deuda heredada)
            CuotaMensual.registrar_pago(
                cliente_id=self.cliente.id,
                año=self.año,
                mes=self.mes,
                monto=self.cliente.valor_cuota,
                metodo_pago=metodo,
                monto_pagado=monto_pagado,
                deuda_previa=deuda_acumulada,
                fecha_inicio_mora=fecha_inicio_mora
            )
            
            # Registrar en la tabla de pagos el monto real pagado
            from datetime import datetime
            monto_real_pagado = monto_pagado if monto_pagado else deuda_total
            Pago.crear(
                cliente_id=self.cliente.id,
                fecha_pago=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                mes_correspondiente=f"{self.año}-{self.mes:02d}",
                monto=monto_real_pagado
            )
            
            # Mensaje de confirmación
            tipo_pago = "Adelanto" if self.es_mes_futuro else "Pago"
            if monto_pagado and monto_pagado < deuda_total:
                deuda_restante = deuda_total - monto_pagado
                dialog = ConfirmacionDialog(
                    self, 
                    "Pago Parcial Registrado", 
                    f"{tipo_pago} parcial: ${monto_pagado:,.0f}\n"
                    f"Deuda total: ${deuda_total:,.0f}\n"
                    f"Deuda restante: ${deuda_restante:,.0f}\n\n"
                    f"El próximo mes se mostrará en amarillo con la deuda pendiente.",
                    tipo="success"
                )
                dialog.exec()
            else:
                dialog = ConfirmacionDialog(
                    self,
                    "Éxito",
                    f"{tipo_pago} registrado correctamente.\nDeuda saldada completamente.",
                    tipo="success"
                )
                dialog.exec()
            
            self.accept()
    
    def _registrar_impago(self):
        """Registra el impago de la cuota"""
        # Validar si es mes futuro
        if self.es_mes_futuro:
            hoy = QDateTime.currentDateTime()
            dialog = ConfirmacionDialog(
                self,
                "Acción No Permitida",
                f"No puede marcar como IMPAGO un mes futuro.\n\n"
                f"El cliente {self.cliente.nombre} tiene hasta el día {self.cliente.dia_cobro} "
                f"del mes actual para realizar el pago.\n\n"
                f"Fecha límite: {hoy.date().year()}-{hoy.date().month():02d}-{self.cliente.dia_cobro:02d}",
                tipo="error"
            )
            dialog.exec()
            return
        
        # Verificar si ya pasó la fecha de cobro del mes actual
        hoy = QDateTime.currentDateTime()
        if self.año == hoy.date().year() and self.mes == hoy.date().month():
            # Es el mes actual, verificar si ya pasó el día de cobro
            if hoy.date().day() < self.cliente.dia_cobro:
                # Obtener nombre del mes en español
                meses_es = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
                           "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
                mes_nombre = meses_es[hoy.date().month() - 1]
                
                dialog = ConfirmacionDialog(
                    self,
                    "Advertencia",
                    f"El cliente aún tiene tiempo para pagar.\n\n"
                    f"Fecha límite: {self.cliente.dia_cobro} de {mes_nombre} {hoy.date().year()}\n"
                    f"Hoy es: {hoy.date().day()} de {mes_nombre} {hoy.date().year()}\n\n"
                    f"¿Está seguro de marcar como impago ahora?",
                    tipo="warning"
                )
                dialog.exec()
                # Aún permitir continuar pero con advertencia
        
        dialog = ConfirmacionDialog(
            self,
            "Confirmar Impago",
            f"¿Confirmar que {self.cliente.nombre} NO pagó la cuota de este mes?\n\n"
            f"La deuda de ${self.cliente.valor_cuota:,.2f} se acumulará.",
            tipo="question"
        )
        
        if dialog.exec() == QDialog.DialogCode.Accepted:
            # Calcular deuda acumulada del mes anterior
            mes_anterior = self.mes - 1 if self.mes > 1 else 12
            año_anterior = self.año if self.mes > 1 else self.año - 1
            cuota_anterior = CuotaMensual.obtener_cuota(self.cliente.id, año_anterior, mes_anterior)
            
            deuda_acumulada = 0
            fecha_inicio_mora = None  # Por defecto, generar nueva fecha
            
            if cuota_anterior:
                if cuota_anterior.estado == 'impago':
                    # Solo heredar fecha si el mes anterior es impago (cadena continua sin pagos)
                    deuda_acumulada = cuota_anterior.monto + (cuota_anterior.deuda_acumulada or 0)
                    fecha_inicio_mora = cuota_anterior.fecha_inicio_mora
                elif cuota_anterior.estado == 'con_deuda':
                    # Hay deuda pendiente del mes anterior
                    deuda_acumulada = cuota_anterior.deuda_acumulada or 0
                    # NO heredar fecha - cualquier pago (parcial o total previo) rompe la cadena
                    # Se generará una nueva fecha de inicio de mora para este mes
                    fecha_inicio_mora = None
                # Si es 'pagado' o cualquier otro estado, deuda_acumulada = 0 y fecha nueva
            
            # Registrar cuota como impago con deuda heredada (si hay) y fecha nueva/heredada
            CuotaMensual.registrar_impago(
                cliente_id=self.cliente.id,
                año=self.año,
                mes=self.mes,
                monto=self.cliente.valor_cuota,
                deuda_previa=deuda_acumulada,
                fecha_inicio_mora=fecha_inicio_mora
            )
            
            dialog = ConfirmacionDialog(
                self,
                "Registrado",
                "Impago registrado. La deuda se acumulará.",
                tipo="success"
            )
            dialog.exec()
            self.accept()


class MetodoPagoSeleccionDialog(QDialog):
    """Diálogo para seleccionar método de pago"""
    
    def __init__(self, parent, metodos: list):
        super().__init__(parent)
        self.metodos = metodos
        self.metodo_seleccionado = None
        self.setWindowTitle("Seleccionar Método de Pago")
        self.setMinimumWidth(350)
        self._init_ui()
    
    def _init_ui(self):
        """Inicializa la interfaz"""
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)
        
        # Título
        titulo = QLabel("Seleccionar Método de Pago")
        titulo.setStyleSheet("font-size: 20px; color: #cbd5e1; font-weight: 700;")
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(titulo)
        
        layout.addSpacing(10)
        
        # Botones para cada método
        for metodo in self.metodos:
            if metodo.activo:
                btn = QPushButton(metodo.nombre)
                btn.setMinimumHeight(40)
                btn.setCursor(Qt.CursorShape.PointingHandCursor)
                btn.setStyleSheet("""
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
                """)
                btn.clicked.connect(lambda checked, m=metodo.nombre: self._seleccionar(m))
                layout.addWidget(btn)
    
    def _seleccionar(self, metodo: str):
        """Selecciona un método"""
        self.metodo_seleccionado = metodo
        self.accept()
    
    def get_metodo(self) -> str:
        """Retorna el método seleccionado"""
        return self.metodo_seleccionado


class ConfirmacionDialog(QDialog):
    """Diálogo de confirmación personalizado con estilo consistente"""
    
    def __init__(self, parent, titulo: str, mensaje: str, tipo: str = "info"):
        super().__init__(parent)
        self.titulo = titulo
        self.mensaje = mensaje
        self.tipo = tipo  # "success", "error", "warning", "question", "info"
        self.setWindowTitle(titulo)
        self.setMinimumWidth(400)
        self._init_ui()
    
    def _init_ui(self):
        """Inicializa la interfaz del diálogo"""
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)
        
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
        mensaje_label.setStyleSheet("font-size: 14px; color: #cbd5e1; line-height: 1.5;")
        mensaje_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        mensaje_label.setWordWrap(True)
        layout.addWidget(mensaje_label)
        
        layout.addSpacing(10)
        
        # Botones según el tipo
        if self.tipo == "question":
            # Dos botones: Sí y No
            btn_layout = QHBoxLayout()
            btn_layout.setSpacing(15)
            
            btn_si = QPushButton("Sí")
            btn_si.setMinimumHeight(40)
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
            btn_no.setMinimumHeight(40)
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
            btn_aceptar.setMinimumHeight(40)
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
