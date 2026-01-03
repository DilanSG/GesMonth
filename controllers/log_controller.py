"""
Controlador para la gestión de logs del sistema
"""

# Typing: Type hints para estructuras de datos complejas
from typing import List, Dict, Any, Optional  # List: listas, Dict: diccionarios, Any: cualquier tipo, Optional: valores opcionales

# Datetime: Manejo de fechas para filtros y timestamps
from datetime import datetime, timedelta  # datetime: fechas actuales, timedelta: cálculos de intervalos

# Database: Modelo de logs del sistema
from database.models import LogSistema  # LogSistema: CRUD de logs de auditoría

# CSV: Exportación de logs a archivos CSV
import csv  # csv: generación de reportes en formato CSV

# OS: Operaciones con rutas de archivos
import os  # os: manejo de rutas para exportaciones


class LogController:
    """Controlador para gestionar logs del sistema"""
    
    def __init__(self):
        pass
    
    def registrar_log(self, usuario_id: Optional[int], usuario_nombre: str, 
                      accion: str, detalles: str = "") -> bool:
        """
        Registra un nuevo log en el sistema
        
        Args:
            usuario_id: ID del usuario que realiza la acción
            usuario_nombre: Nombre del usuario
            accion: Acción realizada (crear, editar, eliminar, pago, impago, etc.)
            detalles: Información adicional sobre la acción
        
        Returns:
            True si se registró exitosamente
        """
        try:
            LogSistema.registrar(
                usuario_id=usuario_id,
                usuario_nombre=usuario_nombre,
                accion=accion,
                detalles=detalles
            )
            return True
        except Exception as e:
            print(f"Error al registrar log: {e}")
            return False
    
    def obtener_ultimo_log_login_fallido(self, username: str) -> Optional[Dict[str, Any]]:
        """
        Obtiene el último log de login fallido para un usuario específico
        
        Args:
            username: Username del usuario
        
        Returns:
            Diccionario con el log o None si no existe
        """
        try:
            from database.connection import DatabaseConnection
            db = DatabaseConnection()
            conn = db.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT id, usuario_id, usuario_nombre, fecha_hora, accion, detalles
                FROM logs_sistema
                WHERE accion = 'Login fallido' 
                AND detalles LIKE ?
                ORDER BY fecha_hora DESC
                LIMIT 1
            ''', (f'%{username}%',))
            
            row = cursor.fetchone()
            if row:
                return {
                    'id': row['id'],
                    'usuario_id': row['usuario_id'],
                    'usuario_nombre': row['usuario_nombre'],
                    'fecha_hora': row['fecha_hora'],
                    'accion': row['accion'],
                    'detalles': row['detalles']
                }
            return None
        except Exception as e:
            print(f"Error al obtener último log: {e}")
            return None
    
    def actualizar_log(self, log_id: int, nuevos_detalles: str) -> bool:
        """
        Actualiza los detalles de un log existente
        
        Args:
            log_id: ID del log a actualizar
            nuevos_detalles: Nuevos detalles del log
        
        Returns:
            True si se actualizó exitosamente
        """
        try:
            from database.connection import DatabaseConnection
            db = DatabaseConnection()
            conn = db.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                UPDATE logs_sistema
                SET detalles = ?,
                    fecha_hora = CURRENT_TIMESTAMP
                WHERE id = ?
            ''', (nuevos_detalles, log_id))
            
            conn.commit()
            return True
        except Exception as e:
            print(f"Error al actualizar log: {e}")
            return False
    
    def obtener_logs(self, filtro: Optional[Dict[str, Any]] = None, 
                     limite: int = 1000) -> List[Dict[str, Any]]:
        """
        Obtiene logs del sistema con filtros opcionales
        
        Args:
            filtro: Diccionario con filtros (accion, usuario_id, fecha_inicio, fecha_fin)
            limite: Cantidad máxima de logs a retornar
        
        Returns:
            Lista de logs como diccionarios
        """
        try:
            if filtro:
                # Aplicar filtros específicos
                if 'accion' in filtro:
                    logs = LogSistema.obtener_por_accion(filtro['accion'], limite)
                elif 'usuario_id' in filtro:
                    logs = LogSistema.obtener_por_usuario(filtro['usuario_id'], limite)
                elif 'fecha_inicio' in filtro and 'fecha_fin' in filtro:
                    logs = LogSistema.obtener_por_fecha(
                        filtro['fecha_inicio'], 
                        filtro['fecha_fin'], 
                        limite
                    )
                else:
                    logs = LogSistema.obtener_todos(limite)
            else:
                logs = LogSistema.obtener_todos(limite)
            
            # Convertir a diccionarios
            return [{
                'id': log.id,
                'usuario_id': log.usuario_id,
                'usuario_nombre': log.usuario_nombre,
                'fecha_hora': log.fecha_hora,
                'accion': log.accion,
                'detalles': log.detalles
            } for log in logs]
        
        except Exception as e:
            print(f"Error al obtener logs: {e}")
            return []
    
    def exportar_logs_csv(self, ruta_archivo: str, 
                         filtro: Optional[Dict[str, Any]] = None) -> bool:
        """
        Exporta los logs a un archivo CSV
        
        Args:
            ruta_archivo: Ruta donde guardar el archivo CSV
            filtro: Filtros opcionales para los logs
        
        Returns:
            True si se exportó exitosamente
        """
        try:
            logs = self.obtener_logs(filtro, limite=10000)
            
            if not logs:
                return False
            
            with open(ruta_archivo, 'w', newline='', encoding='utf-8') as archivo:
                campos = ['ID', 'Usuario ID', 'Usuario', 'Fecha y Hora', 'Acción', 'Detalles']
                
                writer = csv.DictWriter(archivo, fieldnames=campos)
                writer.writeheader()
                
                for log in logs:
                    writer.writerow({
                        'ID': log['id'],
                        'Usuario ID': log['usuario_id'] if log['usuario_id'] else 'N/A',
                        'Usuario': log['usuario_nombre'],
                        'Fecha y Hora': log['fecha_hora'],
                        'Acción': log['accion'],
                        'Detalles': log['detalles']
                    })
            
            return True
        
        except Exception as e:
            print(f"Error al exportar logs: {e}")
            return False
    
    def limpiar_logs_antiguos(self, dias: int = 365) -> int:
        """
        Elimina logs más antiguos que X días
        
        Args:
            dias: Cantidad de días a mantener
        
        Returns:
            Cantidad de logs eliminados
        """
        try:
            return LogSistema.eliminar_antiguos(dias)
        except Exception as e:
            print(f"Error al limpiar logs: {e}")
            return 0
    
    def obtener_estadisticas(self) -> Dict[str, Any]:
        """
        Obtiene estadísticas de los logs
        
        Returns:
            Diccionario con estadísticas
        """
        try:
            logs = LogSistema.obtener_todos(10000)
            
            if not logs:
                return {
                    'total_logs': 0,
                    'por_accion': {},
                    'usuarios_activos': 0
                }
            
            # Contar por acción
            por_accion = {}
            usuarios = set()
            
            for log in logs:
                # Contar por acción
                por_accion[log.accion] = por_accion.get(log.accion, 0) + 1
                
                # Contar usuarios únicos
                if log.usuario_id:
                    usuarios.add(log.usuario_id)
            
            return {
                'total_logs': len(logs),
                'por_accion': por_accion,
                'usuarios_activos': len(usuarios)
            }
        
        except Exception as e:
            print(f"Error al obtener estadísticas: {e}")
            return {
                'total_logs': 0,
                'por_accion': {},
                'usuarios_activos': 0
            }
    
    def borrar_todos_logs(self) -> int:
        """
        Borra todos los logs del sistema (solo para superadmin)
        
        Returns:
            Cantidad de logs eliminados
        """
        try:
            from database.connection import DatabaseConnection
            db = DatabaseConnection()
            conn = db.get_connection()
            cursor = conn.cursor()
            
            # Contar logs antes de borrar
            cursor.execute('SELECT COUNT(*) FROM logs_sistema')
            cantidad = cursor.fetchone()[0]
            
            # Borrar todos los logs
            cursor.execute('DELETE FROM logs_sistema')
            conn.commit()
            
            return cantidad
        except Exception as e:
            print(f"Error al borrar logs: {e}")
            return 0
