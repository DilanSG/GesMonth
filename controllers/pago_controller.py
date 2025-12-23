"""
Controlador para la lógica de negocio de Pagos
"""

from database.models import Pago, Cliente, CuotaMensual
from typing import List, Dict, Any
from datetime import datetime


class PagoController:
    """Controlador para gestionar la lógica de pagos"""
    
    def registrar_pago(self, cliente_id: int, fecha_pago: str,
                       mes_correspondiente: str, monto: float) -> bool:
        """
        Registra un nuevo pago con validaciones
        
        Args:
            cliente_id: ID del cliente que paga
            fecha_pago: Fecha del pago (YYYY-MM-DD)
            mes_correspondiente: Mes al que corresponde (YYYY-MM)
            monto: Monto del pago
        
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
                    metodo_pago="Pago registrado"
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
            return Pago.eliminar(pago_id)
        except Exception as e:
            print(f"Error al eliminar pago: {e}")
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
        Verifica si un cliente ya pagó en un mes específico
        
        Args:
            cliente_id: ID del cliente
            mes: Mes a verificar (YYYY-MM)
        
        Returns:
            True si ya pagó, False si no
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
