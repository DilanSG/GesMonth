"""
Gestión de usuarios - Widget para administrar usuarios del sistema
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
                             QTableWidget, QTableWidgetItem, QDialog, QLineEdit, 
                             QComboBox, QMessageBox, QHeaderView, QFrame)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon, QColor, QBrush, QFont
from database.user_models import Usuario


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


class DialogoCrearUsuario(QDialog):
    """Diálogo para crear/editar usuarios"""
    
    def __init__(self, usuario=None, usuario_actual=None, parent=None):
        super().__init__(parent)
        self.usuario = usuario
        self.usuario_actual = usuario_actual
        self.setWindowTitle("Crear Usuario" if not usuario else "Editar Usuario")
        self.setModal(True)
        self.setMinimumWidth(450)
        self._init_ui()
        
        if usuario:
            self._cargar_datos()
    
    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Aplicar estilo del tema al diálogo
        from PyQt6.QtWidgets import QApplication
        self.setStyleSheet(QApplication.instance().styleSheet())
        
        # Username
        layout.addWidget(QLabel("Usuario:"))
        self.txt_username = QLineEdit()
        self.txt_username.setPlaceholderText("Nombre de usuario (login)")
        self.txt_username.setMinimumHeight(35)
        if self.usuario:
            self.txt_username.setEnabled(False)  # No editable al editar
        layout.addWidget(self.txt_username)
        
        # Nombre completo
        layout.addWidget(QLabel("Nombre Completo:"))
        self.txt_nombre = QLineEdit()
        self.txt_nombre.setPlaceholderText("Nombre completo del usuario")
        self.txt_nombre.setMinimumHeight(35)
        layout.addWidget(self.txt_nombre)
        
        # Contraseña (solo al crear)
        if not self.usuario:
            layout.addWidget(QLabel("Contraseña:"))
            self.txt_password = QLineEdit()
            self.txt_password.setPlaceholderText("Contraseña inicial")
            self.txt_password.setEchoMode(QLineEdit.EchoMode.Password)
            self.txt_password.setMinimumHeight(35)
            layout.addWidget(self.txt_password)
        
        # Rol
        layout.addWidget(QLabel("Rol:"))
        self.combo_rol = QComboBox()
        self.combo_rol.addItems(["admin", "operador", "solo_lectura"])
        self.combo_rol.setMinimumHeight(35)
        layout.addWidget(self.combo_rol)
        
        # Nota informativa
        nota = QLabel("Nota: Solo los superadministradores pueden crear otros usuarios.")
        nota.setStyleSheet("font-size: 11px; color: #94a3b8; font-style: italic;")
        nota.setWordWrap(True)
        layout.addWidget(nota)
        
        # Detectar tema actual para los botones
        is_dark = True
        widget = self.parent()
        while widget:
            if hasattr(widget, 'current_theme'):
                is_dark = widget.current_theme == 'dark'
                break
            widget = widget.parent() if hasattr(widget, 'parent') and callable(widget.parent) else None
            if widget:
                widget = widget.window()
        
        # Botones
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        
        btn_cancelar = QPushButton("Cancelar")
        btn_cancelar.setMinimumSize(100, 35)
        btn_cancelar.setStyleSheet("""
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
        btn_cancelar.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_cancelar.clicked.connect(self.reject)
        btn_layout.addWidget(btn_cancelar)
        
        btn_guardar = QPushButton("Guardar")
        btn_guardar.setMinimumSize(100, 35)
        if is_dark:
            btn_guardar_style = """
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
            btn_guardar_style = """
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
        btn_guardar.setStyleSheet(btn_guardar_style)
        btn_guardar.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_guardar.clicked.connect(self._guardar)
        btn_layout.addWidget(btn_guardar)
        
        layout.addLayout(btn_layout)
    
    def _cargar_datos(self):
        """Carga los datos del usuario a editar"""
        self.txt_username.setText(self.usuario.username)
        self.txt_nombre.setText(self.usuario.nombre_completo)
        
        # Seleccionar rol
        index = self.combo_rol.findText(self.usuario.rol)
        if index >= 0:
            self.combo_rol.setCurrentIndex(index)
    
    def _guardar(self):
        """Guarda el usuario"""
        username = self.txt_username.text().strip()
        nombre = self.txt_nombre.text().strip()
        rol = self.combo_rol.currentText()
        
        # Validaciones
        if not username or not nombre:
            dialog = ConfirmacionDialog(self, "Error", "Debe completar todos los campos", tipo="error")
            dialog.exec()
            return
        
        if not self.usuario:
            # Crear nuevo
            password = self.txt_password.text()
            if not password or len(password) < 6:
                dialog = ConfirmacionDialog(self, "Error", "La contraseña debe tener al menos 6 caracteres", tipo="error")
                dialog.exec()
                return
            
            # Obtener ID del usuario actual
            creado_por_id = self.usuario_actual.id if self.usuario_actual else 1
            
            try:
                nuevo_usuario = Usuario.crear(
                    username=username,
                    password=password,
                    nombre_completo=nombre,
                    rol=rol,
                    creado_por_usuario_id=creado_por_id
                )
                
                if nuevo_usuario:
                    dialog = ConfirmacionDialog(self, "Éxito", "Usuario creado correctamente", tipo="success")
                    dialog.exec()
                else:
                    dialog = ConfirmacionDialog(self, "Error", "No se pudo crear el usuario", tipo="error")
                    dialog.exec()
                    return
            except Exception as e:
                dialog = ConfirmacionDialog(self, "Error", f"Error al crear usuario: {str(e)}", tipo="error")
                dialog.exec()
                return
        else:
            # Actualizar existente
            exito = Usuario.actualizar(
                self.usuario.id,
                nombre_completo=nombre,
                rol=rol,
                activo=self.usuario.activo
            )
            
            if not exito:
                dialog = ConfirmacionDialog(self, "Error", "No se pudo actualizar el usuario", tipo="error")
                dialog.exec()
                return
                
            dialog = ConfirmacionDialog(self, "Éxito", "Usuario actualizado correctamente", tipo="success")
            dialog.exec()
        
        self.accept()


class DialogoCambiarPassword(QDialog):
    """Diálogo para cambiar contraseña de usuario"""
    
    def __init__(self, usuario, parent=None):
        super().__init__(parent)
        self.usuario = usuario
        self.setWindowTitle(f"Cambiar Contraseña - {usuario.username}")
        self.setModal(True)
        self.setMinimumWidth(400)
        self._init_ui()
    
    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Aplicar estilo del tema al diálogo
        from PyQt6.QtWidgets import QApplication
        self.setStyleSheet(QApplication.instance().styleSheet())
        
        # Nueva contraseña
        layout.addWidget(QLabel("Nueva Contraseña:"))
        self.txt_password = QLineEdit()
        self.txt_password.setEchoMode(QLineEdit.EchoMode.Password)
        self.txt_password.setPlaceholderText("Mínimo 6 caracteres")
        self.txt_password.setMinimumHeight(35)
        layout.addWidget(self.txt_password)
        
        # Confirmar contraseña
        layout.addWidget(QLabel("Confirmar Contraseña:"))
        self.txt_confirmar = QLineEdit()
        self.txt_confirmar.setEchoMode(QLineEdit.EchoMode.Password)
        self.txt_confirmar.setPlaceholderText("Repetir contraseña")
        self.txt_confirmar.setMinimumHeight(35)
        layout.addWidget(self.txt_confirmar)
        
        # Detectar tema actual para los botones
        is_dark = True
        widget = self.parent()
        while widget:
            if hasattr(widget, 'current_theme'):
                is_dark = widget.current_theme == 'dark'
                break
            widget = widget.parent() if hasattr(widget, 'parent') and callable(widget.parent) else None
            if widget:
                widget = widget.window()
        
        # Botones
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        
        btn_cancelar = QPushButton("Cancelar")
        btn_cancelar.setMinimumSize(100, 35)
        btn_cancelar.setStyleSheet("""
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
        btn_cancelar.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_cancelar.clicked.connect(self.reject)
        btn_layout.addWidget(btn_cancelar)
        
        btn_guardar = QPushButton("Cambiar")
        btn_guardar.setMinimumSize(100, 35)
        if is_dark:
            btn_guardar_style = """
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
            btn_guardar_style = """
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
        btn_guardar.setStyleSheet(btn_guardar_style)
        btn_guardar.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_guardar.clicked.connect(self._cambiar)
        btn_layout.addWidget(btn_guardar)
        
        layout.addLayout(btn_layout)
    
    def _cambiar(self):
        """Cambia la contraseña"""
        password = self.txt_password.text()
        confirmar = self.txt_confirmar.text()
        
        if not password or len(password) < 6:
            dialog = ConfirmacionDialog(self, "Error", "La contraseña debe tener al menos 6 caracteres", tipo="error")
            dialog.exec()
            return
        
        if password != confirmar:
            dialog = ConfirmacionDialog(self, "Error", "Las contraseñas no coinciden", tipo="error")
            dialog.exec()
            return
        
        try:
            if Usuario.cambiar_password(self.usuario.id, password):
                dialog = ConfirmacionDialog(self, "Éxito", "Contraseña cambiada correctamente", tipo="success")
                dialog.exec()
                self.accept()
            else:
                dialog = ConfirmacionDialog(self, "Error", "No se pudo cambiar la contraseña", tipo="error")
                dialog.exec()
        except Exception as e:
            dialog = ConfirmacionDialog(self, "Error", f"Error al cambiar contraseña: {str(e)}", tipo="error")
            dialog.exec()


class UsuariosManagement(QWidget):
    """Widget de gestión de usuarios"""
    
    def __init__(self, usuario_actual=None):
        super().__init__()
        self.usuario_actual = usuario_actual
        self._init_ui()
        self._cargar_usuarios()
    
    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Header
        header_layout = QHBoxLayout()
        
        title = QLabel("Gestión de Usuarios")
        title.setStyleSheet("font-size: 18px; font-weight: bold; color: #60a5fa;")
        header_layout.addWidget(title)
        
        header_layout.addStretch()
        
        # Botón crear usuario
        btn_crear = QPushButton("Crear Usuario")
        btn_crear.setMinimumHeight(40)
        btn_crear.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(59, 130, 246, 0.9),
                    stop:1 rgba(37, 99, 235, 0.9));
                border: 1px solid rgba(59, 130, 246, 0.6);
                border-radius: 8px;
                color: white;
                font-size: 13px;
                font-weight: bold;
                padding: 0 20px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(59, 130, 246, 1.0),
                    stop:1 rgba(37, 99, 235, 1.0));
            }
        """)
        btn_crear.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_crear.clicked.connect(self._crear_usuario)
        header_layout.addWidget(btn_crear)
        
        layout.addLayout(header_layout)
        
        # Descripción
        desc = QLabel("Administre los usuarios que tienen acceso al sistema. Cree, edite, active o desactive usuarios según sea necesario.")
        desc.setStyleSheet("font-size: 13px; color: #94a3b8;")
        desc.setWordWrap(True)
        layout.addWidget(desc)
        
        # Tabla de usuarios
        self.tabla = QTableWidget()
        self.tabla.setColumnCount(5)
        self.tabla.setHorizontalHeaderLabels(['Usuario', 'Nombre', 'Rol', 'Estado', 'Acciones'])
        
        header = self.tabla.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Fixed)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.Fixed)
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.Fixed)
        
        self.tabla.setColumnWidth(2, 150)
        self.tabla.setColumnWidth(3, 100)
        self.tabla.setColumnWidth(4, 250)
        
        self.tabla.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.tabla.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.tabla.setAlternatingRowColors(True)
        self.tabla.verticalHeader().setVisible(False)
        
        layout.addWidget(self.tabla)
    
    def _cargar_usuarios(self):
        """Carga la lista de usuarios"""
        usuarios = Usuario.obtener_todos()
        
        # Ordenar: superadmin primero, luego el resto
        usuarios_ordenados = sorted(usuarios, key=lambda u: (not u.es_superadmin, u.username))
        
        # Detectar tema actual
        is_dark = True
        if hasattr(self.window(), 'current_theme'):
            is_dark = self.window().current_theme == 'dark'
        
        self.tabla.setRowCount(len(usuarios_ordenados))
        
        for row, usuario in enumerate(usuarios_ordenados):
            # Username
            self.tabla.setItem(row, 0, QTableWidgetItem(usuario.username))
            
            # Nombre completo
            self.tabla.setItem(row, 1, QTableWidgetItem(usuario.nombre_completo))
            
            # Rol
            rol_text = f"{usuario.rol.capitalize()}"
            if usuario.es_superadmin:
                rol_text += " (SuperUser)"
            
            item_rol = QTableWidgetItem(rol_text)
            
            if usuario.es_superadmin:
                # Aplicar color con font bold
                if is_dark:
                    color = QColor("#fbbf24")  # Amarillo/dorado brillante
                else:
                    color = QColor("#c2410c")  # Naranja muy oscuro
                
                item_rol.setForeground(QBrush(color))
                font = QFont()
                font.setBold(True)
                font.setPointSize(10)
                item_rol.setFont(font)
            
            self.tabla.setItem(row, 2, item_rol)
            
            # Estado
            estado = "Activo" if usuario.activo else "Inactivo"
            item_estado = QTableWidgetItem(estado)
            if not usuario.activo:
                item_estado.setForeground(Qt.GlobalColor.red)
            self.tabla.setItem(row, 3, item_estado)
            
            # Acciones
            actions_widget = QWidget()
            actions_layout = QHBoxLayout(actions_widget)
            actions_layout.setContentsMargins(5, 5, 5, 5)
            actions_layout.setSpacing(8)
            
            # Botón editar (todos los usuarios pueden editar su info)
            btn_editar = QPushButton("✏️ Editar")
            btn_editar.setFixedHeight(32)
            btn_editar.setMinimumWidth(70)
            btn_editar.setStyleSheet("""
                QPushButton {
                    background: rgba(59, 130, 246, 0.2);
                    border: 2px solid rgba(59, 130, 246, 0.6);
                    border-radius: 6px;
                    color: #3b82f6;
                    font-size: 11px;
                    font-weight: 600;
                    padding: 0 8px;
                }
                QPushButton:hover {
                    background: rgba(59, 130, 246, 0.3);
                    border: 2px solid #3b82f6;
                }
            """)
            btn_editar.setCursor(Qt.CursorShape.PointingHandCursor)
            btn_editar.clicked.connect(lambda checked, u=usuario: self._editar_usuario(u))
            actions_layout.addWidget(btn_editar)
            
            # Solo para usuarios NO superadmin: botón activar/desactivar
            if not usuario.es_superadmin:
                if usuario.activo:
                    toggle_text = "❌ Off"
                    toggle_style = """
                        QPushButton {
                            background: rgba(239, 68, 68, 0.2);
                            border: 2px solid rgba(239, 68, 68, 0.6);
                            border-radius: 6px;
                            color: #ef4444;
                            font-size: 11px;
                            font-weight: 600;
                            padding: 0 8px;
                        }
                        QPushButton:hover {
                            background: rgba(239, 68, 68, 0.3);
                            border: 2px solid #ef4444;
                        }
                    """
                else:
                    toggle_text = "✅ On"
                    toggle_style = """
                        QPushButton {
                            background: rgba(34, 197, 94, 0.2);
                            border: 2px solid rgba(34, 197, 94, 0.6);
                            border-radius: 6px;
                            color: #22c55e;
                            font-size: 11px;
                            font-weight: 600;
                            padding: 0 8px;
                        }
                        QPushButton:hover {
                            background: rgba(34, 197, 94, 0.3);
                            border: 2px solid #22c55e;
                        }
                    """
                btn_toggle = QPushButton(toggle_text)
                btn_toggle.setFixedHeight(32)
                btn_toggle.setMinimumWidth(60)
                btn_toggle.setStyleSheet(toggle_style)
                btn_toggle.setCursor(Qt.CursorShape.PointingHandCursor)
                btn_toggle.clicked.connect(lambda checked, u=usuario: self._toggle_usuario(u))
                actions_layout.addWidget(btn_toggle)
            
            # Botón cambiar contraseña (todos los usuarios)
            btn_password = QPushButton("🔑 Pass")
            btn_password.setFixedHeight(32)
            btn_password.setMinimumWidth(65)
            btn_password.setStyleSheet("""
                QPushButton {
                    background: rgba(139, 92, 246, 0.2);
                    border: 2px solid rgba(139, 92, 246, 0.6);
                    border-radius: 6px;
                    color: #8b5cf6;
                    font-size: 11px;
                    font-weight: 600;
                    padding: 0 8px;
                }
                QPushButton:hover {
                    background: rgba(139, 92, 246, 0.3);
                    border: 2px solid #8b5cf6;
                }
            """)
            btn_password.setCursor(Qt.CursorShape.PointingHandCursor)
            btn_password.clicked.connect(lambda checked, u=usuario: self._cambiar_password(u))
            actions_layout.addWidget(btn_password)
            
            self.tabla.setCellWidget(row, 4, actions_widget)
            self.tabla.setRowHeight(row, 58)
    
    def _crear_usuario(self):
        """Abre diálogo para crear usuario"""
        dialogo = DialogoCrearUsuario(usuario_actual=self.usuario_actual, parent=self)
        if dialogo.exec() == QDialog.DialogCode.Accepted:
            self._cargar_usuarios()
    
    def _editar_usuario(self, usuario):
        """Abre diálogo para editar usuario"""
        dialogo = DialogoCrearUsuario(usuario=usuario, parent=self)
        if dialogo.exec() == QDialog.DialogCode.Accepted:
            self._cargar_usuarios()
    
    def _toggle_usuario(self, usuario):
        """Activa o desactiva un usuario"""
        accion = "desactivar" if usuario.activo else "activar"
        
        dialog = ConfirmacionDialog(
            self,
            "Confirmar",
            f"¿Está seguro de {accion}r al usuario {usuario.username}?",
            tipo="question"
        )
        
        if dialog.exec() == QDialog.DialogCode.Accepted:
            nuevo_estado = not usuario.activo
            if Usuario.actualizar(usuario.id, activo=nuevo_estado):
                success_dialog = ConfirmacionDialog(self, "Éxito", f"Usuario {accion}do correctamente", tipo="success")
                success_dialog.exec()
                self._cargar_usuarios()
            else:
                error_dialog = ConfirmacionDialog(self, "Error", f"No se pudo {accion} el usuario", tipo="error")
                error_dialog.exec()
    
    def _cambiar_password(self, usuario):
        """Abre diálogo para cambiar contraseña"""
        dialogo = DialogoCambiarPassword(usuario=usuario, parent=self)
        dialogo.exec()
