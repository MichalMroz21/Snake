import pygame

class ColorPicker:
    def __init__(self, x, y, w, h):

        self.rect = pygame.Rect(x, y, w, h)

        self.rad = h//2
        self.pwidth = w-self.rad*2

        self.p = 0
        self.h = h
        self.x = x
        self.y = y

    def get_color(self):

        color = pygame.Color(0)
        color.hsla = (int(self.p * self.pwidth), 100, 50, 100)
        return color

    def update(self, mouse_position, mouse_buttons):

        if mouse_buttons[0] and self.rect.collidepoint(mouse_position):
            self.p = (mouse_position[0] - self.rect.left - self.rad) / self.pwidth
            self.p = (max(0, min(self.p, 1)))

    def draw(self, screen):

        center = self.rect.left + self.rad + self.p * self.pwidth, self.rect.centery

        for i in range(self.pwidth):

            color = pygame.Color(0)
            color.hsla = (int (360*i/self.pwidth), 100, 50, 100)
            pygame.draw.rect(screen, color, (self.x + i+self.rad, self.y + self.h//3, 1, self.h-2*self.h//3))
        
        pygame.draw.circle(screen, self.get_color(), center, self.rect.height // 2)
