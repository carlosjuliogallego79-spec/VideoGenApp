"""
Pantalla principal con menú de opciones.
"""

from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.metrics import dp
from kivy.utils import platform


class MainScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._build_ui()

    def _build_ui(self):
        layout = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(20))

        # Logo / Título
        title = Label(
            text="VideoGenApp",
            font_size=dp(36),
            bold=True,
            size_hint_y=0.15,
        )
        layout.add_widget(title)

        subtitle = Label(
            text="Generación de Video y Sincronización de Voz",
            font_size=dp(16),
            size_hint_y=0.08,
        )
        layout.add_widget(subtitle)

        # Menú de opciones
        menu = GridLayout(cols=1, spacing=dp(15), size_hint_y=0.6,
                          pos_hint={'center_x': 0.5})
        menu.bind(minimum_height=menu.setter('height'))
        menu.cols = 1 if platform == 'android' else 2

        buttons = [
            ("Generar Video", "video", "Crear video desde imágenes con transiciones"),
            ("Texto a Voz", "tts", "Convertir texto a voz narrada"),
            ("Presentaciones", "presentation", "Crear slideshows animados"),
            ("Sincronizar Voz", "voice_sync", "Sincronizar y clonar voces"),
            ("Configuración", "settings", "Ajustes de la aplicación"),
        ]

        for label, screen_name, desc in buttons:
            btn = Button(
                text=f"{label}\n{desc}",
                size_hint_y=None,
                height=dp(80),
                font_size=dp(14),
                background_color=(0.2, 0.6, 1, 1),
                color=(1, 1, 1, 1),
            )
            btn.bind(on_press=lambda x, s=screen_name: self._go_to_screen(s))
            menu.add_widget(btn)

        layout.add_widget(menu)

        # Footer
        footer = Label(
            text="Hecho con Kivy | Python para Android",
            font_size=dp(12),
            size_hint_y=0.05,
            color=(0.5, 0.5, 0.5, 1),
        )
        layout.add_widget(footer)

        self.add_widget(layout)

    def _go_to_screen(self, screen_name):
        self.manager.current = screen_name
