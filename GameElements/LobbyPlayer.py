import pygame
from GuiElements.Button import Button
from GuiElements.ColorPicker import ColorPicker
from GuiElements.TextBox import TextBox
import enum
import math


class BoxId(enum.Enum):
    NAME_BOX = 0
    LEFT_BOX = 1
    RIGHT_BOX = 2
    SPEED_BOX = 3


class LobbyPlayer:

    MAX_NAME_LENGTH = 6
    MAX_PRECISION = 4
    DEFAULT_THICKNESS = 5
    INITIAL_SPEED = 1.75
    DEFAULT_COLOR = "Red"
    DEFAULT_LEFT = 'a'
    DEFAULT_RIGHT = 'd'

    # whichPlayer from 1. 1,2,3,4...
    def __init__(self, screen, screen_width, screen_height, which_player, font, max_players):

        self.screen = screen
        self.screenWidth = screen_width
        self.screenHeight = screen_height
        self.Font = font
        self.nickFont = self.Font.get_normal_font(smaller=1.5)

        self.halfWidth = self.screenWidth / 2
        self.halfHeight = self.screenHeight / 2

        self.name = ""

        if which_player > max_players:
            return

        self.color = LobbyPlayer.DEFAULT_COLOR
        self.speed = str(LobbyPlayer.INITIAL_SPEED)
        self.thickness = LobbyPlayer.DEFAULT_THICKNESS
        self.maxThickness = LobbyPlayer.DEFAULT_THICKNESS

        self.whichPlayer = which_player

        self.sumProportion = (self.screenWidth + self.screenHeight) / 1000

        self.ADD_PLAYER_BUTTON = Button(image=None, pos=(self.halfWidth * ((which_player - 1) % 2) + self.halfWidth / 2,
                                                         self.halfHeight * (
                                                             int((which_player - 1) / 2)) + self.halfHeight / 2),
                                        text_input="+",
                                        font=self.Font.get_title_font(smaller=1, higher=self.sumProportion),
                                        base_color="White", hovering_color="Green")

        self.nickFontSize = self.Font.normalTextFontSize

        self.TEXT_MARGIN_X = self.screenWidth / 10
        self.TEXT_MARGIN_Y = self.screenHeight / 10

        self.TEXT_BOX_WIDTH = (LobbyPlayer.MAX_NAME_LENGTH / 2 + LobbyPlayer.MAX_NAME_LENGTH / 5) * self.nickFontSize
        self.TEXT_BOX_HEIGHT = self.nickFontSize

        self.TEXT_BOX_Y_POS = self.halfHeight * (int((which_player - 1) / 2)) + self.TEXT_MARGIN_Y * abs(
            int((which_player - 1) / 2) - 1) + (int((which_player - 1) / 2)) * (self.TEXT_MARGIN_Y / 2)

        self.TEXT_BOX_X_POS = (self.halfWidth * ((which_player - 1) % 2) + self.TEXT_MARGIN_X * (which_player % 2)
                               + abs(which_player % 2 - 1) * (self.halfWidth -
                                                              self.TEXT_MARGIN_X - self.TEXT_BOX_WIDTH))

        self.TEXT_RECT = pygame.Rect(self.TEXT_BOX_X_POS, self.TEXT_BOX_Y_POS, self.TEXT_BOX_WIDTH,
                                     self.TEXT_BOX_HEIGHT)

        self.TEXT_RECT_COLOR = pygame.Color('lightskyblue3')
        self.TEXT_RECT_COLOR_PICKED = pygame.Color('Red')

        self.NAME_BOX = TextBox(self.TEXT_BOX_X_POS, self.TEXT_BOX_Y_POS, self.TEXT_BOX_WIDTH, self.TEXT_BOX_HEIGHT,
                                self.TEXT_RECT_COLOR, self.TEXT_RECT_COLOR_PICKED, self.nickFont, self.name,
                                BoxId.NAME_BOX.value)

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

        self.colorPicker = ColorPicker(round(self.COLOR_PICKER_X_POS), round(self.COLOR_PICKER_Y_POS),
                                       round(self.COLOR_PICKER_WIDTH), round(self.COLOR_PICKER_HEIGHT))

        self.initialLeft = LobbyPlayer.DEFAULT_LEFT
        self.initialRight = LobbyPlayer.DEFAULT_RIGHT

        self.left = self.initialLeft
        self.right = self.initialRight

        self.LEFT_BOX_WIDTH = ((LobbyPlayer.MAX_NAME_LENGTH / 2 + LobbyPlayer.MAX_NAME_LENGTH / 5) *
                               self.nickFontSize / 4)
        self.LEFT_BOX_HEIGHT = self.nickFontSize

        self.LEFT_BOX_X_POS = self.COLOR_PICKER_X_POS
        self.LEFT_BOX_Y_POS = self.COLOR_PICKER_Y_POS + self.LEFT_BOX_HEIGHT

        self.LEFT_RECT = pygame.Rect(self.LEFT_BOX_X_POS, self.LEFT_BOX_Y_POS, self.LEFT_BOX_WIDTH,
                                     self.LEFT_BOX_HEIGHT)

        self.LEFT_RECT_COLOR = pygame.Color('lightskyblue3')
        self.LEFT_RECT_COLOR_PICKED = pygame.Color('Blue')

        self.LEFT_BOX = TextBox(self.LEFT_BOX_X_POS, self.LEFT_BOX_Y_POS, self.LEFT_BOX_WIDTH, self.LEFT_BOX_HEIGHT,
                                self.LEFT_RECT_COLOR, self.LEFT_RECT_COLOR_PICKED,
                                self.nickFont, self.initialLeft, BoxId.LEFT_BOX.value)

        self.LEFT_TEXT_WIDTH, self.LEFT_TEXT_HEIGHT = (self.Font.get_normal_font(smaller=3.0 / self.sumProportion)
                                                       .size("<-"))

        self.LEFT_TEXT = self.Font.get_normal_font(smaller=3.0 / self.sumProportion).render("<-", True, "White")

        self.LEFT_TEXT_RECT = self.LEFT_TEXT.get_rect(center=(self.LEFT_BOX_X_POS + self.LEFT_BOX_WIDTH / 2,
                                                              self.COLOR_PICKER_Y_POS + self.COLOR_PICKER_HEIGHT +
                                                              (self.LEFT_BOX_Y_POS - self.COLOR_PICKER_Y_POS -
                                                               self.COLOR_PICKER_HEIGHT -
                                                               self.LEFT_TEXT_HEIGHT / 4) / 2))

        self.RIGHT_BOX_WIDTH = ((LobbyPlayer.MAX_NAME_LENGTH / 2 + LobbyPlayer.MAX_NAME_LENGTH / 5) *
                                self.nickFontSize / 4)
        self.RIGHT_BOX_HEIGHT = self.nickFontSize

        self.RIGHT_BOX_X_POS = self.COLOR_PICKER_X_POS + self.COLOR_PICKER_WIDTH - self.RIGHT_BOX_WIDTH
        self.RIGHT_BOX_Y_POS = self.COLOR_PICKER_Y_POS + self.RIGHT_BOX_HEIGHT

        self.RIGHT_RECT_COLOR = self.LEFT_RECT_COLOR
        self.RIGHT_RECT_COLOR_PICKED = self.LEFT_RECT_COLOR_PICKED

        self.RIGHT_BOX = TextBox(self.RIGHT_BOX_X_POS, self.RIGHT_BOX_Y_POS, self.RIGHT_BOX_WIDTH,
                                 self.RIGHT_BOX_HEIGHT, self.RIGHT_RECT_COLOR, self.RIGHT_RECT_COLOR_PICKED,
                                 self.nickFont, self.initialRight, BoxId.RIGHT_BOX.value)

        self.RIGHT_TEXT_WIDTH, self.RIGHT_TEXT_HEIGHT = (self.Font.get_normal_font(smaller=3.0 / self.sumProportion)
                                                         .size("->"))

        self.RIGHT_TEXT = self.Font.get_normal_font(smaller=3.0 / self.sumProportion).render("->", True, "White")

        self.RIGHT_TEXT_RECT = self.RIGHT_TEXT.get_rect(center=(self.RIGHT_BOX_X_POS + self.RIGHT_BOX_WIDTH / 2,
                                                                self.COLOR_PICKER_Y_POS + self.COLOR_PICKER_HEIGHT +
                                                                (self.RIGHT_BOX_Y_POS - self.COLOR_PICKER_Y_POS -
                                                                 self.COLOR_PICKER_HEIGHT - self.RIGHT_TEXT_HEIGHT / 4)
                                                                / 2))

        self.SPEED_BOX_WIDTH = ((LobbyPlayer.MAX_NAME_LENGTH / 2 + LobbyPlayer.MAX_NAME_LENGTH / 5) *
                                self.nickFontSize / 4)
        self.SPEED_BOX_HEIGHT = self.nickFontSize

        self.SPEED_BOX_X_POS = (self.LEFT_BOX_X_POS + self.RIGHT_BOX_X_POS +
                                self.RIGHT_BOX_WIDTH - self.SPEED_BOX_WIDTH) / 2

        self.SPEED_BOX_Y_POS = self.COLOR_PICKER_Y_POS + self.RIGHT_BOX_HEIGHT

        self.SPEED_RECT_COLOR = self.LEFT_RECT_COLOR
        self.SPEED_RECT_COLOR_PICKED = self.LEFT_RECT_COLOR_PICKED

        self.SPEED_BOX = TextBox(self.SPEED_BOX_X_POS, self.SPEED_BOX_Y_POS, self.SPEED_BOX_WIDTH,
                                 self.SPEED_BOX_HEIGHT,
                                 self.SPEED_RECT_COLOR, self.SPEED_RECT_COLOR_PICKED,
                                 self.Font.get_normal_font(smaller=3.0 / math.sqrt(self.sumProportion)),
                                 LobbyPlayer.INITIAL_SPEED, BoxId.SPEED_BOX.value)

        self.SPEED_TEXT_WIDTH, self.SPEED_TEXT_HEIGHT = self.Font.get_normal_font(
            smaller=3.0 / math.sqrt(self.sumProportion)).size("Speed")

        self.SPEED_TEXT = self.Font.get_normal_font(smaller=3.0 / math.sqrt(self.sumProportion)).render("Speed",
                                                                                                        True, "White")

        self.SPEED_TEXT_RECT = self.SPEED_TEXT.get_rect(center=(self.SPEED_BOX_X_POS + self.SPEED_BOX_WIDTH / 2,
                                                                self.COLOR_PICKER_Y_POS + self.COLOR_PICKER_HEIGHT +
                                                                (self.RIGHT_BOX_Y_POS - self.COLOR_PICKER_Y_POS -
                                                                 self.COLOR_PICKER_HEIGHT - self.RIGHT_TEXT_HEIGHT / 4)
                                                                / 2))

        self.TEXT_BOXES = [self.NAME_BOX, self.LEFT_BOX, self.RIGHT_BOX, self.SPEED_BOX]

        self.whichPicked = BoxId.NAME_BOX.value

        self.isTextPicked = False
        self.isAdded = False

    def display_player(self, menu_mouse_pos, menu_mouse_buttons):

        for TEXT_BOX in self.TEXT_BOXES:
            TEXT_BOX.update()

        self.colorPicker.update(menu_mouse_pos, menu_mouse_buttons)
        self.color = self.colorPicker.get_color()

        if self.isAdded is False:

            self.ADD_PLAYER_BUTTON.change_color(menu_mouse_pos)
            self.ADD_PLAYER_BUTTON.update(self.screen)

        else:
            for TEXT_BOX in self.TEXT_BOXES:
                TEXT_BOX.draw_not_picked_rectangle(self.screen)

            if self.isTextPicked:

                for TEXT_BOX in self.TEXT_BOXES:
                    if self.whichPicked == TEXT_BOX.text_id:
                        TEXT_BOX.draw_picked_rectangle(self.screen)

            for TEXT_BOX in self.TEXT_BOXES:
                TEXT_BOX.blit_text(self.screen)

            pygame.draw.rect(self.screen, self.colorPicker.get_color(), self.SNAKE_RECT)

            self.colorPicker.draw(self.screen)

            for playerObject in [(self.LEFT_TEXT, self.LEFT_TEXT_RECT), (self.RIGHT_TEXT, self.RIGHT_TEXT_RECT),
                                 (self.SPEED_TEXT, self.SPEED_TEXT_RECT)]:
                self.screen.blit(playerObject[0], playerObject[1])

    def disable_text_input(self):
        self.isTextPicked = False

    def check_for_input(self, x, y, event):

        if event.type == pygame.KEYDOWN:
            if self.isTextPicked:
                character_pressed = event.unicode

                if event.key == pygame.K_BACKSPACE:

                    for TEXT_BOX in self.TEXT_BOXES:
                        if self.whichPicked == TEXT_BOX.text_id:

                            if TEXT_BOX.text_id == BoxId.NAME_BOX.value:
                                TEXT_BOX.pop_back_text()

                            if TEXT_BOX.text_id == BoxId.SPEED_BOX.value:
                                if len(TEXT_BOX.text) == 1:
                                    continue

                                elif len(TEXT_BOX.text) == 2:
                                    temp = list(TEXT_BOX.text)
                                    temp.pop(0)
                                    TEXT_BOX.text = ''.join(temp)

                                else:
                                    TEXT_BOX.pop_back_text()

                elif character_pressed.isalnum():

                    for TEXT_BOX in self.TEXT_BOXES:

                        if self.whichPicked == TEXT_BOX.text_id:

                            if (TEXT_BOX.text_id == BoxId.NAME_BOX.value and
                                    len(TEXT_BOX.text) < LobbyPlayer.MAX_NAME_LENGTH):
                                TEXT_BOX.add_to_text(character_pressed.upper())

                            if ((TEXT_BOX.text_id == BoxId.LEFT_BOX.value and self.RIGHT_BOX.text
                                 != character_pressed.lower() and character_pressed.isalpha())
                                    or (TEXT_BOX.text_id == BoxId.RIGHT_BOX.value and
                                        self.LEFT_BOX.text != character_pressed.lower()
                                        and character_pressed.isalpha())):
                                TEXT_BOX.set_text(character_pressed.lower())

                            if TEXT_BOX.text_id == BoxId.SPEED_BOX.value and len(
                                    TEXT_BOX.text) < LobbyPlayer.MAX_PRECISION and character_pressed.isnumeric():

                                if TEXT_BOX.text[0] != '.':
                                    TEXT_BOX.add_to_text(character_pressed)

                                else:
                                    temp = list(TEXT_BOX.text)
                                    temp.insert(0, character_pressed)
                                    TEXT_BOX.text = ''.join(temp)

        self.name = self.NAME_BOX.text
        self.left, self.right = self.LEFT_BOX.text, self.RIGHT_BOX.text
        self.speed = self.SPEED_BOX.text

        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.isAdded:

                for TEXT_BOX in self.TEXT_BOXES:
                    text_box_id = TEXT_BOX.check_if_clicked(x, y)

                    if text_box_id is not None:
                        self.isTextPicked = True
                        self.whichPicked = text_box_id
                        return self.whichPlayer

            if self.ADD_PLAYER_BUTTON.check_for_input((x, y)) and self.isAdded is False:
                self.isAdded = True

        return None
