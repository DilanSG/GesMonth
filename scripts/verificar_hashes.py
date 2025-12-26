#!/usr/bin/env python3
"""
Script para verificar la integridad de los password hashes en la base de datos
"""

from database.user_connection import UserDatabaseConnection
import bcrypt

def verificar_hashes():
    """Verifica que todos los password hashes sean válidos"""
    print("Verificando integridad de password hashes...\n")
    
    db = UserDatabaseConnection()
    conn = db.get_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT id, username, password_hash FROM usuarios')
    usuarios = cursor.fetchall()
    
    problemas = []
    
    for usuario in usuarios:
        user_id = usuario['id']
        username = usuario['username']
        password_hash = usuario['password_hash']
        
        # Verificar formato
        es_valido = True
        detalles = []
        
        if not password_hash:
            es_valido = False
            detalles.append("Hash vacío")
        else:
            # Verificar longitud
            if len(password_hash) != 60:
                es_valido = False
                detalles.append(f"Longitud incorrecta: {len(password_hash)} (esperado: 60)")
            
            # Verificar prefijo bcrypt
            if not password_hash.startswith('$2b$') and not password_hash.startswith('$2a$'):
                es_valido = False
                detalles.append(f"Prefijo incorrecto: {password_hash[:4]} (esperado: $2b$ o $2a$)")
            
            # Verificar formato general
            partes = password_hash.split('$')
            if len(partes) != 4:
                es_valido = False
                detalles.append(f"Formato inválido: {len(partes)} partes (esperado: 4)")
        
        if es_valido:
            print(f"✓ {username} (ID: {user_id}): Hash válido")
        else:
            print(f"✗ {username} (ID: {user_id}): PROBLEMAS DETECTADOS")
            for detalle in detalles:
                print(f"  - {detalle}")
            problemas.append((user_id, username, detalles))
    
    print(f"\n{'='*60}")
    if problemas:
        print(f"❌ Se encontraron {len(problemas)} usuario(s) con problemas")
        print("\nRecomendación: Regenerar las contraseñas de estos usuarios")
    else:
        print(f"✅ Todos los password hashes son válidos ({len(usuarios)} usuarios verificados)")
    print('='*60)
    
    return len(problemas) == 0

if __name__ == "__main__":
    verificar_hashes()
