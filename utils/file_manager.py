"""
Gestor de archivos multimedia.
Maneja la selección, organización y almacenamiento de archivos.
"""

import os
import shutil
import mimetypes
from datetime import datetime
from kivy.utils import platform


class FileManager:
    MEDIA_EXTENSIONS = {
        'image': ('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp'),
        'video': ('.mp4', '.avi', '.mov', '.mkv', '.webm', '.flv'),
        'audio': ('.mp3', '.wav', '.ogg', '.aac', '.flac', '.m4a'),
    }

    def __init__(self):
        self.base_dir = self._get_base_dir()
        self.import_dir = os.path.join(self.base_dir, 'imports')
        self.export_dir = os.path.join(self.base_dir, 'exports')
        self.temp_dir = os.path.join(self.base_dir, 'temp')
        self._ensure_dirs()

    def _get_base_dir(self):
        if platform == 'android':
            from android.storage import app_storage_path
            return os.path.join(app_storage_path(), 'VideoGenApp')
        return os.path.join(os.path.expanduser('~'), 'VideoGenApp')

    def _ensure_dirs(self):
        for d in [self.import_dir, self.export_dir, self.temp_dir]:
            os.makedirs(d, exist_ok=True)

    def get_media_files(self, media_type=None):
        """
        Lista archivos multimedia importados.
        Args:
            media_type: 'image', 'video', 'audio', o None para todos
        Returns:
            Lista de diccionarios con info de archivos
        """
        files = []
        extensions = []
        if media_type:
            extensions = self.MEDIA_EXTENSIONS.get(media_type, [])
        else:
            for exts in self.MEDIA_EXTENSIONS.values():
                extensions.extend(exts)

        for f in os.listdir(self.import_dir):
            if f.lower().endswith(extensions):
                fpath = os.path.join(self.import_dir, f)
                stat = os.stat(fpath)
                files.append({
                    'name': f,
                    'path': fpath,
                    'size': stat.st_size,
                    'modified': datetime.fromtimestamp(stat.st_mtime),
                    'type': self._classify_file(f),
                })

        files.sort(key=lambda x: x['modified'], reverse=True)
        return files

    def _classify_file(self, filename):
        ext = os.path.splitext(filename)[1].lower()
        for media_type, exts in self.MEDIA_EXTENSIONS.items():
            if ext in exts:
                return media_type
        return 'unknown'

    def import_file(self, source_path, rename=None):
        """
        Importa un archivo al directorio de imports.
        Returns: Ruta del archivo importado o None
        """
        if not os.path.exists(source_path):
            return None

        if rename:
            dest_name = rename
        else:
            dest_name = os.path.basename(source_path)

        dest_path = os.path.join(self.import_dir, dest_name)

        try:
            shutil.copy2(source_path, dest_path)
            return dest_path
        except Exception as e:
            print(f"Error importando archivo: {e}")
            return None

    def delete_file(self, filepath):
        """Elimina un archivo."""
        try:
            if os.path.exists(filepath):
                os.remove(filepath)
                return True
        except Exception as e:
            print(f"Error eliminando archivo: {e}")
        return False

    def get_temp_path(self, prefix='temp', extension='.mp4'):
        """Genera una ruta temporal única."""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
        return os.path.join(self.temp_dir, f"{prefix}_{timestamp}{extension}")

    def clear_temp(self):
        """Limpia archivos temporales."""
        try:
            for f in os.listdir(self.temp_dir):
                fpath = os.path.join(self.temp_dir, f)
                if os.path.isfile(fpath):
                    os.remove(fpath)
        except Exception as e:
            print(f"Error limpiando temp: {e}")

    def get_export_path(self, filename):
        """Obtiene ruta completa de exportación."""
        return os.path.join(self.export_dir, filename)
