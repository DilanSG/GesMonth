"""
Controlador para configuración general de la aplicación.
"""

from __future__ import annotations

import os
import shutil
from datetime import datetime
from typing import List

from database.connection import DatabaseConnection


class ConfigController:
    """Encapsula operaciones de configuración y utilidades."""

    def __init__(self) -> None:
        self.db = DatabaseConnection()

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
