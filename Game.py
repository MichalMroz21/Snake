from Player import Player
from Round import Round
import pygame
import pygame, sys
import time 
import math
from threading import Thread

class Game:

    def __init__(self, screen, screenWidth, screenHeight, FPS, mixer, menu, gamePlayers, minimumAlivePlayers, rounds, font):

        self.screen = screen
        self.screenWidth = screenWidth
        self.screenHeight = screenHeight
        self.gameBackgroundColor = "black" 
        self.MENU_MOUSE_POS = pygame.mouse.get_pos()
        self.FPS = FPS

        self.Font = font

        self.menu = menu
        self.MINIMUM_ALIVE_PLAYERS = minimumAlivePlayers

        self.gameMixer = mixer
        self.deathOrder = []

        self.gamePlayers = gamePlayers
        self.players = []

        self.rounds = (int)(rounds)
        self.currentRound = 1

        self.SCORES_DISPLAY_TIME = 5.0

        self.scores = {}
        self.scoreTexts = []

        self.sumProportion = (self.screenWidth + self.screenHeight) / 1000

        for player in self.gamePlayers:
            self.scores[player.whichPlayer] = 0

        self.initializeText()


    def dealWithGameEvents(self):
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == self.gameMixer.SONG_END:
                self.gameMixer.switchMusicAndPlay()


    def initializeText(self):

        self.SCORES_TEXT = self.Font.get_title_font(smaller = 3 / self.sumProportion).render("Scores", True, "Yellow")
        self.SCORES_RECT = self.SCORES_TEXT.get_rect(center=(self.screenWidth / 2, self.screenHeight / 5.0))


    def initializeChangableText(self):

        self.scoreTexts.clear()

        for i, player in enumerate(self.gamePlayers, 1):

            scoreText = player.name + " " + str(self.scores[player.whichPlayer])

            self.SCORE_TEXT_WIDTH, self.SCORE_TEXT_HEIGHT = self.Font.get_normal_font(smaller=2.0 / self.sumProportion).size(scoreText)

            self.SCORE_TEXT = self.Font.get_title_font(smaller=4 / self.sumProportion).render(scoreText, True, player.color)
            self.SCORE_RECT = self.SCORE_TEXT.get_rect(center=(self.screenWidth / 2, self.screenHeight / 5.0 + self.SCORE_TEXT_HEIGHT * i))

            self.scoreTexts.append((self.SCORE_TEXT, self.SCORE_RECT))


    def displayScores(self):

        self.initializeChangableText()

        for scoreObject in [(self.SCORES_TEXT, self.SCORES_RECT)]:
                self.screen.blit(scoreObject[0], scoreObject[1])

        for playerScoreObject in self.scoreTexts:
            self.screen.blit(playerScoreObject[0], playerScoreObject[1])

        pygame.display.update()

        time.sleep(self.SCORES_DISPLAY_TIME)


    def runGame(self):

        self.gameMixer.switchMusicAndPlay()

        self.screen.fill(self.gameBackgroundColor)

        clock = pygame.time.Clock() 
        
        while True:
            
            self.MENU_MOUSE_POS = pygame.mouse.get_pos()
            input = pygame.key.get_pressed() 
   
            round = Round(self.screen, self.screenWidth, self.screenHeight, self.gameMixer, self.gamePlayers, self.MINIMUM_ALIVE_PLAYERS, self.FPS)
            self.deathOrder = round.startRound()

            for player in self.gamePlayers:
                self.scores[player.whichPlayer] = self.scores[player.whichPlayer] + len(self.gamePlayers) * 10

            deathPenalty = 10
            
            if len(self.deathOrder) == len(self.gamePlayers):
                self.deathOrder.pop()

            for death in self.deathOrder:
                self.scores[death] = self.scores[death] - deathPenalty
                deathPenalty += 10

            self.displayScores()

            self.currentRound += 1



            if(self.currentRound == self.rounds + 1):
            
                self.gameMixer.pauseMusic()
                self.gameMixer.selectRandomSong()

                self.gameMixer.playMenuMusic()

                break

            self.dealWithGameEvents()
                        
            pygame.display.update()
            clock.tick(self.FPS)
