"""
Módulo de presentaciones animadas.
Genera videos tipo slideshow con animaciones, narración y sincronización.
"""

import os
import json
from kivy.utils import platform

from modules.video_generator import VideoGenerator
from modules.tts_engine import TTSEngine


class Slide:
    def __init__(self, title="", content="", image_path=None,
                 animation="fade_in", duration=5.0, notes=""):
        self.title = title
        self.content = content
        self.image_path = image_path
        self.animation = animation
        self.duration = duration
        self.notes = notes


class PresentationGenerator:
    ANIMATIONS = [
        "fade_in", "slide_from_left", "slide_from_right",
        "zoom_in", "flip", "none",
    ]

    def __init__(self):
        self.video_gen = VideoGenerator()
        self.tts = TTSEngine()
        self.slides = []

    def add_slide(self, slide):
        self.slides.append(slide)

    def clear_slides(self):
        self.slides.clear()

    def generate_presentation(
        self,
        slides=None,
        output_name="presentation.mp4",
        fps=30,
        background_color=(0, 0, 0),
        resolution=(1920, 1080),
        add_narration=True,
        add_music=False,
        music_path=None,
    ):
        """
        Genera un video de presentación animada.

        Args:
            slides: Lista de objetos Slide (usa self.slides si es None)
            output_name: Nombre del archivo de salida
            fps: Cuadros por segundo
            background_color: Color RGB de fondo
            resolution: Resolución del video
            add_narration: Si añadir narración TTS
            add_music: Si añadir música de fondo
            music_path: Ruta del archivo de música

        Returns:
            Ruta del video generado o None
        """
        if slides is None:
            slides = self.slides

        if not slides:
            print("No hay slides para generar")
            return None

        self.video_gen.ensure_dirs()
        self.tts.ensure_dirs()
        output_path = os.path.join(self.video_gen.output_dir, output_name)

        try:
            # Generar imágenes para cada slide
            slide_images = []
            for i, slide in enumerate(slides):
                img_path = self._render_slide_to_image(
                    slide, i, resolution, background_color
                )
                if img_path:
                    slide_images.append(img_path)

            # Convertir imágenes a video
            video_path = self.video_gen.images_to_video(
                slide_images,
                output_name=f"raw_{output_name}",
                fps=fps,
                duration_per_image=max(s.duration for s in slides),
                transition="fade",
                transition_duration=0.5,
                resolution=resolution,
            )

            if not video_path:
                return None

            # Añadir narración
            if add_narration and slides:
                full_text = " ".join(s.notes or s.title for s in slides)
                audio = self.tts.text_to_speech(
                    full_text,
                    output_name=f"narration_{output_name}.mp3"
                )
                if audio:
                    video_path = self.video_gen.add_music(video_path, audio)

            # Añadir música de fondo
            if add_music and music_path:
                video_path = self.video_gen.add_music(video_path, music_path)

            # Renombrar al nombre final
            final_path = output_path
            if video_path != final_path:
                import shutil
                shutil.move(video_path, final_path)

            return final_path

        except Exception as e:
            print(f"Error generando presentación: {e}")
            return None

    def _render_slide_to_image(self, slide, index, resolution, bg_color):
        """Renderiza un slide como imagen usando Pillow."""
        try:
            from PIL import Image, ImageDraw, ImageFont

            img = Image.new('RGB', resolution, bg_color)
            draw = ImageDraw.Draw(img)

            # Cargar fuentes
            try:
                title_font = ImageFont.truetype("arial.ttf", 72)
                content_font = ImageFont.truetype("arial.ttf", 36)
            except Exception:
                title_font = ImageFont.load_default()
                content_font = ImageFont.load_default()

            # Dibujar título
            if slide.title:
                bbox = draw.textbbox((0, 0), slide.title, font=title_font)
                tw = bbox[2] - bbox[0]
                draw.text(
                    ((resolution[0] - tw) // 2, 100),
                    slide.title, fill='white', font=title_font
                )

            # Dibujar contenido
            if slide.content:
                lines = self._wrap_text(slide.content, content_font, resolution[0] - 200)
                y = 250
                for line in lines:
                    draw.text((100, y), line, fill='white', font=content_font)
                    y += 50

            # Añadir número de slide
            slide_num = f"{index + 1} / {len(self.slides)}"
            draw.text(
                (resolution[0] - 150, resolution[1] - 50),
                slide_num, fill='gray', font=content_font
            )

            # Guardar imagen temporal
            img_path = os.path.join(
                self.video_gen.output_dir,
                f"slide_{index:04d}.png"
            )
            img.save(img_path)
            return img_path

        except ImportError:
            print("Pillow no instalado. Usando modo texto plano.")
            return self._render_text_slide(slide, index, resolution)
        except Exception as e:
            print(f"Error renderizando slide {index}: {e}")
            return None

    def _render_text_slide(self, slide, index, resolution):
        """Renderiza slide como texto simple cuando Pillow no está disponible."""
        text_path = os.path.join(
            self.video_gen.output_dir,
            f"slide_{index:04d}.txt"
        )
        with open(text_path, 'w', encoding='utf-8') as f:
            f.write(f"{slide.title}\n{'='*40}\n{slide.content}")
        return text_path

    def _wrap_text(self, text, font, max_width):
        """Divide texto en líneas que caben en max_width píxeles."""
        words = text.split()
        lines = []
        current_line = ""

        for word in words:
            test_line = f"{current_line} {word}".strip()
            if font.getlength(test_line) > max_width:
                lines.append(current_line)
                current_line = word
            else:
                current_line = test_line

        if current_line:
            lines.append(current_line)
        return lines

    def export_to_json(self, filepath):
        """Exporta la presentación a JSON."""
        data = {
            "slides": [
                {
                    "title": s.title,
                    "content": s.content,
                    "image_path": s.image_path,
                    "animation": s.animation,
                    "duration": s.duration,
                    "notes": s.notes,
                }
                for s in self.slides
            ]
        }
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)

    def import_from_json(self, filepath):
        """Importa una presentación desde JSON."""
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)

        self.slides = []
        for s in data.get("slides", []):
            self.slides.append(Slide(
                title=s.get("title", ""),
                content=s.get("content", ""),
                image_path=s.get("image_path"),
                animation=s.get("animation", "fade_in"),
                duration=s.get("duration", 5.0),
                notes=s.get("notes", ""),
            ))
        return self.slides
