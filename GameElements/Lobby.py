import pygame
import sys

from GuiElements.Button import Button
from GameElements.LobbyPlayer import LobbyPlayer
from GameElements.Game import Game


class Lobby:

    MINIMUM_ALIVE_PLAYERS = 2
    MAX_PLAYERS = 4
    MAX_ROUNDS = 10
    WHICH_PLAYER_ID_BEGIN = 1

    def __init__(self, screen, screen_width, screen_height, fps, mixer, menu, font):
        self.round_text = self.round_rect =\
            self.round_button = self.back_button = self.play_button =\
            self.lobby_mouse_buttons = None

        self.screen = screen
        self.screenWidth = screen_width
        self.screenHeight = screen_height
        self.FPS = fps
        self.mixer = mixer
        self.menu = menu
        self.Font = font

        self.BG = menu.BG
        self.lobby_mouse_pos = pygame.mouse.get_pos()

        self.lobbyPlayers = []

        self.initialRoundNumber = "1"
        self.roundNumber = 1

        for whichPlayer in range(Lobby.WHICH_PLAYER_ID_BEGIN, Lobby.MAX_PLAYERS + 1):
            self.lobbyPlayers.append(LobbyPlayer(self.screen, self.screenWidth, self.screenHeight, whichPlayer,
                                                 self.Font, Lobby.MAX_PLAYERS))

        self.initialize_gui()

    def initialize_gui(self):
        self.round_text = self.Font.get_title_font(smaller=2).render("Rounds", True, "White")
        self.round_rect = self.round_text.get_rect(center=(self.screenWidth / 2, self.screenHeight / 3.9))

        self.round_button = Button(image=None, pos=(self.screenWidth / 2, self.screenHeight / 2.8),
                                   text_input=self.initialRoundNumber, font=self.Font.get_normal_font(),
                                   base_color="White", hovering_color="Red")

        self.back_button = Button(image=None, pos=(self.screenWidth / 2, self.screenHeight / 1.3), text_input="BACK",
                                  font=self.Font.get_normal_font(), base_color="White", hovering_color="Red")
        self.play_button = Button(image=None, pos=(self.screenWidth / 2, self.screenHeight / 1.1), text_input="PLAY",
                                  font=self.Font.get_normal_font(), base_color="White", hovering_color="Red")

    def display_lobby(self):

        while True:

            self.screen.blit(self.BG, (0, 0))
            self.lobby_mouse_pos = pygame.mouse.get_pos()
            self.lobby_mouse_buttons = pygame.mouse.get_pressed()

            for button in [self.play_button, self.back_button, self.round_button]:
                button.change_color(self.lobby_mouse_pos)
                button.update(self.screen)

            for lobbyObject in [(self.round_text, self.round_rect)]:
                self.screen.blit(lobbyObject[0], lobbyObject[1])

            for lobbyPlayer in self.lobbyPlayers:
                lobbyPlayer.display_player(self.lobby_mouse_pos, self.lobby_mouse_buttons)

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                for lobby_player_outer in self.lobbyPlayers:
                    text_enabled = lobby_player_outer.check_for_input(self.lobby_mouse_pos[0], self.lobby_mouse_pos[1],
                                                                      event)

                    if text_enabled is not None:
                        i = Lobby.WHICH_PLAYER_ID_BEGIN

                        for lobby_player_inner in self.lobbyPlayers:
                            if i != text_enabled:
                                lobby_player_inner.disable_text_input()

                            i += 1

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.back_button.check_for_input(self.lobby_mouse_pos):
                        return

                    if self.play_button.check_for_input(self.lobby_mouse_pos):

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

                        if dont_start is False and added_players >= Lobby.MINIMUM_ALIVE_PLAYERS:
                            game = Game(self.screen, self.screenWidth, self.screenHeight, self.FPS, self.mixer, self,
                                        game_players, Lobby.MINIMUM_ALIVE_PLAYERS, self.roundNumber, self.Font)
                            game.run_game()
                            return

                    if self.round_button.check_for_input(self.lobby_mouse_pos):

                        self.roundNumber = str(int(self.roundNumber) + 1)

                        if int(self.roundNumber) > Lobby.MAX_ROUNDS:
                            self.roundNumber = "1"

                        self.round_button.change_text(self.roundNumber)

                if event.type == self.mixer.SONG_END:
                    self.mixer.play_menu_music()

            pygame.display.update()
