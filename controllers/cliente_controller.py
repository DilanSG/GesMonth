"""
Controlador para la lógica de negocio de Clientes
"""

from database.models import Cliente
from typing import Optional


class ClienteController:
    """Controlador para gestionar la lógica de clientes"""
    
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
            return Cliente.actualizar(
                cliente_id=cliente_id,
                nombre=nombre.strip(),
                documento=documento.strip(),
                telefono=telefono.strip(),
                valor_cuota=valor_cuota,
                estado=estado,
                dia_cobro=dia_cobro
            )
        
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
            return Cliente.eliminar(cliente_id)
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
