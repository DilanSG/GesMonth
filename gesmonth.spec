# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec file para GesMonth
Genera un ejecutable standalone de la aplicación
"""

import sys
from PyInstaller.utils.hooks import collect_data_files, collect_submodules

block_cipher = None

# Icono según plataforma
icon_path = None
if sys.platform == 'win32':
    icon_path = 'assets/icons/LOGO.ico'  # Windows necesita .ico
elif sys.platform == 'darwin':
    icon_path = 'assets/icons/LOGO.png'  # macOS puede usar .png
# Linux ignora el icono en PyInstaller

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
    'PyQt6.QtSvg',
    'pandas',
    'openpyxl',
    'bcrypt',
    'utils',
    'database',
    'database.connection',
    'database.models',
    'database.user_connection',
    'database.user_models',
    'ui',
    'ui.main_window',
    'ui.home_view',
    'ui.clientes_view',
    'ui.cuotas_view',
    'ui.reportes_view',
    'ui.configuracion_view',
    'ui.pagos_view',
    'ui.detalles_cuota_dialog',
    'ui.login_view',
    'ui.usuarios_management',
    'ui.splash_screen',
    'ui.theme_colors',
    'controllers',
    'controllers.cliente_controller',
    'controllers.pago_controller',
    'controllers.reporte_controller',
    'controllers.config_controller',
    'controllers.auth_controller',
    'controllers.theme_controller',
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
        'tkinter',
        '_tkinter',
        'PIL',
        'setuptools',
        'pkg_resources',
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
    [],
    exclude_binaries=True,  # Cambiar a onedir para incluir assets externos
    name='GesMonth',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,  # Sin consola (GUI application)
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=icon_path,  # Icono condicional según plataforma
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='GesMonth',
)
