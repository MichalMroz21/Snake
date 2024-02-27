from GuiElements.Button import Button
from GameElements.Mixer import Mixer
from GuiElements.Slider import Slider
from GameElements.Lobby import Lobby

from Utils.AssetManager import AssetManager

from GuiElements.Font import Font

import pygame
import sys

import os
import re


class MainMenu:

    GAME_TITLE = "Snake Game"
    TEXT_COLOR = "White"
    TEXT_COLOR_HOVER = "Red"
    GAME_TITLE_COLOR = "Yellow"
    INITIAL_VOLUME = 0.5
    FPS = 60
    RESOLUTIONS = [(640, 480), (800, 600), (1024, 768), (1280, 800), (1440, 900), (1680, 1050), (1920, 1200),
                   (1280, 720), (1366, 768), (1920, 1080), (2560, 1440)]

    def __init__(self):

        self.OPTIONS_APPLY = self.OPTIONS_RESOLUTION = self.OPTIONS_RECT_RESOLUTION \
            = self.OPTIONS_TEXT_RESOLUTION = self.OPTIONS_RECT \
            = self.OPTIONS_BACK = self.OPTIONS_TEXT = self.QUIT_BUTTON\
            = self.OPTIONS_BUTTON = self.PLAY_BUTTON = self.MENU_RECT \
            = self.MENU_TEXT = self.Font = self.BG = self.screen \
            = self.OPTIONS_TEXT_MUSIC = self.OPTIONS_RECT_MUSIC \
            = self.OPTIONS_MUSIC_SLIDER = self.OPTIONS_TEXT_SOUND \
            = self.OPTIONS_RECT_SOUND = self.OPTIONS_SOUND_SLIDER \
            = self.MENU_MOUSE_POS = None

        pygame.init()

        self.maxResolutionObject = pygame.display.Info()

        self.maxResolutionWidth = self.maxResolutionObject.current_w
        self.maxResolutionHeight = self.maxResolutionObject.current_h

        self.screenWidth = self.maxResolutionWidth
        self.screenHeight = self.maxResolutionHeight

        self.mixer = Mixer(MainMenu.INITIAL_VOLUME)
        self.RESOLUTIONS_INDEX = {}

        i = 0

        for resolution in MainMenu.RESOLUTIONS:
            if resolution[0] <= self.maxResolutionWidth and resolution[1] <= self.maxResolutionHeight:
                self.RESOLUTIONS_INDEX[str(resolution[0]) + "x" + str(resolution[1])] = i
                i += 1

        self.resolutionsAmount = len(self.RESOLUTIONS_INDEX)

        self.RESOLUTIONS_INDEX[str(self.screenWidth) + "x" + str(self.screenHeight)] = self.resolutionsAmount

        self.RESOLUTIONS_MAP = {val: key for key, val in self.RESOLUTIONS_INDEX.items()}

        for k, v in self.RESOLUTIONS_MAP.items():
            self.RESOLUTIONS_MAP[k] = re.split('x', v)[0], re.split('x', v)[1]

        self.RESOLUTIONS_MAP[self.resolutionsAmount] = str(self.screenWidth), str(self.screenHeight)

        self.resolutionsAmount += 1

        self.resolution_init()

    def resolution_init(self, first_time=True):
        pygame.display.quit()

        self.set_game_window_center((self.maxResolutionWidth - self.screenWidth) / 2,
                                    (self.maxResolutionHeight - self.screenHeight) / 2)

        pygame.display.init()

        self.screen = pygame.display.set_mode((self.screenWidth, self.screenHeight))
        self.MENU_MOUSE_POS = pygame.mouse.get_pos()

        pygame.display.set_caption(MainMenu.GAME_TITLE)

        self.BG = pygame.image.load(AssetManager.Pictures.MENU_BACKGROUND.value)
        self.BG = pygame.transform.scale(self.BG, (self.screenWidth, self.screenHeight))

        self.Font = Font(self.screenWidth, self.screenHeight)

        self.MENU_TEXT = self.Font.get_title_font().render(MainMenu.GAME_TITLE, True, MainMenu.GAME_TITLE_COLOR)
        self.MENU_RECT = self.MENU_TEXT.get_rect(center=(self.screenWidth / 2, self.screenHeight / 7.2))

        self.OPTIONS_TEXT = self.Font.get_title_font().render("Options", True, MainMenu.GAME_TITLE_COLOR)
        self.OPTIONS_RECT = self.OPTIONS_TEXT.get_rect(center=(self.screenWidth / 2, self.screenHeight / 8.5))

        self.OPTIONS_TEXT_RESOLUTION = self.Font.get_normal_font(1.5).render("Resolution", True, MainMenu.TEXT_COLOR)
        self.OPTIONS_RECT_RESOLUTION = self.OPTIONS_TEXT_RESOLUTION.get_rect(center=(self.screenWidth / 2,
                                                                                     self.screenHeight / 4.0))

        self.OPTIONS_TEXT_MUSIC = self.Font.get_normal_font(smaller=2).render("Music Volume", True, MainMenu.TEXT_COLOR)
        self.OPTIONS_RECT_MUSIC = self.OPTIONS_TEXT_RESOLUTION.get_rect(center=(self.screenWidth / 2.0,
                                                                                self.screenHeight / 1.9))

        self.OPTIONS_TEXT_SOUND = self.Font.get_normal_font(smaller=2).render("Effects Volume", True,
                                                                              MainMenu.TEXT_COLOR)
        self.OPTIONS_RECT_SOUND = self.OPTIONS_TEXT_RESOLUTION.get_rect(center=(self.screenWidth / 2.0,
                                                                                self.screenHeight / 1.4))

        self.PLAY_BUTTON = Button(image=None, pos=(self.screenWidth / 2, self.screenHeight / 2.8), text_input="PLAY",
                                  font=self.Font.get_normal_font(), base_color=MainMenu.TEXT_COLOR,
                                  hovering_color=MainMenu.TEXT_COLOR_HOVER)

        self.OPTIONS_BUTTON = Button(image=None, pos=(self.screenWidth / 2, self.screenHeight / 1.8),
                                     text_input="OPTIONS",
                                     font=self.Font.get_normal_font(), base_color=MainMenu.TEXT_COLOR,
                                     hovering_color=MainMenu.TEXT_COLOR_HOVER)

        self.QUIT_BUTTON = Button(image=None, pos=(self.screenWidth / 2, self.screenHeight / 1.3), text_input="QUIT",
                                  font=self.Font.get_normal_font(), base_color=MainMenu.TEXT_COLOR,
                                  hovering_color=MainMenu.TEXT_COLOR_HOVER)

        self.OPTIONS_BACK = Button(image=None, pos=(self.screenWidth / 2, self.screenHeight / 1.1),
                                   text_input="GO BACK",
                                   font=self.Font.get_normal_font(smaller=2), base_color=MainMenu.TEXT_COLOR,
                                   hovering_color=MainMenu.TEXT_COLOR_HOVER)

        self.OPTIONS_RESOLUTION = Button(image=None, pos=(self.screenWidth / 2, self.screenHeight / 3.0),
                                         text_input=(str(self.screenWidth) + "x" + str(self.screenHeight)),
                                         font=self.Font.get_normal_font(smaller=2), base_color=MainMenu.TEXT_COLOR,
                                         hovering_color=MainMenu.TEXT_COLOR_HOVER)

        self.OPTIONS_APPLY = Button(image=None, pos=(self.screenWidth / 2, self.screenHeight / 2.5),
                                    text_input="APPLY",
                                    font=self.Font.get_normal_font(smaller=2), base_color=MainMenu.TEXT_COLOR,
                                    hovering_color=MainMenu.TEXT_COLOR_HOVER)

        slider_width = self.screenWidth / 3
        slider_height = self.screenHeight / 20

        if self.OPTIONS_MUSIC_SLIDER is not None:
            self.OPTIONS_MUSIC_SLIDER = Slider(self.screenWidth / 2 - slider_width / 2, self.screenHeight / 1.7,
                                               slider_width, slider_height, (200, 200, 200), (255, 30, 30), 1, 0, 1,
                                               slider_height, self.OPTIONS_MUSIC_SLIDER.get_value())
        else:
            self.OPTIONS_MUSIC_SLIDER = Slider(self.screenWidth / 2 - slider_width / 2, self.screenHeight / 1.7,
                                               slider_width, slider_height, (200, 200, 200), (255, 30, 30), 1, 0, 1,
                                               slider_height, 0.5)

        if self.OPTIONS_SOUND_SLIDER is not None:
            self.OPTIONS_SOUND_SLIDER = Slider(self.screenWidth / 2 - slider_width / 2, self.screenHeight / 1.3,
                                               slider_width, slider_height, (200, 200, 200), (30, 255, 30),
                                               1, 0, 1, slider_height, self.OPTIONS_SOUND_SLIDER.get_value())
        else:
            self.OPTIONS_SOUND_SLIDER = Slider(self.screenWidth / 2 - slider_width / 2, self.screenHeight / 1.3,
                                               slider_width, slider_height, (200, 200, 200), (30, 255, 30), 1,
                                               0, 1, slider_height, 0.5)

        self.display_main_menu(first_time=first_time)

    @staticmethod
    def set_game_window_center(x, y):
        os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (x, y)

    def options(self):
        cur_index = self.RESOLUTIONS_INDEX[str(self.screenWidth) + "x" + str(self.screenHeight)]
        initial_index = cur_index

        while True:
            self.screen.blit(self.BG, (0, 0))

            for menuObject in [(self.OPTIONS_TEXT, self.OPTIONS_RECT),
                               (self.OPTIONS_TEXT_RESOLUTION, self.OPTIONS_RECT_RESOLUTION),
                               (self.OPTIONS_TEXT_MUSIC, self.OPTIONS_RECT_MUSIC),
                               (self.OPTIONS_TEXT_SOUND, self.OPTIONS_RECT_SOUND)]:
                self.screen.blit(menuObject[0], menuObject[1])

            self.OPTIONS_MUSIC_SLIDER.draw(self.screen)
            self.OPTIONS_SOUND_SLIDER.draw(self.screen)

            self.MENU_MOUSE_POS = pygame.mouse.get_pos()

            for button in [self.OPTIONS_BACK, self.OPTIONS_RESOLUTION, self.OPTIONS_APPLY]:
                button.change_color(self.MENU_MOUSE_POS)
                button.update(self.screen)

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:

                    if self.OPTIONS_BACK.check_for_input(self.MENU_MOUSE_POS):
                        self.OPTIONS_RESOLUTION.change_text(self.RESOLUTIONS_MAP[initial_index][0] + "x"
                                                            + self.RESOLUTIONS_MAP[initial_index][1])
                        self.display_main_menu()

                    if self.OPTIONS_RESOLUTION.check_for_input(self.MENU_MOUSE_POS):

                        cur_index += 1

                        if cur_index == self.resolutionsAmount:
                            cur_index = 0

                        self.OPTIONS_RESOLUTION.change_text(self.RESOLUTIONS_MAP[cur_index][0] + "x"
                                                            + self.RESOLUTIONS_MAP[cur_index][1])

                    if self.OPTIONS_APPLY.check_for_input(self.MENU_MOUSE_POS):
                        self.screenWidth = int(self.RESOLUTIONS_MAP[cur_index][0])
                        self.screenHeight = int(self.RESOLUTIONS_MAP[cur_index][1])
                        self.resolution_init(first_time=False)

                if pygame.mouse.get_pressed()[0]:
                    self.OPTIONS_MUSIC_SLIDER.update(self.MENU_MOUSE_POS)
                    self.OPTIONS_SOUND_SLIDER.update(self.MENU_MOUSE_POS)

                    self.mixer.set_music_volume(self.OPTIONS_MUSIC_SLIDER.get_value())
                    self.mixer.set_sound_volume(self.OPTIONS_SOUND_SLIDER.get_value())

                if event.type == self.mixer.SONG_END:
                    self.mixer.play_menu_music()

            pygame.display.update()

    def display_main_menu(self, first_time=False):

        if first_time:
            self.mixer.play_menu_music()

        while True:

            self.screen.blit(self.BG, (0, 0))
            self.MENU_MOUSE_POS = pygame.mouse.get_pos()

            self.screen.blit(self.MENU_TEXT, self.MENU_RECT)

            for button in [self.PLAY_BUTTON, self.OPTIONS_BUTTON, self.QUIT_BUTTON]:
                button.change_color(self.MENU_MOUSE_POS)
                button.update(self.screen)

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.PLAY_BUTTON.check_for_input(self.MENU_MOUSE_POS):
                        lobby = Lobby(self.screen, self.screenWidth, self.screenHeight, MainMenu.FPS, self.mixer, self,
                                      self.Font)
                        lobby.display_lobby()

                    if self.OPTIONS_BUTTON.check_for_input(self.MENU_MOUSE_POS):
                        self.options()

                    if self.QUIT_BUTTON.check_for_input(self.MENU_MOUSE_POS):
                        pygame.quit()
                        sys.exit()

                if event.type == self.mixer.SONG_END:
                    self.mixer.play_menu_music()

            pygame.display.update()
