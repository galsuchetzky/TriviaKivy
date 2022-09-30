"""
Utilities file.
"""

import kivy
import string
import json

kivy.require('2.1.0')

from kivy.core.text import Label
from kivy.core.window import Window
from defaults import *

from datetime import date

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
                    w = w[:j] + fliped_braces[c] + w[j+1:]

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
def save_score(score):
    with open('scores.json', 'w+') as f:
        scores = json.load(f)

    id = len(scores)
    new_score = {
        "id": id,
        "score": score,
        "date": date.today().strftime("%d/%m/%Y")
    }

    scores[id] = new_score

    with open('scores.json', 'w+') as f:
        json.dump(scores, f)