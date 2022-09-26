import string

import kivy
import json
import random
import certifi

kivy.require('2.1.0')

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.text import LabelBase, Label
from kivy.properties import StringProperty
from kivy.clock import Clock
from kivy.network.urlrequest import UrlRequest
from kivy.core.window import Window

"""
Notes:
"""


class Question:
    """
    Represents a question in the game.
    """

    def __init__(self, question_dict):
        """
        Initiates a new question from a python dict of the following format:
        {
            "index": 5,
            "question": "your question here",
            "correct": 0,
            "ans0": "a",
            "ans1": "b",
            "ans2": "c",
            "ans3": "d"
        }
        :param question_dict: the question dict.
        """
        self.index = question_dict["index"]
        self.question = fix_string(question_dict["question"])
        self.correct_answer = int(question_dict["correct"])
        self.answers = []

        for i in range(4):
            tag = 'ans' + str(i)
            self.answers.append(fix_string(question_dict[tag]))


class Timer:
    def __init__(self, label, countdown=False, countdown_start_time=0, countdown_callback=None):
        self.label = label
        self.countdown = countdown
        self.time = countdown_start_time if countdown else 0
        self.countdown_callback = countdown_callback
        self.running = False

    def start(self):
        self.running = True
        Clock.schedule_once(self.update, 1)

    def update(self, *args):
        if not self.countdown:
            self.time += 1
        else:
            self.time -= 1
            if not self.time:
                self.countdown_callback()
                return

        self.label.text = str(self)

        if self.running:
            Clock.schedule_once(self.update, 1)

    def stop(self):
        self.running = False

    def __str__(self):
        return str((self.time // 60) % 60).zfill(2) + ':' + str(self.time % 60).zfill(2)


def is_hebrew(s):
    for c in s:
        if 1488 <= ord(c) <= 1514:
            return True

    return False


def get_str_pixel_width(s, **kwargs):
    return Label(**kwargs).get_extents(s)[0]


def fix_string(s):
    x_size = Window.width
    acceptable_width = 9 * x_size // 10
    strings = []
    tmp = []
    for w in s.split():
        if get_str_pixel_width(' '.join(tmp + [w]), font_name="arial", font_size=kivy.metrics.sp(15)) > acceptable_width:
            strings.append(tmp[:])
            tmp = []
        tmp.append(w)
    if tmp:
        strings.append(tmp[:])

    # print(Window.size)
    # print(get_str_pixel_width(s, font_name="arial"))
    # fixed = s.split()
    final = []
    for fixed in strings:
        tmp = []
        for i, w in enumerate(fixed):
            if not is_hebrew(w):
                all_punc = True
                for c in w:
                    if c not in string.punctuation:
                        all_punc = False

                if all_punc:
                    w = w[::-1]
                else:
                    while w[-1] in string.punctuation:
                        w = w[-1] + w[:-1]
            tmp.append(w)
        fixed = tmp
        fixed = fixed[::-1]
        fixed = [w[::-1] if is_hebrew(w) else w for w in fixed]
        fixed = ' '.join(fixed)
        final.append(fixed)

    return '\n'.join(final)


class MainWindow(Screen):
    WELCOME_TXT = StringProperty("ברוכים הבאים!"[::-1])
    WELCOME_TXT = StringProperty(fix_string(
        "שלום, dude לי קוראים Gal. איך קוראים לך??? זה טקסט ארוך בעברית כדי לבדוק האם זה הולך להוריד שורה כמו שצריך אם אני יורד ידנית"))
    PLAY_TXT = StringProperty("שחק"[::-1])
    SCORE_TXT = StringProperty("ניקוד"[::-1])
    SETTINGS_TXT = StringProperty("הגדרות"[::-1])
    EXIT_TXT = StringProperty("צא"[::-1])

    def __init__(self, name):
        super().__init__()
        self.name = name
        self.ids.welcome_label.text = str(Window.width) + '\n' + str(get_str_pixel_width("שלום, dude לי קוראים Gal. איך קוראים לך??? זה טקסט ארוך בעברית כדי לבדוק האם זה הולך להוריד שורה כמו שצריך אם אני יורד ידנית", font_name="arial", font_size=kivy.metrics.sp(15)))

    def quit(self):
        exit()

    def pass_screen_game_mode_selection(self):
        manager.current = 'game_mode_selection'

    def pass_screen_score(self):
        manager.current = 'score'

    def pass_screen_settings(self):
        manager.current = 'settings'


class GameModeSelectionWindow(Screen):
    GAME_MODE_WELCOME_TXT = StringProperty("איך תרצה לשחק?"[::-1])
    PRACTICE_TXT = StringProperty("התאמן"[::-1])
    EASY_TXT = StringProperty("3 פסילות"[::-1])
    MEDIUM_TXT = StringProperty("פסילה אחת"[::-1])
    TIME_MODE_TXT = StringProperty("על זמן"[::-1])
    BACK_TXT = StringProperty("חזור"[::-1])

    def __init__(self, name):
        super().__init__()
        self.name = name

    def pass_screen_main(self):
        manager.current = 'main'

    def start_game(self, mode):
        manager.get_screen('game').mode = mode
        manager.current = 'load_screen'


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
        manager.get_screen('game_score').final_score = str(self.correct_answers) + '/' + str(self.num_questions)
        manager.current = 'game_score'
        self.timer.stop()


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

        manager.get_screen('game').questions = questions
        manager.current = 'game'


class ScoreWindow(Screen):
    def __init__(self, name):
        super().__init__()
        self.name = name


class GameScoreWindow(Screen):
    FINAL_SCORE_TXT = StringProperty("ההצלחה שלך היא:"[::-1])

    def __init__(self, name):
        super().__init__()
        self.name = name
        self.final_score = ""

    def on_pre_enter(self, *args):
        self.ids.score.text = self.final_score

        Clock.schedule_once(lambda *args: self.pass_main(), 3)

    def pass_main(self):
        manager.current = 'main'


class SettingsWindow(Screen):
    def __init__(self, name):
        super().__init__()
        self.name = name


kv = Builder.load_file("trivia.kv")

manager = ScreenManager()

screens = [MainWindow(name="main"),
           GameModeSelectionWindow(name="game_mode_selection"),
           ScoreWindow(name="score"),
           SettingsWindow(name="settings"),
           GameWindow(name="game"),
           GameScoreWindow(name="game_score"),
           LoadingWindow(name="load_screen")]


class TriviaApp(App):
    def build(self):
        for screen in screens:
            manager.add_widget(screen)

        return manager


if __name__ == '__main__':
    LabelBase.register(name="Arial", fn_regular="arial.ttf")

    TriviaApp().run()
