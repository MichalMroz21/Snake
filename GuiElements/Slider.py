import pygame


class Slider:

    def __init__(self, x, y, slider_width, slider_height, color, handle_color, step,
                 min_val, max_val, radius, current_val):
        self.xTop = x
        self.yTop = y
        self.sliderWidth = slider_width
        self.sliderHeight = slider_height
        self.color = color
        self.handleColor = handle_color
        self.step = step
        self.min = min_val
        self.max = max_val
        self.radius = radius

        self.currentVal = current_val

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, pygame.Rect(self.xTop, self.yTop, self.sliderWidth, self.sliderHeight))
        pygame.draw.circle(screen, self.handleColor, (self.xTop + self.sliderWidth * (self.currentVal/self.max),
                                                      self.yTop + self.sliderHeight / 2), self.radius)

    def update(self, mouse_pos):

        x = mouse_pos[0]
        y = mouse_pos[1]

        if self.xTop <= x <= self.xTop + self.sliderWidth and self.yTop - (
                self.radius - self.sliderHeight / 2) <= y <= self.yTop + (
                self.radius - self.sliderHeight / 2) + self.sliderHeight:

            percentage_value = float(x - self.xTop)/self.sliderWidth
            self.currentVal = (self.max - self.min) * percentage_value + self.min

    def get_value(self):
        return self.currentVal
