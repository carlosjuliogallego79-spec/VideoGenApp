"""
Pantalla de configuración de la aplicación.
"""

import os
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.switch import Switch
from kivy.uix.progressbar import ProgressBar
from kivy.metrics import dp
from kivy.utils import platform

from utils.ffmpeg_helper import FFmpegHelper
from utils.file_manager import FileManager


class SettingsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ffmpeg = FFmpegHelper()
        self.fm = FileManager()
        self._build_ui()

    def _build_ui(self):
        layout = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10))

        # Header
        header = BoxLayout(size_hint_y=0.08, spacing=dp(10))
        back_btn = Button(text="< Atrás", size_hint_x=0.3)
        back_btn.bind(on_press=lambda x: setattr(self.manager, 'current', 'main'))
        header.add_widget(back_btn)
        header.add_widget(Label(text="Configuración", font_size=dp(22), bold=True))
        layout.add_widget(header)

        scroll_content = GridLayout(cols=1, spacing=dp(10), size_hint_y=None)
        scroll_content.bind(minimum_height=scroll_content.setter('height'))

        # Información del sistema
        scroll_content.add_widget(Label(
            text="Información del Sistema",
            font_size=dp(16), bold=True,
            size_hint_y=None, height=dp(30),
        ))

        ffmpeg_status = "Disponible" if self.ffmpeg.is_available() else "No instalado"
        scroll_content.add_widget(Label(
            text=f"FFmpeg: {ffmpeg_status}",
            size_hint_y=None, height=dp(25),
        ))

        scroll_content.add_widget(Label(
            text=f"Plataforma: {platform}",
            size_hint_y=None, height=dp(25),
        ))

        scroll_content.add_widget(Label(
            text=f"Directorio base: {self.fm.base_dir}",
            size_hint_y=None, height=dp(25),
        ))

        # Almacenamiento
        scroll_content.add_widget(Label(
            text="Almacenamiento",
            font_size=dp(16), bold=True,
            size_hint_y=None, height=dp(30),
        ))

        storage_box = BoxLayout(size_hint_y=None, height=dp(30), spacing=dp(10))
        storage_box.add_widget(Label(text="Espacio usado:"))
        storage_box.add_widget(Label(
            text=self._get_storage_info(),
        ))
        scroll_content.add_widget(storage_box)

        # Acciones
        scroll_content.add_widget(Label(
            text="Acciones",
            font_size=dp(16), bold=True,
            size_hint_y=None, height=dp(30),
        ))

        clear_temp_btn = Button(
            text="Limpiar Archivos Temporales",
            size_hint_y=None, height=dp(50),
        )
        clear_temp_btn.bind(on_press=self._clear_temp)
        scroll_content.add_widget(clear_temp_btn)

        open_folder_btn = Button(
            text="Abrir Carpeta de Exportación",
            size_hint_y=None, height=dp(50),
        )
        open_folder_btn.bind(on_press=self._open_export_folder)
        scroll_content.add_widget(open_folder_btn)

        # Acerca de
        scroll_content.add_widget(Label(
            text="Acerca de",
            font_size=dp(16), bold=True,
            size_hint_y=None, height=dp(30),
        ))

        scroll_content.add_widget(Label(
            text="VideoGenApp v1.0.0",
            size_hint_y=None, height=dp(25),
        ))

        scroll_content.add_widget(Label(
            text="Hecho con Kivy + Python",
            size_hint_y=None, height=dp(25),
        ))

        scroll_content.add_widget(Label(
            text="© 2026 VideoGenApp",
            size_hint_y=None, height=dp(25),
        ))

        layout.add_widget(scroll_content)

        # Estado
        self.status_label = Label(
            text="Listo",
            size_hint_y=0.05,
            color=(0.5, 0.5, 0.5, 1),
        )
        layout.add_widget(self.status_label)

        self.add_widget(layout)

    def _get_storage_info(self):
        total_size = 0
        for root, dirs, files in os.walk(self.fm.base_dir):
            for f in files:
                try:
                    total_size += os.path.getsize(os.path.join(root, f))
                except Exception:
                    pass

        if total_size < 1024:
            return f"{total_size} B"
        elif total_size < 1024**2:
            return f"{total_size/1024:.1f} KB"
        elif total_size < 1024**3:
            return f"{total_size/1024**2:.1f} MB"
        else:
            return f"{total_size/1024**3:.1f} GB"

    def _clear_temp(self, instance):
        self.fm.clear_temp()
        self.status_label.text = "Archivos temporales limpiados"

    def _open_export_folder(self, instance):
        try:
            if platform == 'android':
                from android import mActivity
                from jnius import autoclass
                Intent = autoclass('android.content.Intent')
                intent = Intent(Intent.ACTION_VIEW)
                uri = autoclass('android.net.Uri').parse(
                    f"file://{self.fm.export_dir}"
                )
                intent.setDataAndType(uri, "resource/folder")
                mActivity.startActivity(intent)
            else:
                import subprocess
                subprocess.run(['explorer', self.fm.export_dir], check=True)
        except Exception as e:
            self.status_label.text = f"Error abriendo carpeta: {e}"
