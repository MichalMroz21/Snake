from Button import Button
from Game import Game
from Mixer import Mixer
from Slider import Slider
import pygame
import pygame, sys
from pygame._sdl2.video import Window
import time 
import math
import asyncio
import os
import re

class MainMenu:

    def __init__(self):

        pygame.init()

        self.maxResolutionObject = pygame.display.Info()
        self.maxResolutionWidth = self.maxResolutionObject.current_w
        self.maxResolutionHeight = self.maxResolutionObject.current_h

        self.SCREEN_WIDTH = self.maxResolutionWidth
        self.SCREEN_HEIGHT = self.maxResolutionHeight

        self.initialVolume = 0.5
        self.mixer = Mixer(self.initialVolume)

        self.FPS = 60

        self.RESOLUTIONS_INDEX = {}

        self.RESOLUTIONS = [(640, 480), (800, 600), (1024, 768), (1280, 800), (1440, 900), (1680, 1050), (1920, 1200), (1280, 720), (1366, 768), (1920, 1080), (2560, 1440)]

        i = 0

        for resolution in self.RESOLUTIONS:
            if(resolution[0] <= self.maxResolutionWidth and resolution[1] <= self.maxResolutionHeight):
                self.RESOLUTIONS_INDEX[str(resolution[0]) + "x" + str(resolution[1])] = i 
                i += 1


        self.resolutionsAmount = len(self.RESOLUTIONS_INDEX)

        self.RESOLUTIONS_INDEX[str(self.SCREEN_WIDTH) + "x" + str(self.SCREEN_HEIGHT)] = self.resolutionsAmount

        self.RESOLUTIONS_MAP = {val:key for key, val in self.RESOLUTIONS_INDEX.items() }

        for k, v in self.RESOLUTIONS_MAP.items():
            self.RESOLUTIONS_MAP[k] = ( re.split('x', v)[0], re.split('x', v)[1] )

        self.RESOLUTIONS_MAP[self.resolutionsAmount] = (str(self.SCREEN_WIDTH), str(self.SCREEN_HEIGHT))

        self.resolutionsAmount += 1

        self.resolution_init()


    def resolution_init(self):

        pygame.display.quit()
        self.setgamewindowcenter((self.maxResolutionWidth - self.SCREEN_WIDTH) / 2, (self.maxResolutionHeight - self.SCREEN_HEIGHT) / 2)
        pygame.display.init()
        self.SCREEN = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT) ) 

        pygame.display.set_caption("Snake Game")
        self.BG = pygame.image.load("assets/picture/MenuBackground.jpg")
        self.BG = pygame.transform.scale(self.BG, (self.SCREEN_WIDTH, self.SCREEN_HEIGHT))

        self.titleFontSize = (self.SCREEN_WIDTH + self.SCREEN_HEIGHT) / 20
        self.normalTextFontSize = (self.SCREEN_WIDTH + self.SCREEN_HEIGHT) / 28

        self.MENU_TEXT = self.get_font(self.titleFontSize).render("Snake Game", True, "Yellow")
        self.MENU_RECT = self.MENU_TEXT.get_rect(center=(self.SCREEN_WIDTH / 2, self.SCREEN_HEIGHT / 7.2))

        self.PLAY_BUTTON = Button(image=None, pos=(self.SCREEN_WIDTH / 2, self.SCREEN_HEIGHT / 2.8), text_input="PLAY", font=self.get_font(self.normalTextFontSize), base_color="White", hovering_color="Red")
        self.OPTIONS_BUTTON = Button(image=None, pos=(self.SCREEN_WIDTH / 2, self.SCREEN_HEIGHT / 1.8), text_input="OPTIONS", font=self.get_font(self.normalTextFontSize), base_color="White", hovering_color="Red")
        self.QUIT_BUTTON = Button(image=None, pos=(self.SCREEN_WIDTH / 2, self.SCREEN_HEIGHT / 1.3), text_input="QUIT", font=self.get_font(self.normalTextFontSize), base_color="White", hovering_color="Red")

        self.MENU_MOUSE_POS = pygame.mouse.get_pos()

        self.OPTIONS_TEXT = self.get_font(self.titleFontSize).render("Options", True, "Yellow")
        self.OPTIONS_RECT = self.OPTIONS_TEXT.get_rect(center=(self.SCREEN_WIDTH / 2, self.SCREEN_HEIGHT / 7.2))

        self.OPTIONS_BACK = Button(image=None, pos=(self.SCREEN_WIDTH / 2, self.SCREEN_HEIGHT / 1.3), text_input="GO BACK", font=self.get_font(self.normalTextFontSize), base_color="White", hovering_color="Red")
        self.OPTIONS_RESOLUTION = Button(image=None, pos=(self.SCREEN_WIDTH / 2, self.SCREEN_HEIGHT / 2.8), text_input=(str(self.SCREEN_WIDTH) + "x" + str(self.SCREEN_HEIGHT)), font=self.get_font(self.normalTextFontSize), base_color="White", hovering_color="Red")
        self.OPTIONS_APPLY = Button(image=None, pos=(self.SCREEN_WIDTH / 2, self.SCREEN_HEIGHT / 2.05), text_input="APPLY", font=self.get_font(self.normalTextFontSize), base_color="White", hovering_color="Red")

       # self.OPTIONS_MUSIC_SLIDER = Slider()

        self.displayMainMenu()


    def get_font(self, size): 
        return pygame.font.Font("assets/font/Lato-Regular.ttf", (int)(size))


    def setgamewindowcenter(self, x, y):
        os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (x,y)
        print(os.environ['SDL_VIDEO_WINDOW_POS'])


    def options(self):

        curWidth = self.SCREEN_WIDTH
        curHeight = self.SCREEN_HEIGHT
        curIndex = self.RESOLUTIONS_INDEX[str(self.SCREEN_WIDTH) + "x" + str(self.SCREEN_HEIGHT)]

        while True:

            self.SCREEN.blit(self.BG, (0, 0))
            self.MENU_MOUSE_POS = pygame.mouse.get_pos()
       
            self.SCREEN.blit(self.OPTIONS_TEXT, self.OPTIONS_RECT)

            self.OPTIONS_BACK.changeColor(self.MENU_MOUSE_POS)
            self.OPTIONS_BACK.update(self.SCREEN)

            self.OPTIONS_RESOLUTION.changeColor(self.MENU_MOUSE_POS)
            self.OPTIONS_RESOLUTION.update(self.SCREEN)

            self.OPTIONS_APPLY.changeColor(self.MENU_MOUSE_POS)
            self.OPTIONS_APPLY.update(self.SCREEN)

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.OPTIONS_BACK.checkForInput(self.MENU_MOUSE_POS):
                        self.displayMainMenu()

                    if self.OPTIONS_RESOLUTION.checkForInput(self.MENU_MOUSE_POS):

                        curIndex += 1

                        if(curIndex == self.resolutionsAmount):
                            curIndex = 0

                        self.OPTIONS_RESOLUTION.changeText(self.RESOLUTIONS_MAP[curIndex][0] + "x" + self.RESOLUTIONS_MAP[curIndex][1])

                    if self.OPTIONS_APPLY.checkForInput(self.MENU_MOUSE_POS):

                        self.SCREEN_WIDTH = (int)(self.RESOLUTIONS_MAP[curIndex][0])
                        self.SCREEN_HEIGHT = (int)(self.RESOLUTIONS_MAP[curIndex][1])
                        self.resolution_init()
                       
            pygame.display.update()



    def displayMainMenu(self):
        
        while True:

            self.SCREEN.blit(self.BG, (0, 0))
            self.MENU_MOUSE_POS = pygame.mouse.get_pos()

            self.SCREEN.blit(self.MENU_TEXT, self.MENU_RECT)

            for button in [self.PLAY_BUTTON, self.OPTIONS_BUTTON, self.QUIT_BUTTON]:
                button.changeColor(self.MENU_MOUSE_POS)
                button.update(self.SCREEN)
        
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.PLAY_BUTTON.checkForInput(self.MENU_MOUSE_POS):

                        game = Game(self.SCREEN, self.SCREEN_WIDTH, self.SCREEN_HEIGHT, self.FPS, self.mixer, self)
                        game.play()
                        

                    if self.OPTIONS_BUTTON.checkForInput(self.MENU_MOUSE_POS):
                        self.options()

                    if self.QUIT_BUTTON.checkForInput(self.MENU_MOUSE_POS):
                        pygame.quit()
                        sys.exit()

            pygame.display.update()


    
