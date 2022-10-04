from kivy.core.audio import SoundLoader
from enum import Enum

# Constants
DEFAULT_FONT_SIZE = 25
DEFALUT_FONT_NAME = "Linux-Biolinum"
MASTER_VOLUME = 0.5

# Sounds
click_sound = SoundLoader.load('sounds/Click_Audio.wav')
right_answer_sound = SoundLoader.load('sounds/Right_Answer.wav')
wrong_answer_sound = SoundLoader.load('sounds/Wrong_Answer.wav')

menu_music = SoundLoader.load('sounds/Menu_Audio.wav')
menu_music.loop = True

game_music = SoundLoader.load('sounds/Game_Audio.wav')
game_music.loop = True

sounds = [click_sound, right_answer_sound, wrong_answer_sound, menu_music, game_music]

# Game Modes
class GameModes(Enum):
    PRACTICE = 0
    ERRORS3 = 1
    ERRORS1 = 2
    TIME = 3

    @staticmethod
    def get_name(n):
        names = {
            0: 'אימון'[::-1],
            1: '3 טעויות'[::-1],
            2: 'טעות אחת'[::-1],
            3: 'זמן'[::-1]
        }
        return names[n]
