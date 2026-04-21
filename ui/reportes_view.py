"""
Vista de reportes y estadísticas
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QFrame, QGridLayout, QScrollArea, QSizePolicy, QComboBox)
from PyQt6.QtCore import Qt, QDateTime
from .responsive import UIScale
from database.models import CuotaMensual, MetodoPago


class ReportesView(QWidget):
    """Vista para visualizar reportes y estadísticas"""
    
    def __init__(self):
        super().__init__()
        self.año_seleccionado = QDateTime.currentDateTime().date().year()
        self.mes_seleccionado = QDateTime.currentDateTime().date().month()
        self.selector_frame = None
        self.container_cuotas = None
        self.container_metodos = None
        self._init_ui()
    
    def showEvent(self, event):
        """Se ejecuta cuando la vista se muestra"""
        super().showEvent(event)
        self._actualizar_estilos_contenedores()
        self._actualizar_estadisticas()
    
    def _actualizar_estilos_contenedores(self):
        """Actualiza los estilos de todos los contenedores según el tema actual"""
        # Detectar tema actual
        main_window = self.window()
        is_dark = True
        if hasattr(main_window, 'current_theme'):
            is_dark = main_window.current_theme == 'dark'
        
        # Actualizar selector de fecha
        if self.selector_frame:
            if is_dark:
                self.selector_frame.setStyleSheet("""
                    QFrame {
                        background: rgba(30, 41, 59, 0.5);
                        border: 1px solid rgba(71, 85, 105, 0.5);
                        border-radius: 12px;
                    }
                    QLabel {
                        border: none;
                        background: transparent;
                    }
                """)
            else:
                self.selector_frame.setStyleSheet("""
                    QFrame {
                        background: rgba(255, 255, 255, 0.95);
                        border: 2px solid rgba(148, 163, 184, 0.3);
                        border-radius: 12px;
                    }
                    QLabel {
                        border: none;
                        background: transparent;
                    }
                """)
            
            # Actualizar label "Período:"
            labels = self.selector_frame.findChildren(QLabel)
            if labels:
                for label in labels:
                    if is_dark:
                        label.setStyleSheet("font-size: 14px; color: #94a3b8; font-weight: 500; border: none;")
                    else:
                        label.setStyleSheet("font-size: 14px; color: #1e293b; font-weight: 700; border: none;")
            
            # Actualizar ComboBox de mes
            if hasattr(self, 'combo_mes') and self.combo_mes:
                if is_dark:
                    self.combo_mes.setStyleSheet("""
                        QComboBox {
                            background: rgba(71, 85, 105, 0.3);
                            border: 1px solid rgba(71, 85, 105, 0.5);
                            border-radius: 6px;
                            padding: 8px 12px;
                            color: #cbd5e1;
                            font-size: 14px;
                        }
                        QComboBox:hover {
                            background: rgba(71, 85, 105, 0.4);
                        }
                        QComboBox::drop-down {
                            border: none;
                        }
                        QComboBox::down-arrow {
                            image: none;
                            border-left: 4px solid transparent;
                            border-right: 4px solid transparent;
                            border-top: 6px solid #cbd5e1;
                            margin-right: 8px;
                        }
                    """)
                else:
                    self.combo_mes.setStyleSheet("""
                        QComboBox {
                            background: rgba(255, 255, 255, 0.9);
                            border: 2px solid rgba(148, 163, 184, 0.4);
                            border-radius: 6px;
                            padding: 8px 12px;
                            color: #0f172a;
                            font-size: 14px;
                            font-weight: 600;
                        }
                        QComboBox:hover {
                            background: rgba(248, 250, 252, 1);
                            border: 2px solid rgba(148, 163, 184, 0.6);
                        }
                        QComboBox::drop-down {
                            border: none;
                        }
                        QComboBox::down-arrow {
                            image: none;
                            border-left: 4px solid transparent;
                            border-right: 4px solid transparent;
                            border-top: 6px solid #475569;
                            margin-right: 8px;
                        }
                    """)
            
            # Actualizar ComboBox de año
            if hasattr(self, 'combo_año') and self.combo_año:
                if is_dark:
                    self.combo_año.setStyleSheet("""
                        QComboBox {
                            background: rgba(71, 85, 105, 0.3);
                            border: 1px solid rgba(71, 85, 105, 0.5);
                            border-radius: 6px;
                            padding: 8px 12px;
                            color: #cbd5e1;
                            font-size: 14px;
                        }
                        QComboBox:hover {
                            background: rgba(71, 85, 105, 0.4);
                        }
                        QComboBox::drop-down {
                            border: none;
                        }
                        QComboBox::down-arrow {
                            image: none;
                            border-left: 4px solid transparent;
                            border-right: 4px solid transparent;
                            border-top: 6px solid #cbd5e1;
                            margin-right: 8px;
                        }
                    """)
                else:
                    self.combo_año.setStyleSheet("""
                        QComboBox {
                            background: rgba(255, 255, 255, 0.9);
                            border: 2px solid rgba(148, 163, 184, 0.4);
                            border-radius: 6px;
                            padding: 8px 12px;
                            color: #0f172a;
                            font-size: 14px;
                            font-weight: 600;
                        }
                        QComboBox:hover {
                            background: rgba(248, 250, 252, 1);
                            border: 2px solid rgba(148, 163, 184, 0.6);
                        }
                        QComboBox::drop-down {
                            border: none;
                        }
                        QComboBox::down-arrow {
                            image: none;
                            border-left: 4px solid transparent;
                            border-right: 4px solid transparent;
                            border-top: 6px solid #475569;
                            margin-right: 8px;
                        }
                    """)
        
        # Actualizar contenedor de cuotas
        if self.container_cuotas:
            if is_dark:
                self.container_cuotas.setStyleSheet("""
                    QFrame {
                        background: rgba(30, 41, 59, 0.5);
                        border: 1px solid rgba(71, 85, 105, 0.5);
                        border-radius: 12px;
                    }
                    QLabel {
                        border: none;
                        background: transparent;
                    }
                """)
            else:
                self.container_cuotas.setStyleSheet("""
                    QFrame {
                        background: rgba(255, 255, 255, 0.95);
                        border: 2px solid rgba(148, 163, 184, 0.3);
                        border-radius: 12px;
                    }
                    QLabel {
                        border: none;
                        background: transparent;
                    }
                """)
            
            # Actualizar título de sección
            section_labels = self.container_cuotas.findChildren(QLabel)
            if section_labels:
                title_label = section_labels[0]
                if is_dark:
                    title_label.setStyleSheet("font-size: 18px; font-weight: 700; color: #e0e7ff; border: none;")
                else:
                    title_label.setStyleSheet("font-size: 18px; font-weight: 700; color: #0f172a; border: none;")
        
        # Actualizar contenedor de métodos de pago
        if self.container_metodos:
            if is_dark:
                self.container_metodos.setStyleSheet("""
                    QFrame {
                        background: rgba(30, 41, 59, 0.5);
                        border: 1px solid rgba(71, 85, 105, 0.5);
                        border-radius: 12px;
                    }
                    QLabel {
                        border: none;
                        background: transparent;
                    }
                """)
            else:
                self.container_metodos.setStyleSheet("""
                    QFrame {
                        background: rgba(255, 255, 255, 0.95);
                        border: 2px solid rgba(148, 163, 184, 0.3);
                        border-radius: 12px;
                    }
                    QLabel {
                        border: none;
                        background: transparent;
                    }
                """)
            
            # Actualizar título de sección
            section_labels = self.container_metodos.findChildren(QLabel)
            if section_labels:
                title_label = section_labels[0]
                if is_dark:
                    title_label.setStyleSheet("font-size: 18px; font-weight: 700; color: #e0e7ff; border: none;")
                else:
                    title_label.setStyleSheet("font-size: 18px; font-weight: 700; color: #0f172a; border: none;")
        
        # Actualizar tarjetas de estadísticas
        if hasattr(self, 'stat_total_cuotas') and self.stat_total_cuotas:
            for stat_card in [self.stat_total_cuotas, self.stat_cuotas_pagadas, 
                             self.stat_cuotas_impago, self.stat_cuotas_deuda]:
                if stat_card:
                    if is_dark:
                        stat_card.setStyleSheet("""
                            QFrame {
                                background: rgba(30, 41, 59, 0.5);
                                border: 1px solid rgba(71, 85, 105, 0.5);
                                border-radius: 12px;
                            }
                            QLabel {
                                border: none;
                                background: transparent;
                            }
                        """)
                    else:
                        stat_card.setStyleSheet("""
                            QFrame {
                                background: rgba(255, 255, 255, 0.95);
                                border: 2px solid rgba(148, 163, 184, 0.3);
                                border-radius: 12px;
                            }
                            QLabel {
                                border: none;
                                background: transparent;
                            }
                        """)
                    
                    # Actualizar etiqueta de título dentro de la tarjeta
                    labels = stat_card.findChildren(QLabel)
                    if len(labels) >= 2:
                        titulo_label = labels[0]
                        if is_dark:
                            titulo_label.setStyleSheet("font-size: 14px; color: #94a3b8; font-weight: 500; border: none;")
                        else:
                            titulo_label.setStyleSheet("font-size: 14px; color: #475569; font-weight: 600; border: none;")
    
    def _init_ui(self):
        """Inicializa la interfaz"""
        # Layout principal
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(UIScale.px(0), UIScale.px(0), UIScale.px(0), UIScale.px(0))
        main_layout.setSpacing(UIScale.px(0))
        
        # Scroll area para todo el contenido
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll.setStyleSheet("""
            QScrollArea {
                background: transparent;
                border: none;
            }
        """)
        
        # Widget contenedor del scroll
        scroll_widget = QWidget()
        scroll_widget.setStyleSheet("""
            QWidget {
                background: transparent;
            }
        """)
        scroll_layout = QVBoxLayout(scroll_widget)
        scroll_layout.setContentsMargins(UIScale.px(30), UIScale.px(30), UIScale.px(30), UIScale.px(30))
        scroll_layout.setSpacing(UIScale.px(25))
        
        # Header
        self._crear_header(scroll_layout)
        
        # Selectores de fecha
        self._crear_selectores_fecha(scroll_layout)
        
        # Sección de estadísticas de cuotas
        self._crear_seccion_cuotas(scroll_layout)
        
        # Sección de estadísticas por método de pago
        self._crear_seccion_metodos_pago(scroll_layout)
        
        scroll_layout.addStretch()
        
        scroll.setWidget(scroll_widget)
        main_layout.addWidget(scroll)
    
    def _crear_header(self, layout: QVBoxLayout):
        """Crea el header de la vista"""
        title = QLabel("Reportes y Estadísticas")
        title.setObjectName("pageTitle")
        title.setStyleSheet("border: none;")
        layout.addWidget(title)
    
    def _crear_selectores_fecha(self, layout: QVBoxLayout):
        """Crea los selectores de mes y año"""
        # Detectar tema actual
        main_window = self.window()
        is_dark = True
        if hasattr(main_window, 'current_theme'):
            is_dark = main_window.current_theme == 'dark'
        
        self.selector_frame = QFrame()
        if is_dark:
            self.selector_frame.setStyleSheet("""
                QFrame {
                    background: rgba(30, 41, 59, 0.5);
                    border: 1px solid rgba(71, 85, 105, 0.5);
                    border-radius: 12px;
                }
                QLabel {
                    border: none;
                    background: transparent;
                }
            """)
        else:
            self.selector_frame.setStyleSheet("""
                QFrame {
                    background: rgba(255, 255, 255, 0.95);
                    border: 2px solid rgba(148, 163, 184, 0.3);
                    border-radius: 12px;
                }
                QLabel {
                    border: none;
                    background: transparent;
                }
            """)
        
        selector_layout = QHBoxLayout(self.selector_frame)
        selector_layout.setContentsMargins(UIScale.px(25), UIScale.px(20), UIScale.px(25), UIScale.px(20))
        selector_layout.setSpacing(UIScale.px(20))
        
        # Label
        label = QLabel("Período:")
        if is_dark:
            label.setStyleSheet("font-size: 14px; color: #94a3b8; font-weight: 500; border: none;")
        else:
            label.setStyleSheet("font-size: 14px; color: #1e293b; font-weight: 700; border: none;")
        selector_layout.addWidget(label)
        
        # Selector de mes
        self.combo_mes = QComboBox()
        self.combo_mes.addItem("Todos los meses", 0)
        meses = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
                 "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
        for i, mes in enumerate(meses, 1):
            self.combo_mes.addItem(mes, i)
        
        # Seleccionar mes actual por defecto
        self.combo_mes.setCurrentIndex(self.mes_seleccionado)
        self.combo_mes.setMinimumWidth(UIScale.px(180))
        if is_dark:
            self.combo_mes.setStyleSheet("""
                QComboBox {
                    background: rgba(71, 85, 105, 0.3);
                    border: 1px solid rgba(71, 85, 105, 0.5);
                    border-radius: 6px;
                    padding: 8px 12px;
                    color: #cbd5e1;
                    font-size: 14px;
                }
                QComboBox:hover {
                    background: rgba(71, 85, 105, 0.4);
                }
                QComboBox::drop-down {
                    border: none;
                }
                QComboBox::down-arrow {
                    image: none;
                    border-left: 4px solid transparent;
                    border-right: 4px solid transparent;
                    border-top: 6px solid #cbd5e1;
                    margin-right: 8px;
                }
            """)
        else:
            self.combo_mes.setStyleSheet("""
                QComboBox {
                    background: rgba(255, 255, 255, 0.9);
                    border: 2px solid rgba(148, 163, 184, 0.4);
                    border-radius: 6px;
                    padding: 8px 12px;
                    color: #0f172a;
                    font-size: 14px;
                    font-weight: 600;
                }
                QComboBox:hover {
                    background: rgba(248, 250, 252, 1);
                    border: 2px solid rgba(148, 163, 184, 0.6);
                }
                QComboBox::drop-down {
                    border: none;
                }
                QComboBox::down-arrow {
                    image: none;
                    border-left: 4px solid transparent;
                    border-right: 4px solid transparent;
                    border-top: 6px solid #475569;
                    margin-right: 8px;
                }
            """)
        self.combo_mes.currentIndexChanged.connect(self._on_fecha_changed)
        selector_layout.addWidget(self.combo_mes)
        
        # Selector de año
        self.combo_año = QComboBox()
        self.combo_año.addItem("Todos los años", 0)
        año_actual = QDateTime.currentDateTime().date().year()
        for año in range(año_actual - 5, año_actual + 2):
            self.combo_año.addItem(str(año), año)
        
        # Seleccionar año actual por defecto
        index_año = self.combo_año.findData(año_actual)
        if index_año >= 0:
            self.combo_año.setCurrentIndex(index_año)
        
        self.combo_año.setMinimumWidth(UIScale.px(150))
        if is_dark:
            self.combo_año.setStyleSheet("""
                QComboBox {
                    background: rgba(71, 85, 105, 0.3);
                    border: 1px solid rgba(71, 85, 105, 0.5);
                    border-radius: 6px;
                    padding: 8px 12px;
                    color: #cbd5e1;
                    font-size: 14px;
                }
                QComboBox:hover {
                    background: rgba(71, 85, 105, 0.4);
                }
                QComboBox::drop-down {
                    border: none;
                }
                QComboBox::down-arrow {
                    image: none;
                    border-left: 4px solid transparent;
                    border-right: 4px solid transparent;
                    border-top: 6px solid #cbd5e1;
                    margin-right: 8px;
                }
            """)
        else:
            self.combo_año.setStyleSheet("""
                QComboBox {
                    background: rgba(255, 255, 255, 0.9);
                    border: 2px solid rgba(148, 163, 184, 0.4);
                    border-radius: 6px;
                    padding: 8px 12px;
                    color: #0f172a;
                    font-size: 14px;
                    font-weight: 600;
                }
                QComboBox:hover {
                    background: rgba(248, 250, 252, 1);
                    border: 2px solid rgba(148, 163, 184, 0.6);
                }
                QComboBox::drop-down {
                    border: none;
                }
                QComboBox::down-arrow {
                    image: none;
                    border-left: 4px solid transparent;
                    border-right: 4px solid transparent;
                    border-top: 6px solid #475569;
                    margin-right: 8px;
                }
            """)
        self.combo_año.currentIndexChanged.connect(self._on_fecha_changed)
        selector_layout.addWidget(self.combo_año)
        
        selector_layout.addStretch()
        
        layout.addWidget(self.selector_frame)
    
    def _on_fecha_changed(self):
        """Se ejecuta cuando cambia la selección de fecha"""
        self.mes_seleccionado = self.combo_mes.currentData()
        self.año_seleccionado = self.combo_año.currentData()
        self._actualizar_estadisticas()
    
    def _crear_seccion_cuotas(self, layout: QVBoxLayout):
        """Crea la sección de estadísticas de cuotas"""
        # Detectar tema actual
        main_window = self.window()
        is_dark = True
        if hasattr(main_window, 'current_theme'):
            is_dark = main_window.current_theme == 'dark'
        
        self.container_cuotas = QFrame()
        if is_dark:
            self.container_cuotas.setStyleSheet("""
                QFrame {
                    background: rgba(30, 41, 59, 0.5);
                    border: 1px solid rgba(71, 85, 105, 0.5);
                    border-radius: 12px;
                }
                QLabel {
                    border: none;
                    background: transparent;
                }
            """)
        else:
            self.container_cuotas.setStyleSheet("""
                QFrame {
                    background: rgba(255, 255, 255, 0.95);
                    border: 2px solid rgba(148, 163, 184, 0.3);
                    border-radius: 12px;
                }
                QLabel {
                    border: none;
                    background: transparent;
                }
            """)
        
        container_layout = QVBoxLayout(self.container_cuotas)
        container_layout.setContentsMargins(UIScale.px(25), UIScale.px(25), UIScale.px(25), UIScale.px(25))
        container_layout.setSpacing(UIScale.px(20))
        
        # Título de la sección
        section_title = QLabel("Estadísticas de Cuotas")
        if is_dark:
            section_title.setStyleSheet("font-size: 18px; font-weight: 700; color: #e0e7ff; border: none;")
        else:
            section_title.setStyleSheet("font-size: 18px; font-weight: 700; color: #0f172a; border: none;")
        container_layout.addWidget(section_title)
        
        # Grid de estadísticas
        grid = QGridLayout()
        grid.setSpacing(UIScale.px(20))
        grid.setContentsMargins(UIScale.px(0), UIScale.px(0), UIScale.px(0), UIScale.px(0))
        
        # Crear widgets de estadísticas
        self.stat_total_cuotas = self._crear_stat_card(
            "Total Cuotas Registradas",
            "0",
            "#3b82f6"
        )
        
        self.stat_cuotas_pagadas = self._crear_stat_card(
            "Cantidad en pagos",
            "$0",   
            "#22c55e"
        )
        
        self.stat_cuotas_impago = self._crear_stat_card(
            "Cantidad sin pagar",
            "$0",
            "#ef4444"
        )
        
        self.stat_cuotas_deuda = self._crear_stat_card(
            "Cantidad con deuda",
            "$0",
            "#eab308"
        )
        
        # Agregar al grid (2x2)
        grid.addWidget(self.stat_total_cuotas, 0, 0)
        grid.addWidget(self.stat_cuotas_pagadas, 0, 1)
        grid.addWidget(self.stat_cuotas_impago, 1, 0)
        grid.addWidget(self.stat_cuotas_deuda, 1, 1)
        
        # Hacer que las columnas tengan el mismo ancho
        grid.setColumnStretch(0, 1)
        grid.setColumnStretch(1, 1)
        
        container_layout.addLayout(grid)
        layout.addWidget(self.container_cuotas)
    
    def _crear_seccion_metodos_pago(self, layout: QVBoxLayout):
        """Crea la sección de estadísticas por método de pago"""
        # Detectar tema actual
        main_window = self.window()
        is_dark = True
        if hasattr(main_window, 'current_theme'):
            is_dark = main_window.current_theme == 'dark'
        
        self.container_metodos = QFrame()
        if is_dark:
            self.container_metodos.setStyleSheet("""
                QFrame {
                    background: rgba(30, 41, 59, 0.5);
                    border: 1px solid rgba(71, 85, 105, 0.5);
                    border-radius: 12px;
                }
                QLabel {
                    border: none;
                    background: transparent;
                }
            """)
        else:
            self.container_metodos.setStyleSheet("""
                QFrame {
                    background: rgba(255, 255, 255, 0.95);
                    border: 2px solid rgba(148, 163, 184, 0.3);
                    border-radius: 12px;
                }
                QLabel {
                    border: none;
                    background: transparent;
                }
            """)
        
        container_layout = QVBoxLayout(self.container_metodos)
        container_layout.setContentsMargins(UIScale.px(25), UIScale.px(25), UIScale.px(25), UIScale.px(25))
        container_layout.setSpacing(UIScale.px(20))
        
        # Título de la sección
        section_title = QLabel("Estadísticas por Método de Pago")
        if is_dark:
            section_title.setStyleSheet("font-size: 18px; font-weight: 700; color: #e0e7ff; border: none;")
        else:
            section_title.setStyleSheet("font-size: 18px; font-weight: 700; color: #0f172a; border: none;")
        container_layout.addWidget(section_title)
        
        # Contenedor dinámico para los métodos
        self.metodos_container = QVBoxLayout()
        self.metodos_container.setSpacing(UIScale.px(12))
        self.metodos_container.setContentsMargins(UIScale.px(0), UIScale.px(0), UIScale.px(0), UIScale.px(0))
        container_layout.addLayout(self.metodos_container)
        
        layout.addWidget(self.container_metodos)
    
    def _crear_stat_card(self, titulo: str, valor: str, color: str) -> QFrame:
        """Crea una tarjeta de estadística"""
        # Detectar tema actual
        main_window = self.window()
        is_dark = True
        if hasattr(main_window, 'current_theme'):
            is_dark = main_window.current_theme == 'dark'
        
        card = QFrame()
        card.setMinimumHeight(UIScale.px(130))
        card.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        if is_dark:
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
        else:
            card.setStyleSheet(f"""
                QFrame {{
                    background: rgba(255, 255, 255, 0.95);
                    border: 2px solid rgba(148, 163, 184, 0.3);
                    border-radius: 12px;
                }}
                QLabel {{
                    border: none;
                    background: transparent;
                }}
            """)
        
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(UIScale.px(25), UIScale.px(25), UIScale.px(25), UIScale.px(25))
        card_layout.setSpacing(UIScale.px(15))
        
        # Título
        titulo_label = QLabel(titulo)
        if is_dark:
            titulo_label.setStyleSheet("font-size: 14px; color: #94a3b8; font-weight: 500; border: none;")
        else:
            titulo_label.setStyleSheet("font-size: 14px; color: #475569; font-weight: 600; border: none;")
        titulo_label.setWordWrap(True)
        card_layout.addWidget(titulo_label)
        
        # Valor
        valor_label = QLabel(valor)
        valor_label.setStyleSheet(f"font-size: 36px; color: {color}; font-weight: 700; border: none;")
        valor_label.setObjectName("valor_stat")
        card_layout.addWidget(valor_label)
        
        card_layout.addStretch()
        
        return card
    
    def _crear_fila_metodo(self, nombre: str, cantidad: int, total: float) -> QFrame:
        """Crea una fila para mostrar estadísticas de un método de pago"""
        # Detectar tema actual
        main_window = self.window()
        is_dark = True
        if hasattr(main_window, 'current_theme'):
            is_dark = main_window.current_theme == 'dark'
        
        row = QFrame()
        row.setMinimumHeight(UIScale.px(70))
        row.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        if is_dark:
            row.setStyleSheet("""
                QFrame {
                    background: rgba(30, 41, 59, 0.3);
                    border: 1px solid rgba(71, 85, 105, 0.5);
                    border-radius: 10px;
                }
                QLabel {
                    border: none;
                    background: transparent;
                }
            """)
        else:
            row.setStyleSheet("""
                QFrame {
                    background: rgba(255, 255, 255, 0.9);
                    border: 2px solid rgba(148, 163, 184, 0.3);
                    border-radius: 10px;
                }
                QLabel {
                    border: none;
                    background: transparent;
                }
            """)
        
        row_layout = QHBoxLayout(row)
        row_layout.setContentsMargins(UIScale.px(20), UIScale.px(15), UIScale.px(20), UIScale.px(15))
        row_layout.setSpacing(UIScale.px(15))
        
        # Columna 1: Nombre del método con indicador de color
        nombre_widget = QWidget()
        nombre_layout = QVBoxLayout(nombre_widget)
        nombre_layout.setContentsMargins(UIScale.px(0), UIScale.px(0), UIScale.px(0), UIScale.px(0))
        nombre_layout.setSpacing(UIScale.px(2))
        
        label_metodo = QLabel("Método")
        label_metodo.setStyleSheet("font-size: 11px; color: #64748b;")
        nombre_layout.addWidget(label_metodo)
        
        # Contenedor horizontal para el color + nombre
        nombre_container = QWidget()
        nombre_container_layout = QHBoxLayout(nombre_container)
        nombre_container_layout.setContentsMargins(UIScale.px(0), UIScale.px(0), UIScale.px(0), UIScale.px(0))
        nombre_container_layout.setSpacing(UIScale.px(10))
        
        # Buscar el color del método de pago
        metodos = MetodoPago.obtener_todos()
        color_metodo = "#3b82f6"  # Color por defecto
        for m in metodos:
            if m.nombre == nombre:
                color_metodo = m.color
                break
        
        # Nombre del método con su color
        nombre_label = QLabel(nombre)
        nombre_label.setStyleSheet(f"font-size: 16px; color: {color_metodo}; font-weight: 700;")
        nombre_container_layout.addWidget(nombre_label)
        nombre_container_layout.addStretch()
        
        nombre_layout.addWidget(nombre_container)
        
        row_layout.addWidget(nombre_widget, 2)
        
        # Columna 2: Cantidad de pagos
        cantidad_widget = QWidget()
        cantidad_layout = QVBoxLayout(cantidad_widget)
        cantidad_layout.setContentsMargins(UIScale.px(0), UIScale.px(0), UIScale.px(0), UIScale.px(0))
        cantidad_layout.setSpacing(UIScale.px(2))
        
        label_cantidad = QLabel("Cantidad")
        label_cantidad.setStyleSheet("font-size: 11px; color: #64748b;")
        cantidad_layout.addWidget(label_cantidad)
        
        cantidad_label = QLabel(f"{cantidad}")
        if is_dark:
            cantidad_label.setStyleSheet("font-size: 16px; color: #94a3b8; font-weight: 500;")
        else:
            cantidad_label.setStyleSheet("font-size: 16px; color: #475569; font-weight: 600;")
        cantidad_layout.addWidget(cantidad_label)
        
        row_layout.addWidget(cantidad_widget, 1)
        
        # Columna 3: Total
        total_widget = QWidget()
        total_layout = QVBoxLayout(total_widget)
        total_layout.setContentsMargins(UIScale.px(0), UIScale.px(0), UIScale.px(0), UIScale.px(0))
        total_layout.setSpacing(UIScale.px(2))
        
        label_total = QLabel("Total")
        label_total.setStyleSheet("font-size: 11px; color: #64748b;")
        label_total.setAlignment(Qt.AlignmentFlag.AlignRight)
        total_layout.addWidget(label_total)
        
        total_label = QLabel(f"${total:,.0f}")
        total_label.setStyleSheet("font-size: 18px; color: #3b82f6; font-weight: 700;")
        total_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        total_layout.addWidget(total_label)
        
        row_layout.addWidget(total_widget, 1)
        
        return row
    
    def _actualizar_estadisticas(self):
        """Actualiza todas las estadísticas con los filtros seleccionados"""
        # Determinar parámetros de filtrado
        año = self.año_seleccionado if self.año_seleccionado != 0 else None
        mes = self.mes_seleccionado if self.mes_seleccionado != 0 else None
        
        # Obtener estadísticas de cuotas filtradas
        stats_cuotas = CuotaMensual.obtener_estadisticas(año, mes)
        
        # Actualizar tarjetas de cuotas
        self._actualizar_valor_stat(
            self.stat_total_cuotas,
            str(stats_cuotas.get('total', 0))
        )
        
        self._actualizar_valor_stat(
            self.stat_cuotas_pagadas,
            f"${stats_cuotas.get('total_pagado', 0):,.0f}"
        )
        
        self._actualizar_valor_stat(
            self.stat_cuotas_impago,
            f"${stats_cuotas.get('total_impago', 0):,.0f}"
        )
        
        self._actualizar_valor_stat(
            self.stat_cuotas_deuda,
            f"${stats_cuotas.get('total_deuda', 0):,.0f}"
        )
        
        # Actualizar métodos de pago
        self._actualizar_metodos_pago(año, mes)
    
    def _actualizar_valor_stat(self, card: QFrame, nuevo_valor: str):
        """Actualiza el valor de una tarjeta de estadística"""
        # Detectar tema actual
        main_window = self.window()
        is_dark = True
        if hasattr(main_window, 'current_theme'):
            is_dark = main_window.current_theme == 'dark'
        
        # Determinar color según el tipo de tarjeta
        if card == self.stat_total_cuotas:
            color = "#3b82f6" if is_dark else "#1e40af"
        elif card == self.stat_cuotas_pagadas:
            color = "#22c55e" if is_dark else "#15803d"
        elif card == self.stat_cuotas_impago:
            color = "#ef4444" if is_dark else "#b91c1c"
        elif card == self.stat_cuotas_deuda:
            color = "#eab308" if is_dark else "#a16207"
        else:
            color = "#3b82f6" if is_dark else "#1e40af"
        
        valor_label = card.findChild(QLabel, "valor_stat")
        if valor_label:
            valor_label.setText(nuevo_valor)
            valor_label.setStyleSheet(f"font-size: 36px; color: {color}; font-weight: 700; border: none;")
    
    def _actualizar_metodos_pago(self, año=None, mes=None):
        """Actualiza las estadísticas por método de pago"""
        # Limpiar contenedor
        while self.metodos_container.count():
            item = self.metodos_container.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        # Obtener datos filtrados
        metodos = MetodoPago.obtener_todos()
        stats_metodos = CuotaMensual.obtener_estadisticas_por_metodo(año, mes)
        
        # Crear filas para cada método activo
        for metodo in metodos:
            if metodo.activo:
                cantidad = stats_metodos.get(metodo.nombre, {}).get('cantidad', 0)
                total = stats_metodos.get(metodo.nombre, {}).get('total', 0)
                
                fila = self._crear_fila_metodo(metodo.nombre, cantidad, total)
                self.metodos_container.addWidget(fila)


