"""
VideoGenApp - Aplicación para generar video y sincronizar voces
Hecho con Kivy para Android
"""

import kivy
kivy.require('2.1.0')

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.utils import platform

from screens.main_screen import MainScreen
from screens.video_screen import VideoScreen
from screens.tts_screen import TTSScreen
from screens.presentation_screen import PresentationScreen
from screens.voice_sync_screen import VoiceSyncScreen
from screens.settings_screen import SettingsScreen


class VideoGenApp(App):
    def build(self):
        self.title = "VideoGenApp"
        self.sm = ScreenManager()

        self.sm.add_widget(MainScreen(name='main'))
        self.sm.add_widget(VideoScreen(name='video'))
        self.sm.add_widget(TTSScreen(name='tts'))
        self.sm.add_widget(PresentationScreen(name='presentation'))
        self.sm.add_widget(VoiceSyncScreen(name='voice_sync'))
        self.sm.add_widget(SettingsScreen(name='settings'))

        return self.sm


if __name__ == '__main__':
    if platform == 'android':
        from android.permissions import request_permissions, Permission
        request_permissions([
            Permission.WRITE_EXTERNAL_STORAGE,
            Permission.READ_EXTERNAL_STORAGE,
            Permission.RECORD_AUDIO,
        ])
    VideoGenApp().run()
