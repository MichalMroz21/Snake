from Button import Button
from Game import Game
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
        self.gameVolume = 0.5
        self.FPS = 60

        self.SCREEN = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))

        self.game = Game(self.SCREEN, self.SCREEN_WIDTH, self.SCREEN_HEIGHT, self.gameVolume, self.FPS)

        pygame.display.set_caption("Snake Game")
        self.BG = pygame.image.load("assets/picture/MenuBackground.jpg")

        self.MENU_TEXT = self.get_font(100).render("Snake Game", True, "Yellow")
        self.MENU_RECT = self.MENU_TEXT.get_rect(center=(640, 100))

        self.PLAY_BUTTON = Button(image=None, pos=(640, 250), text_input="PLAY", font=self.get_font(75), base_color="White", hovering_color="Red")
        self.OPTIONS_BUTTON = Button(image=None, pos=(640, 400), text_input="OPTIONS", font=self.get_font(75), base_color="White", hovering_color="Red")
        self.QUIT_BUTTON = Button(image=None, pos=(640, 550), text_input="QUIT", font=self.get_font(75), base_color="White", hovering_color="Red")

        self.MENU_MOUSE_POS = pygame.mouse.get_pos()

        self.OPTIONS_TEXT = self.get_font(80).render("Options", True, "Yellow")
        self.OPTIONS_RECT = self.OPTIONS_TEXT.get_rect(center=(640, 100))

        self.OPTIONS_BACK = Button(image=None, pos=(640, 550), text_input="GO BACK", font=self.get_font(75), base_color="White", hovering_color="Red")



    def get_font(self, size): 
        return pygame.font.Font("assets/font/Lato-Regular.ttf", size)

    def options(self):

        while True:

            self.SCREEN.blit(self.BG, (0, 0))
            self.MENU_MOUSE_POS = pygame.mouse.get_pos()
       
            self.SCREEN.blit(self.OPTIONS_TEXT, self.OPTIONS_RECT)

            self.OPTIONS_BACK.changeColor(self.MENU_MOUSE_POS)
            self.OPTIONS_BACK.update(self.SCREEN)

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.OPTIONS_BACK.checkForInput(self.MENU_MOUSE_POS):
                        self.displayMainMenu()

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
                        asyncio.run(self.game.play())

                    if self.OPTIONS_BUTTON.checkForInput(self.MENU_MOUSE_POS):
                        self.options()

                    if self.QUIT_BUTTON.checkForInput(self.MENU_MOUSE_POS):
                        pygame.quit()
                        sys.exit()

            pygame.display.update()


    
