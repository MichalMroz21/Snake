import pygame

class Font:    
    
    def __init__(self, screenWidth, screenHeight):

        self.screenWidth = screenWidth
        self.screenHeight = screenHeight

        self.titleFontSize = (self.screenWidth + self.screenHeight) / 20
        self.normalTextFontSize = (self.screenWidth + self.screenHeight) / 28

        self.font = "assets/font/Lato-Regular.ttf"


    def get_title_font(self, smaller = 1, higher = 1, bold = False, italic = False): 
        return pygame.font.Font(self.font, round(self.titleFontSize/smaller * higher), bold=bold, italic=italic)


    def get_normal_font(self, smaller = 1, higher = 1, bold = False, italic = False):
        return pygame.font.Font(self.font, round(self.normalTextFontSize/smaller * higher), bold=bold, italic=italic)


    def updateFontSizes(self, screenWidth, screenHeight):

        self.screenWidth = screenWidth
        self.screenHeight = screenHeight

        self.titleFontSize = (self.screenWidth + self.screenHeight) / 20
        self.normalTextFontSize = (self.screenWidth + self.screenHeight) / 28