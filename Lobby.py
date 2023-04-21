import pygame, sys

from Button import Button
from LobbyPlayer import LobbyPlayer
from Game import Game

import time 

class Lobby:

    def __init__(self, screen, screenWidth, screenHeight, FPS, mixer, menu, font):
         
        self.screen = screen
        self.screenWidth = screenWidth
        self.screenHeight = screenHeight
        self.FPS = FPS
        self.mixer = mixer
        self.menu = menu
        self.Font = font

        self.BG = menu.BG
        self.LOBBY_MOUSE_POS = pygame.mouse.get_pos()
        
        self.maxPlayers = 4
        self.whichPlayerID_begin = 1

        self.lobbyPlayers = []

        for whichPlayer in range(self.whichPlayerID_begin, self.maxPlayers + 1):
            self.lobbyPlayers.append(LobbyPlayer(self.screen, self.screenWidth, self.screenHeight, whichPlayer, self.Font))

        self.initializeGUI()


    def initializeGUI(self):
        self.BACK_BUTTON = Button(image=None, pos=(self.screenWidth / 2, self.screenHeight / 1.3), text_input="BACK", font=self.Font.get_normal_font(), base_color="White", hovering_color="Red")
        self.PLAY_BUTTON = Button(image=None, pos=(self.screenWidth / 2, self.screenHeight / 1.1), text_input="PLAY", font=self.Font.get_normal_font(), base_color="White", hovering_color="Red")


    def displayLobby(self):

        while True:

            self.screen.blit(self.BG, (0, 0))
            self.LOBBY_MOUSE_POS = pygame.mouse.get_pos()
            self.LOBBY_MOUSE_BUTTONS = pygame.mouse.get_pressed()

            self.PLAY_BUTTON.changeColor(self.LOBBY_MOUSE_POS)
            self.PLAY_BUTTON.update(self.screen)

            self.BACK_BUTTON.changeColor(self.LOBBY_MOUSE_POS)
            self.BACK_BUTTON.update(self.screen)
           
            for lobbyPlayer in self.lobbyPlayers:
                lobbyPlayer.displayPlayer(self.LOBBY_MOUSE_POS, self.LOBBY_MOUSE_BUTTONS)
            
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                for lobbyPlayer in self.lobbyPlayers:
                    textEnabled = lobbyPlayer.checkForInput(self.LOBBY_MOUSE_POS[0], self.LOBBY_MOUSE_POS[1], event)

                    if textEnabled != None:
                        i = self.whichPlayerID_begin

                        for lobbyPlayer in self.lobbyPlayers:
                            if i != textEnabled:
                                lobbyPlayer.disableTextInput()

                            i += 1

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.BACK_BUTTON.checkForInput(self.LOBBY_MOUSE_POS):
                        return

                    if self.PLAY_BUTTON.checkForInput(self.LOBBY_MOUSE_POS):
                         game = Game(self.screen, self.screenWidth, self.screenHeight, self.FPS, self.mixer, self, self.lobbyPlayers)
                         game.play()
                         return
                        
                if event.type == self.mixer.SONG_END:
                    self.mixer.playMenuMusic()

            pygame.display.update()


