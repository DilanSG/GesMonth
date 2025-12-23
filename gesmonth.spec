# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec file para GesMonth
Genera un ejecutable standalone de la aplicación
"""

import sys
from PyInstaller.utils.hooks import collect_data_files, collect_submodules

block_cipher = None

# Datos adicionales a incluir
datas = [
    ('assets', 'assets'),  # Incluir carpeta de assets (estilos, iconos)
    ('VERSION', '.'),      # Incluir archivo de versión
]

# Módulos ocultos que PyInstaller podría no detectar
hiddenimports = [
    'PyQt6.QtCore',
    'PyQt6.QtGui',
    'PyQt6.QtWidgets',
    'pandas',
    'openpyxl',
    'database',
    'database.connection',
    'database.models',
    'ui',
    'ui.main_window',
    'ui.dashboard_view',
    'ui.clientes_view',
    'ui.cuotas_view',
    'ui.reportes_view',
    'ui.configuracion_view',
    'ui.detalles_cuota_dialog',
    'controllers',
    'controllers.cliente_controller',
    'controllers.pago_controller',
    'controllers.reporte_controller',
    'controllers.config_controller',
]

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'matplotlib',
        'scipy',
        'numpy',
        'tkinter',
        '_tkinter',
        'PIL',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='GesMonth',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # Sin consola (GUI application)
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='assets/icons/LOGO.png',  # Icono de la aplicación
)
