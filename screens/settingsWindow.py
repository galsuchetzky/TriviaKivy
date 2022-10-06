import kivy

import utils

kivy.require('2.1.0')

from kivy.uix.screenmanager import Screen
from kivy.app import App
from kivy.properties import StringProperty, NumericProperty
from kivy.core.window import Window
from kivy.uix.gridlayout import GridLayout

import defaults


class SettingsWindow(Screen):
    """
    Settings Window.
    """
    SETTINGS_HEADER_TXT = StringProperty("הגדרות"[::-1])
    FONT_TXT = StringProperty("גודל גופן:"[::-1])
    VOLUME_TXT = StringProperty("עוצמת מוזיקה:"[::-1])
    DARK_MODE_TXT = StringProperty("מצב אפל:"[::-1])

    def __init__(self, name):
        super().__init__()
        self.name = name
        self.ids.font_size_slider.value = defaults.DEFAULT_FONT_SIZE
        self.ids.volume_slider.value = defaults.MASTER_VOLUME
        self.initialized = False

    def on_pre_enter(self, *args):
        if self.initialized:
            return

        self.ids.master_scroll_view.height = Window.size[1] - self.ids.settings_title.height
        grid = self.ids.master_grid
        self.set_grid_heights(grid)

    def set_grid_heights(self, grid):
        grid.height = 0
        for element in grid.children:
            grid.height += element.height
            if type(element) == GridLayout:
                self.set_grid_heights(element)

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

    def toggle_dark_mode(self, active):
        """
        Toggle dark mode on and off.
        """
        app = App.get_running_app()

        if active:
            app.background_src = defaults.BACKGROUND_DARK_SRC
            app.font_color = defaults.FONT_COLOR_DARK
        else:
            app.background_src = defaults.BACKGROUND_LIGHT_SRC
            app.font_color = defaults.FONT_COLOR_LIGHT
