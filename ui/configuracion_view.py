"""
Vista de configuración
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QPushButton,
                             QHBoxLayout, QTableWidget,
                             QTableWidgetItem, QDialog, QFormLayout, QLineEdit,
                             QHeaderView, QTabWidget, QCheckBox, QFrame, QSpinBox, QSizePolicy, QFileDialog)
from PyQt6.QtCore import Qt
from database.models import MetodoPago
from controllers.config_controller import ConfigController
from controllers.reporte_controller import ReporteController


class ConfiguracionView(QWidget):
    """Vista de configuración del sistema"""
    
    def __init__(self):
        super().__init__()
        self.config_controller = ConfigController()
        self.reporte_controller = ReporteController()
        self._init_ui()
    
    def _init_ui(self):
        """Inicializa la interfaz"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)
        
        # Header con título y botón salir
        header_layout = QHBoxLayout()
        
        title = QLabel("Configuración")
        title.setObjectName("pageTitle")
        header_layout.addWidget(title)
        header_layout.addStretch()
        
        # Botón reiniciar
        btn_reiniciar = QPushButton("Reiniciar")
        btn_reiniciar.setStyleSheet("""
            QPushButton {
                background: rgba(59, 130, 246, 0.3);
                border: 1px solid rgba(59, 130, 246, 0.5);
                border-radius: 8px;
                color: #3b82f6;
                font-size: 14px;
                font-weight: bold;
                padding: 10px 20px;
            }
            QPushButton:hover {
                background: rgba(59, 130, 246, 0.5);
                border: 1px solid rgba(59, 130, 246, 0.7);
            }
        """)
        btn_reiniciar.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_reiniciar.clicked.connect(self._reiniciar_app)
        header_layout.addWidget(btn_reiniciar)
        
        # Botón salir
        btn_salir = QPushButton("Salir")
        btn_salir.setStyleSheet("""
            QPushButton {
                background: rgba(239, 68, 68, 0.3);
                border: 1px solid rgba(239, 68, 68, 0.5);
                border-radius: 8px;
                color: #ef4444;
                font-size: 14px;
                font-weight: bold;
                padding: 10px 20px;
            }
            QPushButton:hover {
                background: rgba(239, 68, 68, 0.5);
                border: 1px solid rgba(239, 68, 68, 0.7);
            }
        """)
        btn_salir.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_salir.clicked.connect(self._salir_programa)
        header_layout.addWidget(btn_salir)
        
        layout.addLayout(header_layout)
        
        # Tabs para diferentes secciones
        tabs = QTabWidget()
        
        # Tab de información general
        info_tab = self._crear_tab_info()
        tabs.addTab(info_tab, "General")
        
        # Tab de configuración de pagos
        pagos_tab = self._crear_tab_pagos()
        tabs.addTab(pagos_tab, "Configuracion para Pagos")
        
        layout.addWidget(tabs)
    
    def _crear_tab_info(self) -> QWidget:
        """Crea el tab de información general"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)
        
        # Configuración de pantalla completa
        fullscreen_layout = QVBoxLayout()
        fullscreen_layout.setSpacing(10)
        
        fullscreen_label = QLabel("● Pantalla")
        fullscreen_label.setStyleSheet("font-size: 19px; font-weight: bold; margin-top: 20px;")
        fullscreen_layout.addWidget(fullscreen_label)
        
        self.checkbox_fullscreen = QCheckBox("Pantalla Completa")
        self.checkbox_fullscreen.setChecked(True)  # Por defecto está activado
        self.checkbox_fullscreen.setStyleSheet("font-size: 17px; padding: 5px;")
        self.checkbox_fullscreen.setCursor(Qt.CursorShape.PointingHandCursor)
        self.checkbox_fullscreen.stateChanged.connect(self._toggle_fullscreen)
        fullscreen_layout.addWidget(self.checkbox_fullscreen)
        
        layout.addLayout(fullscreen_layout)
        
        # Sección de respaldos y exportaciones
        backup_title = QLabel("● Respaldos y Exportaciones")
        backup_title.setStyleSheet("font-size: 18px; font-weight: 600; margin-top: 30px; margin-bottom: 15px; color: #cbd5e1;")
        layout.addWidget(backup_title)
        
        # Botón de crear respaldo
        btn_backup = QPushButton("    •  Crear Respaldo de Base de Datos")
        btn_backup.setMinimumHeight(40)
        btn_backup.setMaximumWidth(400)
        btn_backup.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_backup.setStyleSheet("""
            QPushButton {
                background: transparent;
                color: #cbd5e1;
                border: none;
                border-radius: 6px;
                font-size: 16px;
                font-weight: 500;
                padding-left: 0px;
                text-align: left;
            }
            QPushButton:hover {
                color: #e2e8f0;
            }
        """)
        btn_backup.clicked.connect(self._create_backup)
        layout.addWidget(btn_backup, alignment=Qt.AlignmentFlag.AlignLeft)
        
        # Botones de exportación
        btn_export_clientes = QPushButton("    •  Exportar Lista de Clientes")
        btn_export_clientes.setMinimumHeight(40)
        btn_export_clientes.setMaximumWidth(400)
        btn_export_clientes.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_export_clientes.setStyleSheet("""
            QPushButton {
                background: transparent;
                color: #cbd5e1;
                border: none;
                border-radius: 6px;
                font-size: 16px;
                font-weight: 500;
                padding-left: 0px;
                text-align: left;
            }
            QPushButton:hover {
                color: #e2e8f0;
            }
        """)
        btn_export_clientes.clicked.connect(self._export_clientes)
        layout.addWidget(btn_export_clientes, alignment=Qt.AlignmentFlag.AlignLeft)
        
        btn_export_pagos = QPushButton("    •  Exportar Historial de Pagos")
        btn_export_pagos.setMinimumHeight(40)
        btn_export_pagos.setMaximumWidth(400)
        btn_export_pagos.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_export_pagos.setStyleSheet("""
            QPushButton {
                background: transparent;
                color: #cbd5e1;
                border: none;
                border-radius: 6px;
                font-size: 16px;
                font-weight: 500;
                padding-left: 0px;
                text-align: left;
            }
            QPushButton:hover {
                color: #e2e8f0;
            }
        """)
        btn_export_pagos.clicked.connect(self._export_pagos)
        layout.addWidget(btn_export_pagos, alignment=Qt.AlignmentFlag.AlignLeft)
        
        btn_export_mora = QPushButton("    •  Exportar Clientes en Mora")
        btn_export_mora.setMinimumHeight(40)
        btn_export_mora.setMaximumWidth(400)
        btn_export_mora.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_export_mora.setStyleSheet("""
            QPushButton {
                background: transparent;
                color: #cbd5e1;
                border: none;
                border-radius: 6px;
                font-size: 16px;
                font-weight: 500;
                padding-left: 0px;
                text-align: left;
            }
            QPushButton:hover {
                color: #e2e8f0;
            }
        """)
        btn_export_mora.clicked.connect(self._export_mora)
        layout.addWidget(btn_export_mora, alignment=Qt.AlignmentFlag.AlignLeft)
        
        # Sección de mantenimiento
        maintenance_header = QHBoxLayout()
        maintenance_header.setSpacing(15)
        
        maintenance_title = QLabel("● Mantenimiento")
        maintenance_title.setStyleSheet("font-size: 18px; font-weight: 600; margin-top: 30px; color: #cbd5e1;")
        maintenance_header.addWidget(maintenance_title)
        
        maintenance_desc = QLabel("Herramientas para corregir problemas en la base de datos")
        maintenance_desc.setStyleSheet("font-size: 14px; color: #64748b; margin-top: 30px;")
        maintenance_header.addWidget(maintenance_desc)
        maintenance_header.addStretch()
        
        layout.addLayout(maintenance_header)
        layout.addSpacing(10)
        
        btn_clean_duplicates = QPushButton("    •  Limpiar Pagos Duplicados")
        btn_clean_duplicates.setMinimumHeight(40)
        btn_clean_duplicates.setMaximumWidth(400)
        btn_clean_duplicates.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_clean_duplicates.setStyleSheet("""
            QPushButton {
                background: transparent;
                color: #fbbf24;
                border: none;
                border-radius: 6px;
                font-size: 16px;
                font-weight: 500;
                padding-left: 0px;
                text-align: left;
            }
            QPushButton:hover {
                color: #fcd34d;
            }
        """)
        btn_clean_duplicates.clicked.connect(self._limpiar_duplicados)
        layout.addWidget(btn_clean_duplicates, alignment=Qt.AlignmentFlag.AlignLeft)
        
        # Sección peligrosa - Reiniciar DB
        danger_header = QHBoxLayout()
        danger_header.setSpacing(15)
        
        danger_title = QLabel("● Zona Peligrosa")
        danger_title.setStyleSheet("font-size: 18px; font-weight: 600; margin-top: 30px; color: #ef4444;")
        danger_header.addWidget(danger_title)
        
        danger_desc = QLabel("⚠️ Las acciones en esta sección son irreversibles")
        danger_desc.setStyleSheet("font-size: 14px; color: #ef4444; margin-top: 30px;")
        danger_header.addWidget(danger_desc)
        danger_header.addStretch()
        
        layout.addLayout(danger_header)
        layout.addSpacing(10)
        
        btn_reset_db = QPushButton("    •  Reiniciar Base de Datos")
        btn_reset_db.setMinimumHeight(40)
        btn_reset_db.setMaximumWidth(400)
        btn_reset_db.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_reset_db.setStyleSheet("""
            QPushButton {
                background: transparent;
                color: #ef4444;
                border: none;
                border-radius: 6px;
                font-size: 16px;
                font-weight: 500;
                padding-left: 0px;
                text-align: left;
            }
            QPushButton:hover {
                color: #f87171;
            }
        """)
        btn_reset_db.clicked.connect(self._reset_database)
        layout.addWidget(btn_reset_db, alignment=Qt.AlignmentFlag.AlignLeft)
        
        layout.addStretch()
        
        # Información de la aplicación (al final, izquierda, sin contenedor visible)
        info_layout = QHBoxLayout()
        
        info_content = QVBoxLayout()
        info_content.setSpacing(6)
        
        # Nombre de la aplicación
        app_name = QLabel("GesMonth")
        app_name.setStyleSheet("font-size: 20px; font-weight: bold; color: #94a3b8;")
        app_name.setAlignment(Qt.AlignmentFlag.AlignLeft)
        info_content.addWidget(app_name)
        
        # Descripción
        description = QLabel("Sistema para gestión de cuotas mensuales")
        description.setStyleSheet("font-size: 11px; color: #94a3b8;")
        description.setAlignment(Qt.AlignmentFlag.AlignLeft)
        info_content.addWidget(description)
        
        # Versión y desarrollador en layout horizontal
        details_layout = QHBoxLayout()
        details_layout.setSpacing(15)
        
        version = QLabel("v1.0.1")
        version.setStyleSheet("font-size: 10px; color: #94a3b8;")
        details_layout.addWidget(version)
        
        developer = QLabel("By: Dilan Acuña")
        developer.setStyleSheet("font-size: 10px; color: #94a3b8;")
        details_layout.addWidget(developer)
        
        info_content.addLayout(details_layout)
        
        info_layout.addLayout(info_content)
        info_layout.addStretch()
        
        layout.addLayout(info_layout)
        
        return widget
    
    def _crear_tab_pagos(self) -> QWidget:
        """Crea el tab de configuración de pagos"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(25)
        
        # ===== SECCION 1: AÑOS DE FACTURACION =====
        anos_title = QLabel("Años de Facturacion")
        anos_title.setStyleSheet("font-size: 16px; font-weight: bold; color: #60a5fa;")
        layout.addWidget(anos_title)
        
        anos_desc = QLabel("Seleccione los años que se mostrarán en el control de cuotas")
        anos_desc.setStyleSheet("font-size: 12px; color: #94a3b8;")
        layout.addWidget(anos_desc)
        
        # Selector de años
        anos_layout = QHBoxLayout()
        anos_layout.setSpacing(15)
        
        # Año inicial
        label_inicio = QLabel("Primer Año:")
        label_inicio.setStyleSheet("font-size: 13px;")
        anos_layout.addWidget(label_inicio)
        
        self.spin_ano_inicio = QSpinBox()
        self.spin_ano_inicio.setMinimum(2020)
        self.spin_ano_inicio.setMaximum(2050)
        self.spin_ano_inicio.setValue(2025)
        self.spin_ano_inicio.setMinimumHeight(40)
        self.spin_ano_inicio.setMinimumWidth(100)
        self.spin_ano_inicio.setStyleSheet("font-size: 14px; padding: 5px;")
        anos_layout.addWidget(self.spin_ano_inicio)
        
        # Año final
        label_fin = QLabel("Segundo Año:")
        label_fin.setStyleSheet("font-size: 13px;")
        anos_layout.addWidget(label_fin)
        
        self.spin_ano_fin = QSpinBox()
        self.spin_ano_fin.setMinimum(2020)
        self.spin_ano_fin.setMaximum(2050)
        self.spin_ano_fin.setValue(2026)
        self.spin_ano_fin.setMinimumHeight(40)
        self.spin_ano_fin.setMinimumWidth(100)
        self.spin_ano_fin.setStyleSheet("font-size: 14px; padding: 5px;")
        anos_layout.addWidget(self.spin_ano_fin)
        
        anos_layout.addStretch()
        
        btn_guardar_anos = QPushButton("Guardar Años")
        btn_guardar_anos.setObjectName("primaryButton")
        btn_guardar_anos.setMinimumHeight(40)
        btn_guardar_anos.setMinimumWidth(130)
        btn_guardar_anos.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_guardar_anos.clicked.connect(self._guardar_anos)
        anos_layout.addWidget(btn_guardar_anos)
        
        layout.addLayout(anos_layout)
        
        # Cargar años actuales
        anos_list = self.config_controller.get_billing_years()
        if len(anos_list) >= 1:
            self.spin_ano_inicio.setValue(anos_list[0])
        if len(anos_list) >= 2:
            self.spin_ano_fin.setValue(anos_list[1])
        
        # Separador visual
        layout.addSpacing(20)
        separador = QLabel("")
        separador.setStyleSheet("border-top: 1px solid rgba(148, 163, 184, 0.2);")
        separador.setMaximumHeight(1)
        layout.addWidget(separador)
        layout.addSpacing(20)
        
        # ===== SECCION 2: METODOS DE PAGO =====
        metodos_header = QHBoxLayout()
        
        metodos_title = QLabel("Metodos de Pago")
        metodos_title.setStyleSheet("font-size: 16px; font-weight: bold; color: #60a5fa;")
        metodos_header.addWidget(metodos_title)
        metodos_header.addStretch()
        
        btn_add = QPushButton("Agregar Metodo")
        btn_add.setObjectName("primaryButton")
        btn_add.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_add.clicked.connect(self._agregar_metodo_pago)
        metodos_header.addWidget(btn_add)
        
        layout.addLayout(metodos_header)
        
        # Tabla de métodos de pago
        self.tabla_metodos = QTableWidget()
        self.tabla_metodos.setColumnCount(2)
        self.tabla_metodos.setHorizontalHeaderLabels(['Metodo de Pago', 'Acciones'])
        
        header = self.tabla_metodos.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)  # Metodo de Pago
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Fixed)  # Acciones
        
        self.tabla_metodos.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.tabla_metodos.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.tabla_metodos.setAlternatingRowColors(True)
        self.tabla_metodos.verticalHeader().setVisible(False)
        self.tabla_metodos.setColumnWidth(1, 90)
        
        layout.addWidget(self.tabla_metodos)
        
        # Cargar datos
        self._cargar_metodos_pago()
        
        return widget
    
    def _guardar_anos(self):
        """Guarda los años de facturacion"""
        ano_1 = self.spin_ano_inicio.value()
        ano_2 = self.spin_ano_fin.value()
        
        # Guardar los 2 años específicos (ordenados)
        try:
            anos_formatted = self.config_controller.set_billing_years(ano_1, ano_2)
            dialog = ConfirmacionDialog(
                self,
                "Éxito",
                f"Anos actualizados: {anos_formatted}\n\nActualice la vista de Cuotas para ver los cambios.",
                tipo="success"
            )
            dialog.exec()
        except Exception as e:
            dialog = ConfirmacionDialog(
                self,
                "Error",
                f"No se pudo guardar: {str(e)}",
                tipo="error"
            )
            dialog.exec()
    
    def _cargar_metodos_pago(self):
        """Carga los métodos de pago en la tabla"""
        metodos = MetodoPago.obtener_todos()
        self.tabla_metodos.setRowCount(len(metodos))
        
        for row, metodo in enumerate(metodos):
            self.tabla_metodos.setItem(row, 0, QTableWidgetItem(metodo.nombre))
            
            # Botones de acción con iconos compactos
            actions_widget = QWidget()
            actions_layout = QHBoxLayout(actions_widget)
            actions_layout.setContentsMargins(0, 0, 0, 0)
            actions_layout.setSpacing(6)
            actions_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
            
            # Botón Editar (icono)
            btn_edit = QPushButton("✏️")
            btn_edit.setFixedSize(26, 26)
            btn_edit.setToolTip("Editar método de pago")
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
            btn_edit.clicked.connect(lambda checked, m=metodo: self._editar_metodo_pago(m))
            
            # Botón Eliminar (icono)
            btn_delete = QPushButton("🗑️")
            btn_delete.setFixedSize(26, 26)
            btn_delete.setToolTip("Eliminar método de pago")
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
            btn_delete.clicked.connect(lambda checked, mid=metodo.id: self._eliminar_metodo_pago(mid))
            
            actions_layout.addWidget(btn_edit)
            actions_layout.addWidget(btn_delete)
            
            self.tabla_metodos.setCellWidget(row, 1, actions_widget)
            self.tabla_metodos.setRowHeight(row, 58)
    
    def _agregar_metodo_pago(self):
        """Muestra el diálogo para agregar método de pago"""
        dialog = MetodoPagoDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            nombre = dialog.get_nombre()
            if nombre:
                try:
                    MetodoPago.crear(nombre)
                    dialog_success = ConfirmacionDialog(
                        self,
                        "Éxito",
                        "Método de pago agregado correctamente",
                        tipo="success"
                    )
                    dialog_success.exec()
                    self._cargar_metodos_pago()
                except Exception as e:
                    dialog_error = ConfirmacionDialog(
                        self,
                        "Error",
                        f"No se pudo agregar el método: {str(e)}",
                        tipo="error"
                    )
                    dialog_error.exec()
    
    def _editar_metodo_pago(self, metodo: MetodoPago):
        """Muestra el diálogo para editar método de pago"""
        dialog = MetodoPagoDialog(self, metodo)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            nombre = dialog.get_nombre()
            if nombre:
                try:
                    MetodoPago.actualizar(metodo.id, nombre, True)
                    dialog_success = ConfirmacionDialog(
                        self,
                        "Éxito",
                        "Método de pago actualizado correctamente",
                        tipo="success"
                    )
                    dialog_success.exec()
                    self._cargar_metodos_pago()
                except Exception as e:
                    dialog_error = ConfirmacionDialog(
                        self,
                        "Error",
                        f"No se pudo actualizar el método: {str(e)}",
                        tipo="error"
                    )
                    dialog_error.exec()
    
    def _eliminar_metodo_pago(self, metodo_id: int):
        """Elimina un método de pago"""
        dialog = ConfirmacionDialog(
            self,
            "Confirmar eliminación",
            "¿Está seguro de eliminar este método de pago?",
            tipo="question"
        )
        
        if dialog.exec() == QDialog.DialogCode.Accepted:
            try:
                MetodoPago.eliminar(metodo_id)
                dialog_success = ConfirmacionDialog(
                    self,
                    "Éxito",
                    "Método de pago eliminado correctamente",
                    tipo="success"
                )
                dialog_success.exec()
                self._cargar_metodos_pago()
            except Exception as e:
                dialog_error = ConfirmacionDialog(
                    self,
                    "Error",
                    f"No se pudo eliminar el método: {str(e)}",
                    tipo="error"
                )
                dialog_error.exec()
    
    def _toggle_fullscreen(self, state):
        """Alterna el modo de pantalla completa"""
        main_window = self.window()
        if hasattr(main_window, 'toggle_fullscreen'):
            main_window.toggle_fullscreen(state == Qt.CheckState.Checked.value)
    
    def _reiniciar_app(self):
        """Reinicia la aplicación"""
        dialog = ConfirmacionDialog(
            self,
            "Reiniciar Aplicación",
            "¿Desea reiniciar la aplicación?\n\nSe cerrará y volverá a iniciar automáticamente.",
            tipo="question"
        )
        
        if dialog.exec() == QDialog.DialogCode.Accepted:
            import sys
            import os
            from PyQt6.QtWidgets import QApplication
            
            # Guardar los argumentos del programa
            python = sys.executable
            script = sys.argv[0]
            
            # Cerrar la aplicación actual
            QApplication.quit()
            
            # Reiniciar con el mismo script
            os.execl(python, python, script)
    
    def _salir_programa(self):
        """Cierra el programa completamente"""
        dialog = ConfirmacionDialog(
            self,
            "Salir",
            "¿Está seguro que desea salir del programa?",
            tipo="question"
        )
        
        if dialog.exec() == QDialog.DialogCode.Accepted:
            from PyQt6.QtWidgets import QApplication
            QApplication.quit()
    
    def _create_backup(self):
        """Crea un respaldo de la base de datos"""
        try:
            backup_path = self.config_controller.create_backup()
            dialog = ConfirmacionDialog(
                self,
                "Éxito",
                f"Respaldo creado exitosamente:\n{backup_path}",
                tipo="success"
            )
            dialog.exec()
        except Exception as e:
            dialog = ConfirmacionDialog(
                self,
                "Error",
                f"No se pudo crear el respaldo:\n{str(e)}",
                tipo="error"
            )
            dialog.exec()
    
    def _export_clientes(self):
        """Exporta la lista de clientes"""
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Guardar reporte",
            "reporte_clientes.xlsx",
            "Excel Files (*.xlsx)"
        )
        
        if file_path:
            if self.reporte_controller.exportar_clientes(file_path):
                dialog = ConfirmacionDialog(
                    self,
                    "Éxito",
                    f"Reporte guardado en:\n{file_path}",
                    tipo="success"
                )
                dialog.exec()
            else:
                dialog = ConfirmacionDialog(
                    self,
                    "Error",
                    "No se pudo generar el reporte",
                    tipo="error"
                )
                dialog.exec()
    
    def _export_pagos(self):
        """Exporta el historial de pagos"""
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Guardar reporte",
            "reporte_pagos.xlsx",
            "Excel Files (*.xlsx)"
        )
        
        if file_path:
            if self.reporte_controller.exportar_pagos(file_path):
                dialog = ConfirmacionDialog(
                    self,
                    "Éxito",
                    f"Reporte guardado en:\n{file_path}",
                    tipo="success"
                )
                dialog.exec()
            else:
                dialog = ConfirmacionDialog(
                    self,
                    "Error",
                    "No se pudo generar el reporte",
                    tipo="error"
                )
                dialog.exec()
    
    def _export_mora(self):
        """Exporta clientes en mora"""
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Guardar reporte",
            "reporte_mora.xlsx",
            "Excel Files (*.xlsx)"
        )
        
        if file_path:
            if self.reporte_controller.exportar_mora(file_path):
                dialog = ConfirmacionDialog(
                    self,
                    "Éxito",
                    f"Reporte guardado en:\n{file_path}",
                    tipo="success"
                )
                dialog.exec()
            else:
                dialog = ConfirmacionDialog(
                    self,
                    "Error",
                    "No se pudo generar el reporte",
                    tipo="error"
                )
                dialog.exec()
    
    def _limpiar_duplicados(self):
        """Limpia pagos duplicados de la base de datos"""
        dialog = ConfirmacionDialog(
            self,
            "Limpiar Pagos Duplicados",
            "Esta acción eliminará los pagos duplicados manteniendo solo el primer registro de cada grupo.\n\n"
            "¿Desea continuar?",
            tipo="question"
        )
        
        if dialog.exec() == QDialog.DialogCode.Accepted:
            try:
                from database.models import Pago
                eliminados = Pago.eliminar_duplicados()
                
                dialog_success = ConfirmacionDialog(
                    self,
                    "Éxito",
                    f"Se eliminaron {eliminados} pagos duplicados.\n\n"
                    "Actualice la vista de reportes para ver los cambios.",
                    tipo="success"
                )
                dialog_success.exec()
            except Exception as e:
                dialog_error = ConfirmacionDialog(
                    self,
                    "Error",
                    f"No se pudieron eliminar los duplicados:\n{str(e)}",
                    tipo="error"
                )
                dialog_error.exec()
    
    def _reset_database(self):
        """Reinicia la base de datos con múltiples advertencias"""
        # Primera advertencia
        dialog1 = ConfirmacionDialog(
            self,
            "⚠️ ADVERTENCIA CRÍTICA",
            "Está a punto de ELIMINAR TODA LA INFORMACIÓN de la base de datos.\n\n"
            "Esto incluye:\n"
            "• Todos los clientes registrados\n"
            "• Todo el historial de cuotas\n"
            "• Todos los pagos registrados\n"
            "• Todas las configuraciones personalizadas\n\n"
            "Esta acción NO se puede deshacer.\n\n"
            "¿Está COMPLETAMENTE SEGURO de continuar?",
            tipo="warning"
        )
        
        if dialog1.exec() != QDialog.DialogCode.Accepted:
            return
        
        # Segunda confirmación
        dialog2 = ConfirmacionDialog(
            self,
            "⛔ ÚLTIMA ADVERTENCIA",
            "SE PERDERÁN TODOS LOS DATOS PERMANENTEMENTE.\n\n"
            "Le recomendamos crear un respaldo antes de continuar.\n\n"
            "¿Desea crear un respaldo ahora?",
            tipo="question"
        )
        
        if dialog2.exec() == QDialog.DialogCode.Accepted:
            # Usuario quiere crear respaldo primero
            try:
                backup_path = self.config_controller.create_backup()
                dialog_backup = ConfirmacionDialog(
                    self,
                    "Respaldo Creado",
                    f"Respaldo guardado en:\n{backup_path}\n\n"
                    "¿Desea continuar con el reinicio de la base de datos?",
                    tipo="question"
                )
                if dialog_backup.exec() != QDialog.DialogCode.Accepted:
                    return
            except Exception as e:
                dialog_error = ConfirmacionDialog(
                    self,
                    "Error al Crear Respaldo",
                    f"No se pudo crear el respaldo:\n{str(e)}\n\n"
                    "¿Desea continuar de todas formas?",
                    tipo="error"
                )
                if dialog_error.exec() != QDialog.DialogCode.Accepted:
                    return
        
        # Confirmación final con texto de verificación
        dialog3 = ConfirmacionDialog(
            self,
            "🔴 CONFIRMACIÓN FINAL",
            "Para confirmar el reinicio de la base de datos,\n"
            "debe estar absolutamente seguro.\n\n"
            "Se eliminarán TODOS los datos del sistema.\n\n"
            "Esta es su última oportunidad para cancelar.",
            tipo="error"
        )
        
        if dialog3.exec() == QDialog.DialogCode.Accepted:
            try:
                # Reiniciar la base de datos
                import os
                import sys
                from database.connection import DatabaseConnection
                
                db = DatabaseConnection()
                db_path = db._db_path  # Acceder al atributo privado
                
                # Cerrar conexión
                if db._connection:
                    db._connection.close()
                    DatabaseConnection._connection = None
                    DatabaseConnection._instance = None
                
                # Eliminar archivo de base de datos
                if os.path.exists(db_path):
                    os.remove(db_path)
                
                # Reinicializar
                DatabaseConnection._instance = None
                db = DatabaseConnection()
                
                dialog_success = ConfirmacionDialog(
                    self,
                    "Base de Datos Reiniciada",
                    "La base de datos ha sido reiniciada exitosamente.\n\n"
                    "El sistema se reiniciará ahora.",
                    tipo="success"
                )
                dialog_success.exec()
                
                # Reiniciar la aplicación
                from PyQt6.QtWidgets import QApplication
                QApplication.quit()
                os.execl(sys.executable, sys.executable, *sys.argv)
                
            except Exception as e:
                dialog_error = ConfirmacionDialog(
                    self,
                    "Error Crítico",
                    f"Error al reiniciar la base de datos:\n{str(e)}",
                    tipo="error"
                )
                dialog_error.exec()


class ConfirmacionDialog(QDialog):
    """Diálogo de confirmación personalizado con estilo consistente"""
    
    def __init__(self, parent, titulo: str, mensaje: str, tipo: str = "info"):
        super().__init__(parent)
        self.titulo = titulo
        self.mensaje = mensaje
        self.tipo = tipo  # "success", "error", "warning", "question", "info"
        self.setWindowTitle(titulo)
        self.setMinimumWidth(450)
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


class MetodoPagoDialog(QDialog):
    """Diálogo para agregar/editar métodos de pago"""
    
    def __init__(self, parent=None, metodo: MetodoPago = None):
        super().__init__(parent)
        self.metodo = metodo
        self.setWindowTitle("Editar Método de Pago" if metodo else "Agregar Método de Pago")
        self.setMinimumWidth(400)
        self._init_ui()
    
    def _init_ui(self):
        """Inicializa la interfaz del diálogo"""
        layout = QFormLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Campo nombre
        self.input_nombre = QLineEdit()
        self.input_nombre.setPlaceholderText("Ej: Efectivo, Transferencia, Tarjeta...")
        
        if self.metodo:
            self.input_nombre.setText(self.metodo.nombre)
        
        layout.addRow("Nombre del Método:", self.input_nombre)
        
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
            QMessageBox.warning(self, "Error", "El nombre del método es obligatorio")
            return
        
        self.accept()
    
    def get_nombre(self) -> str:
        """Retorna el nombre del método"""
        return self.input_nombre.text().strip()
