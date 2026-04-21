"""
Controlador para configuración general de la aplicación.
"""

# Future: Compatibilidad con anotaciones de tipo modernas
from __future__ import annotations  # annotations: permite usar tipos de la propia clase en hints

# OS: Operaciones con el sistema de archivos y rutas
import os  # os: manejo de rutas y directorios
import shutil  # shutil: operaciones avanzadas de archivos (copiar, mover)

# Datetime: Manejo de fechas y tiempos
from datetime import datetime  # datetime: timestamps para configuraciones

# Typing: Type hints para estructuras de datos
from typing import List  # List: listas tipadas de años configurados

# Database: Conexión a la base de datos
from database.connection import DatabaseConnection  # DatabaseConnection: acceso a configuración persistente


class ConfigController:
    """Encapsula operaciones de configuración y utilidades."""

    def __init__(self) -> None:
        self.db = DatabaseConnection()
        self.log_controller = None  # Se inyectará desde la UI
        self.usuario_actual = None
    
    def set_log_controller(self, log_controller):
        """Configura el controlador de logs"""
        self.log_controller = log_controller
    
    def set_usuario_actual(self, usuario):
        """Configura el usuario actual"""
        self.usuario_actual = usuario

    def get_billing_years(self) -> List[int]:
        """Obtiene los años de facturación configurados.
        Retorna lista con dos años, usando valores por defecto si algo falla.
        """
        try:
            cursor = self.db.get_connection().cursor()
            cursor.execute("SELECT valor FROM configuracion WHERE clave = 'años_facturacion'")
            row = cursor.fetchone()
            if row and row["valor"]:
                return [int(valor.strip()) for valor in row["valor"].split(",") if valor.strip()]
        except Exception:
            pass
        return [2025, 2026]

    def set_billing_years(self, ano_1: int, ano_2: int) -> str:
        """Guarda los años de facturación ordenados y retorna la cadena almacenada."""
        anos_list = sorted([ano_1, ano_2])
        anos_formatted = ",".join(map(str, anos_list))

        cursor = self.db.get_connection().cursor()
        cursor.execute(
            """
            INSERT OR REPLACE INTO configuracion (clave, valor)
            VALUES ('años_facturacion', ?)
            """,
            (anos_formatted,),
        )
        self.db.get_connection().commit()
        return anos_formatted

    def get_theme(self) -> str:
        """Obtiene el tema actual ('dark' o 'light')"""
        try:
            cursor = self.db.get_connection().cursor()
            cursor.execute("SELECT valor FROM configuracion WHERE clave = 'theme'")
            row = cursor.fetchone()
            if row and row["valor"] in ["dark", "light"]:
                return row["valor"]
        except Exception:
            pass
        return "dark"  # Por defecto modo oscuro

    def set_theme(self, theme: str) -> bool:
        """
        Establece el tema de la aplicación
        
        Args:
            theme: 'dark' o 'light'
            
        Returns:
            True si se guardó correctamente
        """
        if theme not in ["dark", "light"]:
            return False

        try:
            cursor = self.db.get_connection().cursor()
            cursor.execute(
                """
                INSERT OR REPLACE INTO configuracion (clave, valor)
                VALUES ('theme', ?)
                """,
                (theme,),
            )
            self.db.get_connection().commit()
            return True
        except Exception:
            return False

    def create_backup(self, destination_path: str | None = None) -> str:
        """Crea un respaldo de la base de datos.
        Si destination_path es None, se guarda junto al archivo original.
        Retorna la ruta del respaldo generado.
        """
        db_path = self.db.get_db_path()
        if destination_path:
            backup_path = destination_path
        else:
            backup_name = f"backup_database_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
            backup_path = os.path.join(os.path.dirname(db_path), backup_name)

        shutil.copy2(db_path, backup_path)
        return backup_path

    def get_fullscreen(self) -> bool:
        """Obtiene la configuración de pantalla completa"""
        try:
            cursor = self.db.get_connection().cursor()
            cursor.execute("SELECT valor FROM configuracion WHERE clave = 'fullscreen'")
            row = cursor.fetchone()
            if row and row["valor"] in ["true", "false"]:
                return row["valor"] == "true"
        except Exception:
            pass
        return False  # Por defecto NO en pantalla completa

    def set_fullscreen(self, enabled: bool) -> bool:
        """
        Establece la configuración de pantalla completa
        
        Args:
            enabled: True para activar pantalla completa, False para desactivar
            
        Returns:
            True si se guardó correctamente
        """
        try:
            cursor = self.db.get_connection().cursor()
            cursor.execute(
                """
                INSERT OR REPLACE INTO configuracion (clave, valor)
                VALUES ('fullscreen', ?)
                """,
                ("true" if enabled else "false",),
            )
            self.db.get_connection().commit()
            return True
        except Exception:
            return False
    
    def get_remembered_user(self) -> str:
        """Obtiene el usuario recordado"""
        try:
            cursor = self.db.get_connection().cursor()
            cursor.execute("SELECT valor FROM configuracion WHERE clave = 'remembered_user'")
            row = cursor.fetchone()
            if row and row["valor"]:
                return row["valor"]
        except Exception:
            pass
        return ""
    
    def set_remembered_user(self, username: str) -> bool:
        """
        Guarda el usuario a recordar
        
        Args:
            username: Nombre de usuario a recordar
            
        Returns:
            True si se guardó correctamente
        """
        try:
            cursor = self.db.get_connection().cursor()
            cursor.execute(
                """
                INSERT OR REPLACE INTO configuracion (clave, valor)
                VALUES ('remembered_user', ?)
                """,
                (username,),
            )
            self.db.get_connection().commit()
            return True
        except Exception:
            return False
    
    def clear_remembered_user(self) -> bool:
        """
        Elimina el usuario recordado
        
        Returns:
            True si se eliminó correctamente
        """
        try:
            cursor = self.db.get_connection().cursor()
            cursor.execute("DELETE FROM configuracion WHERE clave = 'remembered_user'")
            self.db.get_connection().commit()
            return True
        except Exception:
            return False
