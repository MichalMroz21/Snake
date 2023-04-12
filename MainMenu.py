from Button import Button
from Game import Game
from Mixer import Mixer
import pygame
import pygame, sys
import time 
import math
import asyncio

class MainMenu:

    def __init__(self):

        pygame.init()

        self.SCREEN_WIDTH = 1280
        self.SCREEN_HEIGHT = 720

        self.initialVolume = 0.5
        self.mixer = Mixer(self.initialVolume)

        self.FPS = 60

        self.SCREEN = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))

        pygame.display.set_caption("Snake Game")
        self.BG = pygame.image.load("assets/picture/MenuBackground.jpg")
        self.BG = pygame.transform.scale(self.BG, (self.SCREEN_WIDTH, self.SCREEN_HEIGHT))

        self.MENU_TEXT = self.get_font(100).render("Snake Game", True, "Yellow")
        self.MENU_RECT = self.MENU_TEXT.get_rect(center=(640, 100))

        self.PLAY_BUTTON = Button(image=None, pos=(640, 250), text_input="PLAY", font=self.get_font(75), base_color="White", hovering_color="Red")
        self.OPTIONS_BUTTON = Button(image=None, pos=(640, 400), text_input="OPTIONS", font=self.get_font(75), base_color="White", hovering_color="Red")
        self.QUIT_BUTTON = Button(image=None, pos=(640, 550), text_input="QUIT", font=self.get_font(75), base_color="White", hovering_color="Red")

        self.MENU_MOUSE_POS = pygame.mouse.get_pos()

        self.OPTIONS_TEXT = self.get_font(80).render("Options", True, "Yellow")
        self.OPTIONS_RECT = self.OPTIONS_TEXT.get_rect(center=(640, 100))

        self.OPTIONS_BACK = Button(image=None, pos=(640, 550), text_input="GO BACK", font=self.get_font(75), base_color="White", hovering_color="Red")
        self.OPTIONS_RESOLUTION = Button(image=None, pos=(640, 250), text_input=(str(self.SCREEN_WIDTH) + "x" + str(self.SCREEN_HEIGHT)), font=self.get_font(75), base_color="White", hovering_color="Red")
        self.OPTIONS_APPLY = Button(image=None, pos=(640, 350), text_input="APPLY", font=self.get_font(75), base_color="White", hovering_color="Red")

        self.RESOLUTIONS_INDEX = {
            "640x480" : 0,
            "800x600" : 1,
            "1024x768" : 2,
            "1280x800" : 3,
            "1440x900" : 4,
            "1680x1050" : 5,
            "1920x1200" : 6,
            "1280x720" : 7,
            "1366x768" : 8,
            "1920x1080" : 9,
            "2560x1440" : 10
        }

        self.RESOLUTIONS_MAP = {
            
            0 : ("640", "480"),
            1 : ("800", "600"),
            2 : ("1024", "768"),
            3 : ("1280", "800"),
            4 : ("1440", "900"),
            5 : ("1680", "1050"),
            6 : ("1920", "1200"),
            7 : ("1280", "720"),
            8 : ("1366", "768"),
            9 : ("1920", "1080"),
            10 : ("2560", "1440")
            
        }

        self.resolutionsAmount = len(self.RESOLUTIONS_MAP)


    def get_font(self, size): 
        return pygame.font.Font("assets/font/Lato-Regular.ttf", size)

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

                       # self.SCREEN.blit(pygame.transform.scale(self.SCREEN,(self.SCREEN_WIDTH, self.SCREEN_HEIGHT)),(0,0))



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

                        game = Game(self.SCREEN, self.SCREEN_WIDTH, self.SCREEN_HEIGHT, self.FPS, self.mixer)
                        asyncio.run(game.play())

                    if self.OPTIONS_BUTTON.checkForInput(self.MENU_MOUSE_POS):
                        self.options()

                    if self.QUIT_BUTTON.checkForInput(self.MENU_MOUSE_POS):
                        pygame.quit()
                        sys.exit()

            pygame.display.update()


    
