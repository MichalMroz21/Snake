from Player import Player
import pygame
import pygame, sys
import time 
import math
from threading import Thread

class Game:

    def __init__(self, screen, screenWidth, screenHeight, FPS, mixer, menu, lobbyPlayers):

        self.screen = screen
        self.screenWidth = screenWidth
        self.screenHeight = screenHeight
        self.gameBackgroundColor = "black" 
        self.MENU_MOUSE_POS = pygame.mouse.get_pos()
        self.FPS = FPS

        self.menu = menu
        self.MINIMUM_ALIVE_PLAYERS = 2

        self.gameMixer = mixer

        self.lobbyPlayers = lobbyPlayers
        self.players = []

        for player in lobbyPlayers:
            if player.isAdded:
                self.players.append(Player(player.colorPicker.get_color(), self.screenWidth, self.screenHeight, player.LEFT_BOX.text, player.RIGHT_BOX.text, self.gameBackgroundColor, self.screen, self.FPS, float(player.SPEED_BOX.text), player.thickness, player.NAME_BOX.text))


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


            if playersAlive < self.MINIMUM_ALIVE_PLAYERS:
                allAnimationDead = True

                for animateThread in self.animateThreads:
                    if(animateThread.is_alive()): allAnimationDead = False

                if allAnimationDead: 

                    self.gameMixer.pauseMusic()
                    self.gameMixer.selectRandomSong()

                    break       

            input = pygame.key.get_pressed() 

            for i in self.players:
                i.handleInputForPlayer(input)

            self.dealWithGameEvents()
                        
            pygame.display.update()
            clock.tick(self.FPS)
