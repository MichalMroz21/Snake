from GameElements.Round import Round
import pygame
import sys
import time
import operator


class Game:

    def __init__(self, screen, screen_width, screen_height, fps, mixer, menu, game_players, minimum_alive_players,
                 rounds, font):
        self.winner_player_rect = None
        self.winner_player_text = None
        self.winningPlayer = None
        self.winningPlayerID = None
        self.profit_rect = None
        self.profit_text = None
        self.profit_text_height = None
        self.profit_text_width = None
        self.score_rect = None
        self.winner_rect = None
        self.winner_text = None
        self.scores_rect = None
        self.scores_text = None
        self.score_text = None
        self.score_text_height = None
        self.score_text_width = None

        self.screen = screen
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.game_background_color = "black"
        self.menu_mouse_pos = pygame.mouse.get_pos()
        self.fps = fps

        self.font = font

        self.menu = menu
        self.minimum_alive_players = minimum_alive_players

        self.game_mixer = mixer
        self.death_order = []

        self.game_players = game_players

        self.id_to_player = {}

        for player in self.game_players:
            self.id_to_player[player.whichPlayer] = player

        self.players = []

        self.rounds = int(rounds)
        self.currentRound = 1

        self.scores_display_time = 5.0
        self.winner_display_time = 6.0

        self.scores = {}
        self.score_texts = []

        self.score_profits = {}

        self.sum_proportion = (self.screen_width + self.screen_height) / 1000

        for player in self.game_players:
            self.scores[player.whichPlayer] = 0

        self.initialize_text()

    def deal_with_game_events(self):
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == self.game_mixer.SONG_END:
                self.game_mixer.switch_music_and_play()

    def initialize_text(self):

        self.scores_text = self.font.get_title_font(smaller=3 / self.sum_proportion).render("Scores", True, "Yellow")
        self.scores_rect = self.scores_text.get_rect(center=(self.screen_width / 2, self.screen_height / 5.0))

        self.winner_text = self.font.get_title_font(smaller=3 / self.sum_proportion).render("Winner", True, "Gold")
        self.winner_rect = self.winner_text.get_rect(center=(self.screen_width / 2, self.screen_height / 5.0))

    def initialize_changeable_text(self):

        self.score_texts.clear()

        i = 1.5

        for key, value in self.scores.items():
            score_text = self.id_to_player[key].name + " " + str(value)
            profit_text = "+ " + str(self.score_profits[key])

            self.score_text_width, self.score_text_height = (self.font.get_title_font(smaller=4.0 / self.sum_proportion)
                                                             .size(score_text))

            self.score_text = (self.font.get_title_font(smaller=4 / self.sum_proportion)
                               .render(score_text, True, self.id_to_player[key].color))

            self.score_rect = self.score_text.get_rect(center=(self.screen_width / 2,
                                                               self.screen_height / 5.0 + self.score_text_height * i))

            self.score_texts.append((self.score_text, self.score_rect))

            self.profit_text_width, self.profit_text_height = self.font.get_normal_font(
                smaller=8.0 / self.sum_proportion).size(profit_text)

            self.profit_text = (self.font.get_title_font(smaller=8 / self.sum_proportion)
                                .render(profit_text, True, self.id_to_player[key].color))

            self.profit_rect = self.profit_text.get_rect(center=
                                                         (self.screen_width / 2 + self.score_text_width / 2 +
                                                          self.profit_text_width, self.screen_height / 5.0 +
                                                          self.score_text_height * i))

            self.score_texts.append((self.profit_text, self.profit_rect))

            i += 1.5

    def display_scores(self):

        self.initialize_changeable_text()

        for scoreObject in [(self.scores_text, self.scores_rect)]:
            self.screen.blit(scoreObject[0], scoreObject[1])

        for playerScoreObject in self.score_texts:
            self.screen.blit(playerScoreObject[0], playerScoreObject[1])

        pygame.display.update()

        time.sleep(self.scores_display_time)

    def display_winner(self):

        for key, value in self.scores.items():
            self.winningPlayerID = key
            break

        self.winningPlayer = self.id_to_player[self.winningPlayerID]

        self.winner_player_text = (self.font.get_title_font(smaller=3 / self.sum_proportion)
                                   .render(self.winningPlayer.name, True, self.winningPlayer.color))

        self.winner_player_rect = self.winner_player_text.get_rect(center=
                                                                   (self.screen_width / 2, self.screen_height / 3.0))

        self.game_mixer.pause_music()

        self.screen.fill(self.game_background_color)

        for winObject in [(self.winner_player_text, self.winner_player_rect), (self.winner_text, self.winner_rect)]:
            self.screen.blit(winObject[0], winObject[1])

        pygame.display.update()

        self.game_mixer.play_sound_effect(self.game_mixer.SoundBoard.gameWin)

        time.sleep(self.winner_display_time)

        self.game_mixer.select_random_song()

        self.game_mixer.play_menu_music()

    def calculate_scores(self):

        for player in self.game_players:
            self.scores[player.whichPlayer] = self.scores[player.whichPlayer] + len(self.game_players) * 10
            self.score_profits[player.whichPlayer] = len(self.game_players) * 10

        death_penalty = 10

        if len(self.death_order) == len(self.game_players):
            self.death_order.pop()

        for death in reversed(self.death_order):
            self.scores[death] = self.scores[death] - death_penalty
            self.score_profits[death] -= death_penalty
            death_penalty += 10

        self.scores = dict(sorted(self.scores.items(), key=operator.itemgetter(1), reverse=True))

    def run_game(self):

        self.game_mixer.switch_music_and_play()

        self.screen.fill(self.game_background_color)

        clock = pygame.time.Clock()

        while True:

            self.menu_mouse_pos = pygame.mouse.get_pos()

            game_round = Round(self.screen, self.screen_width, self.screen_height, self.game_mixer, self.game_players,
                               self.minimum_alive_players, self.fps, self.font)

            self.death_order = game_round.start_round()
            self.calculate_scores()
            self.display_scores()

            self.currentRound += 1

            if self.currentRound == self.rounds + 1:
                self.display_winner()
                break

            self.deal_with_game_events()

            pygame.display.update()
            clock.tick(self.fps)
