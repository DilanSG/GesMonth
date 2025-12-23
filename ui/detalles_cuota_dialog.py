"""
Diálogo para mostrar detalles de una cuota registrada
"""

from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel,
                             QPushButton, QMessageBox, QFrame)
from PyQt6.QtCore import Qt
from database.models import Cliente, CuotaMensual


class DetallesCuotaDialog(QDialog):
    """Diálogo que muestra información detallada de una cuota registrada"""
    
    def __init__(self, parent, cliente: Cliente, año: int, mes: int, cuota: CuotaMensual):
        super().__init__(parent)
        self.cliente = cliente
        self.año = año
        self.mes = mes
        self.cuota = cuota
        
        meses = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
                 "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
        
        self.setWindowTitle(f"Detalles - {meses[mes - 1]} {año}")
        self.setMinimumWidth(500)
        self._init_ui()
    
    def _init_ui(self):
        """Inicializa la interfaz"""
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)
        
        # Título con nombre del cliente
        titulo = QLabel(self.cliente.nombre)
        titulo.setStyleSheet("font-size: 20px; color: #cbd5e1; font-weight: 700;")
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(titulo)
        
        # Separador
        layout.addSpacing(10)
        
        # Información según el estado (directamente en el layout principal)
        if self.cuota.estado == 'pagado':
            self._mostrar_info_pagado(layout)
        elif self.cuota.estado == 'con_deuda':
            self._mostrar_info_con_deuda(layout)
        elif self.cuota.estado == 'impago':
            self._mostrar_info_impago(layout)
        
        layout.addSpacing(20)
        
        # Botón eliminar
        btn_eliminar = QPushButton("🗑️ Eliminar Registro")
        btn_eliminar.setMinimumHeight(45)
        btn_eliminar.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_eliminar.setStyleSheet("""
            QPushButton {
                background: rgba(239, 68, 68, 0.3);
                border: 1px solid rgba(239, 68, 68, 0.5);
                border-radius: 10px;
                color: #fca5a5;
                font-weight: 600;
                font-size: 14px;
            }
            QPushButton:hover {
                background: rgba(239, 68, 68, 0.4);
            }
        """)
        btn_eliminar.clicked.connect(self._eliminar_cuota)
        layout.addWidget(btn_eliminar)
        
        # Botón cerrar
        btn_cerrar = QPushButton("Cerrar")
        btn_cerrar.setObjectName("secondaryButton")
        btn_cerrar.clicked.connect(self.reject)
        layout.addWidget(btn_cerrar)
    
    def _agregar_linea_info(self, layout: QVBoxLayout, etiqueta: str, valor: str, destacado: bool = False):
        """Agrega una línea de información"""
        container = QHBoxLayout()
        
        label_etiqueta = QLabel(etiqueta)
        label_etiqueta.setStyleSheet("font-size: 14px; color: #94a3b8; font-weight: 500;")
        
        label_valor = QLabel(valor)
        if destacado:
            label_valor.setStyleSheet("font-size: 16px; color: #cbd5e1; font-weight: 700;")
        else:
            label_valor.setStyleSheet("font-size: 14px; color: #cbd5e1; font-weight: 600;")
        
        container.addWidget(label_etiqueta)
        container.addStretch()
        container.addWidget(label_valor)
        
        layout.addLayout(container)
    
    def _mostrar_info_pagado(self, layout: QVBoxLayout):
        """Muestra información para cuota pagada"""
        # Estado
        estado_label = QLabel("PAGADO")
        estado_label.setStyleSheet("font-size: 18px; color: #86efac; font-weight: 700;")
        estado_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(estado_label)
        
        layout.addSpacing(10)
        
        # Calcular si se pagó con deuda
        mes_ant = self.mes - 1 if self.mes > 1 else 12
        año_ant = self.año if self.mes > 1 else self.año - 1
        cuota_ant = CuotaMensual.obtener_cuota(self.cliente.id, año_ant, mes_ant)
        
        deuda_previa = 0
        if cuota_ant:
            if cuota_ant.estado == 'impago':
                deuda_previa = cuota_ant.monto + (cuota_ant.deuda_acumulada or 0)
            elif cuota_ant.estado == 'con_deuda' and not cuota_ant.metodo_pago:
                deuda_previa = cuota_ant.deuda_acumulada or 0
        
        monto_total = self.cuota.monto + deuda_previa
        
        # Información
        self._agregar_linea_info(layout, "Método de pago:", self.cuota.metodo_pago or "N/A")
        self._agregar_linea_info(layout, "Fecha de registro:", self.cuota.fecha_registro[:16] if self.cuota.fecha_registro else "N/A")
        self._agregar_linea_info(layout, "Cuota del mes:", f"${self.cuota.monto:,.0f}")
        
        if deuda_previa > 0:
            self._agregar_linea_info(layout, "Deuda previa:", f"${deuda_previa:,.0f}")
            self._agregar_linea_info(layout, "Total pagado:", f"${monto_total:,.0f}", True)
        else:
            self._agregar_linea_info(layout, "Total pagado:", f"${monto_total:,.0f}", True)
    
    def _mostrar_info_con_deuda(self, layout: QVBoxLayout):
        """Muestra información para cuota con deuda"""
        if self.cuota.metodo_pago:
            # Pago parcial
            estado_label = QLabel("PAGO PARCIAL")
            estado_label.setStyleSheet("font-size: 18px; color: #6ee7b7; font-weight: 700;")
        else:
            # Deuda heredada
            estado_label = QLabel("DEUDA PENDIENTE")
            estado_label.setStyleSheet("font-size: 18px; color: #fcd34d; font-weight: 700;")
        
        estado_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(estado_label)
        
        layout.addSpacing(10)
        
        # Calcular deuda previa
        mes_ant = self.mes - 1 if self.mes > 1 else 12
        año_ant = self.año if self.mes > 1 else self.año - 1
        cuota_ant = CuotaMensual.obtener_cuota(self.cliente.id, año_ant, mes_ant)
        
        deuda_previa = 0
        if cuota_ant:
            if cuota_ant.estado == 'impago':
                deuda_previa = cuota_ant.monto + (cuota_ant.deuda_acumulada or 0)
            elif cuota_ant.estado == 'con_deuda':
                deuda_previa = cuota_ant.deuda_acumulada or 0
        
        deuda_total_antes = self.cuota.monto + deuda_previa
        deuda_restante = self.cuota.deuda_acumulada or 0
        
        # Información
        self._agregar_linea_info(layout, "Cuota del mes:", f"${self.cuota.monto:,.0f}")
        
        if deuda_previa > 0:
            self._agregar_linea_info(layout, "Deuda previa:", f"${deuda_previa:,.0f}")
            self._agregar_linea_info(layout, "Deuda total:", f"${deuda_total_antes:,.0f}")
        
        if self.cuota.metodo_pago:
            # Es un pago parcial
            monto_pagado = deuda_total_antes - deuda_restante
            self._agregar_linea_info(layout, "Método de pago:", self.cuota.metodo_pago)
            self._agregar_linea_info(layout, "Fecha de pago:", self.cuota.fecha_registro[:16] if self.cuota.fecha_registro else "N/A")
            self._agregar_linea_info(layout, "Monto pagado:", f"${monto_pagado:,.0f}")
        
        self._agregar_linea_info(layout, "Deuda restante:", f"${deuda_restante:,.0f}", True)
        
        if self.cuota.fecha_inicio_mora:
            self._agregar_linea_info(layout, "Mora desde:", self.cuota.fecha_inicio_mora[:10])
    
    def _mostrar_info_impago(self, layout: QVBoxLayout):
        """Muestra información para cuota impaga"""
        estado_label = QLabel("IMPAGO")
        estado_label.setStyleSheet("font-size: 18px; color: #fca5a5; font-weight: 700;")
        estado_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(estado_label)
        
        layout.addSpacing(10)
        
        # Información
        self._agregar_linea_info(layout, "Cuota del mes:", f"${self.cuota.monto:,.0f}")
        
        if self.cuota.deuda_acumulada and self.cuota.deuda_acumulada > 0:
            self._agregar_linea_info(layout, "Deuda previa:", f"${self.cuota.deuda_acumulada:,.0f}")
            deuda_total = self.cuota.monto + self.cuota.deuda_acumulada
            self._agregar_linea_info(layout, "Deuda total:", f"${deuda_total:,.0f}", True)
        else:
            self._agregar_linea_info(layout, "Deuda total:", f"${self.cuota.monto:,.0f}", True)
        
        if self.cuota.fecha_inicio_mora:
            self._agregar_linea_info(layout, "Mora desde:", self.cuota.fecha_inicio_mora[:10])
        
        if self.cuota.fecha_registro:
            self._agregar_linea_info(layout, "Registrado el:", self.cuota.fecha_registro[:16])
    
    def _eliminar_cuota(self):
        """Elimina el registro de la cuota"""
        meses = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
                 "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
        
        reply = QMessageBox.question(
            self,
            "Confirmar Eliminación",
            f"¿Está seguro de eliminar el registro de {meses[self.mes - 1]} {self.año}?\n\n"
            f"Cliente: {self.cliente.nombre}\n"
            f"Estado: {self.cuota.estado.upper()}\n\n"
            f"Esta acción no se puede deshacer.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            CuotaMensual.eliminar(self.cuota.id)
            QMessageBox.information(self, "Eliminado", "Registro eliminado correctamente.")
            self.accept()
