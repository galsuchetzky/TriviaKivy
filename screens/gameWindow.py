import kivy
import random

from timer import Timer

kivy.require('2.1.0')

from kivy.properties import StringProperty
from kivy.uix.screenmanager import Screen
from kivy.core.audio import SoundLoader
from kivy.clock import Clock


class GameWindow(Screen):
    TIME_TXT = StringProperty("זמן"[::-1])
    SUCCESS_TXT = StringProperty("הצלחה"[::-1])
    TIME_VALUE_TXT = StringProperty("00:00")
    SUCCESS_VALUE_TXT = StringProperty("")

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
        self.right_answer_sound = SoundLoader.load('sounds/Right_Answer.wav')
        self.wrong_answer_sound = SoundLoader.load('sounds/Wrong_Answer.wav')

    def init_game_properties(self):
        """
        Resets all the counters, the questions and labels.
        """
        # Initialize the questions, counters and labels.
        self.num_questions = len(self.questions)
        self.correct_answers = 0
        self.current_mistakes = 0
        self.ids.score.text = str(self.correct_answers) + '/' + str(self.num_questions)
        self.max_mistakes = None

    def init_game_by_mode(self):
        """
        Initialize the game attributes according to the selected mode.
        """
        if self.mode == 0:
            self.timer = Timer(self.ids.timer)

        elif self.mode == 1:
            self.timer = Timer(self.ids.timer)
            self.max_mistakes = 3

        elif self.mode == 2:
            self.timer = Timer(self.ids.timer)
            self.max_mistakes = 1

        elif self.mode == 3:
            self.timer = Timer(self.ids.timer,
                               countdown=True,
                               countdown_start_time=180,
                               countdown_callback=self.finish_game)

    def on_pre_enter(self, *args):
        """
        Runs before the screen is loaded.
        """

        # Stop menu music
        self.manager.get_screen('main').menu_music.stop()

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
            self.ids['ans' + str(selected_ans)].background_normal = ''
            self.ids['ans' + str(selected_ans)].background_color = 0, 1, 0, 1
            self.correct_answers += 1
            self.right_answer_sound.play()

        # Handle incorrect answer.
        else:
            self.ids['ans' + str(selected_ans)].background_normal = ''
            self.ids['ans' + str(selected_ans)].background_color = 1, 0, 0, 1
            self.current_mistakes += 1
            self.wrong_answer_sound.play()

        # Update the score counter.
        self.ids.score.text = str(self.correct_answers) + '/' + str(self.num_questions)

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
        self.manager.get_screen('game_score').final_score = str(self.correct_answers) + '/' + str(self.num_questions)
        self.manager.current = 'game_score'
        self.timer.stop()
