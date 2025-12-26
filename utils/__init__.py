"""
Utilidades compartidas para obtener rutas de recursos
"""
import os
import sys


def get_resource_path(relative_path: str) -> str:
    """
    Obtiene la ruta absoluta de un recurso, funciona en desarrollo y en ejecutable empaquetado
    
    Args:
        relative_path: Ruta relativa desde la raíz del proyecto
        
    Returns:
        Ruta absoluta al recurso
    """
    if getattr(sys, 'frozen', False):
        # Si está empaquetado con PyInstaller
        # Primero intentar desde el directorio del ejecutable
        executable_dir = os.path.dirname(sys.executable)
        resource_path = os.path.join(executable_dir, relative_path)
        
        # Si no existe ahí, buscar en _internal
        if not os.path.exists(resource_path):
            resource_path = os.path.join(sys._MEIPASS, relative_path)
        
        return resource_path
    else:
        # Si está en desarrollo
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        return os.path.join(base_path, relative_path)


def get_data_path(filename: str = None) -> str:
    """
    Obtiene la ruta para archivos de datos persistentes (bases de datos)
    Los datos se guardan en una carpeta .data junto al ejecutable
    
    Args:
        filename: Nombre del archivo de datos (opcional)
        
    Returns:
        Ruta absoluta a la carpeta .data o al archivo si se especifica
    """
    if getattr(sys, 'frozen', False):
        # Si está empaquetado: carpeta donde está el ejecutable
        base_path = os.path.dirname(sys.executable)
    else:
        # Si está en desarrollo: raíz del proyecto
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # Crear carpeta .data si no existe
    data_dir = os.path.join(base_path, '.data')
    if not os.path.exists(data_dir):
        os.makedirs(data_dir, exist_ok=True)
    
    if filename:
        file_path = os.path.join(data_dir, filename)
        # Si el archivo existe pero no tiene permisos (archivo placeholder), eliminarlo
        if os.path.exists(file_path):
            try:
                # Intentar leer el tamaño, si falla es porque no tiene permisos
                os.stat(file_path)
                if os.path.getsize(file_path) == 0:
                    # Archivo vacío sin permisos, eliminarlo
                    os.chmod(file_path, 0o644)
                    os.remove(file_path)
            except (OSError, PermissionError):
                # Archivo sin permisos, forzar eliminación
                try:
                    os.chmod(file_path, 0o644)
                    os.remove(file_path)
                except:
                    pass
        return file_path
    return data_dir
