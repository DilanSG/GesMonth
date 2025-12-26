"""
Diálogo para mostrar detalles de una cuota registrada
"""

from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel,
                             QPushButton, QFrame, QWidget)
from PyQt6.QtCore import Qt
from database.models import Cliente, CuotaMensual, MetodoPago


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
        
        # Detectar tema actual desde la ventana principal - navegar hasta MainWindow
        self.is_dark = True
        widget = self.parent()
        while widget:
            if hasattr(widget, 'current_theme'):
                self.is_dark = widget.current_theme == 'dark'
                break
            widget = widget.parent() if hasattr(widget, 'parent') and callable(widget.parent) else None
            if widget:
                widget = widget.window()
        
        # Título con nombre del cliente
        titulo = QLabel(self.cliente.nombre)
        if self.is_dark:
            titulo.setStyleSheet("font-size: 20px; color: #cbd5e1; font-weight: 700;")
        else:
            titulo.setStyleSheet("font-size: 20px; color: #0f172a; font-weight: 700;")
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
        if self.is_dark:
            btn_eliminar_style = """
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
            """
        else:
            btn_eliminar_style = """
                QPushButton {
                    background: rgba(185, 28, 28, 0.15);
                    border: 2px solid rgba(185, 28, 28, 0.6);
                    border-radius: 10px;
                    color: #b91c1c;
                    font-weight: 700;
                    font-size: 14px;
                }
                QPushButton:hover {
                    background: rgba(185, 28, 28, 0.25);
                }
            """
        btn_eliminar.setStyleSheet(btn_eliminar_style)
        btn_eliminar.clicked.connect(self._eliminar_cuota)
        layout.addWidget(btn_eliminar)
        
        # Botón cerrar
        btn_cerrar = QPushButton("Cerrar")
        btn_cerrar.setObjectName("secondaryButton")
        btn_cerrar.clicked.connect(self.reject)
        layout.addWidget(btn_cerrar)
    
    def _agregar_linea_info(self, layout: QVBoxLayout, etiqueta: str, valor: str, destacado: bool = False, metodo_pago: str = None):
        """Agrega una línea de información"""
        container = QHBoxLayout()
        
        label_etiqueta = QLabel(etiqueta)
        if self.is_dark:
            label_etiqueta.setStyleSheet("font-size: 14px; color: #94a3b8; font-weight: 500;")
        else:
            label_etiqueta.setStyleSheet("font-size: 14px; color: #475569; font-weight: 700;")
        
        # Si es método de pago, aplicar su color al texto
        if metodo_pago:
            # Buscar el color del método de pago
            metodos = MetodoPago.obtener_todos()
            color = "#3b82f6"  # Color por defecto
            for m in metodos:
                if m.nombre == metodo_pago:
                    color = m.color
                    break
            
            # Texto del método con su color
            label_valor = QLabel(valor)
            label_valor.setStyleSheet(f"font-size: 14px; color: {color}; font-weight: 700;")
        else:
            label_valor = QLabel(valor)
            if destacado:
                if self.is_dark:
                    label_valor.setStyleSheet("font-size: 16px; color: #cbd5e1; font-weight: 700;")
                else:
                    label_valor.setStyleSheet("font-size: 16px; color: #0a0a0a; font-weight: 700;")
            else:
                if self.is_dark:
                    label_valor.setStyleSheet("font-size: 14px; color: #cbd5e1; font-weight: 600;")
                else:
                    label_valor.setStyleSheet("font-size: 14px; color: #1e293b; font-weight: 700;")
        
        container.addWidget(label_etiqueta)
        container.addStretch()
        container.addWidget(label_valor)
        
        layout.addLayout(container)
    
    def _mostrar_info_pagado(self, layout: QVBoxLayout):
        """Muestra información para cuota pagada"""
        # Estado
        estado_label = QLabel("PAGADO")
        if self.is_dark:
            estado_label.setStyleSheet("font-size: 18px; color: #86efac; font-weight: 700;")
        else:
            estado_label.setStyleSheet("font-size: 18px; color: #15803d; font-weight: 700;")
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
        self._agregar_linea_info(layout, "Método de pago:", self.cuota.metodo_pago or "N/A", metodo_pago=self.cuota.metodo_pago)
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
            if self.is_dark:
                estado_label.setStyleSheet("font-size: 18px; color: #6ee7b7; font-weight: 700;")
            else:
                estado_label.setStyleSheet("font-size: 18px; color: #047857; font-weight: 700;")
        else:
            # Deuda heredada
            estado_label = QLabel("DEUDA PENDIENTE")
            if self.is_dark:
                estado_label.setStyleSheet("font-size: 18px; color: #fcd34d; font-weight: 700;")
            else:
                estado_label.setStyleSheet("font-size: 18px; color: #a16207; font-weight: 700;")
        
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
            self._agregar_linea_info(layout, "Método de pago:", self.cuota.metodo_pago, metodo_pago=self.cuota.metodo_pago)
            self._agregar_linea_info(layout, "Fecha de pago:", self.cuota.fecha_registro[:16] if self.cuota.fecha_registro else "N/A")
            self._agregar_linea_info(layout, "Monto pagado:", f"${monto_pagado:,.0f}")
        
        self._agregar_linea_info(layout, "Deuda restante:", f"${deuda_restante:,.0f}", True)
        
        if self.cuota.fecha_inicio_mora:
            self._agregar_linea_info(layout, "Mora desde:", self.cuota.fecha_inicio_mora[:10])
    
    def _mostrar_info_impago(self, layout: QVBoxLayout):
        """Muestra información para cuota impaga"""
        estado_label = QLabel("IMPAGO")
        if self.is_dark:
            estado_label.setStyleSheet("font-size: 18px; color: #fca5a5; font-weight: 700;")
        else:
            estado_label.setStyleSheet("font-size: 18px; color: #b91c1c; font-weight: 700;")
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
        
        dialog = ConfirmacionDialog(
            self,
            "Confirmar Eliminación",
            f"¿Está seguro de eliminar el registro de {meses[self.mes - 1]} {self.año}?\n\n"
            f"Cliente: {self.cliente.nombre}\n"
            f"Estado: {self.cuota.estado.upper()}\n\n"
            f"Esta acción no se puede deshacer.",
            tipo="question"
        )
        
        if dialog.exec() == QDialog.DialogCode.Accepted:
            CuotaMensual.eliminar(self.cuota.id)
            
            success_dialog = ConfirmacionDialog(
                self,
                "Eliminado",
                "Registro eliminado correctamente.",
                tipo="success"
            )
            success_dialog.exec()
            self.accept()
