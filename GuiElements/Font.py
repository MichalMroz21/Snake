import pygame

from Utils.AssetManager import AssetManager


class Font:
    def __init__(self, screen_width, screen_height):

        self.screenWidth = screen_width
        self.screenHeight = screen_height

        self.titleFontSize = (self.screenWidth + self.screenHeight) / 20
        self.normalTextFontSize = (self.screenWidth + self.screenHeight) / 28

        self.font = AssetManager.Fonts.LATO.value

    def get_title_font(self, smaller=1, higher=1, bold=False, italic=False):
        return pygame.font.Font(self.font, round(self.titleFontSize/smaller * higher), bold=bold, italic=italic)

    def get_normal_font(self, smaller=1, higher=1, bold=False, italic=False):
        return pygame.font.Font(self.font, round(self.normalTextFontSize/smaller * higher), bold=bold, italic=italic)

    def update_font_sizes(self, screen_width, screen_height):
        self.screenWidth = screen_width
        self.screenHeight = screen_height

        self.titleFontSize = (self.screenWidth + self.screenHeight) / 20
        self.normalTextFontSize = (self.screenWidth + self.screenHeight) / 28
