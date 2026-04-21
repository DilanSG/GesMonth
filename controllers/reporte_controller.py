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
        Exporta la lista de clientes a Excel con formato profesional.
        
        Utiliza pandas y openpyxl para crear un archivo Excel formateado:
        - Convierte datos de BD a DataFrame de pandas
        - Aplica formato a columnas (anchos personalizados)
        - Ajusta altura de filas para mejor legibilidad
        - Formatea encabezados en negrita y más altos
        
        Proceso de exportación:
        1. Obtener todos los clientes de la BD
        2. Transformar objetos Cliente a diccionarios
        3. Crear DataFrame de pandas con los datos
        4. Escribir a Excel usando ExcelWriter (motor openpyxl)
        5. Acceder al worksheet para aplicar formato visual
        6. Ajustar anchos de columnas según contenido esperado
        7. Ajustar alturas de filas (25px encabezado, 20px datos)
        8. Aplicar negrita al encabezado
        
        Ventajas de usar pandas + openpyxl:
        - pandas: manejo eficiente de datos tabulares
        - openpyxl: control fino del formato Excel
        - Archivos compatibles con Excel, LibreOffice, Google Sheets
        
        Args:
            file_path: Ruta completa donde guardar el archivo .xlsx
        
        Returns:
            True si la exportación fue exitosa
            False si ocurrió algún error (permisos, disco lleno, etc)
        
        Ejemplo:
        >>> controller.exportar_clientes('/home/user/clientes.xlsx')
        True
        """
        try:
            clientes = Cliente.obtener_todos()
            
            # Convertir objetos Cliente a diccionarios para pandas
            # Compresión de lista: transforma cada cliente en un dict con campos específicos
            data = [{
                'ID': c.id,
                'Nombre': c.nombre,
                'Documento': c.documento,
                'Teléfono': c.telefono or '',  # or '': manejar None como cadena vacía
                'Cuota Mensual': c.valor_cuota,
                'Día de Cobro': c.dia_cobro,
                'Estado': c.estado
            } for c in clientes]
            
            # DataFrame: estructura de datos tabular de pandas (similar a tabla SQL)
            df = pd.DataFrame(data)
            
            # Crear writer con formato mejorado usando openpyxl como motor
            # Context manager (with): garantiza cierre correcto del archivo
            with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
                # Escribir DataFrame a una hoja llamada 'Clientes'
                df.to_excel(writer, index=False, sheet_name='Clientes')
                
                # Obtener worksheet (hoja) para ajustar formato visual
                # openpyxl permite manipular el Excel a bajo nivel
                worksheet = writer.sheets['Clientes']
                
                # Ajustar ancho de columnas en puntos
                # Columnas más anchas para campos con más texto
                column_widths = {
                    'A': 8,   # ID (números cortos)
                    'B': 35,  # Nombre (texto largo)
                    'C': 18,  # Documento (11-13 dígitos)
                    'D': 15,  # Teléfono (10 dígitos)
                    'E': 15,  # Cuota Mensual (números con formato)
                    'F': 15,  # Día de Cobro (1-28)
                    'G': 12   # Estado (activo/inactivo)
                }
                
                for column, width in column_widths.items():
                    worksheet.column_dimensions[column].width = width
                
                # Ajustar altura de todas las filas de datos a 20 puntos
                for row in worksheet.iter_rows(min_row=1, max_row=worksheet.max_row):
                    worksheet.row_dimensions[row[0].row].height = 20
                
                # Hacer la fila de encabezado más alta (25pt) y en negrita
                worksheet.row_dimensions[1].height = 25
                for cell in worksheet[1]:  # worksheet[1] = primera fila
                    cell.font = cell.font.copy(bold=True)  # Clonar fuente y aplicar negrita
            
            return True
        
        except Exception as e:
            print(f"Error al exportar clientes: {e}")
            return False
    
    def importar_clientes(self, file_path: str) -> tuple[bool, str, int, int]:
        """
        Importa clientes desde un archivo Excel
        
        Args:
            file_path: Ruta del archivo a importar
        
        Returns:
            Tupla (exito, mensaje, insertados, actualizados)
        """
        try:
            # Leer Excel
            df = pd.read_excel(file_path, sheet_name='Clientes')
            
            # Validar columnas requeridas
            columnas_requeridas = ['Nombre', 'Documento', 'Cuota Mensual']
            columnas_faltantes = [col for col in columnas_requeridas if col not in df.columns]
            
            if columnas_faltantes:
                return (False, f"Faltan columnas requeridas: {', '.join(columnas_faltantes)}", 0, 0)
            
            insertados = 0
            actualizados = 0
            errores = []
            
            for index, row in df.iterrows():
                try:
                    # Validar datos obligatorios
                    if pd.isna(row['Nombre']) or not str(row['Nombre']).strip():
                        errores.append(f"Fila {index + 2}: Nombre vacío")
                        continue
                    
                    if pd.isna(row['Documento']) or not str(row['Documento']).strip():
                        errores.append(f"Fila {index + 2}: Documento vacío")
                        continue
                    
                    if pd.isna(row['Cuota Mensual']):
                        errores.append(f"Fila {index + 2}: Cuota Mensual vacía")
                        continue
                    
                    # Preparar datos
                    nombre = str(row['Nombre']).strip()
                    documento = str(row['Documento']).strip()
                    telefono = str(row.get('Teléfono', '')).strip() if not pd.isna(row.get('Teléfono')) else ''
                    valor_cuota = float(row['Cuota Mensual'])
                    dia_cobro = int(row.get('Día de Cobro', 5)) if not pd.isna(row.get('Día de Cobro')) else 5
                    estado = str(row.get('Estado', 'Activo')).strip().capitalize()
                    
                    # Validar estado
                    if estado not in ['Activo', 'Inactivo']:
                        estado = 'Activo'
                    
                    # Buscar si existe por documento
                    cliente_existente = None
                    todos_clientes = Cliente.obtener_todos()
                    for c in todos_clientes:
                        if c.documento == documento:
                            cliente_existente = c
                            break
                    
                    if cliente_existente:
                        # Actualizar cliente existente
                        from controllers.cliente_controller import ClienteController
                        controller = ClienteController()
                        if controller.actualizar_cliente(
                            cliente_existente.id,
                            nombre=nombre,
                            documento=documento,
                            telefono=telefono,
                            valor_cuota=valor_cuota,
                            dia_cobro=dia_cobro,
                            estado=estado
                        ):
                            actualizados += 1
                    else:
                        # Crear nuevo cliente
                        from controllers.cliente_controller import ClienteController
                        controller = ClienteController()
                        if controller.crear_cliente(
                            nombre=nombre,
                            documento=documento,
                            telefono=telefono,
                            valor_cuota=valor_cuota,
                            dia_cobro=dia_cobro,
                            estado=estado
                        ):
                            insertados += 1
                
                except Exception as e:
                    errores.append(f"Fila {index + 2}: {str(e)}")
                    continue
            
            # Generar mensaje de resultado
            if errores:
                mensaje = f"Procesados: {insertados} nuevos, {actualizados} actualizados\n\nErrores encontrados:\n" + "\n".join(errores[:5])
                if len(errores) > 5:
                    mensaje += f"\n... y {len(errores) - 5} errores más"
            else:
                mensaje = f"Importación exitosa:\n{insertados} clientes nuevos\n{actualizados} clientes actualizados"
            
            return (True, mensaje, insertados, actualizados)
        
        except Exception as e:
            return (False, f"Error al leer el archivo: {str(e)}", 0, 0)
    
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
