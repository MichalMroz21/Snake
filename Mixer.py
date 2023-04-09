from pygame import mixer
import pygame
import random
import enum

class Mixer:

    class SoundBoard(enum.Enum):
        death = 0

    def __init__(self, gameVolume):

        mixer.init()

        self.musicPlaylist = ["assets/music/ES_Disco Craze - Rymdklang Soundtracks.mp3",
                              "assets/music/ES_Doozy - _91nova.mp3",
                               "assets/music/ES_Leaving Lunar - Sum Wave.mp3",
                               "assets/music/ES_MANNERS (Instrumental Version) - Zorro.mp3",
                               "assets/music/ES_Twenty Five - Dylan Sitts.mp3"]

        self.soundEffects = ["assets/sounds/417486__mentoslat__8-bit-death-sound.wav"]

        self.volume = gameVolume
        self.setMusicVolume(self.volume)

        self.SONG_END = pygame.USEREVENT
        mixer.music.set_endevent(self.SONG_END)

        self.maxSongs = len(self.musicPlaylist)
        self.currentSong = random.randint(-1, self.maxSongs - 2) 

        
    def switchMusicAndPlay(self):

        self.currentSong = self.currentSong + 1
        if self.currentSong == self.maxSongs: self.currentSong = 0

        mixer.music.load(self.musicPlaylist[self.currentSong])
        mixer.music.play()


    def playSoundEffect(self, soundEffect):
        sound = mixer.Sound(self.soundEffects[soundEffect.value])
        sound.play(0)

    def pauseMusic(self):
        mixer.music.pause()

    def unPauseMusic(self):
        mixer.music.unpause()

    def setMusicVolume(self, volume):
        mixer.music.set_volume(volume)

