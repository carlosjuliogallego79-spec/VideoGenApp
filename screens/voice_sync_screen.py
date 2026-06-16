"""
Pantalla de sincronización y clonación de voz.
"""

import os
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.slider import Slider
from kivy.uix.popup import Popup
from kivy.uix.progressbar import ProgressBar
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.utils import platform

from modules.voice_sync import VoiceSynchronizer


class VoiceSyncScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.sync = VoiceSynchronizer()
        self.selected_video = None
        self.selected_audio = None
        self._build_ui()

    def _build_ui(self):
        layout = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10))

        # Header
        header = BoxLayout(size_hint_y=0.08, spacing=dp(10))
        back_btn = Button(text="< Atrás", size_hint_x=0.3)
        back_btn.bind(on_press=lambda x: setattr(self.manager, 'current', 'main'))
        header.add_widget(back_btn)
        header.add_widget(Label(text="Sincronizar Voz", font_size=dp(22), bold=True))
        layout.add_widget(header)

        # Selección de archivos
        files_section = GridLayout(cols=2, spacing=dp(10), size_hint_y=0.3)

        files_section.add_widget(Label(text="Video:"))
        video_box = BoxLayout(spacing=dp(5))
        self.video_label = Label(text="Ninguno", size_hint_x=0.7)
        video_btn = Button(text="Buscar", size_hint_x=0.3)
        video_btn.bind(on_press=lambda x: self._select_file('video'))
        video_box.add_widget(self.video_label)
        video_box.add_widget(video_btn)
        files_section.add_widget(video_box)

        files_section.add_widget(Label(text="Audio:"))
        audio_box = BoxLayout(spacing=dp(5))
        self.audio_label = Label(text="Ninguno", size_hint_x=0.7)
        audio_btn = Button(text="Buscar", size_hint_x=0.3)
        audio_btn.bind(on_press=lambda x: self._select_file('audio'))
        audio_box.add_widget(self.audio_label)
        audio_box.add_widget(audio_btn)
        files_section.add_widget(audio_box)

        layout.add_widget(files_section)

        # Controles de ajuste de voz
        controls = GridLayout(cols=2, spacing=dp(10), size_hint_y=0.2)

        controls.add_widget(Label(text="Tono (semitones):"))
        pitch_box = BoxLayout(spacing=dp(5))
        self.pitch_slider = Slider(min=-12, max=12, value=0, step=1)
        self.pitch_label = Label(text="0", size_hint_x=0.2)
        self.pitch_slider.bind(value=lambda s, v: setattr(self.pitch_label, 'text', str(int(v))))
        pitch_box.add_widget(self.pitch_slider)
        pitch_box.add_widget(self.pitch_label)
        controls.add_widget(pitch_box)

        controls.add_widget(Label(text="Velocidad:"))
        speed_box = BoxLayout(spacing=dp(5))
        self.speed_slider = Slider(min=0.5, max=2.0, value=1.0, step=0.1)
        self.speed_label = Label(text="1.0x", size_hint_x=0.2)
        self.speed_slider.bind(value=lambda s, v: setattr(self.speed_label, 'text', f'{v:.1f}x'))
        speed_box.add_widget(self.speed_slider)
        speed_box.add_widget(self.speed_label)
        controls.add_widget(speed_box)

        layout.add_widget(controls)

        # Botones de acción
        actions = GridLayout(cols=2, spacing=dp(10), size_hint_y=0.2)

        sync_btn = Button(text="Sincronizar Audio\ncon Video")
        sync_btn.bind(on_press=self._sync_audio)
        actions.add_widget(sync_btn)

        extract_btn = Button(text="Extraer Audio\ndel Video")
        extract_btn.bind(on_press=self._extract_audio)
        actions.add_widget(extract_btn)

        adjust_btn = Button(text="Ajustar Tono\nde Audio")
        adjust_btn.bind(on_press=self._adjust_pitch)
        actions.add_widget(adjust_btn)

        speed_btn = Button(text="Cambiar\nVelocidad")
        speed_btn.bind(on_press=self._change_speed)
        actions.add_widget(speed_btn)

        layout.add_widget(actions)

        # Barra de progreso
        self.progress = ProgressBar(max=100, value=0, size_hint_y=0.04)
        layout.add_widget(self.progress)

        # Estado
        self.status_label = Label(
            text="Listo",
            size_hint_y=0.04,
            color=(0.5, 0.5, 0.5, 1),
        )
        layout.add_widget(self.status_label)

        self.add_widget(layout)

    def _select_file(self, file_type):
        if platform == 'android':
            self.status_label.text = f"Selecciona archivo de {file_type} desde tu dispositivo"
            return

        filters = ['*.mp4', '*.avi', '*.mov', '*.mkv'] if file_type == 'video' else ['*.mp3', '*.wav', '*.ogg', '*.m4a']

        content = BoxLayout(orientation='vertical')
        filechooser = FileChooserListView(
            path=os.path.expanduser('~'),
            filters=filters,
        )
        content.add_widget(filechooser)

        popup = Popup(
            title=f"Seleccionar {file_type}",
            content=content,
            size_hint=(0.9, 0.9),
        )

        select_btn = Button(text="Seleccionar", size_hint_y=0.15)
        def on_select(instance):
            if filechooser.selection:
                if file_type == 'video':
                    self.selected_video = filechooser.selection[0]
                    self.video_label.text = os.path.basename(self.selected_video)
                else:
                    self.selected_audio = filechooser.selection[0]
                    self.audio_label.text = os.path.basename(self.selected_audio)
            popup.dismiss()

        select_btn.bind(on_press=on_select)
        content.add_widget(select_btn)
        popup.open()

    def _sync_audio(self, instance):
        if not self.selected_video or not self.selected_audio:
            self.status_label.text = "Selecciona video y audio primero"
            return

        self.status_label.text = "Sincronizando audio..."
        self.progress.value = 20
        Clock.schedule_once(lambda dt: self._do_sync(), 0.1)

    def _do_sync(self):
        output = self.sync.sync_audio_to_video(
            self.selected_video, self.selected_audio
        )
        self.progress.value = 100
        if output:
            self.status_label.text = f"Sincronizado: {output}"
            self._show_success_popup(output)
        else:
            self.status_label.text = "Error en sincronización"
            self.progress.value = 0

    def _extract_audio(self, instance):
        if not self.selected_video:
            self.status_label.text = "Selecciona un video primero"
            return

        self.status_label.text = "Extrayendo audio..."
        self.progress.value = 30
        Clock.schedule_once(lambda dt: self._do_extract(), 0.1)

    def _do_extract(self):
        output = self.sync.extract_audio_from_video(self.selected_video)
        self.progress.value = 100
        if output:
            self.status_label.text = f"Audio extraído: {output}"
            self._show_success_popup(output)
        else:
            self.status_label.text = "Error extrayendo audio"
            self.progress.value = 0

    def _adjust_pitch(self, instance):
        if not self.selected_audio:
            self.status_label.text = "Selecciona un audio primero"
            return

        semitones = int(self.pitch_slider.value)
        self.status_label.text = f"Ajustando tono ({semitones} semitonos)..."
        self.progress.value = 30
        Clock.schedule_once(lambda dt: self._do_adjust_pitch(semitones), 0.1)

    def _do_adjust_pitch(self, semitones):
        output = self.sync.adjust_voice_pitch(
            self.selected_audio, semitones=semitones
        )
        self.progress.value = 100
        if output:
            self.status_label.text = f"Tono ajustado: {output}"
            self._show_success_popup(output)
        else:
            self.status_label.text = "Error ajustando tono"
            self.progress.value = 0

    def _change_speed(self, instance):
        if not self.selected_audio:
            self.status_label.text = "Selecciona un audio primero"
            return

        speed = self.speed_slider.value
        self.status_label.text = f"Cambiando velocidad ({speed:.1f}x)..."
        self.progress.value = 30
        Clock.schedule_once(lambda dt: self._do_change_speed(speed), 0.1)

    def _do_change_speed(self, speed):
        output = self.sync.change_voice_speed(
            self.selected_audio, speed=speed
        )
        self.progress.value = 100
        if output:
            self.status_label.text = f"Velocidad cambiada: {output}"
            self._show_success_popup(output)
        else:
            self.status_label.text = "Error cambiando velocidad"
            self.progress.value = 0

    def _show_success_popup(self, path):
        content = BoxLayout(orientation='vertical', spacing=dp(10))
        content.add_widget(Label(text=f"Archivo generado:\n{path}"))
        close_btn = Button(text="Cerrar", size_hint_y=0.3)
        popup = Popup(title="Éxito", content=content, size_hint=(0.8, 0.4))
        close_btn.bind(on_press=popup.dismiss)
        content.add_widget(close_btn)
        popup.open()
