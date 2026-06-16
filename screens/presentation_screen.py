"""
Pantalla de creación de presentaciones animadas.
"""

from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from kivy.uix.progressbar import ProgressBar
from kivy.clock import Clock
from kivy.metrics import dp

from modules.presentation import PresentationGenerator, Slide


class PresentationScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.pres_gen = PresentationGenerator()
        self._build_ui()

    def _build_ui(self):
        layout = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10))

        # Header
        header = BoxLayout(size_hint_y=0.08, spacing=dp(10))
        back_btn = Button(text="< Atrás", size_hint_x=0.3)
        back_btn.bind(on_press=lambda x: setattr(self.manager, 'current', 'main'))
        header.add_widget(back_btn)
        header.add_widget(Label(text="Presentaciones", font_size=dp(22), bold=True))
        layout.add_widget(header)

        # Editor de slide actual
        layout.add_widget(Label(text="Nuevo Slide:", size_hint_y=0.04))
        editor = GridLayout(cols=2, spacing=dp(8), size_hint_y=0.25)

        editor.add_widget(Label(text="Título:"))
        self.title_input = TextInput(text="Título del Slide", multiline=False)
        editor.add_widget(self.title_input)

        editor.add_widget(Label(text="Contenido:"))
        self.content_input = TextInput(
            text="Contenido del slide aquí...",
            multiline=True,
            size_hint_y=None,
            height=dp(60),
        )
        editor.add_widget(self.content_input)

        editor.add_widget(Label(text="Duración (s):"))
        self.dur_input = TextInput(text="5", multiline=False, input_filter='float')
        editor.add_widget(self.dur_input)

        editor.add_widget(Label(text="Animación:"))
        self.anim_input = TextInput(text="fade_in", multiline=False)
        editor.add_widget(self.anim_input)

        layout.add_widget(editor)

        # Botones de slide
        slide_actions = BoxLayout(size_hint_y=0.08, spacing=dp(10))
        add_btn = Button(text="Añadir Slide")
        add_btn.bind(on_press=self._add_slide)
        slide_actions.add_widget(add_btn)

        clear_btn = Button(text="Limpiar Todo")
        clear_btn.bind(on_press=self._clear_slides)
        slide_actions.add_widget(clear_btn)
        layout.add_widget(slide_actions)

        # Lista de slides (scroll)
        layout.add_widget(Label(text="Slides en la presentación:", size_hint_y=0.04))
        self.slides_container = BoxLayout(orientation='vertical', size_hint_y=None)
        self.slides_container.bind(minimum_height=self.slides_container.setter('height'))

        scroll = ScrollView(size_hint_y=0.25)
        scroll.add_widget(self.slides_container)
        layout.add_widget(scroll)

        # Contador
        self.count_label = Label(text="Total: 0 slides", size_hint_y=0.03)
        layout.add_widget(self.count_label)

        # Botones de generación
        gen_actions = BoxLayout(size_hint_y=0.1, spacing=dp(10))

        export_btn = Button(text="Exportar JSON")
        export_btn.bind(on_press=self._export_json)
        gen_actions.add_widget(export_btn)

        generate_btn = Button(
            text="Generar Presentación",
            background_color=(0, 0.8, 0, 1),
            color=(1, 1, 1, 1),
        )
        generate_btn.bind(on_press=self._generate_presentation)
        gen_actions.add_widget(generate_btn)

        layout.add_widget(gen_actions)

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

    def _add_slide(self, instance):
        slide = Slide(
            title=self.title_input.text,
            content=self.content_input.text,
            animation=self.anim_input.text,
            duration=float(self.dur_input.text),
        )
        self.pres_gen.add_slide(slide)
        self._refresh_slide_list()

    def _clear_slides(self, instance):
        self.pres_gen.clear_slides()
        self._refresh_slide_list()

    def _refresh_slide_list(self):
        self.slides_container.clear_widgets()
        for i, slide in enumerate(self.pres_gen.slides):
            slide_box = BoxLayout(size_hint_y=None, height=dp(40), spacing=dp(5))
            slide_box.add_widget(Label(
                text=f"{i+1}. {slide.title[:30]}",
                size_hint_x=0.7,
            ))
            del_btn = Button(text="X", size_hint_x=0.1, background_color=(0.8, 0, 0, 1))
            del_btn.bind(on_press=lambda x, idx=i: self._delete_slide(idx))
            slide_box.add_widget(del_btn)
            self.slides_container.add_widget(slide_box)

        self.count_label.text = f"Total: {len(self.pres_gen.slides)} slides"

    def _delete_slide(self, index):
        if 0 <= index < len(self.pres_gen.slides):
            self.pres_gen.slides.pop(index)
            self._refresh_slide_list()

    def _export_json(self, instance):
        from utils.file_manager import FileManager
        fm = FileManager()
        path = fm.get_export_path("presentation.json")
        self.pres_gen.export_to_json(path)
        self.status_label.text = f"Exportado a {path}"

    def _generate_presentation(self, instance):
        if not self.pres_gen.slides:
            self.status_label.text = "Añade al menos un slide"
            return

        self.status_label.text = "Generando presentación..."
        self.progress.value = 10

        Clock.schedule_once(lambda dt: self._do_generate(), 0.1)

    def _do_generate(self):
        self.progress.value = 30

        output = self.pres_gen.generate_presentation(
            output_name="presentation_final.mp4",
            add_narration=True,
        )

        self.progress.value = 100

        if output:
            self.status_label.text = f"Presentación generada: {output}"
            self._show_success_popup(output)
        else:
            self.status_label.text = "Error generando presentación"
            self.progress.value = 0

    def _show_success_popup(self, path):
        content = BoxLayout(orientation='vertical', spacing=dp(10))
        content.add_widget(Label(text=f"Presentación guardada en:\n{path}"))
        close_btn = Button(text="Cerrar", size_hint_y=0.3)
        popup = Popup(title="Éxito", content=content, size_hint=(0.8, 0.4))
        close_btn.bind(on_press=popup.dismiss)
        content.add_widget(close_btn)
        popup.open()
