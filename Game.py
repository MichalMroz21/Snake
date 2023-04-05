from Button import Button
from Player import Player
from Mixer import Mixer
import pygame
import pygame, sys
import time 
import math

class Game:

    def __init__(self, SCREEN):

        self.SCREEN = SCREEN
        self.MENU_MOUSE_POS = pygame.mouse.get_pos()
        self.gameBackgroundColor = "black" 
        self.gameVolume = 0.5
        self.player = Player()
        self.gameMixer = Mixer()


    def dealWithEvents(self):
        for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == self.gameMixer.SONG_END:
                    self.gameMixer.switchMusicAndPlay()


    def play(self):

        self.gameMixer.setMusicVolume(self.gameVolume)
        self.gameMixer.switchMusicAndPlay()

        self.SCREEN.fill(self.gameBackgroundColor)

        lastFrameTime = time.time()
        clock = pygame.time.Clock() 
        

        while True:
            
            self.MENU_MOUSE_POS = pygame.mouse.get_pos()

            self.player.movePlayerOnScreen(self.SCREEN, self.gameBackgroundColor)

            input = pygame.key.get_pressed() 
            self.player.useInputForPlayer(input)

            self.dealWithEvents()
                        
            pygame.display.update()
            clock.tick(60)
