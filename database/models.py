"""
Modelos de datos para Clientes, Pagos, Cuotas y Métodos de Pago
"""

# Datetime: Manejo de fechas y tiempos para registros
from datetime import datetime  # datetime: timestamps de creación y modificación

# Typing: Type hints para estructuras de datos complejas
from typing import List, Optional, Dict, Any  # List: listas, Optional: valores opcionales, Dict: diccionarios, Any: cualquier tipo

# Database: Conexión a la base de datos
from .connection import DatabaseConnection  # DatabaseConnection: acceso a la base de datos SQLite


class Cliente:
    """Modelo para gestionar clientes"""
    
    def __init__(self, id: Optional[int] = None, nombre: str = "", 
                 documento: str = "", telefono: str = "", estado: str = "activo", 
                 valor_cuota: float = 0.0, dia_cobro: int = 5):
        self.id = id
        self.nombre = nombre
        self.documento = documento
        self.telefono = telefono
        self.estado = estado
        self.valor_cuota = valor_cuota
        self.dia_cobro = dia_cobro
    
    @staticmethod
    def crear(nombre: str, documento: str, telefono: str = "", estado: str = "activo", 
              valor_cuota: float = 0.0, dia_cobro: int = 5) -> int:
        """Crea un nuevo cliente en la base de datos"""
        db = DatabaseConnection()
        conn = db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO clientes (nombre, documento, telefono, estado, valor_cuota, dia_cobro)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (nombre, documento, telefono, estado, valor_cuota, dia_cobro))
        
        conn.commit()
        return cursor.lastrowid
    
    @staticmethod
    def obtener_todos() -> List['Cliente']:
        """Obtiene todos los clientes"""
        db = DatabaseConnection()
        conn = db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM clientes ORDER BY nombre')
        rows = cursor.fetchall()
        
        return [Cliente(
            id=row['id'],
            nombre=row['nombre'],
            documento=row['documento'],
            telefono=row['telefono'],
            estado=row['estado'],
            valor_cuota=row['valor_cuota'],
            dia_cobro=row['dia_cobro'] if 'dia_cobro' in row.keys() else 5
        ) for row in rows]
    
    @staticmethod
    def obtener_por_id(cliente_id: int) -> Optional['Cliente']:
        """Obtiene un cliente por su ID"""
        db = DatabaseConnection()
        conn = db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM clientes WHERE id = ?', (cliente_id,))
        row = cursor.fetchone()
        
        if row:
            return Cliente(
                id=row['id'],
                nombre=row['nombre'],
                documento=row['documento'],
                telefono=row['telefono'],
                estado=row['estado'],
                valor_cuota=row['valor_cuota'],
                dia_cobro=row['dia_cobro'] if 'dia_cobro' in row.keys() else 5
            )
        return None
    
    @staticmethod
    def actualizar(cliente_id: int, nombre: str, documento: str, 
                   telefono: str = "", estado: str = "activo", valor_cuota: float = 0.0,
                   dia_cobro: int = 5) -> bool:
        """Actualiza los datos de un cliente"""
        db = DatabaseConnection()
        conn = db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE clientes 
            SET nombre = ?, documento = ?, telefono = ?, estado = ?, valor_cuota = ?, dia_cobro = ?
            WHERE id = ?
        ''', (nombre, documento, telefono, estado, valor_cuota, dia_cobro, cliente_id))
        
        conn.commit()
        return cursor.rowcount > 0
    
    @staticmethod
    def eliminar(cliente_id: int) -> bool:
        """Elimina un cliente y todos sus registros relacionados"""
        db = DatabaseConnection()
        conn = db.get_connection()
        cursor = conn.cursor()
        
        # Eliminar pagos del cliente
        cursor.execute('DELETE FROM pagos WHERE cliente_id = ?', (cliente_id,))
        pagos_eliminados = cursor.rowcount
        
        # Eliminar cuotas del cliente
        cursor.execute('DELETE FROM cuotas_mensuales WHERE cliente_id = ?', (cliente_id,))
        cuotas_eliminadas = cursor.rowcount
        
        # Eliminar cliente
        cursor.execute('DELETE FROM clientes WHERE id = ?', (cliente_id,))
        
        # Cliente eliminado: {pagos_eliminados} pago(s), {cuotas_eliminadas} cuota(s)
        
        conn.commit()
        return cursor.rowcount > 0
    
    @staticmethod
    def buscar(termino: str) -> List['Cliente']:
        """Busca clientes por nombre o documento"""
        db = DatabaseConnection()
        conn = db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM clientes 
            WHERE nombre LIKE ? OR documento LIKE ?
            ORDER BY nombre
        ''', (f'%{termino}%', f'%{termino}%'))
        
        rows = cursor.fetchall()
        
        return [Cliente(
            id=row['id'],
            nombre=row['nombre'],
            documento=row['documento'],
            telefono=row['telefono'],
            estado=row['estado'],
            valor_cuota=row['valor_cuota'],
            dia_cobro=row['dia_cobro'] if 'dia_cobro' in row.keys() else 5
        ) for row in rows]


class Pago:
    """Modelo para gestionar pagos"""
    
    def __init__(self, id: Optional[int] = None, cliente_id: int = 0, 
                 fecha_pago: str = "", mes_correspondiente: str = "", monto: float = 0.0):
        self.id = id
        self.cliente_id = cliente_id
        self.fecha_pago = fecha_pago
        self.mes_correspondiente = mes_correspondiente
        self.monto = monto
    
    @staticmethod
    def crear(cliente_id: int, fecha_pago: str, mes_correspondiente: str, monto: float) -> int:
        """Registra un nuevo pago"""
        db = DatabaseConnection()
        conn = db.get_connection()
        cursor = conn.cursor()
        
        # Verificar si ya existe un pago para este cliente y mes con el mismo monto
        # (para evitar duplicados por doble click)
        cursor.execute('''
            SELECT id FROM pagos 
            WHERE cliente_id = ? 
            AND mes_correspondiente = ? 
            AND monto = ?
            AND datetime(fecha_pago) > datetime('now', '-5 seconds')
        ''', (cliente_id, mes_correspondiente, monto))
        
        existe = cursor.fetchone()
        if existe:
            # Duplicado detectado, se retorna el ID existente sin crear uno nuevo
            return existe['id']
        
        cursor.execute('''
            INSERT INTO pagos (cliente_id, fecha_pago, mes_correspondiente, monto)
            VALUES (?, ?, ?, ?)
        ''', (cliente_id, fecha_pago, mes_correspondiente, monto))
        
        conn.commit()
        return cursor.lastrowid
    
    @staticmethod
    def obtener_todos() -> List[Dict[str, Any]]:
        """Obtiene todos los pagos con información del cliente"""
        db = DatabaseConnection()
        conn = db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT p.*, c.nombre as cliente_nombre, c.documento
            FROM pagos p
            INNER JOIN clientes c ON p.cliente_id = c.id
            ORDER BY p.fecha_pago DESC
        ''')
        
        return [dict(row) for row in cursor.fetchall()]
    
    @staticmethod
    def obtener_por_cliente(cliente_id: int) -> List[Dict[str, Any]]:
        """Obtiene el historial de pagos de un cliente"""
        db = DatabaseConnection()
        conn = db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM pagos 
            WHERE cliente_id = ?
            ORDER BY fecha_pago DESC
        ''', (cliente_id,))
        
        return [dict(row) for row in cursor.fetchall()]
    
    @staticmethod
    def eliminar(pago_id: int) -> bool:
        """Elimina un pago"""
        db = DatabaseConnection()
        conn = db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM pagos WHERE id = ?', (pago_id,))
        conn.commit()
        return cursor.rowcount > 0
    
    @staticmethod
    def eliminar_duplicados() -> int:
        """
        Elimina pagos duplicados manteniendo solo el primero de cada grupo.
        
        Lógica de eliminación:
        - Considera duplicados: mismo cliente_id, mes_correspondiente y monto
        - Mantiene el registro con el ID más bajo (el más antiguo)
        - Elimina el resto de registros duplicados
        
        Funcionamiento de la consulta SQL:
        1. Subconsulta: SELECT MIN(id) FROM pagos GROUP BY ...
           - Agrupa pagos por cliente, mes y monto
           - Para cada grupo, obtiene el ID mánimo (más antiguo)
        2. Consulta principal: DELETE FROM pagos WHERE id NOT IN (...)
           - Elimina todos los IDs que NO estén en la lista de IDs mínimos
           - Resultado: solo quedan los registros más antiguos de cada grupo
        
        Ejemplo:
        Si existen 3 pagos idénticos con IDs 10, 15, 20
        - MIN(id) retorna 10
        - Se eliminan los IDs 15 y 20
        - Solo permanece el ID 10
        
        Returns:
            Número de registros duplicados eliminados
        """
        db = DatabaseConnection()
        conn = db.get_connection()
        cursor = conn.cursor()
        
        # Encontrar duplicados (mismo cliente, mes y monto)
        cursor.execute('''
            DELETE FROM pagos
            WHERE id NOT IN (
                SELECT MIN(id)
                FROM pagos
                GROUP BY cliente_id, mes_correspondiente, monto
            )
        ''')
        
        eliminados = cursor.rowcount
        conn.commit()
        # Pagos duplicados eliminados: {eliminados}
        return eliminados
    
    @staticmethod
    def obtener_estadisticas() -> Dict[str, Any]:
        """Obtiene estadísticas generales de pagos"""
        db = DatabaseConnection()
        conn = db.get_connection()
        cursor = conn.cursor()
        
        # Total recaudado este mes
        mes_actual = datetime.now().strftime('%Y-%m')
        cursor.execute('''
            SELECT COALESCE(SUM(monto), 0) as total
            FROM pagos
            WHERE fecha_pago LIKE ?
        ''', (f'{mes_actual}%',))
        
        total_mes = cursor.fetchone()['total']
        
        # Total de clientes
        cursor.execute('SELECT COUNT(*) as total FROM clientes WHERE estado = "activo"')
        total_clientes = cursor.fetchone()['total']
        
        # Clientes que pagaron este mes
        cursor.execute('''
            SELECT COUNT(DISTINCT cliente_id) as total
            FROM pagos
            WHERE mes_correspondiente = ?
        ''', (datetime.now().strftime('%Y-%m'),))
        
        clientes_pagaron = cursor.fetchone()['total']
        
        return {
            'total_mes': total_mes,
            'total_clientes': total_clientes,
            'clientes_pagaron': clientes_pagaron,
            'clientes_mora': total_clientes - clientes_pagaron
        }


class MetodoPago:
    """Modelo para gestionar métodos de pago"""
    
    def __init__(self, id: Optional[int] = None, nombre: str = "", activo: bool = True, color: str = "#3b82f6"):
        self.id = id
        self.nombre = nombre
        self.activo = activo
        self.color = color
    
    @staticmethod
    def crear(nombre: str, color: str = "#3b82f6") -> int:
        """Crea un nuevo método de pago"""
        db = DatabaseConnection()
        conn = db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO metodos_pago (nombre, activo, color)
            VALUES (?, 1, ?)
        ''', (nombre, color))
        
        conn.commit()
        return cursor.lastrowid
    
    @staticmethod
    def obtener_todos() -> List['MetodoPago']:
        """Obtiene todos los métodos de pago"""
        db = DatabaseConnection()
        conn = db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM metodos_pago ORDER BY nombre')
        rows = cursor.fetchall()
        
        return [MetodoPago(
            id=row['id'],
            nombre=row['nombre'],
            activo=bool(row['activo']),
            color=row['color'] if 'color' in row.keys() else '#3b82f6'
        ) for row in rows]
    
    @staticmethod
    def obtener_activos() -> List['MetodoPago']:
        """Obtiene los métodos de pago activos"""
        db = DatabaseConnection()
        conn = db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM metodos_pago WHERE activo = 1 ORDER BY nombre')
        rows = cursor.fetchall()
        
        return [MetodoPago(
            id=row['id'],
            nombre=row['nombre'],
            activo=True,
            color=row['color'] if 'color' in row.keys() else '#3b82f6'
        ) for row in rows]
    
    @staticmethod
    def actualizar(metodo_id: int, nombre: str, activo: bool = True, color: str = "#3b82f6") -> bool:
        """Actualiza un método de pago"""
        db = DatabaseConnection()
        conn = db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE metodos_pago 
            SET nombre = ?, activo = ?, color = ?
            WHERE id = ?
        ''', (nombre, 1 if activo else 0, color, metodo_id))
        
        conn.commit()
        return cursor.rowcount > 0
    
    @staticmethod
    def eliminar(metodo_id: int) -> bool:
        """Elimina un método de pago"""
        db = DatabaseConnection()
        conn = db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM metodos_pago WHERE id = ?', (metodo_id,))
        conn.commit()
        return cursor.rowcount > 0


class CuotaMensual:
    """Modelo para gestionar cuotas mensuales"""
    
    def __init__(self, id: Optional[int] = None, cliente_id: int = 0, año: int = 0,
                 mes: int = 0, estado: str = "pendiente", monto: float = 0.0,
                 metodo_pago: Optional[str] = None, fecha_registro: Optional[str] = None,
                 fecha_inicio_mora: Optional[str] = None, deuda_acumulada: float = 0.0):
        self.id = id
        self.cliente_id = cliente_id
        self.año = año
        self.mes = mes
        self.estado = estado  # 'pendiente', 'pagado', 'impago', 'con_deuda'
        self.monto = monto
        self.metodo_pago = metodo_pago
        self.fecha_registro = fecha_registro
        self.fecha_inicio_mora = fecha_inicio_mora
        self.deuda_acumulada = deuda_acumulada
    
    @staticmethod
    def registrar_pago(cliente_id: int, año: int, mes: int, monto: float, metodo_pago: str, 
                       monto_pagado: Optional[float] = None, deuda_previa: Optional[float] = None,
                       fecha_inicio_mora: Optional[str] = None) -> int:
        """
        Registra el pago de una cuota (total o parcial) con cálculo de deuda.
        
        Esta función maneja toda la lógica de pagos incluyendo:
        - Pagos completos (liquidan toda la deuda)
        - Pagos parciales (dejan deuda pendiente)
        - Acumulación de deudas previas
        - Generación automática de fechas de mora
        
        Proceso de cálculo:
        1. Recuperar día de cobro del cliente (default: 5)
        2. Buscar deuda acumulada previa de este mes (si existe)
        3. Calcular deuda total = monto de cuota + deuda previa
        4. Determinar si el pago es completo o parcial:
           - Completo: monto_pagado >= deuda_total → estado 'pagado', deuda = 0
           - Parcial: monto_pagado < deuda_total → estado 'con_deuda', deuda > 0
        5. Generar fecha_inicio_mora si no existe (para cálculos de mora)
        
        Ejemplo de uso:
        - Cliente tiene cuota de $100 del mes actual
        - Tiene deuda previa de $50 de meses anteriores
        - Deuda total = $150
        - Si paga $100: queda deuda de $50 (pago parcial)
        - Si paga $150: queda deuda de $0 (pago completo)
        
        Args:
            cliente_id: ID del cliente que realiza el pago
            año: Año de la cuota (ej: 2025)
            mes: Mes de la cuota (1-12)
            monto: Monto base de la cuota mensual
            metodo_pago: Método usado (Efectivo, Transferencia, etc)
            monto_pagado: Cantidad efectivamente pagada (None = pago completo)
            deuda_previa: Deuda acumulada anterior (None = buscar en BD)
            fecha_inicio_mora: Fecha desde que empezó la mora (None = generar)
        
        Returns:
            ID del registro de cuota creado/actualizado
        """
        db = DatabaseConnection()
        conn = db.get_connection()
        cursor = conn.cursor()
        
        fecha_actual = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Obtener día de cobro del cliente para generar fecha de mora si es necesario
        cursor.execute('SELECT dia_cobro FROM clientes WHERE id = ?', (cliente_id,))
        cliente_row = cursor.fetchone()
        dia_cobro = cliente_row['dia_cobro'] if cliente_row and 'dia_cobro' in cliente_row.keys() else 5
        
        # Si se proporciona deuda_previa, usarla; si no, buscar en la BD
        if deuda_previa is None:
            cursor.execute('''
                SELECT deuda_acumulada, fecha_inicio_mora FROM cuotas_mensuales
                WHERE cliente_id = ? AND año = ? AND mes = ?
            ''', (cliente_id, año, mes))
            
            row = cursor.fetchone()
            if row:
                deuda_previa = row['deuda_acumulada'] if 'deuda_acumulada' in row.keys() else 0.0
                if fecha_inicio_mora is None:
                    fecha_inicio_mora = row['fecha_inicio_mora'] if 'fecha_inicio_mora' in row.keys() else None
            else:
                deuda_previa = 0.0
        
        # Si no se especifica monto pagado, se asume pago completo
        if monto_pagado is None:
            monto_pagado = monto + deuda_previa
        
        deuda_total = monto + deuda_previa
        
        if monto_pagado >= deuda_total:
            # Pago completo - limpiar toda la deuda
            cursor.execute('''
                INSERT OR REPLACE INTO cuotas_mensuales 
                (cliente_id, año, mes, estado, monto, metodo_pago, fecha_registro, deuda_acumulada, fecha_inicio_mora)
                VALUES (?, ?, ?, 'pagado', ?, ?, ?, 0.0, NULL)
            ''', (cliente_id, año, mes, monto, metodo_pago, fecha_actual))
        else:
            # Pago parcial - queda deuda
            deuda_restante = deuda_total - monto_pagado
            
            # Si no había fecha de inicio de mora previa, generarla ahora usando la fecha del mes que se está pagando
            # (esto pasa cuando se hace un pago parcial en un mes sin mora previa)
            if fecha_inicio_mora is None:
                fecha_inicio_mora = f"{año}-{mes:02d}-{dia_cobro:02d} 00:00:00"
            
            cursor.execute('''
                INSERT OR REPLACE INTO cuotas_mensuales 
                (cliente_id, año, mes, estado, monto, metodo_pago, fecha_registro, deuda_acumulada, fecha_inicio_mora)
                VALUES (?, ?, ?, 'con_deuda', ?, ?, ?, ?, ?)
            ''', (cliente_id, año, mes, monto, metodo_pago, fecha_actual, deuda_restante, fecha_inicio_mora))
        
        conn.commit()
        return cursor.lastrowid
    
    @staticmethod
    def registrar_impago(cliente_id: int, año: int, mes: int, monto: float,
                        deuda_previa: Optional[float] = None, fecha_inicio_mora: Optional[str] = None) -> int:
        """Registra la falta de pago de una cuota"""
        db = DatabaseConnection()
        conn = db.get_connection()
        cursor = conn.cursor()
        
        fecha_actual = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # IMPORTANTE: Eliminar pagos asociados a este mes antes de marcar como impago
        mes_correspondiente = f"{año}-{mes:02d}"
        cursor.execute('''
            DELETE FROM pagos 
            WHERE cliente_id = ? AND mes_correspondiente = ?
        ''', (cliente_id, mes_correspondiente))
        
        eliminados = cursor.rowcount
        # Eliminados {eliminados} pago(s) al marcar como impago
        
        # Si no se proporciona fecha_inicio_mora, generarla para este mes/año específico
        if fecha_inicio_mora is None:
            # Obtener día de cobro del cliente
            cursor.execute('SELECT dia_cobro FROM clientes WHERE id = ?', (cliente_id,))
            cliente_row = cursor.fetchone()
            dia_cobro = cliente_row['dia_cobro'] if cliente_row else 5
            
            # Crear fecha con el año y mes de la cuota (nueva cadena de mora)
            fecha_inicio_mora = f"{año}-{mes:02d}-{dia_cobro:02d}"
        
        # Si no se proporciona deuda_previa, usar 0
        if deuda_previa is None:
            deuda_previa = 0.0
        
        cursor.execute('''
            INSERT OR REPLACE INTO cuotas_mensuales 
            (cliente_id, año, mes, estado, monto, fecha_registro, fecha_inicio_mora, deuda_acumulada)
            VALUES (?, ?, ?, 'impago', ?, ?, ?, ?)
        ''', (cliente_id, año, mes, monto, fecha_actual, fecha_inicio_mora, deuda_previa))
        
        conn.commit()
        return cursor.lastrowid
    
    @staticmethod
    def obtener_por_cliente(cliente_id: int) -> List['CuotaMensual']:
        """Obtiene todas las cuotas de un cliente"""
        db = DatabaseConnection()
        conn = db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM cuotas_mensuales 
            WHERE cliente_id = ?
            ORDER BY año DESC, mes DESC
        ''', (cliente_id,))
        
        rows = cursor.fetchall()
        
        return [CuotaMensual(
            id=row['id'],
            cliente_id=row['cliente_id'],
            año=row['año'],
            mes=row['mes'],
            estado=row['estado'],
            monto=row['monto'],
            metodo_pago=row['metodo_pago'],
            fecha_registro=row['fecha_registro'],
            fecha_inicio_mora=row['fecha_inicio_mora'] if 'fecha_inicio_mora' in row.keys() else None,
            deuda_acumulada=row['deuda_acumulada'] if 'deuda_acumulada' in row.keys() else 0.0
        ) for row in rows]
    
    @staticmethod
    def obtener_cuota(cliente_id: int, año: int, mes: int) -> Optional['CuotaMensual']:
        """Obtiene una cuota específica"""
        db = DatabaseConnection()
        conn = db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM cuotas_mensuales 
            WHERE cliente_id = ? AND año = ? AND mes = ?
        ''', (cliente_id, año, mes))
        
        row = cursor.fetchone()
        
        if row:
            return CuotaMensual(
                id=row['id'],
                cliente_id=row['cliente_id'],
                año=row['año'],
                mes=row['mes'],
                estado=row['estado'],
                monto=row['monto'],
                metodo_pago=row['metodo_pago'],
                fecha_registro=row['fecha_registro'],
                fecha_inicio_mora=row['fecha_inicio_mora'] if 'fecha_inicio_mora' in row.keys() else None,
                deuda_acumulada=row['deuda_acumulada'] if 'deuda_acumulada' in row.keys() else 0.0
            )
        return None
    
    @staticmethod
    def calcular_deuda_acumulada(cliente_id: int, hasta_año: int, hasta_mes: int) -> float:
        """Calcula la deuda acumulada de impagos hasta una fecha"""
        db = DatabaseConnection()
        conn = db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT COALESCE(SUM(monto), 0) as total
            FROM cuotas_mensuales
            WHERE cliente_id = ? AND estado = 'impago'
            AND (año < ? OR (año = ? AND mes <= ?))
        ''', (cliente_id, hasta_año, hasta_año, hasta_mes))
        
        return cursor.fetchone()['total']
    
    @staticmethod
    def eliminar(cuota_id: int) -> bool:
        """Elimina una cuota mensual y sus pagos asociados"""
        db = DatabaseConnection()
        conn = db.get_connection()
        cursor = conn.cursor()
        
        # Primero obtener datos de la cuota para eliminar pagos relacionados
        cursor.execute('SELECT cliente_id, año, mes FROM cuotas_mensuales WHERE id = ?', (cuota_id,))
        cuota = cursor.fetchone()
        
        if cuota:
            mes_correspondiente = f"{cuota['año']}-{cuota['mes']:02d}"
            # Eliminar pagos asociados
            cursor.execute('''
                DELETE FROM pagos 
                WHERE cliente_id = ? AND mes_correspondiente = ?
            ''', (cuota['cliente_id'], mes_correspondiente))
            
            eliminados = cursor.rowcount
            if eliminados > 0:
                print(f"[INFO] Eliminados {eliminados} pago(s) asociado(s) a la cuota")
        
        # Eliminar la cuota
        cursor.execute('DELETE FROM cuotas_mensuales WHERE id = ?', (cuota_id,))
        conn.commit()
        return cursor.rowcount > 0
    
    @staticmethod
    def obtener_estadisticas(año: Optional[int] = None, mes: Optional[int] = None) -> Dict[str, Any]:
        """Obtiene estadísticas generales de cuotas para un mes específico o globales"""
        db = DatabaseConnection()
        conn = db.get_connection()
        cursor = conn.cursor()
        
        # Construir filtro de fecha si se especifica
        filtro_fecha = ""
        params = []
        if año and mes:
            filtro_fecha = "WHERE año = ? AND mes = ?"
            params = [año, mes]
        
        # Total de cuotas registradas
        query_total = f'SELECT COUNT(*) as total FROM cuotas_mensuales {filtro_fecha}'
        cursor.execute(query_total, params)
        total_cuotas = cursor.fetchone()['total']
        
        # Total pagado (obtener de tabla pagos que tiene el monto real pagado)
        # Filtrar por mes_correspondiente que indica a qué mes pertenece el pago
        filtro_pagos = ""
        params_pagos = []
        if año and mes:
            filtro_pagos = "WHERE mes_correspondiente = ?"
            params_pagos = [f"{año}-{mes:02d}"]
        
        # DEBUG: Ver qué hay en la tabla pagos
        query_debug = f'''
            SELECT id, cliente_id, fecha_pago, mes_correspondiente, monto
            FROM pagos
            {filtro_pagos}
        '''
        cursor.execute(query_debug, params_pagos)
        pagos_debug = cursor.fetchall()
        print(f"\n=== DEBUG PAGOS (Año: {año}, Mes: {mes}) ===")
        for pago in pagos_debug:
            print(f"  ID: {pago['id']}, Cliente: {pago['cliente_id']}, Mes: {pago['mes_correspondiente']}, Monto: ${pago['monto']:,.2f}")
        
        query_pagado = f'''
            SELECT COALESCE(SUM(monto), 0) as total
            FROM pagos
            {filtro_pagos}
        '''
        cursor.execute(query_pagado, params_pagos)
        total_pagado = cursor.fetchone()['total']
        print(f"  TOTAL PAGADO: ${total_pagado:,.2f}")
        print("=" * 50)
        
        # Total en impago (SOLO el monto de la cuota del mes, NO incluir deuda_acumulada)
        # La deuda_acumulada se reporta aparte
        query_impago = f'''
            SELECT COALESCE(SUM(monto), 0) as total
            FROM cuotas_mensuales
            {filtro_fecha}{"AND" if filtro_fecha else "WHERE"} estado = 'impago'
        '''
        cursor.execute(query_impago, params)
        total_impago = cursor.fetchone()['total']
        
        # Total con deuda acumulada (solo la deuda pendiente de meses anteriores)
        # deuda_acumulada ya incluye toda la deuda de meses pasados
        query_deuda = f'''
            SELECT COALESCE(SUM(COALESCE(deuda_acumulada, 0)), 0) as total
            FROM cuotas_mensuales
            {filtro_fecha}{"AND" if filtro_fecha else "WHERE"} estado IN ('con_deuda', 'impago')
        '''
        cursor.execute(query_deuda, params)
        total_deuda = cursor.fetchone()['total']
        
        return {
            'total': total_cuotas,
            'total_pagado': total_pagado,
            'total_impago': total_impago,
            'total_deuda': total_deuda
        }
    
    @staticmethod
    def obtener_estadisticas_por_metodo(año: Optional[int] = None, mes: Optional[int] = None) -> Dict[str, Dict[str, Any]]:
        """Obtiene estadísticas agrupadas por método de pago para un mes específico o globales"""
        db = DatabaseConnection()
        conn = db.get_connection()
        cursor = conn.cursor()
        
        # Construir filtro de fecha si se especifica
        # Filtrar por mes_correspondiente que tiene formato 'YYYY-MM'
        filtro_fecha = ""
        params = []
        if año and mes:
            filtro_fecha = "AND p.mes_correspondiente = ?"
            params = [f"{año}-{mes:02d}"]
        
        # DEBUG: Ver el JOIN completo
        query_debug = f'''
            SELECT 
                p.id as pago_id,
                p.cliente_id,
                p.mes_correspondiente,
                p.monto as pago_monto,
                cm.metodo_pago,
                cm.año as cuota_año,
                cm.mes as cuota_mes,
                cm.monto as cuota_monto
            FROM pagos p
            INNER JOIN cuotas_mensuales cm ON (
                p.cliente_id = cm.cliente_id 
                AND p.mes_correspondiente = printf('%04d-%02d', cm.año, cm.mes)
            )
            WHERE cm.metodo_pago IS NOT NULL {filtro_fecha}
        '''
        cursor.execute(query_debug, params)
        debug_rows = cursor.fetchall()
        
        print(f"\n=== DEBUG MÉTODOS DE PAGO (Año: {año}, Mes: {mes}) ===")
        print(f"Total filas en JOIN: {len(debug_rows)}")
        for row in debug_rows:
            print(f"  Pago ID: {row['pago_id']}, Cliente: {row['cliente_id']}, "
                  f"Mes Pago: {row['mes_correspondiente']}, Monto Pago: ${row['pago_monto']:,.2f}, "
                  f"Método: {row['metodo_pago']}, Cuota: {row['cuota_año']}-{row['cuota_mes']:02d}")
        
        # Obtener datos de la tabla pagos que contiene el monto real pagado
        # JOIN con cuotas_mensuales para obtener el método de pago
        query = f'''
            SELECT 
                cm.metodo_pago,
                COUNT(p.id) as cantidad,
                COALESCE(SUM(p.monto), 0) as total
            FROM pagos p
            INNER JOIN cuotas_mensuales cm ON (
                p.cliente_id = cm.cliente_id 
                AND p.mes_correspondiente = printf('%04d-%02d', cm.año, cm.mes)
            )
            WHERE cm.metodo_pago IS NOT NULL {filtro_fecha}
            GROUP BY cm.metodo_pago
        '''
        cursor.execute(query, params)
        
        resultado = {}
        for row in cursor.fetchall():
            metodo = row['metodo_pago']
            resultado[metodo] = {
                'cantidad': row['cantidad'],
                'total': row['total']
            }
            print(f"  {metodo}: Cantidad={row['cantidad']}, Total=${row['total']:,.2f}")
        
        print("=" * 50)
        
        return resultado


class LogSistema:
    """Modelo para gestionar los logs del sistema"""
    
    def __init__(self, id: Optional[int] = None, usuario_id: Optional[int] = None, 
                 usuario_nombre: str = "", fecha_hora: str = "", accion: str = "",
                 detalles: str = ""):
        self.id = id
        self.usuario_id = usuario_id
        self.usuario_nombre = usuario_nombre
        self.fecha_hora = fecha_hora
        self.accion = accion
        self.detalles = detalles
    
    @staticmethod
    def registrar(usuario_id: Optional[int], usuario_nombre: str, accion: str, 
                  detalles: str = "") -> int:
        """
        Registra un log en el sistema
        
        Args:
            usuario_id: ID del usuario (puede ser None si fue eliminado)
            usuario_nombre: Nombre del usuario que realiza la acción
            accion: Acción realizada (crear, editar, eliminar, etc.)
            detalles: Detalles adicionales de la acción
        
        Returns:
            ID del log creado
        """
        db = DatabaseConnection()
        conn = db.get_connection()
        cursor = conn.cursor()
        
        fecha_hora = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        cursor.execute('''
            INSERT INTO logs_sistema (usuario_id, usuario_nombre, fecha_hora, accion, detalles)
            VALUES (?, ?, ?, ?, ?)
        ''', (usuario_id, usuario_nombre, fecha_hora, accion, detalles))
        
        conn.commit()
        return cursor.lastrowid
    
    @staticmethod
    def obtener_todos(limite: int = 1000) -> List['LogSistema']:
        """
        Obtiene todos los logs del sistema
        
        Args:
            limite: Cantidad máxima de logs a obtener (por defecto 1000)
        
        Returns:
            Lista de logs ordenados por fecha descendente
        """
        db = DatabaseConnection()
        conn = db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM logs_sistema 
            ORDER BY fecha_hora DESC 
            LIMIT ?
        ''', (limite,))
        
        rows = cursor.fetchall()
        
        return [LogSistema(
            id=row['id'],
            usuario_id=row['usuario_id'],
            usuario_nombre=row['usuario_nombre'],
            fecha_hora=row['fecha_hora'],
            accion=row['accion'],
            detalles=row['detalles']
        ) for row in rows]
    
    @staticmethod
    def obtener_por_accion(accion: str, limite: int = 500) -> List['LogSistema']:
        """Obtiene logs filtrados por acción"""
        db = DatabaseConnection()
        conn = db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM logs_sistema 
            WHERE accion = ?
            ORDER BY fecha_hora DESC 
            LIMIT ?
        ''', (accion, limite))
        
        rows = cursor.fetchall()
        
        return [LogSistema(
            id=row['id'],
            usuario_id=row['usuario_id'],
            usuario_nombre=row['usuario_nombre'],
            fecha_hora=row['fecha_hora'],
            accion=row['accion'],
            detalles=row['detalles']
        ) for row in rows]
    
    @staticmethod
    def obtener_por_usuario(usuario_id: int, limite: int = 500) -> List['LogSistema']:
        """Obtiene logs filtrados por usuario"""
        db = DatabaseConnection()
        conn = db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM logs_sistema 
            WHERE usuario_id = ?
            ORDER BY fecha_hora DESC 
            LIMIT ?
        ''', (usuario_id, limite))
        
        rows = cursor.fetchall()
        
        return [LogSistema(
            id=row['id'],
            usuario_id=row['usuario_id'],
            usuario_nombre=row['usuario_nombre'],
            fecha_hora=row['fecha_hora'],
            accion=row['accion'],
            detalles=row['detalles']
        ) for row in rows]
    
    @staticmethod
    def obtener_por_fecha(fecha_inicio: str, fecha_fin: str, limite: int = 1000) -> List['LogSistema']:
        """
        Obtiene logs filtrados por rango de fechas
        
        Args:
            fecha_inicio: Fecha inicio (YYYY-MM-DD)
            fecha_fin: Fecha fin (YYYY-MM-DD)
            limite: Cantidad máxima de logs
        
        Returns:
            Lista de logs en el rango de fechas
        """
        db = DatabaseConnection()
        conn = db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM logs_sistema 
            WHERE DATE(fecha_hora) BETWEEN ? AND ?
            ORDER BY fecha_hora DESC 
            LIMIT ?
        ''', (fecha_inicio, fecha_fin, limite))
        
        rows = cursor.fetchall()
        
        return [LogSistema(
            id=row['id'],
            usuario_id=row['usuario_id'],
            usuario_nombre=row['usuario_nombre'],
            fecha_hora=row['fecha_hora'],
            accion=row['accion'],
            detalles=row['detalles']
        ) for row in rows]
    
    @staticmethod
    def eliminar_antiguos(dias: int = 365) -> int:
        """
        Elimina logs más antiguos que X días
        
        Args:
            dias: Cantidad de días a mantener (por defecto 365)
        
        Returns:
            Cantidad de logs eliminados
        """
        db = DatabaseConnection()
        conn = db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            DELETE FROM logs_sistema 
            WHERE fecha_hora < datetime('now', '-' || ? || ' days')
        ''', (dias,))
        
        conn.commit()
        return cursor.rowcount

