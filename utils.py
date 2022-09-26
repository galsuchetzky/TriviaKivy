import kivy
import string

kivy.require('2.1.0')

from kivy.core.text import Label
from kivy.core.window import Window


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
