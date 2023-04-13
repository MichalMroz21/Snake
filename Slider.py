import pygame_widgets as pw
import pygame

class Slider():

    def __init__(self, x, y, sliderwidth, sliderheight, color, handleColor):

        self.slider = pw.Slider(self.win, x, y, sliderwidth, sliderheight, min=0, max=99, step=1, colour=color, handleColour=handleColor)

    def update(self, screen):

        screen.blit(self.slider, self.slider)