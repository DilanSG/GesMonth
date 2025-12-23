"""
Vista de gestión de clientes
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QPushButton, QTableWidget, QTableWidgetItem,
                             QLineEdit, QMessageBox, QDialog, QFormLayout,
                             QComboBox, QHeaderView, QDoubleSpinBox, QSizePolicy)
from PyQt6.QtCore import Qt
from database.models import Cliente
from controllers.cliente_controller import ClienteController


class ClientesView(QWidget):
    """Vista para gestionar clientes"""
    
    def __init__(self):
        super().__init__()
        self.controller = ClienteController()
        self._init_ui()
    
    def _init_ui(self):
        """Inicializa la interfaz"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)
        
        # Título y botón de agregar
        header_layout = QHBoxLayout()
        title = QLabel("Gestión de Clientes")
        title.setObjectName("pageTitle")
        header_layout.addWidget(title)
        header_layout.addStretch()
        
        btn_add = QPushButton("Agregar Cliente")
        btn_add.setObjectName("primaryButton")
        btn_add.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_add.clicked.connect(self._show_add_dialog)
        header_layout.addWidget(btn_add)
        
        layout.addLayout(header_layout)
        
        # Barra de búsqueda
        search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Buscar por nombre o documento...")
        self.search_input.setMinimumHeight(40)
        self.search_input.textChanged.connect(self._search_clientes)
        search_layout.addWidget(self.search_input)
        
        layout.addLayout(search_layout)
        
        # Tabla de clientes con diseño mejorado
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(['Nombre', 'Documento', 'Teléfono', 'Cuota Mensual', 'Estado', 'Acciones'])
        
        # Configurar ancho de columnas para mejor distribución
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)  # Nombre
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)  # Documento
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)  # Teléfono
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)  # Cuota
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)  # Estado
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
        """Recarga la tabla de clientes"""
        clientes = Cliente.obtener_todos()
        self._populate_table(clientes)
    
    def _populate_table(self, clientes: list):
        """Llena la tabla con los clientes"""
        self.table.setRowCount(len(clientes))
        
        for row, cliente in enumerate(clientes):
            # Nombre
            nombre_item = QTableWidgetItem(cliente.nombre)
            nombre_item.setData(Qt.ItemDataRole.UserRole, cliente.id)  # Guardar ID oculto
            self.table.setItem(row, 0, nombre_item)
            
            # Documento
            doc_item = QTableWidgetItem(cliente.documento)
            self.table.setItem(row, 1, doc_item)
            
            # Teléfono
            tel_item = QTableWidgetItem(cliente.telefono if cliente.telefono else 'N/A')
            self.table.setItem(row, 2, tel_item)
            
            # Cuota con formato de moneda
            cuota_item = QTableWidgetItem(f"${cliente.valor_cuota:,.2f}")
            cuota_item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            self.table.setItem(row, 3, cuota_item)
            
            # Estado
            estado_item = QTableWidgetItem(cliente.estado.capitalize())
            self.table.setItem(row, 4, estado_item)
            
            # Botones de acción con iconos compactos
            actions_widget = QWidget()
            actions_layout = QHBoxLayout(actions_widget)
            actions_layout.setContentsMargins(0, 0, 0, 0)
            actions_layout.setSpacing(6)
            actions_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
            
            # Botón Editar (icono)
            btn_edit = QPushButton("✏️")
            btn_edit.setFixedSize(26, 26)
            btn_edit.setToolTip("Editar cliente")
            btn_edit.setStyleSheet("""
                QPushButton {
                    background: rgba(96, 165, 250, 0.2);
                    border: 1px solid rgba(96, 165, 250, 0.5);
                    border-radius: 13px;
                    color: #60a5fa;
                    font-size: 14px;
                    padding: 0;
                }
                QPushButton:hover {
                    background: rgba(96, 165, 250, 0.4);
                    border: 1px solid rgba(96, 165, 250, 0.8);
                }
            """)
            btn_edit.setCursor(Qt.CursorShape.PointingHandCursor)
            btn_edit.clicked.connect(lambda checked, c=cliente: self._show_edit_dialog(c))
            
            # Botón Eliminar (icono)
            btn_delete = QPushButton("🗑️")
            btn_delete.setFixedSize(26, 26)
            btn_delete.setToolTip("Eliminar cliente")
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
            btn_delete.clicked.connect(lambda checked, cid=cliente.id: self._delete_cliente(cid))
            
            actions_layout.addWidget(btn_edit)
            actions_layout.addWidget(btn_delete)
            
            self.table.setCellWidget(row, 5, actions_widget)
            self.table.setRowHeight(row, 58)
    
    def _search_clientes(self, text: str):
        """Busca clientes por término"""
        if text.strip():
            clientes = Cliente.buscar(text)
        else:
            clientes = Cliente.obtener_todos()
        self._populate_table(clientes)
    
    def _show_add_dialog(self):
        """Muestra el diálogo para agregar cliente"""
        dialog = ClienteDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            data = dialog.get_data()
            
            # Validar documento único
            if not self.controller.validar_documento_unico(data['documento']):
                QMessageBox.warning(self, "Error", "Ya existe un cliente con este documento")
                return
            
            if self.controller.crear_cliente(**data):
                QMessageBox.information(self, "Éxito", "Cliente agregado correctamente")
                self.refresh_data()
            else:
                QMessageBox.warning(self, "Error", "No se pudo agregar el cliente")
    
    def _show_edit_dialog(self, cliente: Cliente):
        """Muestra el diálogo para editar cliente"""
        dialog = ClienteDialog(self, cliente)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            data = dialog.get_data()
            
            # Validar documento único (excluyendo el cliente actual)
            if not self.controller.validar_documento_unico(data['documento'], cliente.id):
                QMessageBox.warning(self, "Error", "Ya existe otro cliente con este documento")
                return
            
            if self.controller.actualizar_cliente(cliente.id, **data):
                QMessageBox.information(self, "Éxito", "Cliente actualizado correctamente")
                self.refresh_data()
            else:
                QMessageBox.warning(self, "Error", "No se pudo actualizar el cliente")
    
    def _delete_cliente(self, cliente_id: int):
        """Elimina un cliente"""
        reply = QMessageBox.question(
            self,
            "Confirmar eliminación",
            "¿Está seguro de eliminar este cliente?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            if self.controller.eliminar_cliente(cliente_id):
                QMessageBox.information(self, "Éxito", "Cliente eliminado correctamente")
                self.refresh_data()
            else:
                QMessageBox.warning(self, "Error", "No se pudo eliminar el cliente")


class ClienteDialog(QDialog):
    """Diálogo para agregar/editar clientes"""
    
    def __init__(self, parent=None, cliente: Cliente = None):
        super().__init__(parent)
        self.cliente = cliente
        self.setWindowTitle("Editar Cliente" if cliente else "Agregar Cliente")
        self.setMinimumWidth(400)
        self._init_ui()
    
    def _init_ui(self):
        """Inicializa la interfaz del diálogo"""
        layout = QFormLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Campos
        self.input_nombre = QLineEdit()
        self.input_documento = QLineEdit()
        self.input_telefono = QLineEdit()
        
        # Campo para el valor de la cuota
        self.input_valor_cuota = QDoubleSpinBox()
        self.input_valor_cuota.setPrefix("$ ")
        self.input_valor_cuota.setRange(0, 999999999)
        self.input_valor_cuota.setDecimals(2)
        self.input_valor_cuota.setValue(0)
        
        # Campo para el día de cobro
        self.input_dia_cobro = QComboBox()
        self.input_dia_cobro.addItems([str(i) for i in range(1, 29)])  # Días del 1 al 28
        self.input_dia_cobro.setCurrentText("5")  # Por defecto día 5
        
        self.combo_estado = QComboBox()
        self.combo_estado.addItems(['activo', 'inactivo'])
        
        # Si es edición, llenar datos
        if self.cliente:
            self.input_nombre.setText(self.cliente.nombre)
            self.input_documento.setText(self.cliente.documento)
            self.input_telefono.setText(self.cliente.telefono)
            self.input_valor_cuota.setValue(self.cliente.valor_cuota)
            self.input_dia_cobro.setCurrentText(str(self.cliente.dia_cobro))
            self.combo_estado.setCurrentText(self.cliente.estado)
        
        layout.addRow("Nombre:", self.input_nombre)
        layout.addRow("Documento:", self.input_documento)
        layout.addRow("Teléfono:", self.input_telefono)
        layout.addRow("Cuota Mensual:", self.input_valor_cuota)
        layout.addRow("Día de Cobro:", self.input_dia_cobro)
        layout.addRow("Estado:", self.combo_estado)
        
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
        if not self.input_nombre.text().strip():
            QMessageBox.warning(self, "Error", "El nombre es obligatorio")
            return
        
        if not self.input_documento.text().strip():
            QMessageBox.warning(self, "Error", "El documento es obligatorio")
            return
        
        self.accept()
    
    def get_data(self) -> dict:
        """Retorna los datos del formulario"""
        return {
            'nombre': self.input_nombre.text().strip(),
            'documento': self.input_documento.text().strip(),
            'telefono': self.input_telefono.text().strip(),
            'valor_cuota': self.input_valor_cuota.value(),
            'dia_cobro': int(self.input_dia_cobro.currentText()),
            'estado': self.combo_estado.currentText()
        }
