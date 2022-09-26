import kivy

kivy.require('2.1.0')

from kivy.properties import StringProperty
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty
from kivy.core.audio import SoundLoader


class MainWindow(Screen):
    WELCOME_TXT = StringProperty("ברוכים הבאים!"[::-1])
    PLAY_TXT = StringProperty("שחק"[::-1])
    SCORE_TXT = StringProperty("ניקוד"[::-1])
    SETTINGS_TXT = StringProperty("הגדרות"[::-1])
    EXIT_TXT = StringProperty("צא"[::-1])

    txt_inpt = ObjectProperty(None)

    def __init__(self, name):
        super().__init__()
        self.name = name

        self.menu_music = SoundLoader.load('sounds/Menu_Audio.wav')
        self.menu_music.volume = 0.4

    def on_enter(self, *args):
        if self.menu_music.status != 'play':
            self.menu_music.play()

    def quit(self):
        exit()

    def pass_screen(self, screen):
        self.manager.current = screen
