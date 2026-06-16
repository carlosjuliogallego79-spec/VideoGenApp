"""
Módulo de generación de video a partir de imágenes con transiciones.
Soporta: imágenes a video, transiciones (fade, slide, zoom), overlay de texto.
"""

import os
import tempfile
from kivy.utils import platform


class VideoGenerator:
    def __init__(self):
        self.output_dir = self._get_output_dir()

    def _get_output_dir(self):
        if platform == 'android':
            from android.storage import app_storage_path
            return os.path.join(app_storage_path(), 'videos')
        return os.path.join(os.path.expanduser('~'), 'VideoGenApp', 'videos')

    def ensure_dirs(self):
        os.makedirs(self.output_dir, exist_ok=True)

    def images_to_video(
        self,
        image_paths,
        output_name="output.mp4",
        fps=24,
        duration_per_image=3,
        transition="fade",
        transition_duration=0.5,
        resolution=(1920, 1080),
    ):
        """
        Genera un video a partir de una lista de imágenes.
        Usa FFmpeg para procesamiento.

        Args:
            image_paths: Lista de rutas de imágenes
            output_name: Nombre del archivo de salida
            fps: Cuadros por segundo
            duration_per_image: Duración en segundos por imagen
            transition: Tipo de transición (fade, slide, zoom)
            transition_duration: Duración de la transición en segundos
            resolution: Resolución del video (ancho, alto)

        Returns:
            Ruta del video generado o None si hay error
        """
        self.ensure_dirs()
        output_path = os.path.join(self.output_dir, output_name)

        if platform == 'android':
            return self._generate_android(
                image_paths, output_path, fps, duration_per_image,
                transition, transition_duration, resolution
            )
        return self._generate_desktop(
            image_paths, output_path, fps, duration_per_image,
            transition, transition_duration, resolution
        )

    def _generate_desktop(self, images, output, fps, dur, trans, trans_dur, res):
        try:
            import subprocess
            import ffmpeg

            inputs = []
            for img in images:
                inputs.append(
                    ffmpeg.input(img, loop=1, framerate=fps, t=dur)
                )

            if len(inputs) == 1:
                stream = inputs[0]
            else:
                joined = inputs[0]
                for i in range(1, len(inputs)):
                    if trans == "fade":
                        joined = ffmpeg.filter(
                            [joined, inputs[i]], 'xfade',
                            transition='fade', duration=trans_dur
                        )
                    elif trans == "slide":
                        joined = ffmpeg.filter(
                            [joined, inputs[i]], 'xfade',
                            transition='slideleft', duration=trans_dur
                        )
                    elif trans == "zoom":
                        joined = ffmpeg.filter(
                            [joined, inputs[i]], 'xfade',
                            transition='fadeblack', duration=trans_dur
                        )
                stream = joined

            stream = ffmpeg.output(
                stream, output,
                vcodec='libx264', pix_fmt='yuv420p',
                s=f'{res[0]}x{res[1]}'
            )
            ffmpeg.run(stream, overwrite_output=True, quiet=True)
            return output

        except Exception as e:
            print(f"Error generando video: {e}")
            return None

    def _generate_android(self, images, output, fps, dur, trans, trans_dur, res):
        try:
            import subprocess
            import shutil

            # En Android usamos FFmpeg directamente vía subprocess
            ffmpeg_bin = shutil.which('ffmpeg') or '/data/data/org.videogenapp/files/ffmpeg'

            # Crear archivo de lista de imágenes para FFmpeg concat
            list_file = os.path.join(self.output_dir, 'file_list.txt')
            with open(list_file, 'w') as f:
                for img in images:
                    f.write(f"file '{img}'\n")
                    f.write(f"duration {dur}\n")

            cmd = [
                ffmpeg_bin, '-y',
                '-f', 'concat',
                '-safe', '0',
                '-i', list_file,
                '-c:v', 'libx264',
                '-pix_fmt', 'yuv420p',
                '-s', f'{res[0]}x{res[1]}',
                '-r', str(fps),
                output
            ]
            subprocess.run(cmd, check=True, capture_output=True)
            return output

        except Exception as e:
            print(f"Error generando video en Android: {e}")
            return None

    def add_text_overlay(self, video_path, text, output_name=None):
        """Añade texto superpuesto a un video existente."""
        self.ensure_dirs()
        if output_name is None:
            output_name = f"texted_{os.path.basename(video_path)}"
        output = os.path.join(self.output_dir, output_name)

        try:
            import ffmpeg
            stream = ffmpeg.input(video_path)
            stream = ffmpeg.drawtext(
                stream, text=text,
                fontsize=48, fontcolor='white',
                x='(w-text_w)/2', y='h-th-50',
                enable=f'between(t,0,{self._get_duration(video_path)})'
            )
            stream = ffmpeg.output(stream, output, vcodec='libx264')
            ffmpeg.run(stream, overwrite_output=True, quiet=True)
            return output
        except Exception as e:
            print(f"Error añadiendo texto: {e}")
            return None

    def _get_duration(self, video_path):
        try:
            import ffmpeg
            probe = ffmpeg.probe(video_path)
            return float(probe['format']['duration'])
        except Exception:
            return 10

    def add_music(self, video_path, audio_path, output_name=None):
        """Añade música de fondo a un video."""
        self.ensure_dirs()
        if output_name is None:
            output_name = f"music_{os.path.basename(video_path)}"
        output = os.path.join(self.output_dir, output_name)

        try:
            import ffmpeg
            video = ffmpeg.input(video_path)
            audio = ffmpeg.input(audio_path)

            stream = ffmpeg.output(
                video, audio, output,
                vcodec='copy', acodec='aac',
                shortest=None
            )
            ffmpeg.run(stream, overwrite_output=True, quiet=True)
            return output
        except Exception as e:
            print(f"Error añadiendo música: {e}")
            return None
