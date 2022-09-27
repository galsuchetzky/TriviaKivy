from kivy.core.audio import SoundLoader

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

sounds = [click_sound, right_answer_sound, wrong_answer_sound, menu_music]