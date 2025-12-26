"""
Conexión a la base de datos de usuarios
"""
import sqlite3
import os
from pathlib import Path
from utils import get_data_path


class UserDatabaseConnection:
    """Singleton para manejar la conexión a users.db"""
    
    _instance = None
    _connection = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(UserDatabaseConnection, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance
    
    def _initialize(self):
        """Inicializa la conexión y crea las tablas"""
        # Base de datos en carpeta .data
        self._db_path = get_data_path('users.db')
        self._connection = sqlite3.connect(self._db_path, check_same_thread=False)
        self._connection.row_factory = sqlite3.Row
        
        self._create_tables()
        self._create_superadmin()
    
    def _create_tables(self):
        """Crea las tablas necesarias"""
        cursor = self._connection.cursor()
        
        # Tabla de usuarios
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                nombre_completo TEXT,
                rol TEXT NOT NULL DEFAULT 'operador',
                es_superadmin INTEGER DEFAULT 0,
                puede_crear_usuarios INTEGER DEFAULT 0,
                activo INTEGER DEFAULT 1,
                fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP,
                creado_por_usuario_id INTEGER,
                ultimo_acceso DATETIME,
                intentos_fallidos INTEGER DEFAULT 0,
                bloqueado_hasta DATETIME,
                FOREIGN KEY (creado_por_usuario_id) REFERENCES usuarios(id)
            )
        ''')
        
        # Tabla de sesiones
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sesiones (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario_id INTEGER NOT NULL,
                token_sesion TEXT UNIQUE NOT NULL,
                fecha_inicio DATETIME DEFAULT CURRENT_TIMESTAMP,
                fecha_fin DATETIME,
                activa INTEGER DEFAULT 1,
                FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
            )
        ''')
        
        # Tabla de logs de auditoría
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS logs_auditoria (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario_id INTEGER NOT NULL,
                accion TEXT NOT NULL,
                entidad_tipo TEXT,
                entidad_id INTEGER,
                datos_anteriores TEXT,
                datos_nuevos TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                resultado TEXT DEFAULT 'exitoso',
                FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
            )
        ''')
        
        self._connection.commit()
    
    def _create_superadmin(self):
        """Crea el usuario superadmin si no existe"""
        cursor = self._connection.cursor()
        
        # Verificar si ya existe un superadmin
        cursor.execute('SELECT id FROM usuarios WHERE es_superadmin = 1')
        if cursor.fetchone() is not None:
            return
        
        # Crear superadmin con password hasheado
        import bcrypt
        password = "admin123"
        password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
        cursor.execute('''
            INSERT INTO usuarios (
                username, password_hash, nombre_completo, rol,
                es_superadmin, puede_crear_usuarios
            ) VALUES (?, ?, ?, ?, ?, ?)
        ''', ('admin', password_hash, 'Administrador', 'superadmin', 1, 1))
        
        self._connection.commit()
        print("✓ Usuario superadmin creado: admin/admin123")
    
    def get_connection(self):
        """Retorna la conexión activa"""
        return self._connection
    
    def close(self):
        """Cierra la conexión"""
        if self._connection:
            self._connection.close()
            self._connection = None
