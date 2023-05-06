from Player import Player
from Round import Round
import pygame
import pygame, sys
import time 
import math
import operator
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
        
        self.idToPlayer = {}

        for player in self.gamePlayers:
            self.idToPlayer[player.whichPlayer] = player

        self.players = []

        self.rounds = (int)(rounds)
        self.currentRound = 1

        self.SCORES_DISPLAY_TIME = 5.0
        self.WINNER_DISPLAY_TIME = 6.0

        self.scores = {}
        self.scoreTexts = []

        self.scoreProfits = {}

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

        self.WINNER_TEXT = self.Font.get_title_font(smaller = 3 / self.sumProportion).render("Winner", True, "Gold")
        self.WINNER_RECT = self.WINNER_TEXT.get_rect(center=(self.screenWidth / 2, self.screenHeight / 5.0))


    def initializeChangableText(self):

        self.scoreTexts.clear()

        i = 1.5

        for key, value in self.scores.items():

            scoreText = self.idToPlayer[key].name + " " + str(value)
            profitText = "+ " + str(self.scoreProfits[key]) 

            self.SCORE_TEXT_WIDTH, self.SCORE_TEXT_HEIGHT = self.Font.get_title_font(smaller=4.0 / self.sumProportion).size(scoreText)

            self.SCORE_TEXT = self.Font.get_title_font(smaller=4 / self.sumProportion).render(scoreText, True, self.idToPlayer[key].color)
            self.SCORE_RECT = self.SCORE_TEXT.get_rect(center=(self.screenWidth / 2, self.screenHeight / 5.0 + self.SCORE_TEXT_HEIGHT * i))

            self.scoreTexts.append((self.SCORE_TEXT, self.SCORE_RECT))

            self.PROFIT_TEXT_WIDTH, self.PROFIT_TEXT_HEIGHT = self.Font.get_normal_font(smaller=8.0 / self.sumProportion).size(profitText)

            self.PROFIT_TEXT = self.Font.get_title_font(smaller= 8 / self.sumProportion).render(profitText, True, self.idToPlayer[key].color)
            self.PROFIT_RECT = self.PROFIT_TEXT.get_rect(center=(self.screenWidth / 2 + self.SCORE_TEXT_WIDTH / 2 + self.PROFIT_TEXT_WIDTH, self.screenHeight / 5.0 + self.SCORE_TEXT_HEIGHT * i))

            self.scoreTexts.append((self.PROFIT_TEXT, self.PROFIT_RECT))

            i += 1.5


    def displayScores(self):

        self.initializeChangableText()

        for scoreObject in [(self.SCORES_TEXT, self.SCORES_RECT)]:
                self.screen.blit(scoreObject[0], scoreObject[1])

        for playerScoreObject in self.scoreTexts:
            self.screen.blit(playerScoreObject[0], playerScoreObject[1])

        pygame.display.update()

        time.sleep(self.SCORES_DISPLAY_TIME)


    def displayWinner(self):

        for key, value in self.scores.items():
                     self.winningPlayerID = key
                     break
            
        self.winningPlayer = self.idToPlayer[self.winningPlayerID]

        self.WINNER_PLAYER_TEXT = self.Font.get_title_font(smaller = 3 / self.sumProportion).render(self.winningPlayer.name, True, self.winningPlayer.color)
        self.WINNER_PLAYER_RECT = self.WINNER_PLAYER_TEXT.get_rect(center=(self.screenWidth / 2, self.screenHeight / 3.0))

        self.gameMixer.pauseMusic()

        self.screen.fill(self.gameBackgroundColor)

        for winObject in [(self.WINNER_PLAYER_TEXT, self.WINNER_PLAYER_RECT), (self.WINNER_TEXT, self.WINNER_RECT)]:
            self.screen.blit(winObject[0], winObject[1])

        pygame.display.update()

        self.gameMixer.playSoundEffect(self.gameMixer.SoundBoard.gameWin)

        time.sleep(self.WINNER_DISPLAY_TIME)

        self.gameMixer.selectRandomSong()

        self.gameMixer.playMenuMusic()


    def calculateScores(self):

        for player in self.gamePlayers:
                self.scores[player.whichPlayer] = self.scores[player.whichPlayer] + len(self.gamePlayers) * 10
                self.scoreProfits[player.whichPlayer] = len(self.gamePlayers) * 10

        deathPenalty = 10
            
        if len(self.deathOrder) == len(self.gamePlayers):
            self.deathOrder.pop()

        for death in reversed(self.deathOrder):
            self.scores[death] = self.scores[death] - deathPenalty
            self.scoreProfits[death] -= deathPenalty
            deathPenalty += 10

        self.scores = dict(sorted(self.scores.items(), key=operator.itemgetter(1), reverse=True))


    def runGame(self):

        self.gameMixer.switchMusicAndPlay()

        self.screen.fill(self.gameBackgroundColor)

        clock = pygame.time.Clock() 
        
        while True:
            
            self.MENU_MOUSE_POS = pygame.mouse.get_pos()
            input = pygame.key.get_pressed() 
   
            round = Round(self.screen, self.screenWidth, self.screenHeight, self.gameMixer, self.gamePlayers, self.MINIMUM_ALIVE_PLAYERS, self.FPS, self.Font)
            self.deathOrder = round.startRound()

            self.calculateScores()
            self.displayScores()

            self.currentRound += 1

            if(self.currentRound == self.rounds + 1):

                self.displayWinner()
                break

            self.dealWithGameEvents()
                        
            pygame.display.update()
            clock.tick(self.FPS)
