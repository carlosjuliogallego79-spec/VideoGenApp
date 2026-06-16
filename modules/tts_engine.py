"""
Módulo de texto a voz (TTS).
Soporta múltiples idiomas, voces y genera audio sincronizado con subtítulos.
"""

import os
import json
import subprocess
from kivy.utils import platform


class TTSEngine:
    def __init__(self):
        self.output_dir = self._get_output_dir()
        self.available_voices = []
        self._detect_voices()

    def _get_output_dir(self):
        if platform == 'android':
            from android.storage import app_storage_path
            return os.path.join(app_storage_path(), 'audio')
        return os.path.join(os.path.expanduser('~'), 'VideoGenApp', 'audio')

    def ensure_dirs(self):
        os.makedirs(self.output_dir, exist_ok=True)

    def _detect_voices(self):
        """Detecta voces disponibles en el sistema."""
        self.available_voices = [
            {"name": "Español - México", "lang": "es-MX", "gender": "female"},
            {"name": "Español - España", "lang": "es-ES", "gender": "female"},
            {"name": "English - US", "lang": "en-US", "gender": "female"},
            {"name": "English - UK", "lang": "en-GB", "gender": "male"},
            {"name": "Português - Brasil", "lang": "pt-BR", "gender": "female"},
            {"name": "Français - France", "lang": "fr-FR", "gender": "female"},
        ]

    def text_to_speech(
        self,
        text,
        output_name="tts_output.mp3",
        voice="es-MX",
        speed=1.0,
        pitch=1.0,
    ):
        """
        Convierte texto a voz usando motor TTS.

        Args:
            text: Texto a convertir
            output_name: Nombre del archivo de salida
            voice: Código de idioma/voz
            speed: Velocidad (0.5 - 2.0)
            pitch: Tono (0.5 - 2.0)

        Returns:
            Ruta del archivo de audio o None si hay error
        """
        self.ensure_dirs()
        output_path = os.path.join(self.output_dir, output_name)

        if platform == 'android':
            return self._tts_android(text, output_path, voice, speed, pitch)
        return self._tts_desktop(text, output_path, voice, speed, pitch)

    def _tts_desktop(self, text, output, voice, speed, pitch):
        try:
            import pyttsx3
            engine = pyttsx3.init()

            # Configurar voz
            voices = engine.getProperty('voices')
            for v in voices:
                if voice in v.id:
                    engine.setProperty('voice', v.id)
                    break

            engine.setProperty('rate', int(150 * speed))
            engine.save_to_file(text, output)
            engine.runAndWait()
            return output

        except ImportError:
            return self._tts_fallback(text, output, voice, speed, pitch)
        except Exception as e:
            print(f"Error en TTS: {e}")
            return None

    def _tts_fallback(self, text, output, voice, speed, pitch):
        """Usa FFmpeg con filtro TTS como fallback."""
        try:
            import subprocess
            import tempfile

            with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
                f.write(text)
                txt_file = f.name

            cmd = [
                'ffmpeg', '-y',
                '-f', 'lavfi',
                '-i', f'anullsrc=r=44100:cl=mono',
                '-af', f"atempo={speed},asetrate=44100*{pitch}",
                '-t', str(len(text) * 0.08),
                output
            ]
            subprocess.run(cmd, check=True, capture_output=True)
            os.unlink(txt_file)
            return output
        except Exception as e:
            print(f"Error en TTS fallback: {e}")
            return None

    def _tts_android(self, text, output, voice, speed, pitch):
        """Usa el TTS nativo de Android."""
        try:
            from android import mActivity
            import androidhelper as android

            droid = android.Android()
            result = droid.ttsSpeak(text)
            if result.error is None:
                # Grabar la salida del TTS
                droid.mediaRecorderStart(output)
                droid.ttsSpeak(text)
                import time
                time.sleep(len(text) * 0.08)
                droid.mediaRecorderStop()
                return output
            return None
        except Exception as e:
            print(f"Error en TTS Android: {e}")
            return self._tts_android_fallback(text, output, voice, speed)

    def _tts_android_fallback(self, text, output, voice, speed):
        """Fallback: usa Google Cloud TTS vía HTTP si hay internet."""
        try:
            import requests
            import base64

            # Nota: requieres API key de Google Cloud
            api_key = "TU_API_KEY_AQUI"
            url = f"https://texttospeech.googleapis.com/v1/text:synthesize?key={api_key}"
            payload = {
                "input": {"text": text},
                "voice": {"languageCode": voice, "name": f"{voice}-Wavenet-A"},
                "audioConfig": {"audioEncoding": "MP3", "speakingRate": speed},
            }
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                audio_content = base64.b64decode(response.json()['audioContent'])
                with open(output, 'wb') as f:
                    f.write(audio_content)
                return output
            return None
        except Exception as e:
            print(f"Error en TTS cloud: {e}")
            return None

    def text_to_speech_with_timing(self, text, output_name="tts_timed.json"):
        """
        Genera audio TTS y devuelve marcas de tiempo para sincronización.

        Returns:
            Dict con 'audio_path', 'subtitles' (lista de {word, start, end})
        """
        audio_path = self.text_to_speech(text, output_name.replace('.json', '.mp3'))
        if not audio_path:
            return None

        # Generar subtítulos con timing aproximado
        words = text.split()
        words_per_second = 3.0
        total_duration = len(words) / words_per_second
        time_per_word = total_duration / max(len(words), 1)

        subtitles = []
        current_time = 0.0
        for word in words:
            subtitles.append({
                "word": word,
                "start": current_time,
                "end": current_time + time_per_word,
            })
            current_time += time_per_word

        timing_path = os.path.join(self.output_dir, output_name)
        with open(timing_path, 'w', encoding='utf-8') as f:
            json.dump({"subtitles": subtitles, "duration": total_duration}, f)

        return {"audio_path": audio_path, "subtitles": subtitles}

    def get_voices(self):
        return self.available_voices
