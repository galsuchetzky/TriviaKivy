from kivy.core.audio import SoundLoader
from enum import Enum

# Constants
FONT_SIZE = 25
FONT_NAME = "Calibri"
BACKGROUND_LIGHT_SRC = 'images/background_light_mode.png'
BACKGROUND_DARK_SRC = 'images/background_dark_mode.png'
BUTTON_BACKGROUND_NORMAL = "images/button_background_normal.png"
BUTTON_BACKGROUND_DOWN = "images/button_background_down.png"
CORRECT_ANSWER_BACKGROUND = "images/correct_answer_background.png"
WRONG_ANSWER_BACKGROUND = "images/wrong_answer_background.png"
FONT_COLOR_DARK = (1, 0.9, 0.84, 1)  # White
FONT_COLOR_LIGHT = (0, 0, 0, 1)  # Black
MASTER_VOLUME = 0.5

SERVER_NAME = "http://triviakivy-env.eba-r2pdq2p3.us-east-1.elasticbeanstalk.com/"

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
            0: 'אימון',
            1: '3 טעויות',
            2: 'טעות אחת',
            3: 'זמן'
        }
        return names[n]
