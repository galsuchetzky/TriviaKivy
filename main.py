"""
Main file, this is the file that buildozer runs (this is the application entrypoint).
"""

import kivy

kivy.require('2.1.0')

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager
from kivy.core.text import LabelBase
from kivy.properties import StringProperty
from kivy.core.audio import SoundLoader


from screens import *
from defaults import *


class TriviaApp(App):
    """
    This is the application that kivy builds.
    """
    default_font_size = StringProperty(str(DEFAULT_FONT_SIZE) + "sp")
    default_font_name = DEFALUT_FONT_NAME
    click_sound = SoundLoader.load('sounds/Click_Audio.wav')

    def build(self):
        """
        Adds all the screens to the application.
        :return: The screen manager.
        """
        for screen in screens:
            manager.add_widget(screen)

        return manager

    def btn_pressed(self):
        self.click_sound.play()



if __name__ == '__main__':
    # Instantiate the application.
    app = TriviaApp()

    # Load the kv file that describes the structure and layout of the content in the screens.
    kv = Builder.load_file("trivia.kv")

    # Instantiate the screen manager and the screens with their names.
    manager = ScreenManager()
    screens = [MainWindow(name="main"),
               GameModeSelectionWindow(name="game_mode_selection"),
               ScoreWindow(name="score"),
               SettingsWindow(name="settings"),
               GameWindow(name="game"),
               GameScoreWindow(name="game_score"),
               LoadingWindow(name="load_screen")]

    # Register our font.
    LabelBase.register(name="Arial", fn_regular="arial.ttf")



    # Run the application.
    app.run()

