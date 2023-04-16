import pygame, sys

from Button import Button
from LobbyPlayer import LobbyPlayer

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

        self.lobbyPlayers = []

        for whichPlayer in range(1, self.maxPlayers + 1):
            self.lobbyPlayers.append(LobbyPlayer(self.screen, self.screenWidth, self.screenHeight, whichPlayer, self.Font))

        self.initializeGUI()


    def initializeGUI(self):
        #self.PLAY_BUTTON = Button(image=None, pos=(self.screenWidth / 2, self.screenHeight / 2.8), text_input="PLAY", font=font.get_font(self.normalTextFontSize), base_color="White", hovering_color="Red")
        pass


    def displayLobby(self):

        while True:

            self.screen.blit(self.BG, (0, 0))
            self.LOBBY_MOUSE_POS = pygame.mouse.get_pos()
           
            for lobbyPlayer in self.lobbyPlayers:
                lobbyPlayer.displayPlayer(self.LOBBY_MOUSE_POS)
            
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                for lobbyPlayer in self.lobbyPlayers:
                    textEnabled = lobbyPlayer.checkForInput(self.LOBBY_MOUSE_POS[0], self.LOBBY_MOUSE_POS[1], event)

                    if textEnabled != 0:
                        i = 1

                        for lobbyPlayer in self.lobbyPlayers:
                            if i != textEnabled:
                                lobbyPlayer.disableTextInput()

                            i += 1
                        
                if event.type == self.mixer.SONG_END:
                    self.mixer.playMenuMusic()

            pygame.display.update()


