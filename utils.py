"""
Utilities file.
"""

import kivy
import string

kivy.require('2.1.0')

from kivy.core.text import Label
from kivy.core.window import Window
from defaults import *


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
    x_size = Window.width
    acceptable_width = 9 * x_size // 10
    strings = []
    tmp = []
    for w in s.split():
        if get_str_pixel_width(' '.join(tmp + [w]), font_name="arial", font_size=kivy.metrics.sp(DEFAULT_FONT_SIZE)) > acceptable_width:
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
