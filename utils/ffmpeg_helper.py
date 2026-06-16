"""
Helper para operaciones con FFmpeg.
Proporciona wrappers para comandos comunes de FFmpeg.
"""

import os
import subprocess
import json
from kivy.utils import platform


class FFmpegHelper:
    def __init__(self):
        self.ffmpeg_path = self._find_ffmpeg()
        self.ffprobe_path = self._find_ffprobe()

    def _find_ffmpeg(self):
        if platform == 'android':
            paths = [
                '/data/data/org.videogenapp/files/ffmpeg',
                '/system/bin/ffmpeg',
                '/data/local/tmp/ffmpeg',
            ]
            for p in paths:
                if os.path.exists(p):
                    return p
            return 'ffmpeg'
        return 'ffmpeg'

    def _find_ffprobe(self):
        if platform == 'android':
            return '/data/data/org.videogenapp/files/ffprobe'
        return 'ffprobe'

    def probe(self, filepath):
        """Obtiene metadatos de un archivo multimedia."""
        try:
            result = subprocess.run(
                [self.ffprobe_path, '-v', 'quiet', '-print_format', 'json',
                 '-show_format', '-show_streams', filepath],
                capture_output=True, text=True, check=True,
            )
            return json.loads(result.stdout)
        except Exception as e:
            print(f"Error probing {filepath}: {e}")
            return None

    def get_duration(self, filepath):
        """Obtiene duración en segundos."""
        info = self.probe(filepath)
        if info and 'format' in info:
            return float(info['format']['duration'])
        return 0

    def get_resolution(self, video_path):
        """Obtiene resolución de un video."""
        info = self.probe(video_path)
        if info:
            for stream in info.get('streams', []):
                if stream['codec_type'] == 'video':
                    return (stream['width'], stream['height'])
        return (0, 0)

    def convert_format(self, input_path, output_path, codec='libx264'):
        """Convierte formato de video."""
        try:
            cmd = [
                self.ffmpeg_path, '-y', '-i', input_path,
                '-c:v', codec, '-preset', 'medium',
                output_path,
            ]
            subprocess.run(cmd, check=True, capture_output=True)
            return output_path
        except Exception as e:
            print(f"Error convirtiendo formato: {e}")
            return None

    def compress_video(self, input_path, output_path=None, crf=28):
        """Comprime un video reduciendo tamaño."""
        if output_path is None:
            name, ext = os.path.splitext(input_path)
            output_path = f"{name}_compressed{ext}"

        try:
            cmd = [
                self.ffmpeg_path, '-y', '-i', input_path,
                '-c:v', 'libx264', '-crf', str(crf),
                '-preset', 'medium', '-c:a', 'aac',
                output_path,
            ]
            subprocess.run(cmd, check=True, capture_output=True)
            return output_path
        except Exception as e:
            print(f"Error comprimiendo video: {e}")
            return None

    def extract_frame(self, video_path, time_sec, output_path):
        """Extrae un frame en un tiempo específico."""
        try:
            cmd = [
                self.ffmpeg_path, '-y', '-i', video_path,
                '-ss', str(time_sec), '-vframes', '1',
                output_path,
            ]
            subprocess.run(cmd, check=True, capture_output=True)
            return output_path
        except Exception as e:
            print(f"Error extrayendo frame: {e}")
            return None

    def resize_video(self, input_path, width, height, output_path=None):
        """Cambia el tamaño de un video."""
        if output_path is None:
            name, ext = os.path.splitext(input_path)
            output_path = f"{name}_{width}x{height}{ext}"

        try:
            cmd = [
                self.ffmpeg_path, '-y', '-i', input_path,
                '-vf', f'scale={width}:{height}',
                '-c:a', 'copy',
                output_path,
            ]
            subprocess.run(cmd, check=True, capture_output=True)
            return output_path
        except Exception as e:
            print(f"Error redimensionando video: {e}")
            return None

    def trim_video(self, input_path, start, end, output_path=None):
        """Corta un video entre start y end (segundos)."""
        if output_path is None:
            name, ext = os.path.splitext(input_path)
            output_path = f"{name}_trimmed{ext}"

        duration = end - start
        try:
            cmd = [
                self.ffmpeg_path, '-y', '-i', input_path,
                '-ss', str(start), '-t', str(duration),
                '-c', 'copy',
                output_path,
            ]
            subprocess.run(cmd, check=True, capture_output=True)
            return output_path
        except Exception as e:
            print(f"Error recortando video: {e}")
            return None

    def concatenate_videos(self, video_paths, output_path):
        """Concatena múltiples videos."""
        try:
            list_file = os.path.join(
                os.path.dirname(output_path), '_concat_list.txt'
            )
            with open(list_file, 'w') as f:
                for vp in video_paths:
                    f.write(f"file '{vp}'\n")

            cmd = [
                self.ffmpeg_path, '-y', '-f', 'concat',
                '-safe', '0', '-i', list_file,
                '-c', 'copy',
                output_path,
            ]
            subprocess.run(cmd, check=True, capture_output=True)
            os.unlink(list_file)
            return output_path
        except Exception as e:
            print(f"Error concatenando videos: {e}")
            return None

    def is_available(self):
        """Verifica si FFmpeg está disponible."""
        try:
            subprocess.run(
                [self.ffmpeg_path, '-version'],
                capture_output=True, check=True,
            )
            return True
        except Exception:
            return False
