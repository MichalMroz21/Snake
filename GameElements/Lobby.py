import pygame
import sys

from GuiElements.Button import Button
from GameElements.LobbyPlayer import LobbyPlayer
from GameElements.Game import Game


class Lobby:

    def __init__(self, screen, screen_width, screen_height, fps, mixer, menu, font):
        self.ROUND_TEXT = None
        self.ROUND_RECT = None
        self.ROUND_BUTTON = None
        self.BACK_BUTTON = None
        self.PLAY_BUTTON = None
        self.LOBBY_MOUSE_BUTTONS = None

        self.screen = screen
        self.screenWidth = screen_width
        self.screenHeight = screen_height
        self.FPS = fps
        self.mixer = mixer
        self.menu = menu
        self.Font = font

        self.minimumAlivePlayers = 2

        self.BG = menu.BG
        self.LOBBY_MOUSE_POS = pygame.mouse.get_pos()

        self.maxPlayers = 4
        self.whichPlayerID_begin = 1

        self.lobbyPlayers = []

        self.initialRoundNumber = "1"
        self.roundNumber = 1

        self.maxRounds = 10

        for whichPlayer in range(self.whichPlayerID_begin, self.maxPlayers + 1):
            self.lobbyPlayers.append(LobbyPlayer(self.screen, self.screenWidth, self.screenHeight, whichPlayer,
                                                 self.Font))

        self.initialize_gui()

    def initialize_gui(self):
        self.ROUND_TEXT = self.Font.get_title_font(smaller=2).render("Rounds", True, "White")
        self.ROUND_RECT = self.ROUND_TEXT.get_rect(center=(self.screenWidth / 2, self.screenHeight / 3.9))

        self.ROUND_BUTTON = Button(image=None, pos=(self.screenWidth / 2, self.screenHeight / 2.8),
                                   text_input=self.initialRoundNumber, font=self.Font.get_normal_font(),
                                   base_color="White", hovering_color="Red")

        self.BACK_BUTTON = Button(image=None, pos=(self.screenWidth / 2, self.screenHeight / 1.3), text_input="BACK",
                                  font=self.Font.get_normal_font(), base_color="White", hovering_color="Red")
        self.PLAY_BUTTON = Button(image=None, pos=(self.screenWidth / 2, self.screenHeight / 1.1), text_input="PLAY",
                                  font=self.Font.get_normal_font(), base_color="White", hovering_color="Red")

    def display_lobby(self):

        while True:

            self.screen.blit(self.BG, (0, 0))
            self.LOBBY_MOUSE_POS = pygame.mouse.get_pos()
            self.LOBBY_MOUSE_BUTTONS = pygame.mouse.get_pressed()

            for button in [self.PLAY_BUTTON, self.BACK_BUTTON, self.ROUND_BUTTON]:
                button.change_color(self.LOBBY_MOUSE_POS)
                button.update(self.screen)

            for lobbyObject in [(self.ROUND_TEXT, self.ROUND_RECT)]:
                self.screen.blit(lobbyObject[0], lobbyObject[1])

            for lobbyPlayer in self.lobbyPlayers:
                lobbyPlayer.display_player(self.LOBBY_MOUSE_POS, self.LOBBY_MOUSE_BUTTONS)

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                for lobby_player_outer in self.lobbyPlayers:
                    text_enabled = lobby_player_outer.check_for_input(self.LOBBY_MOUSE_POS[0], self.LOBBY_MOUSE_POS[1],
                                                                      event)

                    if text_enabled is not None:
                        i = self.whichPlayerID_begin

                        for lobby_player_inner in self.lobbyPlayers:
                            if i != text_enabled:
                                lobby_player_inner.disable_text_input()

                            i += 1

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.BACK_BUTTON.check_for_input(self.LOBBY_MOUSE_POS):
                        return

                    if self.PLAY_BUTTON.check_for_input(self.LOBBY_MOUSE_POS):

                        dont_start = False
                        added_players = 0
                        game_players = []

                        for lobbyPlayer in self.lobbyPlayers:

                            if lobbyPlayer.SPEED_BOX.text == '.' or lobbyPlayer.SPEED_BOX.text == '0.':
                                dont_start = True
                                break

                            if lobbyPlayer.isAdded:
                                added_players += 1
                                lobbyPlayer.speed = float(lobbyPlayer.speed)
                                game_players.append(lobbyPlayer)

                        if dont_start is False and added_players >= self.minimumAlivePlayers:
                            game = Game(self.screen, self.screenWidth, self.screenHeight, self.FPS, self.mixer, self,
                                        game_players, self.minimumAlivePlayers, self.roundNumber, self.Font)
                            game.run_game()
                            return

                    if self.ROUND_BUTTON.check_for_input(self.LOBBY_MOUSE_POS):

                        self.roundNumber = str(int(self.roundNumber) + 1)

                        if int(self.roundNumber) > self.maxRounds:
                            self.roundNumber = "1"

                        self.ROUND_BUTTON.change_text(self.roundNumber)

                if event.type == self.mixer.SONG_END:
                    self.mixer.play_menu_music()

            pygame.display.update()
