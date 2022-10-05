import kivy

import utils

kivy.require('2.1.0')

from kivy.uix.screenmanager import Screen
from kivy.app import App
from kivy.properties import StringProperty


class WelcomeWindow(Screen):
    """
    Welcome Window.
    This window will pop the first time the player starts to play and ask for the player's name.
    """
    WELCOME_NEW_PLAYER_TXT = StringProperty("ברוך הבא! מה שמך?"[::-1])
    CONTINUE_TXT = StringProperty("המשך"[::-1])

    def __init__(self, name):
        super().__init__()
        self.name = name

        self.trigger = True
        self.input_text = ''

    def on_pre_enter(self, *args):
        # Hide the hidden name input
        self.ids.name_input_hidden.size_hint_y = None
        self.ids.name_input_hidden.height = 0

        # Set size of the name input
        self.ids.name_txt_input.size_hint_y = None
        self.ids.name_txt_input.height = utils.get_str_pixel_height() * 2

        # Set pref name if exsists
        prefs = utils.get_prefrences()
        if 'player_name' in prefs:
            self.ids.name_input_hidden.text = prefs['player_name']

    def fix_string(self, txt):
        if not self.trigger:
            return

        self.trigger = False
        self.ids.name_txt_input.text = utils.fix_string(txt)
        self.trigger = True

    def redirect_focus(self):
        self.ids.name_input_hidden.focus = True

    def continue_to_game(self):
        App.get_running_app().player_name = self.ids.name_input_hidden.text
        utils.save_prefrences(player_name=self.ids.name_input_hidden.text)
        self.manager.current = 'main'
