from Player import Player
from Mixer import Mixer
import pygame
import pygame, sys
import time 
import math
from threading import Thread

class Game:

    def __init__(self, SCREEN, SCREEN_WIDTH, SCREEN_HEIGHT, gameVolume, FPS):

        self.SCREEN = SCREEN
        self.SCREEN_WIDTH = SCREEN_WIDTH
        self.SCREEN_HEIGHT = SCREEN_HEIGHT
        self.gameBackgroundColor = "black" 
        self.MENU_MOUSE_POS = pygame.mouse.get_pos()
        self.FPS = FPS

        self.gameVolume = gameVolume
        self.gameMixer = Mixer(self.gameVolume)

        self.players = []

        self.players.append(Player("Red", self.SCREEN_WIDTH, self.SCREEN_HEIGHT, 'a', 'd', self.gameBackgroundColor, self.SCREEN, self.FPS))
        self.players.append(Player("Blue", self.SCREEN_WIDTH, self.SCREEN_HEIGHT, 'g', 'j', self.gameBackgroundColor, self.SCREEN, self.FPS))

        self.fillBoard = [[0 for x in range(self.SCREEN_WIDTH)] for y in range(self.SCREEN_HEIGHT)] 
        self.colorBoard = [[0 for x in range(self.SCREEN_WIDTH)] for y in range(self.SCREEN_HEIGHT)] 

    def dealWithGameEvents(self):
        for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == self.gameMixer.SONG_END:
                    self.gameMixer.switchMusicAndPlay()


    def play(self):

        self.gameMixer.switchMusicAndPlay()

        self.SCREEN.fill(self.gameBackgroundColor)

        clock = pygame.time.Clock() 
        
        while True:
            
            self.MENU_MOUSE_POS = pygame.mouse.get_pos()

            moveThreads = []

            for player in self.players:
                moveThreads.append(Thread(target = player.movePlayerOnScreen, args = (self.SCREEN, self.SCREEN_WIDTH, self.SCREEN_HEIGHT, self.fillBoard, self.colorBoard)))
                moveThreads[-1].start()

            for moveThread in moveThreads:
                moveThread.join()           

            input = pygame.key.get_pressed() 

            for i in self.players:
                i.handleInputForPlayer(input)

            self.dealWithGameEvents()
                        
            pygame.display.update()
            clock.tick(self.FPS)
