import kivy
import random
import time

import defaults
import utils
from timer import Timer

kivy.require('2.1.0')

from kivy.properties import StringProperty
from kivy.uix.screenmanager import Screen
from kivy.clock import Clock

from defaults import *


class GameWindow(Screen):
    TIME_TXT = StringProperty("זמן"[::-1])
    SCORE_TXT = StringProperty("ניקוד"[::-1])
    TIME_VALUE_TXT = StringProperty("00:00")
    SCORE_VALUE_TXT = StringProperty("")

    def __init__(self, name):
        super().__init__()
        self.name = name
        self.current_question = None
        self.clicked = False
        self.default_bg_normal = self.ids.ans0.background_normal
        self.default_bg_color = self.ids.ans0.background_color
        self.questions = None
        self.num_questions = 0
        self.correct_answers = 0
        self.timer = None
        self.mode = 0
        self.max_mistakes = None
        self.current_mistakes = 0
        self.current_streak = 0
        self.question_time = 0
        self.score = 0

    def init_game_properties(self):
        """
        Resets all the counters, the questions and labels.
        """
        # Initialize the questions, counters and labels.
        self.num_questions = len(self.questions)
        self.correct_answers = 0
        self.current_mistakes = 0
        self.ids.score.text = "0"
        self.max_mistakes = None
        self.current_streak = 0
        self.question_time = 0
        self.score = 0

    def init_game_by_mode(self):
        """
        Initialize the game attributes according to the selected mode.
        """
        if self.mode == defaults.GameModes.PRACTICE:
            self.timer = Timer(self.ids.timer)

        elif self.mode == defaults.GameModes.ERRORS3:
            self.timer = Timer(self.ids.timer)
            self.max_mistakes = 3

        elif self.mode == defaults.GameModes.ERRORS1:
            self.timer = Timer(self.ids.timer)
            self.max_mistakes = 1

        elif self.mode == defaults.GameModes.TIME:
            self.timer = Timer(self.ids.timer,
                               countdown=True,
                               countdown_start_time=180,
                               countdown_callback=self.finish_game)

    def on_pre_enter(self, *args):
        """
        Runs before the screen is loaded.
        """

        # Stop the menu music
        menu_music.stop()

        # Start the game music
        if game_music.status != 'play':
            game_music.play()

        # Initialize the game properties to be ready for starting.
        self.init_game_properties()

        # Set the game to the proper mode.
        self.init_game_by_mode()

        # Start the game timer.
        self.ids.timer.text = str(self.timer)
        self.timer.start()

        # Shuffle the questions and set the first question.
        random.shuffle(self.questions)
        self.set_question()

    def on_leave(self, *args):
        """
        Runs when we leave the screen.
        """
        # Stop the game music
        game_music.stop()

    def set_question(self, *args):
        """
        Sets a question in the game.
        """

        # Stop is the game is finished.
        if self.is_game_finished():
            return

        # Get the question.
        self.current_question = self.questions.pop()

        # Set the question text.
        self.ids.question.text = self.current_question.question

        # Shuffle the answers of the question.
        self.current_question.shuffle_answers()

        # Set the answers to the buttons.
        for i in range(4):
            self.ids['ans' + str(i)].background_normal = self.default_bg_normal
            self.ids['ans' + str(i)].background_color = self.default_bg_color
            self.ids['ans' + str(i)].text = self.current_question.answers[i]

        self.clicked = False

        # Take time
        self.question_time = time.time()

    def select_answer(self, selected_ans):
        """
        Runs when an answer is selected.
        :param selected_ans: The index of the selected answer.
        """
        # Make sure a different answer was not already clicked.
        if self.clicked:
            return
        self.clicked = True

        # Handle correct answer.
        if selected_ans == self.current_question.correct_answer:
            right_answer_sound.play()
            self.ids['ans' + str(selected_ans)].background_normal = ''
            self.ids['ans' + str(selected_ans)].background_color = 0, 1, 0, 1

            self.correct_answers += 1
            self.current_streak += 1

            # Calculate score
            t = time.time() - self.question_time
            if t < 8:
                self.score += 10 + self.current_streak * 6
            elif 8 <= t < 16:
                self.score += 8 + self.current_streak * 6
            elif 6 <= t < 32:
                self.score += 6 + self.current_streak * 6
            else:
                self.score += 5 + self.current_streak * 6

            self.question_time = 0

        # Handle incorrect answer.
        else:
            self.ids['ans' + str(selected_ans)].background_normal = ''
            self.ids['ans' + str(selected_ans)].background_color = 1, 0, 0, 1
            self.current_mistakes += 1
            self.current_streak = 0
            wrong_answer_sound.play()

        # Update the score.
        self.ids.score.text = str(self.score)

        # Continue to the next question after one second.
        Clock.schedule_once(self.set_question, 1)

    def is_game_finished(self):
        """
        Checks if the game is finished and if it is, terminates it.
        """
        if not self.questions or \
                (self.max_mistakes is not None and self.current_mistakes == self.max_mistakes):
            self.finish_game()
            return True
        return False

    def finish_game(self):
        """
        Changes to the score screen.
        """
        self.manager.get_screen('game_score').final_score = str(self.score)
        utils.save_score(self.score, self.mode)
        # TODO get real name from user!
        utils.post_score("Cyber", self.score, self.mode)
        self.manager.get_screen('game_score').final_success = str(self.correct_answers) + '/' + str(self.num_questions)
        self.manager.current = 'game_score'
        self.timer.stop()
