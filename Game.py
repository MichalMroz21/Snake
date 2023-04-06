from Player import Player
from Mixer import Mixer
import pygame
import pygame, sys
import time 
import math

class Game:

    def __init__(self, SCREEN, SCREEN_WIDTH, SCREEN_HEIGHT, gameVolume):

        self.SCREEN = SCREEN
        self.MENU_MOUSE_POS = pygame.mouse.get_pos()
        self.gameBackgroundColor = "black" 
        self.gameVolume = gameVolume
        self.player = Player("Red", SCREEN_WIDTH, SCREEN_HEIGHT)
        self.gameMixer = Mixer(self.gameVolume)

        self.fillBoard = [[0 for x in range(SCREEN_WIDTH)] for y in range(SCREEN_HEIGHT)] 

    def dealWithEvents(self):
        for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == self.gameMixer.SONG_END:
                    self.gameMixer.switchMusicAndPlay()


    def play(self):

        self.gameMixer.switchMusicAndPlay()

        self.SCREEN.fill(self.gameBackgroundColor)

        lastFrameTime = time.time()
        clock = pygame.time.Clock() 
        

        while True:
            
            self.MENU_MOUSE_POS = pygame.mouse.get_pos()

            self.player.movePlayerOnScreen(self.SCREEN, self.gameBackgroundColor, self.fillBoard)

            input = pygame.key.get_pressed() 
            self.player.handleInputForPlayer(input)

            self.dealWithEvents()
                        
            pygame.display.update()
            clock.tick(60)
