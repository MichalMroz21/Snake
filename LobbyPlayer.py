import pygame
from Button import Button

class LobbyPlayer:

    def __init__(self, screen, screenWidth, screenHeight, whichPlayer, font): #whichPlayer from 1. 1,2,3,4...
              
        self.screen = screen
        self.screenWidth = screenWidth
        self.screenHeight = screenHeight
        self.Font = font

        self.halfWidth = self.screenWidth / 2
        self.halfHeight = self.screenHeight / 2

        self.name = ""
        self.maxNameLength = 6

        if whichPlayer > 4: return

        self.defaultColors = ["Red", "Blue", "Green", "Yellow"]
        self.color = self.defaultColors[whichPlayer - 1]

        self.whichPlayer = whichPlayer

        self.sumProportion = (self.screenWidth + self.screenHeight) / 1000

        self.ADD_PLAYER_BUTTON = Button(image=None, pos=(self.halfWidth * (( whichPlayer - 1) % 2) + self.halfWidth / 2, self.halfHeight * ((int)((whichPlayer - 1) / 2)) + self.halfHeight / 2), text_input="+", font=self.Font.get_title_font(smaller = 1, higher = self.sumProportion), base_color="White", hovering_color="Green")

        self.nickFontSize = self.Font.normalTextFontSize

        self.TEXT_RECT = pygame.Rect(self.halfWidth * (( whichPlayer - 1) % 2) + self.halfWidth / 2, self.halfHeight * ((int)((whichPlayer - 1) / 2)) + self.halfHeight / 2, ( self.maxNameLength / 2 + self.maxNameLength / 5 ) * self.nickFontSize, self.nickFontSize)
        self.TEXT_RECT_COLOR = pygame.Color('lightskyblue3')

        self.nickFont = self.Font.get_normal_font()
        

        self.TEXT_SURFACE = self.nickFont.render(self.name, True, (255, 255, 255))
        self.isTextPicked = False

        self.isAdded = False

    def displayPlayer(self, menu_mouse_pos):

        self.TEXT_SURFACE = self.nickFont.render(self.name, True, (255, 255, 255))

        if(self.isAdded == False):

            self.ADD_PLAYER_BUTTON.changeColor(menu_mouse_pos)
            self.ADD_PLAYER_BUTTON.update(self.screen)

        else:
            pygame.draw.rect(self.screen, self.TEXT_RECT_COLOR, self.TEXT_RECT, 2)
            self.screen.blit(self.TEXT_SURFACE, (self.TEXT_RECT.x, self.TEXT_RECT.y - self.nickFontSize / 8))


    def disableTextInput(self):
        self.isTextPicked = False


    def checkForInput(self, x, y, event):

        if event.type == pygame.KEYDOWN:
            if self.isTextPicked == True:

                if event.key == pygame.K_BACKSPACE:
                    self.name = self.name[:-1]

                elif len(self.name) < self.maxNameLength:
                    self.name += event.unicode.upper()

        if event.type == pygame.MOUSEBUTTONDOWN:

            if self.isAdded == True and x >= self.TEXT_RECT.x and x <= self.TEXT_RECT.x + self.TEXT_RECT.width and y >= self.TEXT_RECT.y and y <= self.TEXT_RECT.y + self.TEXT_RECT.height:
                self.isTextPicked = True
                return self.whichPlayer

            if self.ADD_PLAYER_BUTTON.checkForInput((x, y)) and self.isAdded == False:
                self.isAdded = True


        return 0

            
