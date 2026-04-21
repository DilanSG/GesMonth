"""
Gestión de conexión a la base de datos SQLite
"""

# SQLite3: Base de datos embebida
import sqlite3  # sqlite3: motor de base de datos SQL ligero

# OS: Operaciones con el sistema de archivos
import os  # os: verificación y creación de directorios

# Typing: Type hints para valores opcionales
from typing import Optional  # Optional: indica que un valor puede ser None

# Pathlib: Manejo moderno de rutas
from pathlib import Path  # Path: construcción y manipulación de rutas

# Utils: Utilidades de rutas
from utils import get_data_path  # get_data_path: ruta del directorio de datos


class DatabaseConnection:
    """Clase singleton para gestionar la conexión a SQLite"""
    
    _instance: Optional['DatabaseConnection'] = None
    _connection: Optional[sqlite3.Connection] = None
    _db_path: Optional[str] = None
    
    def __new__(cls):
        """
        Implementa el patrón Singleton para garantizar una única instancia de conexión.
        
        El patrón Singleton asegura que:
        - Solo exista una conexión a la BD en toda la aplicación
        - Se eviten múltiples conexiones que consuman recursos
        - Todas las partes del código compartan la misma instancia
        
        Funcionamiento:
        1. Verifica si ya existe una instancia (_instance es None)
        2. Si no existe, crea una nueva usando super().__new__()
        3. Si existe, retorna la instancia existente
        
        Returns:
            La única instancia de DatabaseConnection
        """
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        """
        Inicializa la conexión a la base de datos SQLite.
        
        Proceso de inicialización:
        1. Verifica que no exista una conexión previa (protección singleton)
        2. Construye la ruta del archivo .db en el directorio .data
        3. Establece conexión con check_same_thread=False para uso multihilo
        4. Activa PRAGMA foreign_keys para integridad referencial
        5. Configura row_factory para acceder a columnas por nombre
        6. Crea las tablas si no existen
        
        PRAGMA foreign_keys:
        - SQLite desactiva claves foráneas por defecto
        - Este comando las activa para mantener integridad de datos
        - Ejemplo: Si eliminas un cliente, se eliminan sus pagos (CASCADE)
        
        row_factory = sqlite3.Row:
        - Permite acceder a columnas como row['nombre'] en vez de row[0]
        - Hace el código más legible y menos propenso a errores
        """
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
        
        # Tabla de logs de sistema
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS logs_sistema (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario_id INTEGER,
                usuario_nombre TEXT NOT NULL,
                fecha_hora TIMESTAMP NOT NULL,
                accion TEXT NOT NULL,
                detalles TEXT
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
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_logs_usuario ON logs_sistema(usuario_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_logs_fecha ON logs_sistema(fecha_hora)')
        
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
