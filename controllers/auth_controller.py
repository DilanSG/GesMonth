"""
Controlador de autenticación
"""
from typing import Optional, Tuple
from database.user_models import Usuario, Sesion, AuditoriaLog


class AuthController:
    """Controlador para manejar autenticación"""
    
    def __init__(self):
        self.usuario_actual: Optional[Usuario] = None
        self.token_sesion: Optional[str] = None
    
    def login(self, username: str, password: str) -> Tuple[bool, str]:
        """
        Intenta hacer login
        Retorna: (éxito: bool, mensaje: str)
        """
        usuario = Usuario.autenticar(username, password)
        
        if usuario is None:
            return False, "Usuario o contraseña incorrectos"
        
        if not usuario.activo:
            return False, "Usuario desactivado"
        
        # Crear sesión
        self.token_sesion = Sesion.crear(usuario.id)
        self.usuario_actual = usuario
        
        # Registrar login en auditoría
        AuditoriaLog.registrar(
            usuario_id=usuario.id,
            accion='login',
            resultado='exitoso'
        )
        
        return True, f"Bienvenido {usuario.nombre_completo}"
    
    def logout(self):
        """Cierra la sesión actual"""
        if self.token_sesion and self.usuario_actual:
            AuditoriaLog.registrar(
                usuario_id=self.usuario_actual.id,
                accion='logout',
                resultado='exitoso'
            )
            Sesion.cerrar(self.token_sesion)
        
        self.usuario_actual = None
        self.token_sesion = None
    
    def tiene_permiso(self, permiso: str) -> bool:
        """Verifica si el usuario actual tiene un permiso específico"""
        if not self.usuario_actual:
            return False
        
        permisos_por_rol = {
            'superadmin': ['crear_usuarios', 'eliminar_usuarios', 'ver_todos_logs',
                          'gestionar_clientes', 'gestionar_pagos', 'ver_reportes',
                          'exportar_datos', 'configuracion'],
            'admin': ['gestionar_clientes', 'gestionar_pagos', 'ver_reportes',
                     'exportar_datos', 'configuracion'],
            'operador': ['gestionar_clientes', 'gestionar_pagos', 'ver_reportes'],
            'solo_lectura': ['ver_reportes']
        }
        
        permisos = permisos_por_rol.get(self.usuario_actual.rol, [])
        return permiso in permisos
    
    def es_superadmin(self) -> bool:
        """Verifica si el usuario actual es superadmin"""
        return self.usuario_actual and self.usuario_actual.es_superadmin
    
    def puede_crear_usuarios(self) -> bool:
        """Verifica si el usuario actual puede crear usuarios"""
        return self.usuario_actual and self.usuario_actual.puede_crear_usuarios
    
    def registrar_accion(self, accion: str, entidad_tipo: str = None,
                        entidad_id: int = None, datos: str = None):
        """Registra una acción en el log de auditoría"""
        if self.usuario_actual:
            AuditoriaLog.registrar(
                usuario_id=self.usuario_actual.id,
                accion=accion,
                entidad_tipo=entidad_tipo,
                entidad_id=entidad_id,
                datos_nuevos=datos
            )
