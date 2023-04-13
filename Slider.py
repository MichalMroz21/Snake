import pygame

class Slider():

    def __init__(self, x, y, sliderWidth, sliderHeight, color, handleColor, step, min, max, radius, currentVal):

        self.xTop = x
        self.yTop = y
        self.sliderWidth = sliderWidth
        self.sliderHeight = sliderHeight
        self.color = color
        self.handleColor = handleColor
        self.step = step
        self.min = min
        self.max = max
        self.radius = radius

        self.currentVal = currentVal

    def draw(self, screen):

        pygame.draw.rect(screen, self.color, pygame.Rect(self.xTop, self.yTop, self.sliderWidth, self.sliderHeight))
        pygame.draw.circle(screen, self.handleColor, (self.xTop + self.sliderWidth * (self.currentVal/self.max), self.yTop + self.sliderHeight / 2), self.radius)

    def update(self, mousePos):

        x = mousePos[0]
        y = mousePos[1]

        if x >= self.xTop and x <= self.xTop + self.sliderWidth and y >= self.yTop - (self.radius - self.sliderHeight / 2) and y <= self.yTop + (self.radius - self.sliderHeight / 2) + self.sliderHeight:
            percentageValue = (float)(x - self.xTop)/self.sliderWidth
            self.currentVal = (self.max - self.min) * percentageValue + self.min

    def getValue(self):
        return self.currentVal
