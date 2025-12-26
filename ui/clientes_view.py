"""
Vista de gestión de clientes
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QPushButton, QTableWidget, QTableWidgetItem,
                             QLineEdit, QDialog, QComboBox, QHeaderView, 
                             QDoubleSpinBox, QSizePolicy)
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
            
            # Detectar tema para botón eliminar
            is_dark = True
            if hasattr(self.window(), 'current_theme'):
                is_dark = self.window().current_theme == 'dark'
            
            # Botón Eliminar (icono)
            btn_delete = QPushButton("🗑️")
            btn_delete.setFixedSize(26, 26)
            btn_delete.setToolTip("Eliminar cliente")
            if is_dark:
                btn_delete_style = """
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
                """
            else:
                btn_delete_style = """
                    QPushButton {
                        background: rgba(185, 28, 28, 0.15);
                        border: 1px solid rgba(185, 28, 28, 0.5);
                        border-radius: 13px;
                        color: #b91c1c;
                        font-size: 14px;
                        padding: 0;
                    }
                    QPushButton:hover {
                        background: rgba(185, 28, 28, 0.25);
                        border: 1px solid rgba(185, 28, 28, 0.8);
                    }
                """
            btn_delete.setStyleSheet(btn_delete_style)
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
                dialog = ConfirmacionDialog(
                    self,
                    "Error",
                    "Ya existe un cliente con este documento",
                    tipo="error"
                )
                dialog.exec()
                return
            
            if self.controller.crear_cliente(**data):
                dialog = ConfirmacionDialog(
                    self,
                    "Éxito",
                    "Cliente agregado correctamente",
                    tipo="success"
                )
                dialog.exec()
                self.refresh_data()
            else:
                dialog = ConfirmacionDialog(
                    self,
                    "Error",
                    "No se pudo agregar el cliente",
                    tipo="error"
                )
                dialog.exec()
    
    def _show_edit_dialog(self, cliente: Cliente):
        """Muestra el diálogo para editar cliente"""
        dialog = ClienteDialog(self, cliente)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            data = dialog.get_data()
            
            # Validar documento único (excluyendo el cliente actual)
            if not self.controller.validar_documento_unico(data['documento'], cliente.id):
                dialog = ConfirmacionDialog(
                    self,
                    "Error",
                    "Ya existe otro cliente con este documento",
                    tipo="error"
                )
                dialog.exec()
                return
            
            if self.controller.actualizar_cliente(cliente.id, **data):
                dialog = ConfirmacionDialog(
                    self,
                    "Éxito",
                    "Cliente actualizado correctamente",
                    tipo="success"
                )
                dialog.exec()
                self.refresh_data()
            else:
                dialog = ConfirmacionDialog(
                    self,
                    "Error",
                    "No se pudo actualizar el cliente",
                    tipo="error"
                )
                dialog.exec()
    
    def _delete_cliente(self, cliente_id: int):
        """Elimina un cliente"""
        dialog = ConfirmacionDialog(
            self,
            "Confirmar eliminación",
            "¿Está seguro de eliminar este cliente?",
            tipo="question"
        )
        
        if dialog.exec() == QDialog.DialogCode.Accepted:
            if self.controller.eliminar_cliente(cliente_id):
                dialog = ConfirmacionDialog(
                    self,
                    "Éxito",
                    "Cliente eliminado correctamente",
                    tipo="success"
                )
                dialog.exec()
                self.refresh_data()
            else:
                dialog = ConfirmacionDialog(
                    self,
                    "Error",
                    "No se pudo eliminar el cliente",
                    tipo="error"
                )
                dialog.exec()


class ClienteDialog(QDialog):
    """Diálogo para agregar/editar clientes"""
    
    def __init__(self, parent=None, cliente: Cliente = None):
        super().__init__(parent)
        self.cliente = cliente
        self.setWindowTitle("Editar Cliente" if cliente else "Agregar Cliente")
        self.setMinimumWidth(450)
        self._init_ui()
    
    def _init_ui(self):
        """Inicializa la interfaz del diálogo"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)
        
        # Detectar tema actual desde la ventana principal
        main_window = self.parent()
        if main_window:
            main_window = main_window.window()
        self.is_dark = True
        if main_window and hasattr(main_window, 'current_theme'):
            self.is_dark = main_window.current_theme == 'dark'
        
        # Título
        titulo = QLabel("Editar Cliente" if self.cliente else "Agregar Cliente")
        if self.is_dark:
            titulo.setStyleSheet("font-size: 20px; color: #cbd5e1; font-weight: 700;")
        else:
            titulo.setStyleSheet("font-size: 20px; color: #1e293b; font-weight: 700;")
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(titulo)
        
        layout.addSpacing(10)
        
        # Campos con diseño mejorado
        self.input_nombre = QLineEdit()
        self.input_nombre.setPlaceholderText("Nombre completo del cliente")
        self.input_nombre.setMinimumHeight(40)
        self._add_field(layout, "Nombre:", self.input_nombre)
        
        self.input_documento = QLineEdit()
        self.input_documento.setPlaceholderText("Número de documento")
        self.input_documento.setMinimumHeight(40)
        self._add_field(layout, "Documento:", self.input_documento)
        
        self.input_telefono = QLineEdit()
        self.input_telefono.setPlaceholderText("Teléfono (opcional)")
        self.input_telefono.setMinimumHeight(40)
        self._add_field(layout, "Teléfono:", self.input_telefono)
        
        # Campo para el valor de la cuota
        self.input_valor_cuota = QDoubleSpinBox()
        self.input_valor_cuota.setPrefix("$ ")
        self.input_valor_cuota.setRange(0, 999999999)
        self.input_valor_cuota.setDecimals(2)
        self.input_valor_cuota.setValue(0)
        self.input_valor_cuota.setMinimumHeight(40)
        self.input_valor_cuota.setStyleSheet("font-size: 14px;")
        self._add_field(layout, "Cuota Mensual:", self.input_valor_cuota)
        
        # Campo para el día de cobro
        self.input_dia_cobro = QComboBox()
        self.input_dia_cobro.addItems([str(i) for i in range(1, 32)])  # Días del 1 al 31
        self.input_dia_cobro.setCurrentText("5")  # Por defecto día 5
        self.input_dia_cobro.setMinimumHeight(40)
        self._add_field(layout, "Día de Cobro:", self.input_dia_cobro)
        
        self.combo_estado = QComboBox()
        self.combo_estado.addItems(['Activo', 'Inactivo'])
        self.combo_estado.setMinimumHeight(40)
        self._add_field(layout, "Estado:", self.combo_estado)
        
        # Si es edición, llenar datos
        if self.cliente:
            self.input_nombre.setText(self.cliente.nombre)
            self.input_documento.setText(self.cliente.documento)
            self.input_telefono.setText(self.cliente.telefono)
            self.input_valor_cuota.setValue(self.cliente.valor_cuota)
            self.input_dia_cobro.setCurrentText(str(self.cliente.dia_cobro))
            self.combo_estado.setCurrentText(self.cliente.estado)
        
        layout.addSpacing(10)
        
        # Botones con diseño mejorado
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(15)
        
        btn_cancel = QPushButton("Cancelar")
        btn_cancel.setMinimumHeight(45)
        btn_cancel.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_cancel.setStyleSheet("""
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
        btn_cancel.clicked.connect(self.reject)
        
        btn_save = QPushButton("Guardar")
        btn_save.setMinimumHeight(45)
        btn_save.setCursor(Qt.CursorShape.PointingHandCursor)
        if self.is_dark:
            btn_save_style = """
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
        else:
            btn_save_style = """
                QPushButton {
                    background: rgba(21, 128, 61, 0.15);
                    color: #15803d;
                    border: 2px solid #15803d;
                    border-radius: 8px;
                    font-size: 14px;
                    font-weight: 700;
                }
                QPushButton:hover {
                    background: rgba(21, 128, 61, 0.25);
                }
            """
        btn_save.setStyleSheet(btn_save_style)
        btn_save.clicked.connect(self._validate_and_accept)
        
        buttons_layout.addWidget(btn_cancel)
        buttons_layout.addWidget(btn_save)
        
        layout.addLayout(buttons_layout)
    
    def _add_field(self, layout: QVBoxLayout, label_text: str, widget: QWidget):
        """Agrega un campo al formulario con estilo mejorado"""
        label = QLabel(label_text)
        if self.is_dark:
            label.setStyleSheet("font-size: 14px; color: #94a3b8; font-weight: 500; margin-bottom: 5px;")
        else:
            label.setStyleSheet("font-size: 14px; color: #334155; font-weight: 600; margin-bottom: 5px;")
        layout.addWidget(label)
        layout.addWidget(widget)
    
    def _validate_and_accept(self):
        """Valida los datos antes de aceptar"""
        if not self.input_nombre.text().strip():
            dialog = ConfirmacionDialog(
                self,
                "Error",
                "El nombre es obligatorio",
                tipo="warning"
            )
            dialog.exec()
            return
        
        if not self.input_documento.text().strip():
            dialog = ConfirmacionDialog(
                self,
                "Error",
                "El documento es obligatorio",
                tipo="warning"
            )
            dialog.exec()
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
        
        # Detectar tema actual desde la ventana principal - navegar hasta MainWindow
        is_dark = True
        widget = self.parent()
        while widget:
            if hasattr(widget, 'current_theme'):
                is_dark = widget.current_theme == 'dark'
                break
            widget = widget.parent() if hasattr(widget, 'parent') and callable(widget.parent) else None
            if widget:
                widget = widget.window()
        
        # Aplicar estilo del tema al diálogo
        from PyQt6.QtWidgets import QApplication
        self.setStyleSheet(QApplication.instance().styleSheet())
        
        # Título con color según tipo
        titulo = QLabel(self.titulo)
        titulo.setObjectName(f"dialogTitle{self.tipo.capitalize()}")
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        titulo.setWordWrap(True)
        layout.addWidget(titulo)
        
        layout.addSpacing(10)
        
        # Mensaje
        mensaje_label = QLabel(self.mensaje)
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
            if is_dark:
                btn_si_style = """
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
            else:
                btn_si_style = """
                    QPushButton {
                        background: rgba(21, 128, 61, 0.15);
                        color: #15803d;
                        border: 2px solid #15803d;
                        border-radius: 8px;
                        font-size: 14px;
                        font-weight: 700;
                    }
                    QPushButton:hover {
                        background: rgba(21, 128, 61, 0.25);
                    }
                """
            btn_si.setStyleSheet(btn_si_style)
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
                if is_dark:
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
                else:
                    estilo_btn = """
                        QPushButton {
                            background: rgba(21, 128, 61, 0.15);
                            color: #15803d;
                            border: 2px solid #15803d;
                            border-radius: 8px;
                            font-size: 14px;
                            font-weight: 700;
                        }
                        QPushButton:hover {
                            background: rgba(21, 128, 61, 0.25);
                        }
                    """
            elif self.tipo == "error":
                if is_dark:
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
                else:
                    estilo_btn = """
                        QPushButton {
                            background: rgba(185, 28, 28, 0.15);
                            color: #b91c1c;
                            border: 2px solid #b91c1c;
                            border-radius: 8px;
                            font-size: 14px;
                            font-weight: 700;
                        }
                        QPushButton:hover {
                            background: rgba(185, 28, 28, 0.25);
                        }
                    """
            elif self.tipo == "warning":
                if is_dark:
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
                else:
                    estilo_btn = """
                        QPushButton {
                            background: rgba(161, 98, 7, 0.15);
                            color: #a16207;
                            border: 2px solid #a16207;
                            border-radius: 8px;
                            font-size: 14px;
                            font-weight: 700;
                        }
                        QPushButton:hover {
                            background: rgba(161, 98, 7, 0.25);
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

