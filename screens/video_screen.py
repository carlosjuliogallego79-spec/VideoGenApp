"""
Pantalla de generación de video desde imágenes.
"""

import os
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.popup import Popup
from kivy.uix.progressbar import ProgressBar
from kivy.uix.dropdown import DropDown
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.utils import platform

from modules.video_generator import VideoGenerator


class VideoScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.video_gen = VideoGenerator()
        self.selected_images = []
        self._build_ui()

    def _build_ui(self):
        layout = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10))

        # Header
        header = BoxLayout(size_hint_y=0.1, spacing=dp(10))
        back_btn = Button(text="< Atrás", size_hint_x=0.3)
        back_btn.bind(on_press=lambda x: setattr(self.manager, 'current', 'main'))
        header.add_widget(back_btn)

        title = Label(text="Generar Video", font_size=dp(22), bold=True)
        header.add_widget(title)
        layout.add_widget(header)

        # Configuración
        config = GridLayout(cols=2, spacing=dp(10), size_hint_y=0.3)

        config.add_widget(Label(text="FPS:"))
        self.fps_input = TextInput(text="24", multiline=False, input_filter='int')
        config.add_widget(self.fps_input)

        config.add_widget(Label(text="Duración por imagen (s):"))
        self.dur_input = TextInput(text="3", multiline=False, input_filter='float')
        config.add_widget(self.dur_input)

        config.add_widget(Label(text="Transición:"))
        self.trans_dropdown = DropDown()
        for trans in ["fade", "slide", "zoom"]:
            btn = Button(text=trans, size_hint_y=None, height=dp(44))
            btn.bind(on_release=lambda x, t=trans: self._select_transition(t))
            self.trans_dropdown.add_widget(btn)

        self.trans_btn = Button(text="fade")
        self.trans_btn.bind(on_release=self.trans_dropdown.open)
        config.add_widget(self.trans_btn)

        config.add_widget(Label(text="Resolución:"))
        res_grid = BoxLayout(spacing=dp(5))
        self.width_input = TextInput(text="1920", multiline=False, input_filter='int', size_hint_x=0.5)
        self.height_input = TextInput(text="1080", multiline=False, input_filter='int', size_hint_x=0.5)
        res_grid.add_widget(self.width_input)
        res_grid.add_widget(Label(text="x", size_hint_x=0.2))
        res_grid.add_widget(self.height_input)
        config.add_widget(res_grid)

        layout.add_widget(config)

        # Lista de imágenes seleccionadas
        self.images_label = Label(
            text="Imágenes seleccionadas: 0",
            size_hint_y=0.05,
        )
        layout.add_widget(self.images_label)

        # Botones de acción
        actions = BoxLayout(size_hint_y=0.12, spacing=dp(10))

        select_btn = Button(text="Seleccionar Imágenes")
        select_btn.bind(on_press=self._select_images)
        actions.add_widget(select_btn)

        generate_btn = Button(
            text="Generar Video",
            background_color=(0, 0.8, 0, 1),
            color=(1, 1, 1, 1),
        )
        generate_btn.bind(on_press=self._generate_video)
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

    def _select_transition(self, trans):
        self.trans_btn.text = trans
        self.trans_dropdown.dismiss()

    def _select_images(self, instance):
        if platform == 'android':
            self._select_images_android()
        else:
            self._select_images_desktop()

    def _select_images_desktop(self):
        content = BoxLayout(orientation='vertical', spacing=dp(10))
        filechooser = FileChooserListView(
            path=os.path.expanduser('~'),
            filters=['*.png', '*.jpg', '*.jpeg', '*.gif', '*.bmp'],
        )
        content.add_widget(filechooser)

        btn_layout = BoxLayout(size_hint_y=0.15, spacing=dp(10))
        cancel_btn = Button(text="Cancelar")
        select_btn = Button(text="Añadir Seleccionadas")

        popup = Popup(
            title="Seleccionar Imágenes",
            content=content,
            size_hint=(0.9, 0.9),
        )

        def on_select(instance):
            self.selected_images.extend(filechooser.selection)
            self.images_label.text = f"Imágenes seleccionadas: {len(self.selected_images)}"
            popup.dismiss()

        select_btn.bind(on_press=on_select)
        cancel_btn.bind(on_press=popup.dismiss)
        btn_layout.add_widget(cancel_btn)
        btn_layout.add_widget(select_btn)
        content.add_widget(btn_layout)

        popup.open()

    def _select_images_android(self):
        from android import mActivity
        from jnius import autoclass

        Intent = autoclass('android.content.Intent')
        PickVisualMedia = autoclass('androidx.activity.result.contract.PickVisualMedia')
        ActivityResultContracts = autoclass('androidx.activity.result.contract.ActivityResultContracts')

        # Lanzar selector de imágenes
        intent = Intent(Intent.ACTION_GET_CONTENT)
        intent.setType('image/*')
        intent.putExtra(Intent.EXTRA_ALLOW_MULTIPLE, True)
        # Nota: Se necesita ActivityResultLauncher para Android moderno

        self.status_label.text = "Selecciona imágenes desde tu dispositivo"

    def _generate_video(self, instance):
        if not self.selected_images:
            self.status_label.text = "Selecciona al menos una imagen"
            return

        try:
            fps = int(self.fps_input.text)
            duration = float(self.dur_input.text)
            width = int(self.width_input.text)
            height = int(self.height_input.text)
            transition = self.trans_btn.text
        except ValueError:
            self.status_label.text = "Valores inválidos"
            return

        self.status_label.text = "Generando video..."
        self.progress.value = 20

        Clock.schedule_once(lambda dt: self._do_generate(
            fps, duration, transition, width, height
        ), 0.1)

    def _do_generate(self, fps, duration, transition, width, height):
        output = self.video_gen.images_to_video(
            self.selected_images,
            output_name=f"video_{len(self.selected_images)}img.mp4",
            fps=fps,
            duration_per_image=duration,
            transition=transition,
            resolution=(width, height),
        )

        self.progress.value = 100

        if output:
            self.status_label.text = f"Video generado: {output}"
            self._show_success_popup(output)
        else:
            self.status_label.text = "Error generando video"
            self.progress.value = 0

    def _show_success_popup(self, path):
        content = BoxLayout(orientation='vertical', spacing=dp(10))
        content.add_widget(Label(text=f"Video guardado en:\n{path}"))
        close_btn = Button(text="Cerrar", size_hint_y=0.3)
        popup = Popup(title="Éxito", content=content, size_hint=(0.8, 0.4))
        close_btn.bind(on_press=popup.dismiss)
        content.add_widget(close_btn)
        popup.open()
