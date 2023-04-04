from pygame import mixer
import pygame
import random

class Mixer:

    def __init__(self):

        mixer.init()
        self.musicPlaylist = ["assets/sound/ES_Disco Craze - Rymdklang Soundtracks.mp3",
                              "assets/sound/ES_Doozy - _91nova.mp3",
                               "assets/sound/ES_Leaving Lunar - Sum Wave.mp3",
                               "assets/sound/ES_MANNERS (Instrumental Version) - Zorro.mp3",
                               "assets/sound/ES_Twenty Five - Dylan Sitts.mp3"]
        self.soundEffects = []

        self.SONG_END = pygame.USEREVENT
        mixer.music.set_endevent(self.SONG_END)

        self.maxSongs = len(self.musicPlaylist)
        self.currentSong = random.randint(-1, self.maxSongs - 2) 
        
    def switchMusicAndPlay(self):

        self.currentSong = self.currentSong + 1
        if self.currentSong == self.maxSongs: self.currentSong = 0

        mixer.music.load(self.musicPlaylist[self.currentSong])
        mixer.music.play()

    def pauseMusic(self):
        mixer.music.pause()

    def unPauseMusic(self):
        mixer.music.unpause()

    def setMusicVolume(self, volume):
        mixer.music.set_volume(volume)

    def playSoundEffect(self, i):
        mixer.music.load(self.soundEffects[i])

