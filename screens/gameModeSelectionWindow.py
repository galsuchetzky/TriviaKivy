import kivy

import defaults

kivy.require('2.1.0')

from kivy.properties import StringProperty
from kivy.uix.screenmanager import Screen


class GameModeSelectionWindow(Screen):
    GAME_MODE_WELCOME_TXT = StringProperty("איך תרצה לשחק?"[::-1])
    PRACTICE_TXT = StringProperty("התאמן"[::-1])
    EASY_TXT = StringProperty("3 פסילות"[::-1])
    MEDIUM_TXT = StringProperty("פסילה אחת"[::-1])
    TIME_MODE_TXT = StringProperty("על זמן"[::-1])

    def __init__(self, name):
        super().__init__()
        self.name = name

    def pass_screen_main(self):
        self.manager.current = 'main'

    def start_game(self, mode):
        self.manager.get_screen('game').mode = defaults.GameModes(mode)
        self.manager.current = 'load_screen'
