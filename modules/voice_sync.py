"""
Módulo de sincronización y clonación de voz.
Soporta: lip-sync, clonación de voz con IA, ajuste de tono/velocidad.
"""

import os
import json
from kivy.utils import platform


class VoiceSynchronizer:
    def __init__(self):
        self.output_dir = self._get_output_dir()

    def _get_output_dir(self):
        if platform == 'android':
            from android.storage import app_storage_path
            return os.path.join(app_storage_path(), 'voice_sync')
        return os.path.join(os.path.expanduser('~'), 'VideoGenApp', 'voice_sync')

    def ensure_dirs(self):
        os.makedirs(self.output_dir, exist_ok=True)

    def sync_audio_to_video(self, video_path, audio_path, output_name=None):
        """
        Sincroniza un audio con un video existente.
        Reemplaza la pista de audio del video.

        Args:
            video_path: Ruta del video
            audio_path: Ruta del audio nuevo
            output_name: Nombre del archivo de salida

        Returns:
            Ruta del video sincronizado o None
        """
        self.ensure_dirs()
        if output_name is None:
            output_name = f"synced_{os.path.basename(video_path)}"
        output = os.path.join(self.output_dir, output_name)

        try:
            import subprocess
            cmd = [
                'ffmpeg', '-y',
                '-i', video_path,
                '-i', audio_path,
                '-map', '0:v:0',
                '-map', '1:a:0',
                '-c:v', 'copy',
                '-c:a', 'aac',
                '-shortest',
                output,
            ]
            subprocess.run(cmd, check=True, capture_output=True)
            return output
        except Exception as e:
            print(f"Error sincronizando audio: {e}")
            return None

    def adjust_voice_pitch(self, audio_path, semitones=0, output_name=None):
        """
        Ajusta el tono de una voz (positivo = más agudo, negativo = más grave).

        Args:
            audio_path: Ruta del archivo de audio
            semitones: Semitonos a ajustar (-12 a 12)
            output_name: Nombre del archivo de salida

        Returns:
            Ruta del audio ajustado o None
        """
        self.ensure_dirs()
        if output_name is None:
            base = os.path.basename(audio_path).rsplit('.', 1)[0]
            output_name = f"{base}_pitch{semitones}.mp3"
        output = os.path.join(self.output_dir, output_name)

        try:
            import ffmpeg
            stream = ffmpeg.input(audio_path)
            stream = ffmpeg.filter(
                stream, 'rubberband',
                pitch=2.0 ** (semitones / 12.0)
            )
            stream = ffmpeg.output(stream, output, acodec='aac')
            ffmpeg.run(stream, overwrite_output=True, quiet=True)
            return output
        except Exception as e:
            print(f"Error ajustando tono: {e}")
            return None

    def change_voice_speed(self, audio_path, speed=1.0, output_name=None):
        """
        Cambia la velocidad de reproducción sin afectar tono.

        Args:
            audio_path: Ruta del archivo de audio
            speed: Factor de velocidad (0.5 = lento, 2.0 = rápido)
            output_name: Nombre del archivo de salida

        Returns:
            Ruta del audio modificado o None
        """
        self.ensure_dirs()
        if output_name is None:
            base = os.path.basename(audio_path).rsplit('.', 1)[0]
            output_name = f"{base}_speed{speed}.mp3"
        output = os.path.join(self.output_dir, output_name)

        try:
            import ffmpeg
            stream = ffmpeg.input(audio_path)
            stream = ffmpeg.filter(stream, 'atempo', speed)
            stream = ffmpeg.output(stream, output, acodec='aac')
            ffmpeg.run(stream, overwrite_output=True, quiet=True)
            return output
        except Exception as e:
            print(f"Error cambiando velocidad: {e}")
            return None

    def extract_audio_from_video(self, video_path, output_name=None):
        """Extrae la pista de audio de un video."""
        self.ensure_dirs()
        if output_name is None:
            output_name = f"{os.path.basename(video_path)}_audio.mp3"
        output = os.path.join(self.output_dir, output_name)

        try:
            import ffmpeg
            stream = ffmpeg.input(video_path)
            stream = ffmpeg.output(stream, output, acodec='aac', vn=None)
            ffmpeg.run(stream, overwrite_output=True, quiet=True)
            return output
        except Exception as e:
            print(f"Error extrayendo audio: {e}")
            return None

    def merge_audio_with_video(self, video_path, audio_path, output_name=None):
        """Combina audio y video en un solo archivo."""
        return self.sync_audio_to_video(video_path, audio_path, output_name)

    def generate_lipsync_data(self, audio_path, transcript=None):
        """
        Genera datos de sincronización labial a partir de audio.
        Requiere biblioteca de reconocimiento de fonemas.

        Args:
            audio_path: Ruta del archivo de audio
            transcript: Transcripción opcional para mejorar precisión

        Returns:
            Dict con timestamps de fonemas o None
        """
        self.ensure_dirs()

        try:
            import speech_recognition as sr
            recognizer = sr.Recognizer()

            with sr.AudioFile(audio_path) as source:
                audio = recognizer.record(source)

            try:
                result = recognizer.recognize_google(audio, show_all=True)
            except sr.UnknownValueError:
                return None

            # Generar datos de fonemas aproximados
            lipsync_data = {
                "metadata": {
                    "audio_file": audio_path,
                    "sample_rate": 44100,
                    "transcript": transcript or "",
                },
                "phonemes": self._estimate_phonemes(result, audio),
            }

            output_path = os.path.join(
                self.output_dir,
                f"{os.path.basename(audio_path)}_lipsync.json"
            )
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(lipsync_data, f, indent=2)

            return lipsync_data

        except ImportError:
            print("SpeechRecognition no instalado")
            return None
        except Exception as e:
            print(f"Error generando lipsync: {e}")
            return None

    def _estimate_phonemes(self, recognition_result, audio_data):
        """Estima fonemas a partir del resultado de reconocimiento."""
        phonemes = []
        try:
            duration = len(audio_data.frame_data) / audio_data.sample_rate
            interval = duration / max(len(recognition_result), 1)

            current_time = 0.0
            phoneme_map = {
                'a': 'AA', 'e': 'EH', 'i': 'IH', 'o': 'AO', 'u': 'UH',
                'b': 'B', 'p': 'P', 'm': 'M', 'f': 'F', 'v': 'V',
                't': 'T', 'd': 'D', 'n': 'N', 's': 'S', 'z': 'Z',
                'k': 'K', 'g': 'G', 'l': 'L', 'r': 'R', 'w': 'W',
                'y': 'Y', 'h': 'HH',
            }

            for word in recognition_result.split():
                for char in word.lower():
                    phoneme = phoneme_map.get(char, 'SIL')
                    phonemes.append({
                        "phoneme": phoneme,
                        "start": current_time,
                        "end": current_time + interval,
                    })
                    current_time += interval

                # Silencio entre palabras
                current_time += interval * 0.3

        except Exception:
            pass

        return phonemes

    def clone_voice(self, audio_samples, text, output_name=None):
        """
        Clonación de voz usando modelo de IA.
        NOTA: Requiere API key de servicio de clonación (ElevenLabs, etc.)

        Args:
            audio_samples: Lista de rutas de audio de muestra de la voz
            text: Texto a generar con la voz clonada
            output_name: Nombre del archivo de salida

        Returns:
            Ruta del audio generado o None
        """
        self.ensure_dirs()
        if output_name is None:
            output_name = "cloned_voice.mp3"
        output = os.path.join(self.output_dir, output_name)

        # Placeholder - implementación real requiere API externa
        print("Clonación de voz requiere servicio externo (ElevenLabs, Resemble, etc.)")

        try:
            # Ejemplo con ElevenLabs (requiere API key)
            import requests

            api_key = "TU_ELEVENLABS_API_KEY"
            headers = {"xi-api-key": api_key}

            # Subir muestra de voz
            voice_id = self._create_voice_clone(audio_samples, headers)

            if voice_id:
                url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
                response = requests.post(
                    url,
                    headers=headers,
                    json={"text": text},
                )
                if response.status_code == 200:
                    with open(output, 'wb') as f:
                        f.write(response.content)
                    return output

            return None

        except Exception as e:
            print(f"Error clonando voz: {e}")
            return None

    def _create_voice_clone(self, audio_samples, headers):
        """Crea un clon de voz en ElevenLabs."""
        try:
            import requests
            url = "https://api.elevenlabs.io/v1/voices/add"

            files = []
            for i, sample in enumerate(audio_samples):
                files.append(
                    (f"files", (f"sample_{i}.mp3", open(sample, 'rb'), "audio/mpeg"))
                )

            response = requests.post(
                url,
                headers=headers,
                data={"name": "VoiceClone"},
                files=files,
            )

            for _, file_tuple in files:
                file_tuple[1].close()

            if response.status_code == 200:
                return response.json().get("voice_id")
            return None

        except Exception as e:
            print(f"Error creando clon de voz: {e}")
            return None
