import kivy

kivy.require('2.1.0')

from kivy.uix.screenmanager import Screen


class SettingsWindow(Screen):
    def __init__(self, name):
        super().__init__()
        self.name = name