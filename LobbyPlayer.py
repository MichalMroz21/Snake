import pygame
from Button import Button
from ColorPicker import ColorPicker

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

        self.color = "Red"

        self.defaultThickness = 5
        self.defaultSpeed = 1.75
        self.maxThickness = self.defaultThickness

        self.thickness = self.defaultThickness
        self.speed = self.defaultSpeed

        self.whichPlayer = whichPlayer

        self.sumProportion = (self.screenWidth + self.screenHeight) / 1000

        self.ADD_PLAYER_BUTTON = Button(image=None, pos=(self.halfWidth * (( whichPlayer - 1) % 2) + self.halfWidth / 2, self.halfHeight * (int((whichPlayer - 1) / 2)) + self.halfHeight / 2), text_input="+", font=self.Font.get_title_font(smaller = 1, higher = self.sumProportion), base_color="White", hovering_color="Green")

        self.nickFontSize = self.Font.normalTextFontSize

        self.TEXT_MARGIN_X = self.screenWidth / 10
        self.TEXT_MARGIN_Y = self.screenHeight / 10

        self.TEXT_BOX_WIDTH = ( self.maxNameLength / 2 + self.maxNameLength / 5 ) * self.nickFontSize
        self.TEXT_BOX_HEIGHT = self.nickFontSize

        self.TEXT_BOX_Y_POS = self.halfHeight * (int((whichPlayer - 1) / 2)) + self.TEXT_MARGIN_Y * abs(int((whichPlayer - 1) / 2) - 1) + (int((whichPlayer - 1) / 2)) * (self.TEXT_MARGIN_Y / 2)
        self.TEXT_BOX_X_POS = self.halfWidth * (( whichPlayer - 1) % 2) + self.TEXT_MARGIN_X * (whichPlayer % 2) + abs(whichPlayer % 2 - 1) * (self.halfWidth - self.TEXT_MARGIN_X - self.TEXT_BOX_WIDTH)

        self.TEXT_RECT = pygame.Rect(self.TEXT_BOX_X_POS, self.TEXT_BOX_Y_POS, self.TEXT_BOX_WIDTH, self.TEXT_BOX_HEIGHT)

        self.TEXT_RECT_COLOR = pygame.Color('lightskyblue3')
        self.TEXT_RECT_COLOR_PICKED = pygame.Color('Red')

        self.SNAKE_RECT_HEIGHT_MULTIPLIER = 5

        self.SNAKE_RECT_Y_MARGIN = self.maxThickness * self.SNAKE_RECT_HEIGHT_MULTIPLIER

        self.SNAKE_X_POS = self.TEXT_BOX_X_POS
        self.SNAKE_Y_POS = self.TEXT_BOX_Y_POS + self.TEXT_BOX_HEIGHT + self.SNAKE_RECT_Y_MARGIN
        self.SNAKE_HEIGHT = self.thickness * self.SNAKE_RECT_HEIGHT_MULTIPLIER
        self.SNAKE_WIDTH = self.TEXT_BOX_WIDTH

        self.SNAKE_RECT = pygame.Rect(self.SNAKE_X_POS, self.SNAKE_Y_POS, self.SNAKE_WIDTH, self.SNAKE_HEIGHT)

        self.nickFont = self.Font.get_normal_font(smaller = 1.5)
        
        self.TEXT_SURFACE = self.nickFont.render(self.name, True, (255, 255, 255))

        self.TEXT_WIDTH, self.TEXT_HEIGHT = self.nickFont.size(self.name)

        self.COLOR_PICKER_Y_MARGIN = self.SNAKE_HEIGHT
        self.COLOR_PICKER_WIDTH = self.SNAKE_WIDTH
        self.COLOR_PICKER_HEIGHT = self.SNAKE_HEIGHT

        self.COLOR_PICKER_X_POS = self.SNAKE_X_POS
        self.COLOR_PICKER_Y_POS = self.SNAKE_Y_POS + self.SNAKE_HEIGHT + self.COLOR_PICKER_Y_MARGIN

        self.colorPicker = ColorPicker(round(self.COLOR_PICKER_X_POS), round(self.COLOR_PICKER_Y_POS), round(self.COLOR_PICKER_WIDTH), round(self.COLOR_PICKER_HEIGHT))\

        self.defaultLeft =  'a'
        self.defaultRight = 'd'

        self.Left = self.defaultLeft
        self.Right = self.defaultRight


        self.LEFT_BOX_WIDTH = ( self.maxNameLength / 2 + self.maxNameLength / 5 ) * self.nickFontSize / 4
        self.LEFT_BOX_HEIGHT = self.nickFontSize 

        self.LEFT_BOX_X_POS = self.COLOR_PICKER_X_POS 
        self.LEFT_BOX_Y_POS = self.COLOR_PICKER_Y_POS + self.LEFT_BOX_HEIGHT

        self.LEFT_RECT = pygame.Rect(self.LEFT_BOX_X_POS, self.LEFT_BOX_Y_POS, self.LEFT_BOX_WIDTH, self.LEFT_BOX_HEIGHT)

        self.LEFT_RECT_COLOR = pygame.Color('lightskyblue3')
        self.LEFT_RECT_COLOR_PICKED = pygame.Color('Red')


        self.RIGHT_BOX_WIDTH = ( self.maxNameLength / 2 + self.maxNameLength / 5 ) * self.nickFontSize / 4
        self.RIGHT_BOX_HEIGHT = self.nickFontSize 

        self.RIGHT_BOX_X_POS = self.COLOR_PICKER_X_POS + self.COLOR_PICKER_WIDTH - self.RIGHT_BOX_WIDTH
        self.RIGHT_BOX_Y_POS = self.COLOR_PICKER_Y_POS + self.RIGHT_BOX_HEIGHT

        self.RIGHT_RECT = pygame.Rect(self.RIGHT_BOX_X_POS, self.RIGHT_BOX_Y_POS, self.RIGHT_BOX_WIDTH, self.RIGHT_BOX_HEIGHT)

        self.RIGHT_RECT_COLOR = pygame.Color('lightskyblue3')
        self.RIGHT_RECT_COLOR_PICKED = pygame.Color('Red')


        self.whichPicked = 0


        self.isTextPicked = False
        self.isAdded = False

    def displayPlayer(self, menu_mouse_pos, menu_mouse_buttons):

        self.TEXT_SURFACE = self.nickFont.render(self.name, True, (255, 255, 255))
        self.TEXT_WIDTH, self.TEXT_HEIGHT = self.nickFont.size(self.name)

        self.LEFT_SURFACE = self.nickFont.render(self.Left.upper(), True, (255, 255, 255))
        self.LEFT_WIDTH, self.TEXT_HEIGHT = self.nickFont.size(self.Left.upper())

        self.RIGHT_SURFACE = self.nickFont.render(self.Right.upper(), True, (255, 255, 255))
        self.RIGHT_WIDTH, self.TEXT_HEIGHT = self.nickFont.size(self.Right.upper())

        self.colorPicker.update(menu_mouse_pos, menu_mouse_buttons)
        self.color = self.colorPicker.get_color()

        if(self.isAdded == False):

            self.ADD_PLAYER_BUTTON.changeColor(menu_mouse_pos)
            self.ADD_PLAYER_BUTTON.update(self.screen)

        else:
           
            pygame.draw.rect(self.screen, self.TEXT_RECT_COLOR, self.TEXT_RECT, 2)
            pygame.draw.rect(self.screen, self.TEXT_RECT_COLOR, self.LEFT_RECT, 2)
            pygame.draw.rect(self.screen, self.TEXT_RECT_COLOR, self.RIGHT_RECT, 2)

            if self.isTextPicked:
                if self.whichPicked == 0:
                    pygame.draw.rect(self.screen, self.TEXT_RECT_COLOR_PICKED, self.TEXT_RECT, 2)
                if self.whichPicked == 1:
                    pygame.draw.rect(self.screen, self.LEFT_RECT_COLOR_PICKED, self.LEFT_RECT, 2)
                if self.whichPicked == 2:
                    pygame.draw.rect(self.screen, self.RIGHT_RECT_COLOR_PICKED, self.RIGHT_RECT, 2)
            
            self.screen.blit(self.TEXT_SURFACE, (self.TEXT_RECT.x + self.TEXT_BOX_WIDTH / 2 - self.TEXT_WIDTH / 2, self.TEXT_RECT.y + self.TEXT_BOX_HEIGHT / 2 - self.nickFont.get_height() / 2))
            self.screen.blit(self.LEFT_SURFACE, (self.LEFT_RECT.x + self.LEFT_BOX_WIDTH / 2 - self.LEFT_WIDTH / 2, self.LEFT_RECT.y + self.LEFT_BOX_HEIGHT / 2 - self.nickFont.get_height() / 2))
            self.screen.blit(self.RIGHT_SURFACE, (self.RIGHT_RECT.x + self.RIGHT_BOX_WIDTH / 2 - self.RIGHT_WIDTH / 2, self.RIGHT_RECT.y + self.RIGHT_BOX_HEIGHT / 2 - self.nickFont.get_height() / 2))

            pygame.draw.rect(self.screen, self.color, self.SNAKE_RECT)

            self.colorPicker.draw(self.screen)


    def disableTextInput(self):
        self.isTextPicked = False


    def checkForInput(self, x, y, event):

        if event.type == pygame.KEYDOWN:
            if self.isTextPicked == True:

                if event.key == pygame.K_BACKSPACE:
                    if self.whichPicked == 0:
                        self.name = self.name[:-1]

                elif event.unicode.isalnum():
                    if self.whichPicked == 0 and len(self.name) < self.maxNameLength:
                        self.name += event.unicode.upper()
                    if self.whichPicked == 1 and event.unicode.isalpha():
                        self.Left = event.unicode.lower()
                    if self.whichPicked == 2 and event.unicode.isalpha():
                        self.Right = event.unicode.lower()

        if event.type == pygame.MOUSEBUTTONDOWN:

            if self.isAdded == True and x >= self.TEXT_RECT.x and x <= self.TEXT_RECT.x + self.TEXT_RECT.width and y >= self.TEXT_RECT.y and y <= self.TEXT_RECT.y + self.TEXT_RECT.height:
                self.isTextPicked = True
                self.whichPicked = 0
                return self.whichPlayer

            if self.isAdded == True and x >= self.LEFT_RECT.x and x <= self.LEFT_RECT.x + self.LEFT_RECT.width and y >= self.LEFT_RECT.y and y <= self.LEFT_RECT.y + self.LEFT_RECT.height:
                self.isTextPicked = True
                self.whichPicked = 1
                return self.whichPlayer

            if self.isAdded == True and x >= self.RIGHT_RECT.x and x <= self.RIGHT_RECT.x + self.RIGHT_RECT.width and y >= self.RIGHT_RECT.y and y <= self.RIGHT_RECT.y + self.RIGHT_RECT.height:
                self.isTextPicked = True
                self.whichPicked = 2
                return self.whichPlayer

            if self.ADD_PLAYER_BUTTON.checkForInput((x, y)) and self.isAdded == False:
                self.isAdded = True


        return 0

            
