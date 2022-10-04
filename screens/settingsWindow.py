import kivy

kivy.require('2.1.0')

from kivy.uix.screenmanager import Screen
from kivy.app import App
from kivy.properties import StringProperty

import defaults


class SettingsWindow(Screen):
    """
    Settings Window.
    """
    SETTINGS_HEADER_TXT = StringProperty("הגדרות"[::-1])
    FONT_TXT = StringProperty("גודל גופן:"[::-1])
    VOLUME_TXT = StringProperty("עוצמת מוזיקה:"[::-1])

    def __init__(self, name):
        super().__init__()
        self.name = name
        self.ids.font_size_slider.value = defaults.DEFAULT_FONT_SIZE
        self.ids.volume_slider.value = defaults.MASTER_VOLUME

    def set_font_size(self, n):
        """
        Sets the font size.
        :param n: The new font size.
        """
        defaults.DEFAULT_FONT_SIZE = n
        App.get_running_app().default_font_size = str(n) + 'sp'

    def set_master_volume(self, n):
        """
        Sets the volume of everything.
        :param n: The new volume.
        """
        defaults.MASTER_VOLUME = n
        self.ids.volume_slider.value = n
        for sound in defaults.sounds:
            sound.volume = n

    def pass_screen_main(self):
        self.manager.current = 'main'
