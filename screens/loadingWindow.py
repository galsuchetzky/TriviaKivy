import kivy
import json
import certifi

kivy.require('2.1.0')

from kivy.uix.screenmanager import Screen
from kivy.network.urlrequest import UrlRequest

from question import Question


class LoadingWindow(Screen):
    def __init__(self, name):
        super().__init__()
        self.name = name

    def on_pre_enter(self, *args):
        url = 'https://raw.githubusercontent.com/galsuchetzky/TriviaKivy/main/questions/Biology%20test.json'
        req = UrlRequest(url, ca_file=certifi.where(), verify=True, on_success=self.start)

    def start(self, req, *args):
        questions_json = req.result
        questions = [Question(question) for question in list(json.loads(questions_json).values())]

        self.manager.get_screen('game').questions = questions
        self.manager.current = 'game'
