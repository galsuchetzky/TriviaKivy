import kivy

kivy.require('2.1.0')

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager
from kivy.core.text import LabelBase

from screens import *

"""
Notes:
"""


class TriviaApp(App):
    def build(self):
        for screen in screens:
            manager.add_widget(screen)

        return manager


if __name__ == '__main__':
    kv = Builder.load_file("trivia.kv")

    manager = ScreenManager()

    screens = [MainWindow(name="main"),
               GameModeSelectionWindow(name="game_mode_selection"),
               ScoreWindow(name="score"),
               SettingsWindow(name="settings"),
               GameWindow(name="game"),
               GameScoreWindow(name="game_score"),
               LoadingWindow(name="load_screen")]

    LabelBase.register(name="Arial", fn_regular="arial.ttf")

    TriviaApp().run()
