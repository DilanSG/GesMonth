#!/usr/bin/env python3
"""
Script para visualizar y editar datos de las bases de datos
Uso: python scripts/ver_datos.py
"""

import sqlite3
import os
from pathlib import Path

def main():
    # Detectar carpeta .data
    data_dir = Path(__file__).parent.parent / '.data'
    
    if not data_dir.exists():
        print("No existe la carpeta .data")
        print("Ejecuta la aplicación primero para crear las bases de datos")
        return
    
    gesmonth_db = data_dir / 'gesmonth.db'
    users_db = data_dir / 'users.db'
    
    print("=" * 60)
    print("VISUALIZADOR DE DATOS - GesMonth")
    print("=" * 60)
    
    # Mostrar datos de usuarios
    if users_db.exists():
        conn = sqlite3.connect(users_db)
        cursor = conn.cursor()
        
        print("\nUSUARIOS:")
        print("-" * 60)
        cursor.execute("SELECT id, username, rol, activo FROM usuarios")
        for row in cursor.fetchall():
            estado = "✓ Activo" if row[3] else "✗ Inactivo"
            print(f"  [{row[0]}] {row[1]} - Rol: {row[2]} - {estado}")
        
        conn.close()
    
    # Mostrar datos principales
    if gesmonth_db.exists():
        conn = sqlite3.connect(gesmonth_db)
        cursor = conn.cursor()
        
        print("\nCLIENTES:")
        print("-" * 60)
        cursor.execute("SELECT id, nombre, activo FROM clientes ORDER BY nombre")
        clientes = cursor.fetchall()
        if clientes:
            for row in clientes:
                estado = "✓" if row[2] else "✗"
                print(f"  {estado} [{row[0]}] {row[1]}")
        else:
            print("  (No hay clientes registrados)")
        
        print("\nPAGOS REGISTRADOS:")
        print("-" * 60)
        cursor.execute("""
            SELECT p.id, c.nombre, p.monto, p.fecha_pago, m.nombre 
            FROM pagos p
            JOIN clientes c ON p.cliente_id = c.id
            JOIN metodos_pago m ON p.metodo_pago_id = m.id
            ORDER BY p.fecha_pago DESC
            LIMIT 10
        """)
        pagos = cursor.fetchall()
        if pagos:
            for row in pagos:
                print(f"  [{row[0]}] {row[1]} - ${row[2]:,.2f} - {row[3]} ({row[4]})")
        else:
            print("  (No hay pagos registrados)")
        
        # Estadísticas
        print("\nESTADÍSTICAS:")
        print("-" * 60)
        cursor.execute("SELECT COUNT(*) FROM clientes WHERE activo = 1")
        total_clientes = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*), SUM(monto) FROM pagos")
        stats = cursor.fetchone()
        total_pagos = stats[0]
        suma_total = stats[1] or 0
        
        print(f"  Clientes activos: {total_clientes}")
        print(f"  Total pagos: {total_pagos}")
        print(f"  Suma total: ${suma_total:,.2f}")
        
        conn.close()
    
    print("\n" + "=" * 60)
    print("\nOPCIONES PARA EDITAR:")
    print("  1. Usar la aplicación GesMonth (recomendado)")
    print("  2. sqlite3 .data/gesmonth.db")
    print("  3. sqlitebrowser .data/gesmonth.db (GUI)")
    print("=" * 60)

if __name__ == "__main__":
    main()
