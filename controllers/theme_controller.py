"""
Controlador para gestión de temas de la aplicación
"""

import os
from typing import Optional
from database.connection import DatabaseConnection
from controllers.config_controller import ConfigController
from utils import get_resource_path


class ThemeController:
    """Gestiona los temas de la aplicación (oscuro/claro)"""
    
    def __init__(self):
        self.db = DatabaseConnection()
        self.config_controller = ConfigController()
        self._ensure_theme_config()
    
    def _ensure_theme_config(self):
        """Asegura que exista la configuración de tema en la BD"""
        cursor = self.db.get_connection().cursor()
        cursor.execute(
            "SELECT valor FROM configuracion WHERE clave = 'theme'"
        )
        if not cursor.fetchone():
            cursor.execute(
                "INSERT INTO configuracion (clave, valor) VALUES ('theme', 'dark')"
            )
            self.db.get_connection().commit()
    
    def get_current_theme(self) -> str:
        """Obtiene el tema actual ('dark' o 'light')"""
        try:
            cursor = self.db.get_connection().cursor()
            cursor.execute(
                "SELECT valor FROM configuracion WHERE clave = 'theme'"
            )
            row = cursor.fetchone()
            if row and row['valor'] in ['dark', 'light']:
                return row['valor']
        except Exception:
            pass
        return 'dark'  # Por defecto modo oscuro
    
    def set_theme(self, theme: str) -> bool:
        """
        Establece el tema de la aplicación
        
        Args:
            theme: 'dark' o 'light'
            
        Returns:
            True si se guardó correctamente
        """
        if theme not in ['dark', 'light']:
            return False
        
        try:
            cursor = self.db.get_connection().cursor()
            cursor.execute(
                """
                INSERT OR REPLACE INTO configuracion (clave, valor)
                VALUES ('theme', ?)
                """,
                (theme,)
            )
            self.db.get_connection().commit()
            return True
        except Exception:
            return False
    
    def get_theme_stylesheet(self, theme: str) -> Optional[str]:
        """
        Obtiene el contenido del archivo CSS para el tema especificado
        
        Args:
            theme: 'dark' o 'light'
            
        Returns:
            Contenido del archivo CSS o None si no existe
        """
        # Usar función helper para obtener ruta correcta en desarrollo y empaquetado
        theme_file = get_resource_path(os.path.join('assets', 'styles', f'{theme}.qss'))
        
        try:
            with open(theme_file, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            print(f"ERROR cargando tema {theme}: {e}")
            print(f"Ruta intentada: {theme_file}")
            return None
    
    def apply_theme_to_app(self, app, theme: str) -> bool:
        """
        Aplica el tema a toda la aplicación
        
        Args:
            app: Instancia de QApplication
            theme: 'dark' o 'light'
            
        Returns:
            True si se aplicó correctamente
        """
        stylesheet = self.get_theme_stylesheet(theme)
        if stylesheet:
            app.setStyleSheet(stylesheet)
            return True
        return False
