"""
Modelos para usuarios, sesiones y auditoría
"""
from datetime import datetime, timedelta
from typing import Optional, List
import bcrypt
import secrets
from database.user_connection import UserDatabaseConnection


class Usuario:
    """Modelo de Usuario"""
    
    def __init__(self, id: int, username: str, nombre_completo: str, rol: str,
                 es_superadmin: bool, puede_crear_usuarios: bool, activo: bool,
                 fecha_creacion: str, ultimo_acceso: Optional[str] = None):
        self.id = id
        self.username = username
        self.nombre_completo = nombre_completo
        self.rol = rol
        self.es_superadmin = bool(es_superadmin)
        self.puede_crear_usuarios = bool(puede_crear_usuarios)
        self.activo = bool(activo)
        self.fecha_creacion = fecha_creacion
        self.ultimo_acceso = ultimo_acceso
    
    @staticmethod
    def autenticar(username: str, password: str) -> Optional['Usuario']:
        """Autentica un usuario y retorna el objeto Usuario si es válido"""
        db = UserDatabaseConnection()
        conn = db.get_connection()
        cursor = conn.cursor()
        
        # Buscar usuario
        cursor.execute('''
            SELECT * FROM usuarios WHERE username = ? AND activo = 1
        ''', (username,))
        
        row = cursor.fetchone()
        if not row:
            return None
        
        # Verificar si está bloqueado
        if row['bloqueado_hasta']:
            bloqueado_hasta = datetime.fromisoformat(row['bloqueado_hasta'])
            if datetime.now() < bloqueado_hasta:
                return None
        
        # Verificar contraseña
        if not bcrypt.checkpw(password.encode('utf-8'), row['password_hash'].encode('utf-8')):
            # Incrementar intentos fallidos
            cursor.execute('''
                UPDATE usuarios 
                SET intentos_fallidos = intentos_fallidos + 1
                WHERE id = ?
            ''', (row['id'],))
            
            # Bloquear si excede 5 intentos
            if row['intentos_fallidos'] + 1 >= 5:
                bloqueado_hasta = datetime.now() + timedelta(minutes=15)
                cursor.execute('''
                    UPDATE usuarios 
                    SET bloqueado_hasta = ?
                    WHERE id = ?
                ''', (bloqueado_hasta.isoformat(), row['id']))
            
            conn.commit()
            return None
        
        # Resetear intentos fallidos y actualizar último acceso
        cursor.execute('''
            UPDATE usuarios 
            SET intentos_fallidos = 0, 
                bloqueado_hasta = NULL,
                ultimo_acceso = CURRENT_TIMESTAMP
            WHERE id = ?
        ''', (row['id'],))
        conn.commit()
        
        return Usuario(
            id=row['id'],
            username=row['username'],
            nombre_completo=row['nombre_completo'],
            rol=row['rol'],
            es_superadmin=row['es_superadmin'],
            puede_crear_usuarios=row['puede_crear_usuarios'],
            activo=row['activo'],
            fecha_creacion=row['fecha_creacion'],
            ultimo_acceso=row['ultimo_acceso']
        )
    
    @staticmethod
    def crear(username: str, password: str, nombre_completo: str, rol: str,
              creado_por_usuario_id: int) -> 'Usuario':
        """Crea un nuevo usuario"""
        db = UserDatabaseConnection()
        conn = db.get_connection()
        cursor = conn.cursor()
        
        # Hash de contraseña con bcrypt
        password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
        # Validar que el hash generado es correcto antes de guardarlo
        if not password_hash.startswith('$2b$') or len(password_hash) != 60:
            raise ValueError("Error generando hash de contraseña: formato inválido")
        
        # Verificar que el hash funciona correctamente
        if not bcrypt.checkpw(password.encode('utf-8'), password_hash.encode('utf-8')):
            raise ValueError("Error generando hash de contraseña: verificación falló")
        
        # Determinar permisos según rol
        puede_crear_usuarios = 1 if rol == 'superadmin' else 0
        es_superadmin = 1 if rol == 'superadmin' else 0
        
        cursor.execute('''
            INSERT INTO usuarios (
                username, password_hash, nombre_completo, rol,
                es_superadmin, puede_crear_usuarios, creado_por_usuario_id
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (username, password_hash, nombre_completo, rol,
              es_superadmin, puede_crear_usuarios, creado_por_usuario_id))
        
        conn.commit()
        
        return Usuario.obtener_por_id(cursor.lastrowid)
    
    @staticmethod
    def obtener_por_id(usuario_id: int) -> Optional['Usuario']:
        """Obtiene un usuario por ID"""
        db = UserDatabaseConnection()
        conn = db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM usuarios WHERE id = ?', (usuario_id,))
        row = cursor.fetchone()
        
        if not row:
            return None
        
        return Usuario(
            id=row['id'],
            username=row['username'],
            nombre_completo=row['nombre_completo'],
            rol=row['rol'],
            es_superadmin=row['es_superadmin'],
            puede_crear_usuarios=row['puede_crear_usuarios'],
            activo=row['activo'],
            fecha_creacion=row['fecha_creacion'],
            ultimo_acceso=row['ultimo_acceso']
        )
    
    @staticmethod
    def obtener_todos() -> List['Usuario']:
        """Obtiene todos los usuarios"""
        db = UserDatabaseConnection()
        conn = db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM usuarios ORDER BY fecha_creacion DESC')
        rows = cursor.fetchall()
        
        return [Usuario(
            id=row['id'],
            username=row['username'],
            nombre_completo=row['nombre_completo'],
            rol=row['rol'],
            es_superadmin=row['es_superadmin'],
            puede_crear_usuarios=row['puede_crear_usuarios'],
            activo=row['activo'],
            fecha_creacion=row['fecha_creacion'],
            ultimo_acceso=row['ultimo_acceso']
        ) for row in rows]
    
    @staticmethod
    def actualizar(usuario_id: int, nombre_completo: str = None, rol: str = None, activo: bool = None):
        """Actualiza un usuario. Solo actualiza los campos que no sean None."""
        db = UserDatabaseConnection()
        conn = db.get_connection()
        cursor = conn.cursor()
        
        # Construir la consulta dinámicamente solo con los campos proporcionados
        campos = []
        valores = []
        
        if nombre_completo is not None:
            campos.append("nombre_completo = ?")
            valores.append(nombre_completo)
        
        if rol is not None:
            campos.append("rol = ?")
            valores.append(rol)
        
        if activo is not None:
            campos.append("activo = ?")
            valores.append(1 if activo else 0)
        
        if not campos:
            return False
        
        valores.append(usuario_id)
        query = f"UPDATE usuarios SET {', '.join(campos)} WHERE id = ?"
        
        cursor.execute(query, valores)
        conn.commit()
        return True
    
    @staticmethod
    def cambiar_password(usuario_id: int, nueva_password: str):
        """Cambia la contraseña de un usuario"""
        db = UserDatabaseConnection()
        conn = db.get_connection()
        cursor = conn.cursor()
        
        # Generar hash con bcrypt
        password_hash = bcrypt.hashpw(nueva_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
        # Validar que el hash generado es correcto antes de guardarlo
        if not password_hash.startswith('$2b$') or len(password_hash) != 60:
            raise ValueError("Error generando hash de contraseña: formato inválido")
        
        # Verificar que el hash funciona correctamente
        if not bcrypt.checkpw(nueva_password.encode('utf-8'), password_hash.encode('utf-8')):
            raise ValueError("Error generando hash de contraseña: verificación falló")
        
        cursor.execute('''
            UPDATE usuarios 
            SET password_hash = ?
            WHERE id = ?
        ''', (password_hash, usuario_id))
        
        conn.commit()
        return True


class Sesion:
    """Modelo de Sesión"""
    
    @staticmethod
    def crear(usuario_id: int) -> str:
        """Crea una nueva sesión y retorna el token"""
        db = UserDatabaseConnection()
        conn = db.get_connection()
        cursor = conn.cursor()
        
        # Generar token único
        token = secrets.token_urlsafe(32)
        
        cursor.execute('''
            INSERT INTO sesiones (usuario_id, token_sesion)
            VALUES (?, ?)
        ''', (usuario_id, token))
        
        conn.commit()
        return token
    
    @staticmethod
    def validar(token: str) -> Optional[int]:
        """Valida un token y retorna el usuario_id si es válido"""
        db = UserDatabaseConnection()
        conn = db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT usuario_id FROM sesiones 
            WHERE token_sesion = ? AND activa = 1
        ''', (token,))
        
        row = cursor.fetchone()
        return row['usuario_id'] if row else None
    
    @staticmethod
    def cerrar(token: str):
        """Cierra una sesión"""
        db = UserDatabaseConnection()
        conn = db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE sesiones 
            SET activa = 0, fecha_fin = CURRENT_TIMESTAMP
            WHERE token_sesion = ?
        ''', (token,))
        
        conn.commit()


class AuditoriaLog:
    """Modelo de Log de Auditoría"""
    
    @staticmethod
    def registrar(usuario_id: int, accion: str, entidad_tipo: Optional[str] = None,
                  entidad_id: Optional[int] = None, datos_anteriores: Optional[str] = None,
                  datos_nuevos: Optional[str] = None, resultado: str = 'exitoso'):
        """Registra una acción en el log de auditoría"""
        db = UserDatabaseConnection()
        conn = db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO logs_auditoria (
                usuario_id, accion, entidad_tipo, entidad_id,
                datos_anteriores, datos_nuevos, resultado
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (usuario_id, accion, entidad_tipo, entidad_id,
              datos_anteriores, datos_nuevos, resultado))
        
        conn.commit()
    
    @staticmethod
    def obtener_por_usuario(usuario_id: int, limite: int = 100) -> List[dict]:
        """Obtiene los logs de un usuario específico"""
        db = UserDatabaseConnection()
        conn = db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM logs_auditoria 
            WHERE usuario_id = ?
            ORDER BY timestamp DESC
            LIMIT ?
        ''', (usuario_id, limite))
        
        return [dict(row) for row in cursor.fetchall()]
    
    @staticmethod
    def obtener_todos(limite: int = 500) -> List[dict]:
        """Obtiene todos los logs (solo superadmin)"""
        db = UserDatabaseConnection()
        conn = db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT l.*, u.username, u.nombre_completo
            FROM logs_auditoria l
            JOIN usuarios u ON l.usuario_id = u.id
            ORDER BY l.timestamp DESC
            LIMIT ?
        ''', (limite,))
        
        return [dict(row) for row in cursor.fetchall()]
