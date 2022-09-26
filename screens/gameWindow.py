import kivy
import random

from timer import Timer

kivy.require('2.1.0')

from kivy.properties import StringProperty
from kivy.uix.screenmanager import Screen
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

    def on_pre_enter(self, *args):
        self.num_questions = len(self.questions)
        self.correct_answers = 0
        self.current_mistakes = 0
        self.ids.score.text = str(self.correct_answers) + '/' + str(self.num_questions)
        if self.mode == 0:
            self.timer = Timer(self.ids.timer)
            self.max_mistakes = None
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
        self.ids.timer.text = str(self.timer)
        self.timer.start()

        random.shuffle(self.questions)
        self.set_question()

    def set_question(self, *args):
        if self.is_game_finished():
            return

        self.current_question = self.questions.pop()
        self.ids.question.text = self.current_question.question

        for i in range(4):
            self.ids['ans' + str(i)].background_normal = self.default_bg_normal
            self.ids['ans' + str(i)].background_color = self.default_bg_color
            self.ids['ans' + str(i)].text = self.current_question.answers[i]

        self.clicked = False

    def select_answer(self, selected_ans):
        if self.clicked:
            return
        self.clicked = True

        if selected_ans == self.current_question.correct_answer:
            self.ids['ans' + str(selected_ans)].background_normal = ''
            self.ids['ans' + str(selected_ans)].background_color = 0, 1, 0, 1
            self.correct_answers += 1
        else:
            self.ids['ans' + str(selected_ans)].background_normal = ''
            self.ids['ans' + str(selected_ans)].background_color = 1, 0, 0, 1
            self.current_mistakes += 1

        self.ids.score.text = str(self.correct_answers) + '/' + str(self.num_questions)
        Clock.schedule_once(self.set_question, 1)

    def is_game_finished(self):
        print(self.current_mistakes, self.max_mistakes)
        if not self.questions or \
                (self.max_mistakes is not None and self.current_mistakes == self.max_mistakes):
            self.finish_game()
            return True
        return False

    def finish_game(self):
        self.manager.get_screen('game_score').final_score = str(self.correct_answers) + '/' + str(self.num_questions)
        self.manager.current = 'game_score'
        self.timer.stop()
