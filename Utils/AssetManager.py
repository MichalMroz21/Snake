import pygame
import random
import enum


BASE_FOLDER = "Assets"

FONT_FOLDER = "font"
MUSIC_FOLDER = "music"
SOUNDS_FOLDER = "sounds"
PICTURE_FOLDER = "picture"

FONTS_BASE = BASE_FOLDER + "/" + FONT_FOLDER + "/"
MUSIC_BASE = BASE_FOLDER + "/" + MUSIC_FOLDER + "/"
SOUNDS_BASE = BASE_FOLDER + "/" + SOUNDS_FOLDER + "/"
PICTURE_BASE = BASE_FOLDER + "/" + PICTURE_FOLDER + "/"


class AssetManager:
    class Fonts(enum.Enum):
        LATO = FONTS_BASE + 'Lato-Regular.ttf'

    class Music(enum.Enum):
        DISCO_CRAZE = MUSIC_BASE + "ES_Disco Craze - Rymdklang Soundtracks.mp3"
        NOVA = MUSIC_BASE + "ES_Doozy - _91nova.mp3"
        SUN_WAVE = MUSIC_BASE + "ES_Leaving Lunar - Sum Wave.mp3"
        PANDARAPS = MUSIC_BASE + "ES_Loopty Loops (Instrumental Version) - Pandaraps.mp3"
        ZORRO = MUSIC_BASE + "ES_MANNERS (Instrumental Version) - Zorro.mp3"
        DYLAN = MUSIC_BASE + "ES_Twenty Five - Dylan Sitts.mp3"

    class Sounds(enum.Enum):
        DEATH = SOUNDS_BASE + "417486__mentoslat__8-bit-death-sound.wav"
        COUNTDOWN = SOUNDS_BASE + "546602__nxrt__arcade-countdown.wav"
        LEVEL_WIN = SOUNDS_BASE + "258142__tuudurt__level-win.wav"

    class Pictures(enum.Enum):
        MENU_BACKGROUND = PICTURE_BASE + "MenuBackground.jpg"
