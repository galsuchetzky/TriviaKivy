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
    FONT_TXT = StringProperty("גודל גופן"[::-1])
    BACK_TXT = StringProperty("חזור"[::-1])

    def __init__(self, name):
        super().__init__()
        self.name = name

    def update_font_size(self, n):
        """
        Changes the font size.
        :param n: By how much to change.
        """
        new_size = int(App.get_running_app().default_font_size[:-2]) + n
        defaults.DEFAULT_FONT_SIZE = new_size
        App.get_running_app().default_font_size = str(new_size) + 'sp'

    def pass_screen_main(self):
        self.manager.current = 'main'
