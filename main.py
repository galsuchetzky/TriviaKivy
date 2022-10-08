"""
Main file, this is the file that buildozer runs (this is the application entrypoint).
"""

import kivy
import defaults

kivy.require('2.1.0')

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager
from kivy.core.text import LabelBase
from kivy.properties import StringProperty, ListProperty
from kivy.core.window import Window

from screens import *
from defaults import *


class TriviaApp(App):
    """
    This is the application that kivy builds.
    """
    font_size = StringProperty(str(FONT_SIZE) + "sp")
    font_name = FONT_NAME
    player_name = 'no_name'
    background_src = StringProperty(BACKGROUND_LIGHT_SRC)
    font_color = ListProperty(FONT_COLOR_LIGHT)
    button_background_normal = BUTTON_BACKGROUND_NORMAL
    button_background_down = BUTTON_BACKGROUND_DOWN

    def build(self):
        """
        Adds all the screens to the application.
        :return: The screen manager.
        """
        for screen in screens:
            manager.add_widget(screen)

        Window.bind(on_keyboard=self.android_back_button)

        return manager

    def android_back_button(self, window, key, *args):
        """
        When the back button in android is pressed, respond with the appropriate action.
        :param window:
        :param key: The pressed key.
        :param args:
        :return:
        """

        # Checks if the pressed key is the back button (esc on pc)
        if key == 27:
            if manager.current == 'game_mode_selection':
                manager.current = 'main'
            if manager.current == 'score':
                manager.current = 'main'
            if manager.current == 'settings':
                manager.current = 'main'


        return True

    def btn_pressed(self):
        click_sound.volume = MASTER_VOLUME
        click_sound.play()


if __name__ == '__main__':
    # Instantiate the application.
    app = TriviaApp()

    # Load the kv file that describes the structure and layout of the content in the screens.
    kv = Builder.load_file("trivia.kv")

    # Instantiate the screen manager and the screens with their names.
    manager = ScreenManager()
    screens = [WelcomeWindow(name="welcome"),
               MainWindow(name="main"),
               GameModeSelectionWindow(name="game_mode_selection"),
               ScoreWindow(name="score"),
               SettingsWindow(name="settings"),
               GameWindow(name="game"),
               GameScoreWindow(name="game_score"),
               LoadingWindow(name="load_screen")]

    # Register our font.
    LabelBase.register(name="Arial", fn_regular="fonts/arial.ttf")
    LabelBase.register(name="Linux-Biolinum", fn_regular="fonts/Linux-Biolinum.ttf")
    LabelBase.register(name="DavidLibre-Regular", fn_regular="fonts/DavidLibre-Regular.ttf")
    LabelBase.register(name="Calibri", fn_regular="fonts/Calibri.ttf")

    # Run the application.
    app.run()
