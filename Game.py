from Player import Player
from Round import Round
import pygame
import pygame, sys
import time 
import math
from threading import Thread

class Game:

    def __init__(self, screen, screenWidth, screenHeight, FPS, mixer, menu, lobbyPlayers, minimumAlivePlayers, rounds):

        self.screen = screen
        self.screenWidth = screenWidth
        self.screenHeight = screenHeight
        self.gameBackgroundColor = "black" 
        self.MENU_MOUSE_POS = pygame.mouse.get_pos()
        self.FPS = FPS

        self.menu = menu
        self.MINIMUM_ALIVE_PLAYERS = minimumAlivePlayers

        self.gameMixer = mixer

        self.lobbyPlayers = lobbyPlayers
        self.players = []

        self.rounds = (int)(rounds)
        self.currentRound = 1



    def dealWithGameEvents(self):
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == self.gameMixer.SONG_END:
                self.gameMixer.switchMusicAndPlay()



    def runGame(self):

        self.gameMixer.switchMusicAndPlay()

        self.screen.fill(self.gameBackgroundColor)

        clock = pygame.time.Clock() 
        
        while True:
            
            self.MENU_MOUSE_POS = pygame.mouse.get_pos()
            input = pygame.key.get_pressed() 
   
            round = Round(self.screen, self.screenWidth, self.screenHeight, self.gameMixer, self.lobbyPlayers, self.MINIMUM_ALIVE_PLAYERS, self.FPS)
            round.startRound()

            self.currentRound += 1

            if(self.currentRound == self.rounds):
            
                self.gameMixer.pauseMusic()
                self.gameMixer.selectRandomSong()

                self.gameMixer.playMenuMusic()

                break

            self.dealWithGameEvents()
                        
            pygame.display.update()
            clock.tick(self.FPS)
