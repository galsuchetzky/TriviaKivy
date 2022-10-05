"""
Utilities file.
"""

import kivy
import string
import json
import certifi
import urllib

kivy.require('2.1.0')

from kivy.core.text import Label
from kivy.core.window import Window
from kivy.network.urlrequest import UrlRequest
from kivy.app import App

from defaults import *
from datetime import date
from pathlib import Path


def is_hebrew(s):
    """
    Checks if a string is a hebrew word.
    Note:
    - Assuming that a string that contains a letter in hebrew is a hebrew word.
    - Assuming that s is a single word.
    :param s: The word to check.
    :return: True iff the word is in hebrew.
    """
    for c in s:
        if 1488 <= ord(c) <= 1514:
            return True

    return False


def get_str_pixel_width(s, **kwargs):
    """
    Calculates the pixel width of the given string.
    :param s: The string to calculate the length of.
    """
    return Label(**kwargs).get_extents(s)[0]


def get_str_pixel_height():
    """
    Calculates the pixel height of the strings.
    """
    return Label(font_name=DEFALUT_FONT_NAME,
                 font_size=kivy.metrics.sp(DEFAULT_FONT_SIZE)).get_extents('test')[1]


def fix_string(s):
    """
    Fixes a string to be rendered correctly by kivy with both hebrew and english.
    :param s: The initial string to fix.
    :return: The fixed string.
    """
    # Split the text to sentences that fit in the length of the screen.
    x_size = Window.width
    acceptable_width = 9 * x_size // 10
    strings = []
    tmp = []

    for w in s.split():
        new_str_width = get_str_pixel_width(' '.join(tmp + [w]),
                                            font_name=DEFALUT_FONT_NAME,
                                            font_size=kivy.metrics.sp(DEFAULT_FONT_SIZE))
        if new_str_width > acceptable_width:
            strings.append(tmp[:])
            tmp = []
        tmp.append(w)
    if tmp:
        strings.append(tmp[:])

    fliped_braces = {'(': ')', ')': '(', '[': ']', ']': '[', '{': '}', '}': '{'}
    final = []
    # Fix each sentence.
    for fixed in strings:
        tmp = []

        # For each word, change it correctly.
        for i, w in enumerate(fixed):
            # Flip all braces.
            for j, c in enumerate(w):
                if c in fliped_braces:
                    w = w[:j] + fliped_braces[c] + w[j + 1:]

            # Handle Hebrew
            if is_hebrew(w):
                w = w[::-1]

            # Handle English and punctuation.
            else:
                # If the whole word is punctuation just reverse it.
                all_punc = True
                for c in w:
                    if c not in string.punctuation:
                        all_punc = False

                if all_punc:
                    w = w[::-1]

                # Otherwise reverse only the punctuation.
                else:
                    while w[-1] in string.punctuation:
                        w = w[-1] + w[:-1]
            tmp.append(w)

        # Reverse the sentence as it is rendered backward (from hebrew point of view)
        final.append(' '.join(tmp[::-1]))

    return '\n'.join(final)


# Todo later keep player entered name and create in backend a unique player id.
def save_score(score, game_mode):
    scores = get_scores()

    id = len(scores)
    new_score = {
        "id": id,
        "game_mode": game_mode.value,
        "score": score,
        "date": date.today().strftime("%d/%m/%Y")
    }

    scores[id] = new_score

    with open('scores.json', 'w', encoding="utf-8") as f:
        json.dump(scores, f)


def get_scores():
    scores_file = Path('scores.json')
    if not scores_file.is_file():
        with open('scores.json', 'w+', encoding="utf-8") as f:
            f.write('{}')

    with open('scores.json', 'r', encoding="utf-8") as f:
        try:
            scores = json.load(f)
        except:
            scores = {}

    return scores


def get_questions_from_server(question_file_name, callback):
    # TODO add timeout for waiting in case of no connection to server.
    # Request the questions file from the server.
    # Note that we use certifi things and verify otherwise it will not work on phone.
    # We use start as callback to start the game when the questions file is returned.
    url = f'http://10.0.0.7:5000/questions/{question_file_name}'
    UrlRequest(url, ca_file=certifi.where(), verify=True, on_success=callback)


def post_score(score, mode):
    params = urllib.parse.urlencode({'name': App.get_running_app().player_name,
                                     'score': score,
                                     'mode': mode.value})

    headers = {'Content-type': 'application/x-www-form-urlencoded',
               'Accept': 'text/plain'}

    url = 'http://10.0.0.7:5000/postscore'

    req = UrlRequest(url, req_body=params, req_headers=headers, ca_file=certifi.where(), verify=True)


def get_prefrences():
    prefrences_file = Path('prefrences.json')
    if not prefrences_file.is_file():
        with open('prefrences.json', 'w+', encoding="utf-8") as f:
            f.write('{}')

    with open('prefrences.json', 'r', encoding="utf-8") as f:
        try:
            prefrences = json.load(f)
        except:
            prefrences = {}

    return prefrences


def save_prefrences(**kwargs):
    prefs = {
        "player_name": kwargs['player_name'],
    }

    with open('prefrences.json', 'w', encoding="utf-8") as f:
        json.dump(prefs, f)
