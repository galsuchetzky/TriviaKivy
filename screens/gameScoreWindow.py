import kivy

kivy.require('2.1.0')

from kivy.properties import StringProperty
from kivy.uix.screenmanager import Screen
from kivy.clock import Clock


class GameScoreWindow(Screen):
    """
    Window for displaying the results of a game.
    """
    FINAL_SCORE_TXT = StringProperty("ההצלחה שלך היא:"[::-1])

    def __init__(self, name):
        super().__init__()
        self.name = name
        self.final_score = ""

    def on_pre_enter(self, *args):
        self.ids.score.text = self.final_score

        # Return to the main screen after 3 seconds.
        Clock.schedule_once(lambda *args: self.pass_main(), 3)

    def pass_main(self):
        self.manager.current = 'main'
