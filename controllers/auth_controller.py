"""
Controlador de autenticación
"""
# Typing: Type hints para mejorar la claridad del código
from typing import Optional, Tuple  # Optional: permite valores None, Tuple: especifica tipos en tuplas

# Database: Modelos de datos de usuarios
from database.user_models import Usuario, Sesion, AuditoriaLog  # Usuario: autenticación, Sesion: tokens, AuditoriaLog: registro de acciones
from database.models import LogSistema  # LogSistema: logs del sistema de negocio


class AuthController:
    """Controlador para manejar autenticación"""
    
    def __init__(self, log_controller=None):
        self.usuario_actual: Optional[Usuario] = None
        self.token_sesion: Optional[str] = None
        self.log_controller = log_controller
    
    def login(self, username: str, password: str) -> Tuple[bool, str]:
        """
        Intenta hacer login con mensajes diferenciados y registro de logs.
        Retorna: (éxito: bool, mensaje: str)
        """
        # Intentar autenticar con información detallada
        usuario, codigo_error, intentos = Usuario.autenticar(username, password)
        
        # Procesar resultado según código de error
        if codigo_error == 'user_not_found':
            # Usuario no existe en la base de datos
            if self.log_controller:
                self.log_controller.registrar_log(
                    usuario_id=0,
                    usuario_nombre='Sistema',
                    accion='Login fallido',
                    detalles=f'Intento de login con usuario inexistente: {username}'
                )
            return False, "El usuario no existe"
        
        elif codigo_error == 'inactive':
            # Usuario existe pero está desactivado
            if self.log_controller:
                self.log_controller.registrar_log(
                    usuario_id=0,
                    usuario_nombre='Sistema',
                    accion='Login fallido',
                    detalles=f'Intento de login con usuario desactivado: {username}'
                )
            return False, "El usuario está desactivado"
        
        elif codigo_error == 'blocked':
            # Usuario bloqueado por intentos fallidos
            if self.log_controller:
                self.log_controller.registrar_log(
                    usuario_id=0,
                    usuario_nombre='Sistema',
                    accion='Login fallido',
                    detalles=f'Intento de login con usuario bloqueado: {username} (intentos fallidos: {intentos})'
                )
            return False, f"Usuario bloqueado por {intentos} intentos fallidos. Intente en 15 minutos"
        
        elif codigo_error == 'wrong_password':
            # Contraseña incorrecta - actualizar log existente o crear uno nuevo
            # IMPORTANTE: Separar mensaje para usuario (limpio) del detalle para log (con contador)
            sufijo_intentos = f" x{intentos}" if intentos > 1 else ""
            detalle_log = f'Contraseña incorrecta para usuario: {username}{sufijo_intentos}'
            mensaje_usuario = "La contraseña es incorrecta"  # Sin contador, limpio para el usuario
            
            if self.log_controller:
                # Buscar si ya existe un log de login fallido reciente para este usuario
                ultimo_log = self.log_controller.obtener_ultimo_log_login_fallido(username)
                
                if ultimo_log and intentos > 1:
                    # Actualizar el log existente con el nuevo contador
                    self.log_controller.actualizar_log(
                        log_id=ultimo_log['id'],
                        nuevos_detalles=detalle_log
                    )
                else:
                    # Crear nuevo log (primer intento)
                    self.log_controller.registrar_log(
                        usuario_id=0,
                        usuario_nombre='Sistema',
                        accion='Login fallido',
                        detalles=detalle_log
                    )
            
            return False, mensaje_usuario
        
        elif codigo_error == 'success':
            # Login exitoso
            # Crear sesión
            self.token_sesion = Sesion.crear(usuario.id)
            self.usuario_actual = usuario
            
            # Registrar en auditoría
            AuditoriaLog.registrar(
                usuario_id=usuario.id,
                accion='login',
                resultado='exitoso'
            )
            
            # Registrar en logs del sistema
            if self.log_controller:
                self.log_controller.registrar_log(
                    usuario_id=usuario.id,
                    usuario_nombre=usuario.nombre_completo,
                    accion='Login exitoso',
                    detalles=f'Inicio de sesión exitoso: {usuario.username} ({usuario.rol})'
                )
            
            return True, f"Bienvenido {usuario.nombre_completo}"
        
        # Caso no esperado
        return False, "Error al procesar la autenticación"
    
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
