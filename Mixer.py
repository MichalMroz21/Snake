from pygame import mixer
import pygame
import random
import enum

class Mixer:

    class SoundBoard(enum.Enum):
        death = 0
        countdown = 1

    def __init__(self, initialVolume):

        mixer.init()

        self.menuMusic = "assets/music/ES_Loopty Loops (Instrumental Version) - Pandaraps.mp3"

        self.musicPlaylist = ["assets/music/ES_Disco Craze - Rymdklang Soundtracks.mp3",
                              "assets/music/ES_Doozy - _91nova.mp3",
                               "assets/music/ES_Leaving Lunar - Sum Wave.mp3",
                               "assets/music/ES_MANNERS (Instrumental Version) - Zorro.mp3",
                               "assets/music/ES_Twenty Five - Dylan Sitts.mp3"]

        self.soundEffects = ["assets/sounds/417486__mentoslat__8-bit-death-sound.wav",
                             "assets/sounds/546602__nxrt__arcade-countdown.wav"]

        self.musicVolume = initialVolume
        self.soundVolume = initialVolume

        self.setMusicVolume(self.musicVolume)
        self.setSoundVolume(self.soundVolume)

        self.SONG_END = pygame.USEREVENT
        mixer.music.set_endevent(self.SONG_END)

        self.maxSongs = len(self.musicPlaylist)
        self.currentSong = self.selectRandomSong()

        
    def switchMusicAndPlay(self):
        self.unPauseMusic()

        self.currentSong = self.currentSong + 1
        if self.currentSong == self.maxSongs: self.currentSong = 0

        mixer.music.load(self.musicPlaylist[self.currentSong])
        mixer.music.play()


    def selectRandomSong(self):
        return random.randint(-1, self.maxSongs - 2) 

    def playMenuMusic(self):

        mixer.music.load(self.menuMusic)
        mixer.music.play()

    def playSoundEffect(self, soundEffect):

        sound = mixer.Sound(self.soundEffects[soundEffect.value])
        sound.play()
        sound.set_volume(self.soundVolume)

    def pauseMusic(self):
        mixer.music.pause()

    def unPauseMusic(self):
        mixer.music.unpause()

    def setMusicVolume(self, volume):
        self.musicVolume = volume
        mixer.music.set_volume(self.musicVolume)

    def setSoundVolume(self, volume):
        self.soundVolume = volume

        

