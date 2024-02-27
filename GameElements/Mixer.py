from pygame import mixer
import pygame
import random
import enum

from Utils.AssetManager import AssetManager


class Mixer:
    class SoundBoard(enum.Enum):
        death = 0
        countdown = 1
        gameWin = 2

    def __init__(self, initial_volume):
        mixer.init()

        self.menuMusic = AssetManager.Music.PANDARAPS.value

        self.musicPlaylist = [AssetManager.Music.DISCO_CRAZE.value,
                              AssetManager.Music.NOVA.value,
                              AssetManager.Music.SUN_WAVE.value,
                              AssetManager.Music.ZORRO.value,
                              AssetManager.Music.DYLAN.value]

        self.soundEffects = [AssetManager.Sounds.DEATH.value,
                             AssetManager.Sounds.COUNTDOWN.value,
                             AssetManager.Sounds.LEVEL_WIN.value]

        self.musicVolume = self.soundVolume = initial_volume

        self.set_music_volume(self.musicVolume)
        self.set_sound_volume(self.soundVolume)

        self.SONG_END = pygame.USEREVENT
        mixer.music.set_endevent(self.SONG_END)

        self.maxSongs = len(self.musicPlaylist)
        self.currentSong = self.select_random_song()

    def switch_music_and_play(self):
        self.un_pause_music()

        self.currentSong = self.currentSong + 1
        if self.currentSong == self.maxSongs:
            self.currentSong = 0

        mixer.music.load(self.musicPlaylist[self.currentSong])
        mixer.music.play()

    def select_random_song(self):
        return random.randint(-1, self.maxSongs - 2)

    def play_menu_music(self):
        mixer.music.load(self.menuMusic)
        mixer.music.play()

    def play_sound_effect(self, sound_effect):
        sound = mixer.Sound(self.soundEffects[sound_effect.value])
        sound.play()
        sound.set_volume(self.soundVolume)

    @staticmethod
    def pause_music():
        mixer.music.pause()

    @staticmethod
    def un_pause_music():
        mixer.music.unpause()

    def set_music_volume(self, volume):
        self.musicVolume = volume
        mixer.music.set_volume(self.musicVolume)

    def set_sound_volume(self, volume):
        self.soundVolume = volume



