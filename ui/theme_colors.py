"""
Sistema de colores dinámicos para temas
"""

from typing import Dict


class ThemeColors:
    """Gestiona los colores según el tema activo"""
    
    # Definición de paletas de colores
    DARK_THEME = {
        # Fondos
        'bg_primary': '#0f172a',
        'bg_secondary': '#1e293b',
        'bg_tertiary': '#334155',
        'bg_card': 'rgba(30, 41, 59, 0.5)',
        'bg_card_hover': 'rgba(30, 41, 59, 0.7)',
        
        # Textos
        'text_primary': '#e0e7ff',
        'text_secondary': '#cbd5e1',
        'text_tertiary': '#94a3b8',
        'text_disabled': '#64748b',
        
        # Acentos
        'accent_primary': '#60a5fa',
        'accent_secondary': '#3b82f6',
        'accent_hover': '#2563eb',
        
        # Estados
        'success': '#22c55e',
        'success_light': '#86efac',
        'error': '#ef4444',
        'error_light': '#fca5a5',
        'warning': '#eab308',
        'warning_light': '#fcd34d',
        'info': '#3b82f6',
        'info_light': '#60a5fa',
        
        # Bordes
        'border_primary': 'rgba(148, 163, 184, 0.2)',
        'border_secondary': 'rgba(71, 85, 105, 0.5)',
        'border_accent': 'rgba(96, 165, 250, 0.5)',
        
        # Sombras y overlay
        'shadow': 'rgba(0, 0, 0, 0.3)',
        'overlay': 'rgba(15, 23, 42, 0.8)',
    }
    
    LIGHT_THEME = {
        # Fondos
        'bg_primary': '#ffffff',
        'bg_secondary': '#f8f9fa',
        'bg_tertiary': '#f1f5f9',
        'bg_card': 'rgba(255, 255, 255, 0.9)',
        'bg_card_hover': 'rgba(241, 245, 249, 1)',
        
        # Textos
        'text_primary': '#0f172a',
        'text_secondary': '#1e293b',
        'text_tertiary': '#64748b',
        'text_disabled': '#94a3b8',
        
        # Acentos
        'accent_primary': '#3b82f6',
        'accent_secondary': '#2563eb',
        'accent_hover': '#1d4ed8',
        
        # Estados
        'success': '#10b981',
        'success_light': '#34d399',
        'error': '#dc2626',
        'error_light': '#f87171',
        'warning': '#f59e0b',
        'warning_light': '#fbbf24',
        'info': '#0ea5e9',
        'info_light': '#38bdf8',
        
        # Bordes
        'border_primary': 'rgba(148, 163, 184, 0.3)',
        'border_secondary': 'rgba(203, 213, 225, 0.8)',
        'border_accent': 'rgba(59, 130, 246, 0.5)',
        
        # Sombras y overlay
        'shadow': 'rgba(0, 0, 0, 0.1)',
        'overlay': 'rgba(248, 249, 250, 0.95)',
    }
    
    @staticmethod
    def get_colors(theme: str) -> Dict[str, str]:
        """
        Obtiene el diccionario de colores para el tema especificado
        
        Args:
            theme: 'dark' o 'light'
            
        Returns:
            Diccionario con todos los colores del tema
        """
        if theme == 'light':
            return ThemeColors.LIGHT_THEME.copy()
        return ThemeColors.DARK_THEME.copy()
    
    @staticmethod
    def get_dialog_colors(theme: str, tipo: str) -> Dict[str, str]:
        """
        Obtiene colores específicos para diálogos según tipo
        
        Args:
            theme: 'dark' o 'light'
            tipo: 'success', 'error', 'warning', 'question', 'info'
            
        Returns:
            Diccionario con color principal y color del botón
        """
        colors = ThemeColors.get_colors(theme)
        
        tipo_colors = {
            'success': {
                'title': colors['success'],
                'button_bg': 'rgba(34, 197, 94, 0.25)' if theme == 'dark' else 'rgba(16, 185, 129, 0.15)',
                'button_border': colors['success'],
                'button_text': colors['success'],
                'button_hover': 'rgba(34, 197, 94, 0.35)' if theme == 'dark' else 'rgba(16, 185, 129, 0.25)',
            },
            'error': {
                'title': colors['error'],
                'button_bg': 'rgba(239, 68, 68, 0.25)' if theme == 'dark' else 'rgba(220, 38, 38, 0.15)',
                'button_border': colors['error'],
                'button_text': colors['error'],
                'button_hover': 'rgba(239, 68, 68, 0.35)' if theme == 'dark' else 'rgba(220, 38, 38, 0.25)',
            },
            'warning': {
                'title': colors['warning'],
                'button_bg': 'rgba(234, 179, 8, 0.25)' if theme == 'dark' else 'rgba(245, 158, 11, 0.15)',
                'button_border': colors['warning'],
                'button_text': colors['warning'],
                'button_hover': 'rgba(234, 179, 8, 0.35)' if theme == 'dark' else 'rgba(245, 158, 11, 0.25)',
            },
            'question': {
                'title': colors['info'],
                'button_bg': 'rgba(59, 130, 246, 0.25)' if theme == 'dark' else 'rgba(14, 165, 233, 0.15)',
                'button_border': colors['info'],
                'button_text': colors['info'],
                'button_hover': 'rgba(59, 130, 246, 0.35)' if theme == 'dark' else 'rgba(14, 165, 233, 0.25)',
            },
            'info': {
                'title': colors['text_secondary'],
                'button_bg': 'rgba(59, 130, 246, 0.25)' if theme == 'dark' else 'rgba(14, 165, 233, 0.15)',
                'button_border': colors['info'],
                'button_text': colors['info'],
                'button_hover': 'rgba(59, 130, 246, 0.35)' if theme == 'dark' else 'rgba(14, 165, 233, 0.25)',
            },
        }
        
        return tipo_colors.get(tipo, tipo_colors['info'])
