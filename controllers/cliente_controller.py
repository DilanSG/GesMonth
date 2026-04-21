"""
Controlador para la lógica de negocio de Clientes
"""

# Database: Modelo de datos de clientes
from database.models import Cliente  # Cliente: CRUD de clientes y validaciones

# Typing: Type hints para parámetros opcionales
from typing import Optional  # Optional: indica que un valor puede ser None


class ClienteController:
    """Controlador para gestionar la lógica de clientes"""
    
    def __init__(self):
        self.log_controller = None  # Se inyectará desde la UI
        self.usuario_actual = None
    
    def set_log_controller(self, log_controller):
        """Configura el controlador de logs"""
        self.log_controller = log_controller
    
    def set_usuario_actual(self, usuario):
        """Configura el usuario actual"""
        self.usuario_actual = usuario
    
    def crear_cliente(self, nombre: str, documento: str, 
                     telefono: str = "", valor_cuota: float = 0.0, 
                     estado: str = "activo", dia_cobro: int = 5) -> bool:
        """
        Crea un nuevo cliente con validaciones
        
        Args:
            nombre: Nombre del cliente
            documento: Documento de identidad
            telefono: Número de teléfono (opcional)
            valor_cuota: Valor de la cuota mensual
            estado: Estado del cliente (activo/inactivo)
            dia_cobro: Día del mes para cobro (1-28)
        
        Returns:
            True si se creó exitosamente, False en caso contrario
        """
        try:
            # Validaciones
            if not nombre or not nombre.strip():
                return False
            
            if not documento or not documento.strip():
                return False
            
            if valor_cuota < 0:
                return False
            
            if dia_cobro < 1 or dia_cobro > 28:
                dia_cobro = 5  # Valor por defecto si está fuera de rango
            
            # Crear cliente
            cliente_id = Cliente.crear(
                nombre=nombre.strip(),
                documento=documento.strip(),
                telefono=telefono.strip(),
                valor_cuota=valor_cuota,
                estado=estado,
                dia_cobro=dia_cobro
            )
            
            # Registrar log
            if cliente_id > 0 and self.log_controller and self.usuario_actual:
                self.log_controller.registrar_log(
                    usuario_id=self.usuario_actual.id if hasattr(self.usuario_actual, 'id') else None,
                    usuario_nombre=self.usuario_actual.username if hasattr(self.usuario_actual, 'username') else self.usuario_actual.nombre_completo if hasattr(self.usuario_actual, 'nombre_completo') else "Usuario",
                    accion='Crear Cliente',
                    detalles=f"Se registró un nuevo cliente con los siguientes datos: Nombre: {nombre}, CC: {documento} (para más detalles ver en la interfaz)"
                )
            
            return cliente_id > 0
        
        except Exception as e:
            error_msg = str(e)
            if "UNIQUE constraint failed" in error_msg and "documento" in error_msg:
                print(f"Error: Ya existe un cliente con el documento {documento}")
            else:
                print(f"Error al crear cliente: {e}")
            return False
    
    def actualizar_cliente(self, cliente_id: int, nombre: str, documento: str,
                          telefono: str = "", valor_cuota: float = 0.0,
                          estado: str = "activo", dia_cobro: int = 5) -> bool:
        """
        Actualiza los datos de un cliente
        
        Args:
            cliente_id: ID del cliente a actualizar
            nombre: Nuevo nombre
            documento: Nuevo documento
            telefono: Nuevo teléfono
            valor_cuota: Nuevo valor de la cuota
            estado: Nuevo estado
        
        Returns:
            True si se actualizó exitosamente, False en caso contrario
        """
        try:
            # Obtener datos anteriores para el log
            cliente_anterior = Cliente.obtener_por_id(cliente_id)
            
            # Validaciones
            if not nombre or not nombre.strip():
                return False
            
            if not documento or not documento.strip():
                return False
            
            if valor_cuota < 0:
                return False
            
            if dia_cobro < 1 or dia_cobro > 28:
                dia_cobro = 5  # Valor por defecto si está fuera de rango
            
            # Actualizar
            resultado = Cliente.actualizar(
                cliente_id=cliente_id,
                nombre=nombre.strip(),
                documento=documento.strip(),
                telefono=telefono.strip(),
                valor_cuota=valor_cuota,
                estado=estado,
                dia_cobro=dia_cobro
            )
            
            # Registrar log
            if resultado and self.log_controller and self.usuario_actual:
                cambios = []
                if cliente_anterior:
                    if cliente_anterior.nombre != nombre:
                        cambios.append(f"Nombre: {nombre}")
                    if cliente_anterior.documento != documento:
                        cambios.append(f"CC: {documento}")
                    if cliente_anterior.telefono != telefono:
                        cambios.append(f"Teléfono: {telefono}")
                    if cliente_anterior.valor_cuota != valor_cuota:
                        cambios.append(f"Cuota: ${valor_cuota:,.2f}")
                    if cliente_anterior.estado != estado:
                        cambios.append(f"Estado: {estado}")
                    if cliente_anterior.dia_cobro != dia_cobro:
                        cambios.append(f"Día de cobro: {dia_cobro}")
                
                if cambios:
                    detalles = f"Datos de cliente actualizados a: {', '.join(cambios)}"
                else:
                    detalles = f"Cliente {nombre} actualizado"
                
                self.log_controller.registrar_log(
                    usuario_id=self.usuario_actual.id if hasattr(self.usuario_actual, 'id') else None,
                    usuario_nombre=self.usuario_actual.username if hasattr(self.usuario_actual, 'username') else self.usuario_actual.nombre_completo if hasattr(self.usuario_actual, 'nombre_completo') else "Usuario",
                    accion='Editar Cliente',
                    detalles=detalles
                )
            
            return resultado
        
        except Exception as e:
            error_msg = str(e)
            if "UNIQUE constraint failed" in error_msg and "documento" in error_msg:
                print(f"Error: Ya existe otro cliente con el documento {documento}")
            else:
                print(f"Error al actualizar cliente: {e}")
            return False
    
    def eliminar_cliente(self, cliente_id: int) -> bool:
        """
        Elimina un cliente
        
        Args:
            cliente_id: ID del cliente a eliminar
        
        Returns:
            True si se eliminó exitosamente, False en caso contrario
        """
        try:
            # Obtener info del cliente antes de eliminarlo
            cliente = Cliente.obtener_por_id(cliente_id)
            
            resultado = Cliente.eliminar(cliente_id)
            
            # Registrar log
            if resultado and self.log_controller and self.usuario_actual:
                if cliente:
                    detalles = f"Se eliminó el cliente: {cliente.nombre}, CC: {cliente.documento}"
                else:
                    detalles = "Cliente eliminado"
                
                self.log_controller.registrar_log(
                    usuario_id=self.usuario_actual.id if hasattr(self.usuario_actual, 'id') else None,
                    usuario_nombre=self.usuario_actual.username if hasattr(self.usuario_actual, 'username') else self.usuario_actual.nombre_completo if hasattr(self.usuario_actual, 'nombre_completo') else "Usuario",
                    accion='Eliminar Cliente',
                    detalles=detalles
                )
            
            return resultado
        except Exception as e:
            print(f"Error al eliminar cliente: {e}")
            return False
    
    def obtener_cliente(self, cliente_id: int) -> Optional[Cliente]:
        """
        Obtiene un cliente por su ID
        
        Args:
            cliente_id: ID del cliente
        
        Returns:
            Objeto Cliente o None si no se encuentra
        """
        return Cliente.obtener_por_id(cliente_id)
    
    def validar_documento_unico(self, documento: str, excluir_id: Optional[int] = None) -> bool:
        """
        Valida que un documento no esté duplicado
        
        Args:
            documento: Documento a validar
            excluir_id: ID a excluir de la validación (para ediciones)
        
        Returns:
            True si el documento es único, False si ya existe
        """
        clientes = Cliente.obtener_todos()
        for cliente in clientes:
            if cliente.documento == documento and cliente.id != excluir_id:
                return False
        return True
