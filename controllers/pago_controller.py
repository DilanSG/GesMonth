"""
Controlador para la lógica de negocio de Pagos
"""

# Database: Modelos de datos relacionados con pagos
from database.models import Pago, Cliente, CuotaMensual  # Pago: registro de pagos, Cliente: info del cliente, CuotaMensual: estado de cuotas

# Typing: Type hints para estructuras de datos complejas
from typing import List, Dict, Any, Optional  # List: listas tipadas, Dict: diccionarios, Any: cualquier tipo, Optional: valores que pueden ser None

# Datetime: Manejo de fechas y tiempos
from datetime import datetime  # datetime: validación y formato de fechas


class PagoController:
    """Controlador para gestionar la lógica de pagos"""
    
    def __init__(self):
        self.log_controller = None  # Se inyectará desde la UI
        self.usuario_actual = None
    
    def set_log_controller(self, log_controller):
        """Configura el controlador de logs"""
        self.log_controller = log_controller
    
    def set_usuario_actual(self, usuario):
        """Configura el usuario actual"""
        self.usuario_actual = usuario
    
    def registrar_pago(self, cliente_id: int, fecha_pago: str,
                       mes_correspondiente: str, monto: float, 
                       metodo_pago: str = "Efectivo") -> bool:
        """
        Registra un nuevo pago con validaciones
        
        Args:
            cliente_id: ID del cliente que paga
            fecha_pago: Fecha del pago (YYYY-MM-DD)
            mes_correspondiente: Mes al que corresponde (YYYY-MM)
            monto: Monto del pago
            metodo_pago: Método de pago utilizado
        
        Returns:
            True si se registró exitosamente, False en caso contrario
        """
        try:
            # Validaciones
            if not self._validar_cliente_existe(cliente_id):
                print("El cliente no existe")
                return False
            
            if not self._validar_fecha(fecha_pago):
                print("Fecha inválida")
                return False
            
            if not self._validar_mes(mes_correspondiente):
                print("Mes inválido")
                return False
            
            if monto <= 0:
                print("El monto debe ser mayor a 0")
                return False
            
            # Obtener información del cliente
            cliente = Cliente.obtener_por_id(cliente_id)
            cliente_nombre = cliente.nombre if cliente else "Desconocido"
            
            # Registrar pago
            pago_id = Pago.crear(
                cliente_id=cliente_id,
                fecha_pago=fecha_pago,
                mes_correspondiente=mes_correspondiente,
                monto=monto
            )
            
            if pago_id > 0:
                # Sincronizar estado de cuotas
                periodo = datetime.strptime(mes_correspondiente, '%Y-%m')
                CuotaMensual.registrar_pago(
                    cliente_id=cliente_id,
                    año=periodo.year,
                    mes=periodo.month,
                    monto=monto,
                    metodo_pago=metodo_pago
                )
                
                # Registrar log
                if self.log_controller and self.usuario_actual:
                    self.log_controller.registrar_log(
                        usuario_id=self.usuario_actual.id if hasattr(self.usuario_actual, 'id') else None,
                        usuario_nombre=self.usuario_actual.username if hasattr(self.usuario_actual, 'username') else self.usuario_actual.nombre_completo if hasattr(self.usuario_actual, 'nombre_completo') else "Usuario",
                        accion='Registrar Pago',
                        modulo='pagos',
                        entidad_id=pago_id,
                        detalles=f"Cliente: {cliente_nombre} | Mes: {mes_correspondiente} | Monto: ${monto:,.2f} | Método: {metodo_pago}"
                    )
            
            return pago_id > 0
        
        except Exception as e:
            print(f"Error al registrar pago: {e}")
            return False
    
    def eliminar_pago(self, pago_id: int) -> bool:
        """
        Elimina un pago
        
        Args:
            pago_id: ID del pago a eliminar
        
        Returns:
            True si se eliminó exitosamente, False en caso contrario
        """
        try:
            # Obtener información del pago antes de eliminarlo
            from database.connection import DatabaseConnection
            db = DatabaseConnection()
            conn = db.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT p.*, c.nombre as cliente_nombre 
                FROM pagos p 
                LEFT JOIN clientes c ON p.cliente_id = c.id 
                WHERE p.id = ?
            ''', (pago_id,))
            
            pago_info = cursor.fetchone()
            
            resultado = Pago.eliminar(pago_id)
            
            # Registrar log
            if resultado and self.log_controller and self.usuario_actual:
                detalles = "Pago eliminado"
                if pago_info:
                    detalles = f"Cliente: {pago_info['cliente_nombre']} | Mes: {pago_info['mes_correspondiente']} | Monto: ${pago_info['monto']:,.2f}"
                
                self.log_controller.registrar_log(
                    usuario_id=self.usuario_actual.id if hasattr(self.usuario_actual, 'id') else None,
                    usuario_nombre=self.usuario_actual.username if hasattr(self.usuario_actual, 'username') else self.usuario_actual.nombre_completo if hasattr(self.usuario_actual, 'nombre_completo') else "Usuario",
                    accion='Eliminar Pago',
                    modulo='pagos',
                    entidad_id=pago_id,
                    detalles=detalles
                )
            
            return resultado
        except Exception as e:
            print(f"Error al eliminar pago: {e}")
            return False
    
    def registrar_impago(self, cliente_id: int, mes_correspondiente: str) -> bool:
        """
        Registra un impago para un cliente en un mes específico
        
        Args:
            cliente_id: ID del cliente
            mes_correspondiente: Mes del impago (YYYY-MM)
        
        Returns:
            True si se registró exitosamente
        """
        try:
            cliente = Cliente.obtener_por_id(cliente_id)
            if not cliente:
                return False
            
            periodo = datetime.strptime(mes_correspondiente, '%Y-%m')
            
            # Marcar como impago en cuotas
            CuotaMensual.marcar_impago(
                cliente_id=cliente_id,
                año=periodo.year,
                mes=periodo.month
            )
            
            # Registrar log
            if self.log_controller and self.usuario_actual:
                self.log_controller.registrar_log(
                    usuario_id=self.usuario_actual.id if hasattr(self.usuario_actual, 'id') else None,
                    usuario_nombre=self.usuario_actual.username if hasattr(self.usuario_actual, 'username') else self.usuario_actual.nombre_completo if hasattr(self.usuario_actual, 'nombre_completo') else "Usuario",
                    accion='Registrar Impago',
                    modulo='pagos',
                    entidad_id=cliente_id,
                    detalles=f"Cliente: {cliente.nombre} | Mes: {mes_correspondiente}"
                )
            
            return True
        except Exception as e:
            print(f"Error al registrar impago: {e}")
            return False
    
    def registrar_pago_parcial(self, cliente_id: int, fecha_pago: str,
                              mes_correspondiente: str, monto: float, 
                              monto_total: float, metodo_pago: str = "Efectivo") -> bool:
        """
        Registra un pago parcial
        
        Args:
            cliente_id: ID del cliente
            fecha_pago: Fecha del pago
            mes_correspondiente: Mes al que corresponde
            monto: Monto pagado
            monto_total: Monto total de la cuota
            metodo_pago: Método de pago
        
        Returns:
            True si se registró exitosamente
        """
        try:
            cliente = Cliente.obtener_por_id(cliente_id)
            if not cliente:
                return False
            
            # Registrar el pago parcial
            pago_id = Pago.crear(
                cliente_id=cliente_id,
                fecha_pago=fecha_pago,
                mes_correspondiente=mes_correspondiente,
                monto=monto
            )
            
            if pago_id > 0:
                periodo = datetime.strptime(mes_correspondiente, '%Y-%m')
                CuotaMensual.registrar_pago(
                    cliente_id=cliente_id,
                    año=periodo.year,
                    mes=periodo.month,
                    monto=monto,
                    metodo_pago=metodo_pago
                )
                
                # Registrar log
                if self.log_controller and self.usuario_actual:
                    porcentaje = (monto / monto_total) * 100
                    self.log_controller.registrar_log(
                        usuario_id=self.usuario_actual.id if hasattr(self.usuario_actual, 'id') else None,
                        usuario_nombre=self.usuario_actual.username if hasattr(self.usuario_actual, 'username') else self.usuario_actual.nombre_completo if hasattr(self.usuario_actual, 'nombre_completo') else "Usuario",
                        accion='Pago Parcial',
                        modulo='pagos',
                        entidad_id=pago_id,
                        detalles=f"Cliente: {cliente.nombre} | Mes: {mes_correspondiente} | Pagado: ${monto:,.2f} de ${monto_total:,.2f} ({porcentaje:.1f}%) | Método: {metodo_pago}"
                    )
                
                return True
            
            return False
        except Exception as e:
            print(f"Error al registrar pago parcial: {e}")
            return False

    
    def obtener_historial_cliente(self, cliente_id: int) -> List[Dict[str, Any]]:
        """
        Obtiene el historial de pagos de un cliente
        
        Args:
            cliente_id: ID del cliente
        
        Returns:
            Lista de pagos del cliente
        """
        return Pago.obtener_por_cliente(cliente_id)
    
    def verificar_pago_mes(self, cliente_id: int, mes: str) -> bool:
        """
        Verifica si un cliente ya realizó un pago en un mes específico.
        
        Esta función es útil para:
        - Prevenir pagos duplicados del mismo mes
        - Validar antes de registrar un nuevo pago
        - Mostrar estado de pago en interfaces
        
        Algoritmo:
        1. Obtener todos los pagos del cliente de la BD
        2. Iterar sobre cada pago
        3. Comparar el campo 'mes_correspondiente' con el mes buscado
        4. Retornar True al primer match (búsqueda lineal con salida temprana)
        
        Nota: El formato de mes debe ser 'YYYY-MM' (ej: '2025-01')
        
        Args:
            cliente_id: ID del cliente a verificar
            mes: Mes a verificar en formato 'YYYY-MM'
        
        Returns:
            True si el cliente ya tiene un pago registrado para ese mes
            False si no tiene pagos o ninguno corresponde a ese mes
        
        Ejemplo:
        >>> controller.verificar_pago_mes(5, '2025-01')
        True  # El cliente 5 ya pagó enero 2025
        """
        pagos = Pago.obtener_por_cliente(cliente_id)
        for pago in pagos:
            if pago['mes_correspondiente'] == mes:
                return True
        return False
    
    def _validar_cliente_existe(self, cliente_id: int) -> bool:
        """Valida que el cliente exista"""
        cliente = Cliente.obtener_por_id(cliente_id)
        return cliente is not None
    
    def _validar_fecha(self, fecha: str) -> bool:
        """Valida el formato de fecha YYYY-MM-DD"""
        try:
            datetime.strptime(fecha, '%Y-%m-%d')
            return True
        except ValueError:
            return False
    
    def _validar_mes(self, mes: str) -> bool:
        """Valida el formato de mes YYYY-MM"""
        try:
            datetime.strptime(mes, '%Y-%m')
            return True
        except ValueError:
            return False
