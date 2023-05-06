from Player import Player
import pygame
import pygame, sys
import time 
import math
from threading import Thread

class Round:

    def __init__(self, screen, screenWidth, screenHeight, mixer, lobbyPlayers, minimumAlivePlayers, FPS, font):

        self.screen = screen
        self.screenWidth = screenWidth
        self.screenHeight = screenHeight
        self.gameBackgroundColor = "black" 

        self.deathOrder = []
        self.Font = font

        self.MENU_MOUSE_POS = pygame.mouse.get_pos()

        self.FPS = FPS

        self.MINIMUM_ALIVE_PLAYERS = minimumAlivePlayers

        self.gameMixer = mixer

        self.lobbyPlayers = lobbyPlayers
        self.players = []

        for player in lobbyPlayers:
            if player.isAdded:
                self.players.append(Player(player.color, self.screenWidth, self.screenHeight, player.left, player.right, self.gameBackgroundColor, self.screen, self.FPS, player.speed, player.thickness, player.name, player.whichPlayer))


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


    def roundCountdown(self):

        self.gameMixer.setMusicVolume(self.gameMixer.musicVolume / 2)
        
        countDownStart = 3
        countDown = countDownStart

        self.gameMixer.playSoundEffect(self.gameMixer.SoundBoard.countdown)

        while True:

            if countDown == 0: break


            COUNT_TEXT = self.Font.get_title_font(smaller=2.0).render(str(countDown), True, "White")
            COUNT_RECT = COUNT_TEXT.get_rect(center=(self.screenWidth / 2.0, self.screenHeight / 4.0))

            COUNT_TEXT_WIDTH, COUNT_TEXT_HEIGHT = self.Font.get_title_font(smaller=2.0).size(str(countDown))

            self.screen.blit(COUNT_TEXT, COUNT_RECT)

            pygame.display.update()

            time.sleep(1)

            #drawing the same number but in black won't work, so rectangle has to be drawn
            pygame.draw.rect(self.screen, self.gameBackgroundColor, pygame.Rect(self.screenWidth / 2.0 - COUNT_TEXT_WIDTH / 2, self.screenHeight / 4.0 - COUNT_TEXT_HEIGHT / 2, COUNT_TEXT_WIDTH, COUNT_TEXT_HEIGHT))

            pygame.display.update()

            countDown -= 1


        self.gameMixer.setMusicVolume(self.gameMixer.musicVolume * 2)

    def startRound(self):

        self.screen.fill(self.gameBackgroundColor)

        clock = pygame.time.Clock() 

        roundStarted = False
        
        while True:
            
            self.MENU_MOUSE_POS = pygame.mouse.get_pos()

            moveThreads = []

            for player in self.players:
                moveThreads.append(Thread(target = player.movePlayerOnscreen, args = (self.screen, self.screenWidth, self.screenHeight, self.fillBoard, self.colorBoard, self.animateThreads, self.gameMixer, self.deathOrder)))
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
                    return self.deathOrder
                    break       

            input = pygame.key.get_pressed() 

            for i in self.players:
                i.handleInputForPlayer(input)

            self.dealWithGameEvents()

            if roundStarted == False:

                self.roundCountdown()
                roundStarted = True
                        
            pygame.display.update()
            clock.tick(self.FPS)
