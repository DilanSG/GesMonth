"""
Controlador para la generación de reportes
"""

from database.models import Pago, Cliente
from datetime import datetime
from typing import List, Dict, Any
import pandas as pd


class ReporteController:
    """Controlador para generar reportes y exportaciones"""
    
    def exportar_clientes(self, file_path: str) -> bool:
        """
        Exporta la lista de clientes a Excel
        
        Args:
            file_path: Ruta del archivo a guardar
        
        Returns:
            True si se exportó exitosamente, False en caso contrario
        """
        try:
            clientes = Cliente.obtener_todos()
            
            # Convertir a DataFrame
            data = [{
                'ID': c.id,
                'Nombre': c.nombre,
                'Documento': c.documento,
                'Teléfono': c.telefono,
                'Cuota Mensual': c.valor_cuota,
                'Estado': c.estado
            } for c in clientes]
            
            df = pd.DataFrame(data)
            
            # Guardar a Excel
            df.to_excel(file_path, index=False, sheet_name='Clientes')
            return True
        
        except Exception as e:
            print(f"Error al exportar clientes: {e}")
            return False
    
    def exportar_pagos(self, file_path: str) -> bool:
        """
        Exporta el historial de pagos a Excel
        
        Args:
            file_path: Ruta del archivo a guardar
        
        Returns:
            True si se exportó exitosamente, False en caso contrario
        """
        try:
            pagos = Pago.obtener_todos()
            
            # Convertir a DataFrame
            data = [{
                'ID': p['id'],
                'Cliente': p['cliente_nombre'],
                'Documento': p['documento'],
                'Fecha Pago': p['fecha_pago'],
                'Mes Correspondiente': p['mes_correspondiente'],
                'Monto': p['monto']
            } for p in pagos]
            
            df = pd.DataFrame(data)
            
            # Guardar a Excel
            df.to_excel(file_path, index=False, sheet_name='Pagos')
            return True
        
        except Exception as e:
            print(f"Error al exportar pagos: {e}")
            return False
    
    def exportar_mora(self, file_path: str) -> bool:
        """
        Exporta los clientes en mora a Excel
        
        Args:
            file_path: Ruta del archivo a guardar
        
        Returns:
            True si se exportó exitosamente, False en caso contrario
        """
        try:
            clientes_mora = self._obtener_clientes_mora()
            
            # Convertir a DataFrame
            data = [{
                'ID': c['id'],
                'Nombre': c['nombre'],
                'Documento': c['documento'],
                'Teléfono': c['telefono'],
                'Último Pago': c['ultimo_pago'] or 'Sin pagos'
            } for c in clientes_mora]
            
            df = pd.DataFrame(data)
            
            # Guardar a Excel
            df.to_excel(file_path, index=False, sheet_name='Clientes en Mora')
            return True
        
        except Exception as e:
            print(f"Error al exportar clientes en mora: {e}")
            return False
    
    def _obtener_clientes_mora(self) -> List[Dict[str, Any]]:
        """
        Obtiene la lista de clientes que no han pagado el mes actual
        
        Returns:
            Lista de clientes en mora
        """
        mes_actual = datetime.now().strftime('%Y-%m')
        clientes = Cliente.obtener_todos()
        clientes_mora = []
        
        for cliente in clientes:
            if cliente.estado != 'activo':
                continue
            
            pagos = Pago.obtener_por_cliente(cliente.id)
            pago_mes_actual = False
            ultimo_pago = None
            
            for pago in pagos:
                if pago['mes_correspondiente'] == mes_actual:
                    pago_mes_actual = True
                    break
                
                # Guardar el pago más reciente
                if ultimo_pago is None or pago['fecha_pago'] > ultimo_pago:
                    ultimo_pago = pago['fecha_pago']
            
            # Si no pagó este mes, está en mora
            if not pago_mes_actual:
                clientes_mora.append({
                    'id': cliente.id,
                    'nombre': cliente.nombre,
                    'documento': cliente.documento,
                    'telefono': cliente.telefono,
                    'ultimo_pago': ultimo_pago
                })
        
        return clientes_mora
