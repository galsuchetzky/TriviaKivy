import kivy

kivy.require('2.1.0')

from kivy.properties import StringProperty
from kivy.uix.screenmanager import Screen


class MainWindow(Screen):
    WELCOME_TXT = StringProperty("ברוכים הבאים!"[::-1])
    PLAY_TXT = StringProperty("שחק"[::-1])
    SCORE_TXT = StringProperty("ניקוד"[::-1])
    SETTINGS_TXT = StringProperty("הגדרות"[::-1])
    EXIT_TXT = StringProperty("צא"[::-1])

    def __init__(self, name):
        super().__init__()
        self.name = name

    @staticmethod
    def quit():
        exit()

    def pass_screen(self, screen):
        self.manager.current = screen
