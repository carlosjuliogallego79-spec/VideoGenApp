"""
Pantalla de Texto a Voz (TTS).
"""

from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.slider import Slider
from kivy.uix.dropdown import DropDown
from kivy.uix.popup import Popup
from kivy.uix.progressbar import ProgressBar
from kivy.clock import Clock
from kivy.metrics import dp

from modules.tts_engine import TTSEngine


class TTSScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.tts = TTSEngine()
        self._build_ui()

    def _build_ui(self):
        layout = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10))

        # Header
        header = BoxLayout(size_hint_y=0.08, spacing=dp(10))
        back_btn = Button(text="< Atrás", size_hint_x=0.3)
        back_btn.bind(on_press=lambda x: setattr(self.manager, 'current', 'main'))
        header.add_widget(back_btn)
        header.add_widget(Label(text="Texto a Voz", font_size=dp(22), bold=True))
        layout.add_widget(header)

        # Área de texto
        layout.add_widget(Label(text="Texto a convertir:", size_hint_y=0.05))
        self.text_input = TextInput(
            text="Hola, bienvenido a VideoGenApp. Esta es una prueba de texto a voz.",
            multiline=True,
            size_hint_y=0.3,
        )
        layout.add_widget(self.text_input)

        # Controles de voz
        controls = GridLayout(cols=2, spacing=dp(10), size_hint_y=0.3)

        controls.add_widget(Label(text="Voz:"))
        self.voice_dropdown = DropDown()
        for voice in self.tts.get_voices():
            btn = Button(text=voice['name'], size_hint_y=None, height=dp(44))
            btn.bind(on_release=lambda x, v=voice: self._select_voice(v))
            self.voice_dropdown.add_widget(btn)

        self.voice_btn = Button(text=self.tts.available_voices[0]['name'])
        self.voice_btn.bind(on_release=self.voice_dropdown.open)
        controls.add_widget(self.voice_btn)

        controls.add_widget(Label(text="Velocidad:"))
        speed_box = BoxLayout(spacing=dp(5))
        self.speed_slider = Slider(min=0.5, max=2.0, value=1.0, step=0.1)
        self.speed_label = Label(text="1.0x", size_hint_x=0.3)
        self.speed_slider.bind(value=lambda s, v: setattr(self.speed_label, 'text', f'{v:.1f}x'))
        speed_box.add_widget(self.speed_slider)
        speed_box.add_widget(self.speed_label)
        controls.add_widget(speed_box)

        controls.add_widget(Label(text="Tono:"))
        pitch_box = BoxLayout(spacing=dp(5))
        self.pitch_slider = Slider(min=0.5, max=2.0, value=1.0, step=0.1)
        self.pitch_label = Label(text="1.0x", size_hint_x=0.3)
        self.pitch_slider.bind(value=lambda s, v: setattr(self.pitch_label, 'text', f'{v:.1f}x'))
        pitch_box.add_widget(self.pitch_slider)
        pitch_box.add_widget(self.pitch_label)
        controls.add_widget(pitch_box)

        layout.add_widget(controls)

        # Botones de acción
        actions = BoxLayout(size_hint_y=0.12, spacing=dp(10))

        preview_btn = Button(text="Vista Previa")
        preview_btn.bind(on_press=self._preview_tts)
        actions.add_widget(preview_btn)

        generate_btn = Button(
            text="Generar Audio",
            background_color=(0, 0.8, 0, 1),
            color=(1, 1, 1, 1),
        )
        generate_btn.bind(on_press=self._generate_tts)
        actions.add_widget(generate_btn)

        layout.add_widget(actions)

        # Barra de progreso
        self.progress = ProgressBar(max=100, value=0, size_hint_y=0.05)
        layout.add_widget(self.progress)

        # Estado
        self.status_label = Label(
            text="Listo",
            size_hint_y=0.05,
            color=(0.5, 0.5, 0.5, 1),
        )
        layout.add_widget(self.status_label)

        self.add_widget(layout)

    def _select_voice(self, voice):
        self.voice_btn.text = voice['name']
        self.selected_voice = voice
        self.voice_dropdown.dismiss()

    def _preview_tts(self, instance):
        text = self.text_input.text.strip()
        if not text:
            self.status_label.text = "Escribe algún texto primero"
            return

        self.status_label.text = "Generando vista previa..."
        self.progress.value = 30

        Clock.schedule_once(lambda dt: self._do_tts(preview=True), 0.1)

    def _generate_tts(self, instance):
        text = self.text_input.text.strip()
        if not text:
            self.status_label.text = "Escribe algún texto primero"
            return

        self.status_label.text = "Generando audio..."
        self.progress.value = 20

        Clock.schedule_once(lambda dt: self._do_tts(preview=False), 0.1)

    def _do_tts(self, preview=False):
        voice_code = "es-MX"
        if hasattr(self, 'selected_voice'):
            voice_code = self.selected_voice['lang']

        output = self.tts.text_to_speech(
            text=self.text_input.text.strip(),
            output_name="preview.mp3" if preview else "tts_output.mp3",
            voice=voice_code,
            speed=self.speed_slider.value,
            pitch=self.pitch_slider.value,
        )

        self.progress.value = 100

        if output:
            msg = f"Audio generado: {output}"
            if preview:
                msg = "Vista previa lista (reproduciría audio aquí)"
            self.status_label.text = msg
            self._show_success_popup(output)
        else:
            self.status_label.text = "Error generando audio"
            self.progress.value = 0

    def _show_success_popup(self, path):
        content = BoxLayout(orientation='vertical', spacing=dp(10))
        content.add_widget(Label(text=f"Audio guardado en:\n{path}"))
        close_btn = Button(text="Cerrar", size_hint_y=0.3)
        popup = Popup(title="Éxito", content=content, size_hint=(0.8, 0.4))
        close_btn.bind(on_press=popup.dismiss)
        content.add_widget(close_btn)
        popup.open()
