from Button import Button
from Game import Game
from Mixer import Mixer
from Slider import Slider
from Lobby import Lobby

from Font import Font

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

        self.screenWidth = self.maxResolutionWidth
        self.screenHeight = self.maxResolutionHeight

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

        self.RESOLUTIONS_INDEX[str(self.screenWidth) + "x" + str(self.screenHeight)] = self.resolutionsAmount

        self.RESOLUTIONS_MAP = {val:key for key, val in self.RESOLUTIONS_INDEX.items() }

        for k, v in self.RESOLUTIONS_MAP.items():
            self.RESOLUTIONS_MAP[k] = ( re.split('x', v)[0], re.split('x', v)[1] )

        self.RESOLUTIONS_MAP[self.resolutionsAmount] = (str(self.screenWidth), str(self.screenHeight))

        self.resolutionsAmount += 1

        self.resolution_init()


    def resolution_init(self, firstTime = True):

        pygame.display.quit()

        self.setGameWindowCenter((self.maxResolutionWidth - self.screenWidth) / 2, (self.maxResolutionHeight - self.screenHeight) / 2)

        pygame.display.init()

        self.screen = pygame.display.set_mode((self.screenWidth, self.screenHeight) ) 

        pygame.display.set_caption("Snake Game")

        self.BG = pygame.image.load("assets/picture/MenuBackground.jpg")
        self.BG = pygame.transform.scale(self.BG, (self.screenWidth, self.screenHeight))

        self.Font = Font(self.screenWidth, self.screenHeight)

        self.MENU_TEXT = self.Font.get_title_font().render("Snake Game", True, "Yellow")
        self.MENU_RECT = self.MENU_TEXT.get_rect(center=(self.screenWidth / 2, self.screenHeight / 7.2))

        self.PLAY_BUTTON = Button(image=None, pos=(self.screenWidth / 2, self.screenHeight / 2.8), text_input="PLAY", font=self.Font.get_normal_font(), base_color="White", hovering_color="Red")
        self.OPTIONS_BUTTON = Button(image=None, pos=(self.screenWidth / 2, self.screenHeight / 1.8), text_input="OPTIONS", font=self.Font.get_normal_font(), base_color="White", hovering_color="Red")
        self.QUIT_BUTTON = Button(image=None, pos=(self.screenWidth / 2, self.screenHeight / 1.3), text_input="QUIT", font=self.Font.get_normal_font(), base_color="White", hovering_color="Red")

        self.MENU_MOUSE_POS = pygame.mouse.get_pos()

        self.OPTIONS_TEXT = self.Font.get_title_font().render("Options", True, "Yellow")
        self.OPTIONS_RECT = self.OPTIONS_TEXT.get_rect(center=(self.screenWidth / 2, self.screenHeight / 8.5))

        self.OPTIONS_BACK = Button(image=None, pos=(self.screenWidth / 2, self.screenHeight / 1.1), text_input="GO BACK", font=self.Font.get_normal_font(smaller = 2), base_color="White", hovering_color="Red")

        self.OPTIONS_TEXT_RESOLUTION = self.Font.get_normal_font(1.5).render("Resolution", True, "White")
        self.OPTIONS_RECT_RESOLUTION = self.OPTIONS_TEXT_RESOLUTION.get_rect(center=(self.screenWidth / 2, self.screenHeight / 4.0))

        self.OPTIONS_RESOLUTION = Button(image=None, pos=(self.screenWidth / 2, self.screenHeight / 3.0), text_input=(str(self.screenWidth) + "x" + str(self.screenHeight)), font=self.Font.get_normal_font(smaller = 2), base_color="White", hovering_color="Red")
        self.OPTIONS_APPLY = Button(image=None, pos=(self.screenWidth / 2, self.screenHeight / 2.5), text_input="APPLY", font=self.Font.get_normal_font(smaller = 2), base_color="White", hovering_color="Red")

        sliderWidth = self.screenWidth/3
        sliderHeight = self.screenHeight/20

        self.OPTIONS_TEXT_MUSIC = self.Font.get_normal_font(smaller = 2).render("Music Volume", True, "White")
        self.OPTIONS_RECT_MUSIC = self.OPTIONS_TEXT_RESOLUTION.get_rect(center=(self.screenWidth / 2.0, self.screenHeight / 1.9))

        if 'OPTIONS_MUSIC_SLIDER' in dir(self):
            self.OPTIONS_MUSIC_SLIDER = Slider(self.screenWidth / 2 - sliderWidth/2, self.screenHeight / 1.7, sliderWidth, sliderHeight, (200, 200, 200), (255, 30, 30), 1, 0, 1, sliderHeight, self.OPTIONS_MUSIC_SLIDER.getValue())
        else:
            self.OPTIONS_MUSIC_SLIDER = Slider(self.screenWidth / 2 - sliderWidth/2, self.screenHeight / 1.7, sliderWidth, sliderHeight, (200, 200, 200), (255, 30, 30), 1, 0, 1, sliderHeight, 0.5)

        self.OPTIONS_TEXT_SOUND = self.Font.get_normal_font(smaller = 2).render("Effects Volume", True, "White")
        self.OPTIONS_RECT_SOUND = self.OPTIONS_TEXT_RESOLUTION.get_rect(center=(self.screenWidth / 2.0, self.screenHeight / 1.4))

        if 'OPTIONS_SOUND_SLIDER' in dir(self):
            self.OPTIONS_SOUND_SLIDER = Slider(self.screenWidth / 2 - sliderWidth/2, self.screenHeight / 1.3, sliderWidth, sliderHeight, (200, 200, 200), (30, 255, 30), 1, 0, 1, sliderHeight, self.OPTIONS_SOUND_SLIDER.getValue())
        else:
            self.OPTIONS_SOUND_SLIDER = Slider(self.screenWidth / 2 - sliderWidth/2, self.screenHeight / 1.3, sliderWidth, sliderHeight, (200, 200, 200), (30, 255, 30), 1, 0, 1, sliderHeight, 0.5)

        self.displayMainMenu(firstTime = firstTime)


    def setGameWindowCenter(self, x, y):
        os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (x,y)


    def options(self):

        curIndex = self.RESOLUTIONS_INDEX[str(self.screenWidth) + "x" + str(self.screenHeight)]

        initialIndex = curIndex

        while True:

            self.screen.blit(self.BG, (0, 0))

            self.screen.blit(self.OPTIONS_TEXT, self.OPTIONS_RECT)
            self.screen.blit(self.OPTIONS_TEXT_RESOLUTION, self.OPTIONS_RECT_RESOLUTION)
            self.screen.blit(self.OPTIONS_TEXT_MUSIC, self.OPTIONS_RECT_MUSIC)
            self.screen.blit(self.OPTIONS_TEXT_SOUND, self.OPTIONS_RECT_SOUND)

            self.OPTIONS_MUSIC_SLIDER.draw(self.screen)
            self.OPTIONS_SOUND_SLIDER.draw(self.screen)
     
            self.MENU_MOUSE_POS = pygame.mouse.get_pos()

            self.OPTIONS_BACK.changeColor(self.MENU_MOUSE_POS)
            self.OPTIONS_BACK.update(self.screen)

            self.OPTIONS_RESOLUTION.changeColor(self.MENU_MOUSE_POS)
            self.OPTIONS_RESOLUTION.update(self.screen)

            self.OPTIONS_APPLY.changeColor(self.MENU_MOUSE_POS)
            self.OPTIONS_APPLY.update(self.screen)

            
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.OPTIONS_BACK.checkForInput(self.MENU_MOUSE_POS):
                        self.OPTIONS_RESOLUTION.changeText(self.RESOLUTIONS_MAP[initialIndex][0] + "x" + self.RESOLUTIONS_MAP[initialIndex][1])
                        self.displayMainMenu()

                    if self.OPTIONS_RESOLUTION.checkForInput(self.MENU_MOUSE_POS):

                        curIndex += 1

                        if(curIndex == self.resolutionsAmount):
                            curIndex = 0

                        self.OPTIONS_RESOLUTION.changeText(self.RESOLUTIONS_MAP[curIndex][0] + "x" + self.RESOLUTIONS_MAP[curIndex][1])

                    if self.OPTIONS_APPLY.checkForInput(self.MENU_MOUSE_POS):

                        self.screenWidth = int(self.RESOLUTIONS_MAP[curIndex][0])
                        self.screenHeight = int(self.RESOLUTIONS_MAP[curIndex][1])
                        self.resolution_init(firstTime = False)

                if pygame.mouse.get_pressed()[0]:
                    self.OPTIONS_MUSIC_SLIDER.update(self.MENU_MOUSE_POS)
                    self.OPTIONS_SOUND_SLIDER.update(self.MENU_MOUSE_POS)

                    self.mixer.setMusicVolume(self.OPTIONS_MUSIC_SLIDER.getValue())
                    self.mixer.setSoundVolume(self.OPTIONS_SOUND_SLIDER.getValue())

                if event.type == self.mixer.SONG_END:
                    self.mixer.playMenuMusic()

            pygame.display.update()



    def displayMainMenu(self, firstTime = False):

        if firstTime == True:
           self.mixer.playMenuMusic()
        
        while True:

            self.screen.blit(self.BG, (0, 0))
            self.MENU_MOUSE_POS = pygame.mouse.get_pos()

            self.screen.blit(self.MENU_TEXT, self.MENU_RECT)

            for button in [self.PLAY_BUTTON, self.OPTIONS_BUTTON, self.QUIT_BUTTON]:
                button.changeColor(self.MENU_MOUSE_POS)
                button.update(self.screen)
        
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.PLAY_BUTTON.checkForInput(self.MENU_MOUSE_POS):

                      
                      lobby = Lobby(self.screen, self.screenWidth, self.screenHeight, self.FPS, self.mixer, self, self.Font)
                      lobby.displayLobby()
                        

                    if self.OPTIONS_BUTTON.checkForInput(self.MENU_MOUSE_POS):
                        self.options()

                    if self.QUIT_BUTTON.checkForInput(self.MENU_MOUSE_POS):
                        pygame.quit()
                        sys.exit()

                if event.type == self.mixer.SONG_END:
                    self.mixer.playMenuMusic()

            pygame.display.update()


    
