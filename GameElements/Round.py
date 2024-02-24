from GameElements.Player import Player
import pygame, sys
import time
from threading import Thread


class Round:

    def __init__(self, screen, screen_width, screen_height, mixer, lobby_players, minimum_alive_players, fps, font):
        self.screen = screen
        self.screenWidth = screen_width
        self.screenHeight = screen_height
        self.gameBackgroundColor = "black"

        self.deathOrder = []
        self.Font = font

        self.MENU_MOUSE_POS = pygame.mouse.get_pos()

        self.FPS = fps

        self.MINIMUM_ALIVE_PLAYERS = minimum_alive_players

        self.gameMixer = mixer

        self.lobbyPlayers = lobby_players
        self.players = []

        for player in lobby_players:
            if player.isAdded:
                self.players.append(Player(player.color, self.screenWidth, self.screenHeight, player.left, player.right,
                                           self.gameBackgroundColor, self.screen, self.FPS, player.speed,
                                           player.thickness, player.name, player.whichPlayer))

        self.fillBoard = [[0 for x in range(self.screenWidth)] for y in range(self.screenHeight)]
        self.colorBoard = [[0 for x in range(self.screenWidth)] for y in range(self.screenHeight)]

        self.animateThreads = []

    def deal_with_game_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == self.gameMixer.SONG_END:
                self.gameMixer.switch_music_and_play()

    def round_countdown(self):
        self.gameMixer.set_music_volume(self.gameMixer.musicVolume / 2)

        count_down_start = 3
        count_down = count_down_start

        self.gameMixer.play_sound_effect(self.gameMixer.SoundBoard.countdown)

        while True:
            if count_down == 0:
                break

            count_text = self.Font.get_title_font(smaller=2.0).render(str(count_down), True, "White")
            count_rect = count_text.get_rect(center=(self.screenWidth / 2.0, self.screenHeight / 4.0))

            count_text_width, count_text_height = self.Font.get_title_font(smaller=2.0).size(str(count_down))

            self.screen.blit(count_text, count_rect)

            pygame.display.update()

            time.sleep(1)

            # drawing the same number but in black won't work, so rectangle has to be drawn
            pygame.draw.rect(self.screen, self.gameBackgroundColor,
                             pygame.Rect(self.screenWidth / 2.0 - count_text_width / 2,
                                         self.screenHeight / 4.0 - count_text_height / 2,
                                         count_text_width,
                                         count_text_height))

            pygame.display.update()

            count_down -= 1

        self.gameMixer.set_music_volume(self.gameMixer.musicVolume * 2)

    def start_round(self):
        self.screen.fill(self.gameBackgroundColor)

        clock = pygame.time.Clock()
        round_started = False

        while True:
            self.MENU_MOUSE_POS = pygame.mouse.get_pos()

            move_threads = []

            for player in self.players:
                move_threads.append(Thread(target=player.move_player_onscreen, args=(self.screen, self.screenWidth,
                                                                                     self.screenHeight, self.fillBoard,
                                                                                     self.colorBoard,
                                                                                     self.animateThreads,
                                                                                     self.gameMixer, self.deathOrder)))

                move_threads[-1].start()

            for moveThread in move_threads:
                moveThread.join()

            players_alive = 0

            for player in self.players:
                if player.isAlive:
                    players_alive += 1

            if players_alive < self.MINIMUM_ALIVE_PLAYERS:
                all_animation_dead = True

                for animateThread in self.animateThreads:
                    if animateThread.is_alive(): all_animation_dead = False

                if all_animation_dead:
                    return self.deathOrder

            player_input = pygame.key.get_pressed()

            for i in self.players:
                i.handle_input_for_player(player_input)

            self.deal_with_game_events()

            if not round_started:
                self.round_countdown()
                round_started = True

            pygame.display.update()
            clock.tick(self.FPS)
