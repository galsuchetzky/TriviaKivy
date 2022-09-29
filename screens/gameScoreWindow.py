import kivy

kivy.require('2.1.0')

from kivy.properties import StringProperty
from kivy.uix.screenmanager import Screen
from kivy.clock import Clock


class GameScoreWindow(Screen):
    """
    Window for displaying the results of a game.
    """
    FINAL_SUCCESS_TXT = StringProperty("ענית נכון על:"[::-1])
    FINAL_SCORE_TXT = StringProperty("הניקוד שלך:"[::-1])

    def __init__(self, name):
        super().__init__()
        self.name = name
        self.final_score = ""
        self.final_success = ""

    def on_pre_enter(self, *args):
        self.ids.score.text = self.final_score
        self.ids.success.text = self.final_success

        # Return to the main screen after 3 seconds.
        Clock.schedule_once(lambda *args: self.pass_main(), 3)

    def pass_main(self):
        self.manager.current = 'main'
