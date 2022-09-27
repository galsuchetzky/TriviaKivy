import kivy

kivy.require('2.1.0')

from kivy.properties import StringProperty
from kivy.uix.screenmanager import Screen
from kivy.core.audio import SoundLoader

from defaults import *


class MainWindow(Screen):
    """
    The menu screen.
    """
    WELCOME_TXT = StringProperty("ברוכים הבאים!"[::-1])
    PLAY_TXT = StringProperty("שחק"[::-1])
    SCORE_TXT = StringProperty("ניקוד"[::-1])
    SETTINGS_TXT = StringProperty("הגדרות"[::-1])
    EXIT_TXT = StringProperty("צא"[::-1])

    def __init__(self, name):
        super().__init__()
        self.name = name



    def on_enter(self, *args):
        """
        Runs right after the screen is loaded.
        """
        # Play the menu music if it is not playing already.
        if menu_music.status != 'play':
            menu_music.play()

    def quit(self):
        """
        Runs before the game is exited.
        :return:
        """
        exit()

    def pass_screen(self, screen):
        """
        Changes the current screen.
        :param screen: The screen to change to.
        """
        self.manager.current = screen
