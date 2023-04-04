import pygame, sys
from Button import Button
from Player import Player
import time 
import math

class MainMenu:

    def __init__(self):

        pygame.init()
        self.SCREEN = pygame.display.set_mode((1280, 720))
        pygame.display.set_caption("Snake Game")
        self.BG = pygame.image.load("assets/MenuBackground.jpg")

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
        return pygame.font.Font("assets/Lato-Regular.ttf", size)

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
                        self.play()
                    if self.OPTIONS_BUTTON.checkForInput(self.MENU_MOUSE_POS):
                        self.options()
                    if self.QUIT_BUTTON.checkForInput(self.MENU_MOUSE_POS):
                        pygame.quit()
                        sys.exit()

            pygame.display.update()


    def play(self):

        player = Player()
        lastFrameTime = time.time()
        gameBackgroundColor = "black" 

        clock = pygame.time.Clock() 
        self.SCREEN.fill(gameBackgroundColor)

        while True:
            
            self.MENU_MOUSE_POS = pygame.mouse.get_pos()

            newPosition = player.calcNewPosition()
            newPositionHead = player.calcNewHeadPosition()

            player.updatePosition(newPosition[0], newPosition[1])
            player.updatePause()

            if player.addToPreviousPositions(newPositionHead[0], newPositionHead[1]):
                for i in player.previousPositions:
                    pygame.draw.rect(self.SCREEN, gameBackgroundColor, pygame.Rect(i[0], i[1], player.headThickness, player.headThickness))
                
                player.clearPreviousPositions()
                player.addToPreviousPositions(newPositionHead[0], newPositionHead[1])

            pygame.draw.rect(self.SCREEN, player.headColor, pygame.Rect(newPositionHead[0], newPositionHead[1], player.headThickness, player.headThickness))

            if player.checkIfInRange(): pygame.draw.rect(self.SCREEN, player.color, pygame.Rect(newPosition[0], newPosition[1], player.thickness, player.thickness))

            
            keys = pygame.key.get_pressed() 

            if keys[ord('a')]: 

                player.alpha -= player.alphaChange
                player.alphaHead -= player.alphaChange

                if player.alphaDistancedLeft == False:
                    player.alphaHead -= player.alphaChange * 2
                    player.alphaDistancedLeft = True

            elif keys[ord('d')]: 

                player.alpha += player.alphaChange
                player.alphaHead += player.alphaChange

                if player.alphaDistancedRight == False:
                    player.alphaHead += player.alphaChange * 2 
                    player.alphaDistancedRight = True
            else:
                player.alphaHead = player.alpha
                player.alphaDistancedRight = False
                player.alphaDistancedLeft = False

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                        

            pygame.display.update()
            clock.tick(60)
 
 

menu = MainMenu()
menu.displayMainMenu()
 
