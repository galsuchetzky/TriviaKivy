"""
Loading window for waiting between different loading activities in the project.
"""

import kivy

kivy.require('2.1.0')

from kivy.uix.screenmanager import Screen
from utils import *

from question import Question


class LoadingWindow(Screen):
    """
    A loading screen that should be used as a "waiting screen" for async actions to return.
    """
    def __init__(self, name):
        super().__init__()
        self.name = name

    def on_pre_enter(self, *args):
        # Request the questions file from the server.
        # url = 'https://raw.githubusercontent.com/galsuchetzky/TriviaKivy/main/questions/Biology%20test.json'
        # url = 'http://127.0.0.1:5000/questions/Biology%20test.json'


        # Note that we use certifi things and verify otherwise it will not work on phone.
        # We use start as callback to start the game when the questions file is returned.
        # req = UrlRequest(url, ca_file=certifi.where(), verify=True, on_success=self.start)

        # Get the questions file from the server.
        get_questions_from_server('Biology%20test.json', self.start)

    def start(self, req, *args):
        """
        Callback to be used for starting the game
        :param req: The request response.
        :param args: Additional arguments sent by UrlRequest when it returns.
        """
        # Parse the questions from the returned response.
        # questions_json = req.result
        questions = req.result
        # questions = [Question(question) for question in list(json.loads(questions_json).values())]
        questions = [Question(question) for question in list(questions.values())]

        # Set the questions to the game window and change to the game window.
        self.manager.get_screen('game').questions = questions
        self.manager.current = 'game'
