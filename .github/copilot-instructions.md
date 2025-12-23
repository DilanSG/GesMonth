# GesMonth - Sistema de Gestión de Pagos Mensuales

## Descripción del Proyecto
Sistema profesional de escritorio para la gestión de pagos mensuales desarrollado en Python con PyQt6 y SQLite.

## Arquitectura
- Programación orientada a objetos
- Estructura modular por carpetas
- Base de datos SQLite
- Interfaz gráfica con PyQt6

## Estructura del Proyecto
```
GesMonth/
├── main.py                 # Punto de entrada
├── requirements.txt        # Dependencias
├── database/              # Módulo de base de datos
│   ├── connection.py      # Conexión SQLite
│   └── models.py          # Modelos (Alumno, Pago)
├── ui/                    # Interfaces PyQt6
│   ├── main_window.py     # Ventana principal
│   ├── dashboard_view.py  # Dashboard
│   ├── alumnos_view.py    # Gestión de alumnos
│   ├── pagos_view.py      # Registro de pagos
│   ├── reportes_view.py   # Reportes
│   └── configuracion_view.py  # Configuración
├── controllers/           # Lógica de negocio
│   ├── alumno_controller.py
│   ├── pago_controller.py
│   └── reporte_controller.py
└── assets/                # Recursos
    └── styles/
        └── main.qss       # Estilos CSS
```

## Estado del Proyecto
- [x] Estructura base creada
- [x] Módulos implementados
- [x] Base de datos configurada
- [x] Interfaces de usuario completas
- [x] Controladores implementados
- [x] Estilos QSS aplicados
- [x] Scripts de instalación creados
- [x] Documentación completa

## Instalación
- Windows: Ejecutar `install.bat`
- Linux/Mac: Ejecutar `./install.sh`

## Ejecución
- Windows: Ejecutar `run.bat`
- Linux/Mac: Ejecutar `./run.sh`

## Características
- Dashboard con estadísticas
- CRUD completo de alumnos
- Registro de pagos mensuales
- Exportación de reportes a Excel
- Interfaz moderna y profesional
