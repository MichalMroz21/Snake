import pygame
from Button import Button
from ColorPicker import ColorPicker
from TextBox import TextBox
import enum

class BOX_ID(enum.Enum):
    NAME_BOX = 0
    LEFT_BOX = 1
    RIGHT_BOX = 2

class LobbyPlayer:
  
    def __init__(self, screen, screenWidth, screenHeight, whichPlayer, font): #whichPlayer from 1. 1,2,3,4...
              
        self.screen = screen
        self.screenWidth = screenWidth
        self.screenHeight = screenHeight
        self.Font = font
        self.nickFont = self.Font.get_normal_font(smaller = 1.5)

        self.halfWidth = self.screenWidth / 2
        self.halfHeight = self.screenHeight / 2

        self.name = ""
        self.maxNameLength = 6

        if whichPlayer > 4: return

        self.DefaultColor = "Red"

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

        self.NAME_BOX = TextBox(self.TEXT_BOX_X_POS, self.TEXT_BOX_Y_POS, self.TEXT_BOX_WIDTH, self.TEXT_BOX_HEIGHT, self.TEXT_RECT_COLOR, self.TEXT_RECT_COLOR_PICKED, self.nickFont, self.name, BOX_ID.NAME_BOX.value)

        self.SNAKE_RECT_HEIGHT_MULTIPLIER = 5

        self.SNAKE_RECT_Y_MARGIN = self.maxThickness * self.SNAKE_RECT_HEIGHT_MULTIPLIER

        self.SNAKE_X_POS = self.TEXT_BOX_X_POS
        self.SNAKE_Y_POS = self.TEXT_BOX_Y_POS + self.TEXT_BOX_HEIGHT + self.SNAKE_RECT_Y_MARGIN
        self.SNAKE_HEIGHT = self.thickness * self.SNAKE_RECT_HEIGHT_MULTIPLIER
        self.SNAKE_WIDTH = self.TEXT_BOX_WIDTH

        self.SNAKE_RECT = pygame.Rect(self.SNAKE_X_POS, self.SNAKE_Y_POS, self.SNAKE_WIDTH, self.SNAKE_HEIGHT)

        self.COLOR_PICKER_Y_MARGIN = self.SNAKE_HEIGHT
        self.COLOR_PICKER_WIDTH = self.SNAKE_WIDTH
        self.COLOR_PICKER_HEIGHT = self.SNAKE_HEIGHT

        self.COLOR_PICKER_X_POS = self.SNAKE_X_POS
        self.COLOR_PICKER_Y_POS = self.SNAKE_Y_POS + self.SNAKE_HEIGHT + self.COLOR_PICKER_Y_MARGIN

        self.colorPicker = ColorPicker(round(self.COLOR_PICKER_X_POS), round(self.COLOR_PICKER_Y_POS), round(self.COLOR_PICKER_WIDTH), round(self.COLOR_PICKER_HEIGHT))

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

        self.LEFT_BOX = TextBox(self.LEFT_BOX_X_POS, self.LEFT_BOX_Y_POS, self.LEFT_BOX_WIDTH, self.LEFT_BOX_HEIGHT, self.LEFT_RECT_COLOR, self.LEFT_RECT_COLOR_PICKED, self.nickFont, self.Left, BOX_ID.LEFT_BOX.value)

        self.RIGHT_BOX_WIDTH = ( self.maxNameLength / 2 + self.maxNameLength / 5 ) * self.nickFontSize / 4
        self.RIGHT_BOX_HEIGHT = self.nickFontSize 

        self.RIGHT_BOX_X_POS = self.COLOR_PICKER_X_POS + self.COLOR_PICKER_WIDTH - self.RIGHT_BOX_WIDTH
        self.RIGHT_BOX_Y_POS = self.COLOR_PICKER_Y_POS + self.RIGHT_BOX_HEIGHT

        self.RIGHT_RECT_COLOR = pygame.Color('lightskyblue3')
        self.RIGHT_RECT_COLOR_PICKED = pygame.Color('Red')

        self.RIGHT_BOX = TextBox(self.RIGHT_BOX_X_POS, self.RIGHT_BOX_Y_POS, self.RIGHT_BOX_WIDTH, self.RIGHT_BOX_HEIGHT, self.RIGHT_RECT_COLOR, self.RIGHT_RECT_COLOR_PICKED, self.nickFont, self.Right, BOX_ID.RIGHT_BOX.value)

        self.TEXT_BOXES = [self.NAME_BOX, self.LEFT_BOX, self.RIGHT_BOX]
        
        self.whichPicked = BOX_ID.NAME_BOX.value

        self.isTextPicked = False
        self.isAdded = False

    def displayPlayer(self, menu_mouse_pos, menu_mouse_buttons):

        for TEXT_BOX in self.TEXT_BOXES:
            TEXT_BOX.update()

        self.colorPicker.update(menu_mouse_pos, menu_mouse_buttons)

        if(self.isAdded == False):

            self.ADD_PLAYER_BUTTON.changeColor(menu_mouse_pos)
            self.ADD_PLAYER_BUTTON.update(self.screen)

        else:
           
            for TEXT_BOX in self.TEXT_BOXES:
                TEXT_BOX.drawNotPickedRectangle(self.screen)

            if self.isTextPicked:

                for TEXT_BOX in self.TEXT_BOXES:
                    if self.whichPicked == TEXT_BOX.text_id:
                         TEXT_BOX.drawPickedRectangle(self.screen)
            

            for TEXT_BOX in self.TEXT_BOXES:
                 TEXT_BOX.blitText(self.screen)

            pygame.draw.rect(self.screen, self.colorPicker.get_color(), self.SNAKE_RECT)

            self.colorPicker.draw(self.screen)


    def disableTextInput(self):
        self.isTextPicked = False


    def checkForInput(self, x, y, event):

        if event.type == pygame.KEYDOWN:
            if self.isTextPicked == True:

                if event.key == pygame.K_BACKSPACE:

                    for TEXT_BOX in self.TEXT_BOXES:
                        if self.whichPicked == TEXT_BOX.text_id:
                            if TEXT_BOX.text_id == BOX_ID.NAME_BOX.value:
                                TEXT_BOX.popBackText()

                elif event.unicode.isalnum():

                    for TEXT_BOX in self.TEXT_BOXES:

                        if self.whichPicked == TEXT_BOX.text_id:

                            if TEXT_BOX.text_id == BOX_ID.NAME_BOX.value and len(TEXT_BOX.text) < self.maxNameLength:
                                TEXT_BOX.addToText(event.unicode.upper())
                            if (TEXT_BOX.text_id == BOX_ID.LEFT_BOX.value or TEXT_BOX.text_id == BOX_ID.RIGHT_BOX.value) and event.unicode.isalpha():
                                TEXT_BOX.setText(event.unicode.lower())
                                

        if event.type == pygame.MOUSEBUTTONDOWN:

            if self.isAdded == True:
                for TEXT_BOX in self.TEXT_BOXES:
                     TEXT_BOX_ID = TEXT_BOX.checkIfClicked(x, y)
                     if TEXT_BOX_ID != None:
                         self.isTextPicked = True
                         self.whichPicked = TEXT_BOX_ID
                         return self.whichPlayer

            if self.ADD_PLAYER_BUTTON.checkForInput((x, y)) and self.isAdded == False:
                self.isAdded = True


        return 0

            
