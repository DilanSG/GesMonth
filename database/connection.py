"""
Gestión de conexión a la base de datos SQLite
"""

import sqlite3
import os
from typing import Optional
from pathlib import Path
from utils import get_data_path


class DatabaseConnection:
    """Clase singleton para gestionar la conexión a SQLite"""
    
    _instance: Optional['DatabaseConnection'] = None
    _connection: Optional[sqlite3.Connection] = None
    _db_path: Optional[str] = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        """Inicializa la conexión a la base de datos"""
        if self._connection is None:
            # Base de datos en carpeta .data
            self._db_path = get_data_path('gesmonth.db')
            self._connection = sqlite3.connect(self._db_path, check_same_thread=False)
            # Asegura integridad referencial en SQLite
            self._connection.execute("PRAGMA foreign_keys = ON")
            self._connection.row_factory = sqlite3.Row
            self._create_tables()
    
    def _create_tables(self):
        """Crea las tablas de la base de datos si no existen"""
        cursor = self._connection.cursor()
        
        # Tabla de clientes
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS clientes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                documento TEXT UNIQUE NOT NULL,
                telefono TEXT,
                estado TEXT DEFAULT 'activo',
                valor_cuota REAL DEFAULT 0.0,
                dia_cobro INTEGER DEFAULT 5
            )
        ''')
        
        # Agregar columna dia_cobro si no existe (migración)
        try:
            cursor.execute('ALTER TABLE clientes ADD COLUMN dia_cobro INTEGER DEFAULT 5')
            self._connection.commit()
        except sqlite3.OperationalError:
            # La columna ya existe
            pass
        
        # Tabla de pagos
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS pagos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                cliente_id INTEGER NOT NULL,
                fecha_pago DATE NOT NULL,
                mes_correspondiente TEXT NOT NULL,
                monto REAL NOT NULL,
                metodo_pago TEXT,
                FOREIGN KEY (cliente_id) REFERENCES clientes(id) ON DELETE CASCADE
            )
        ''')
        
        # Tabla de cuotas mensuales
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS cuotas_mensuales (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                cliente_id INTEGER NOT NULL,
                año INTEGER NOT NULL,
                mes INTEGER NOT NULL,
                estado TEXT DEFAULT 'pendiente',
                monto REAL NOT NULL,
                metodo_pago TEXT,
                fecha_registro DATE,
                fecha_inicio_mora DATE,
                deuda_acumulada REAL DEFAULT 0.0,
                FOREIGN KEY (cliente_id) REFERENCES clientes(id) ON DELETE CASCADE,
                UNIQUE(cliente_id, año, mes)
            )
        ''')
        
        # Agregar columnas nuevas si no existen (migración)
        try:
            cursor.execute('ALTER TABLE cuotas_mensuales ADD COLUMN fecha_inicio_mora DATE')
            self._connection.commit()
        except sqlite3.OperationalError:
            pass
        
        try:
            cursor.execute('ALTER TABLE cuotas_mensuales ADD COLUMN deuda_acumulada REAL DEFAULT 0.0')
            self._connection.commit()
        except sqlite3.OperationalError:
            pass
        
        # Tabla de métodos de pago
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS metodos_pago (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT UNIQUE NOT NULL,
                activo INTEGER DEFAULT 1,
                color TEXT DEFAULT '#3b82f6'
            )
        ''')
        
        # Tabla de configuración
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS configuracion (
                clave TEXT PRIMARY KEY,
                valor TEXT NOT NULL
            )
        ''')
        
        # Insertar años por defecto si no existen
        cursor.execute('''
            INSERT OR IGNORE INTO configuracion (clave, valor)
            VALUES ('años_facturacion', '2025,2026')
        ''')
        
        # Crear índices para optimizar consultas frecuentes
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_clientes_estado ON clientes(estado)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_clientes_documento ON clientes(documento)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_pagos_cliente ON pagos(cliente_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_pagos_mes ON pagos(mes_correspondiente)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_pagos_fecha ON pagos(fecha_pago)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_cuotas_cliente ON cuotas_mensuales(cliente_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_cuotas_año_mes ON cuotas_mensuales(año, mes)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_cuotas_estado ON cuotas_mensuales(estado)')
        
        # Migración: Agregar columna color a metodos_pago si no existe
        cursor.execute("PRAGMA table_info(metodos_pago)")
        columns = [row[1] for row in cursor.fetchall()]
        if 'color' not in columns:
            cursor.execute("ALTER TABLE metodos_pago ADD COLUMN color TEXT DEFAULT '#3b82f6'")
        
        self._connection.commit()
    
    def get_connection(self) -> sqlite3.Connection:
        """Retorna la conexión activa a la base de datos"""
        return self._connection

    def get_db_path(self) -> str:
        """Retorna la ruta del archivo de base de datos"""
        if self._db_path is None:
            self._db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'gesmonth.db')
        return self._db_path
    
    def close(self):
        """Cierra la conexión a la base de datos"""
        if self._connection:
            self._connection.close()
            self._connection = None
