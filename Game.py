from Player import Player
import pygame
import pygame, sys
import time 
import math
from threading import Thread

class Game:

    def __init__(self, screen, screenWidth, screenHeight, FPS, mixer, menu):

        self.screen = screen
        self.screenWidth = screenWidth
        self.screenHeight = screenHeight
        self.gameBackgroundColor = "black" 
        self.MENU_MOUSE_POS = pygame.mouse.get_pos()
        self.FPS = FPS

        self.menu = menu

        self.gameMixer = mixer

        self.players = []

        self.players.append(Player("Red", self.screenWidth, self.screenHeight, 'a', 'd', self.gameBackgroundColor, self.screen, self.FPS))
        self.players.append(Player("Blue", self.screenWidth, self.screenHeight, 'g', 'j', self.gameBackgroundColor, self.screen, self.FPS))

        self.fillBoard = [[0 for x in range(self.screenWidth)] for y in range(self.screenHeight)] 
        self.colorBoard = [[0 for x in range(self.screenWidth)] for y in range(self.screenHeight)] 

        self.animateThreads = []


    def dealWithGameEvents(self):
        for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == self.gameMixer.SONG_END:
                    self.gameMixer.switchMusicAndPlay()


    def play(self):

        self.gameMixer.switchMusicAndPlay()

        self.screen.fill(self.gameBackgroundColor)

        clock = pygame.time.Clock() 
        
        while True:
            
            self.MENU_MOUSE_POS = pygame.mouse.get_pos()

            moveThreads = []

            for player in self.players:
                moveThreads.append(Thread(target = player.movePlayerOnscreen, args = (self.screen, self.screenWidth, self.screenHeight, self.fillBoard, self.colorBoard, self.animateThreads, self.gameMixer)))
                moveThreads[-1].start()

            for moveThread in moveThreads:
                moveThread.join()      
                
            playersAlive = 0

            for player in self.players:
                if(player.isAlive):
                    playersAlive += 1


            if playersAlive < 2:
                allAnimationDead = True

                for animateThread in self.animateThreads:
                    if(animateThread.is_alive()): allAnimationDead = False

                if allAnimationDead: 

                    self.gameMixer.pauseMusic()
                    self.gameMixer.selectRandomSong()

                    self.menu.displayMainMenu(firstTime = True)
                    break       

            input = pygame.key.get_pressed() 

            for i in self.players:
                i.handleInputForPlayer(input)

            self.dealWithGameEvents()
                        
            pygame.display.update()
            clock.tick(self.FPS)
