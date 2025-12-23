"""
Vista de registro de pagos
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QPushButton, QTableWidget, QTableWidgetItem,
                             QMessageBox, QDialog, QFormLayout, QComboBox,
                             QLineEdit, QDateEdit, QHeaderView, QSizePolicy)
from PyQt6.QtCore import Qt, QDate
from database.models import Pago, Cliente
from controllers.pago_controller import PagoController
from datetime import datetime


class PagosView(QWidget):
    """Vista para registrar y ver pagos"""
    
    def __init__(self):
        super().__init__()
        self.controller = PagoController()
        self._init_ui()
    
    def _init_ui(self):
        """Inicializa la interfaz"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)
        
        # Título y botón de agregar
        header_layout = QHBoxLayout()
        title = QLabel("Registro de Pagos")
        title.setObjectName("pageTitle")
        header_layout.addWidget(title)
        header_layout.addStretch()
        
        btn_add = QPushButton("Registrar Pago")
        btn_add.setObjectName("primaryButton")
        btn_add.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_add.clicked.connect(self._show_add_dialog)
        header_layout.addWidget(btn_add)
        
        layout.addLayout(header_layout)
        
        # Tabla de pagos con diseño mejorado
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels([
            'Cliente', 'Documento', 'Fecha Pago', 'Mes Correspondiente', 'Monto', 'Acciones'
        ])
        
        # Configurar ancho de columnas
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)  # Cliente
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)  # Documento
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)  # Fecha
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)  # Mes
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)  # Monto
        header.setSectionResizeMode(5, QHeaderView.ResizeMode.Fixed)  # Acciones
        header.setDefaultAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        self.table.setColumnWidth(5, 110)
        
        # Configuración visual
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.setAlternatingRowColors(True)
        self.table.setShowGrid(False)
        self.table.verticalHeader().setVisible(False)
        self.table.setMinimumHeight(400)
        
        layout.addWidget(self.table)
        
        # Cargar datos
        self.refresh_data()
    
    def refresh_data(self):
        """Recarga la tabla de pagos"""
        pagos = Pago.obtener_todos()
        self._populate_table(pagos)
    
    def _populate_table(self, pagos: list):
        """Llena la tabla con los pagos"""
        self.table.setRowCount(len(pagos))
        
        for row, pago in enumerate(pagos):
            # Cliente
            cliente_item = QTableWidgetItem(pago['cliente_nombre'])
            cliente_item.setData(Qt.ItemDataRole.UserRole, pago['id'])  # Guardar ID oculto
            self.table.setItem(row, 0, cliente_item)
            
            # Documento
            doc_item = QTableWidgetItem(pago['documento'])
            self.table.setItem(row, 1, doc_item)
            
            # Fecha de pago
            fecha_item = QTableWidgetItem(pago['fecha_pago'])
            self.table.setItem(row, 2, fecha_item)
            
            # Mes correspondiente
            mes_item = QTableWidgetItem(pago['mes_correspondiente'])
            self.table.setItem(row, 3, mes_item)
            
            # Monto con formato
            monto_item = QTableWidgetItem(f"${pago['monto']:,.2f}")
            monto_item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            self.table.setItem(row, 4, monto_item)
            
            # Botón de eliminar con icono compacto
            actions_widget = QWidget()
            actions_layout = QHBoxLayout(actions_widget)
            actions_layout.setContentsMargins(0, 0, 0, 0)
            actions_layout.setSpacing(0)
            actions_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
            
            btn_delete = QPushButton("🗑️")
            btn_delete.setFixedSize(26, 26)
            btn_delete.setToolTip("Eliminar pago")
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
            btn_delete.clicked.connect(lambda checked, pid=pago['id']: self._delete_pago(pid))
            
            actions_layout.addWidget(btn_delete)
            
            self.table.setCellWidget(row, 5, actions_widget)
            self.table.setRowHeight(row, 58)
    
    def _show_add_dialog(self):
        """Muestra el diálogo para registrar pago"""
        dialog = PagoDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            data = dialog.get_data()
            if self.controller.registrar_pago(**data):
                QMessageBox.information(self, "Éxito", "Pago registrado correctamente")
                self.refresh_data()
            else:
                QMessageBox.warning(self, "Error", "No se pudo registrar el pago")
    
    def _delete_pago(self, pago_id: int):
        """Elimina un pago"""
        reply = QMessageBox.question(
            self,
            "Confirmar eliminación",
            "¿Está seguro de eliminar este pago?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            if self.controller.eliminar_pago(pago_id):
                QMessageBox.information(self, "Éxito", "Pago eliminado correctamente")
                self.refresh_data()
            else:
                QMessageBox.warning(self, "Error", "No se pudo eliminar el pago")


class PagoDialog(QDialog):
    """Diálogo para registrar pagos"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Registrar Pago")
        self.setMinimumWidth(400)
        self._init_ui()
    
    def _init_ui(self):
        """Inicializa la interfaz del diálogo"""
        layout = QFormLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Combo de clientes
        self.combo_cliente = QComboBox()
        clientes = Cliente.obtener_todos()
        for cliente in clientes:
            self.combo_cliente.addItem(f"{cliente.nombre} - {cliente.documento}", cliente.id)
        
        # Fecha de pago
        self.date_pago = QDateEdit()
        self.date_pago.setDate(QDate.currentDate())
        self.date_pago.setCalendarPopup(True)
        
        # Mes correspondiente
        self.input_mes = QLineEdit()
        self.input_mes.setText(datetime.now().strftime('%Y-%m'))
        self.input_mes.setPlaceholderText("YYYY-MM")
        
        # Monto
        self.input_monto = QLineEdit()
        self.input_monto.setPlaceholderText("0.00")
        
        layout.addRow("Cliente:", self.combo_cliente)
        layout.addRow("Fecha de Pago:", self.date_pago)
        layout.addRow("Mes Correspondiente:", self.input_mes)
        layout.addRow("Monto:", self.input_monto)
        
        # Botones
        buttons_layout = QHBoxLayout()
        btn_cancel = QPushButton("Cancelar")
        btn_cancel.clicked.connect(self.reject)
        
        btn_save = QPushButton("Guardar")
        btn_save.setObjectName("primaryButton")
        btn_save.clicked.connect(self._validate_and_accept)
        
        buttons_layout.addWidget(btn_cancel)
        buttons_layout.addWidget(btn_save)
        
        layout.addRow(buttons_layout)
    
    def _validate_and_accept(self):
        """Valida los datos antes de aceptar"""
        if self.combo_cliente.currentIndex() < 0:
            QMessageBox.warning(self, "Error", "Debe seleccionar un cliente")
            return
        
        try:
            monto = float(self.input_monto.text())
            if monto <= 0:
                raise ValueError()
        except ValueError:
            QMessageBox.warning(self, "Error", "El monto debe ser un número mayor a 0")
            return
        
        self.accept()
    
    def get_data(self) -> dict:
        """Retorna los datos del formulario"""
        return {
            'cliente_id': self.combo_cliente.currentData(),
            'fecha_pago': self.date_pago.date().toString('yyyy-MM-dd'),
            'mes_correspondiente': self.input_mes.text().strip(),
            'monto': float(self.input_monto.text())
        }
