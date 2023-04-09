import pygame
import enum
import time 

class Animator(Game): #change for Round when round class added

    def __init__(self, SCREEN, SCREEN_WIDTH, SCREEN_HEIGHT):
        pass

    def AnimateDeath(self, x, y, spread, thickness, color):

        clock = pygame.time.Clock()
        radius = 1

        while radius <= spread:

         #   self.pos_x + self.speed * self.steerStrength * math.cos(math.radians(self.alpha)))
         #   (self.pos_y + self.speed * self.steerStrength * math.sin(math.radians(self.alpha))

         #   pygame.draw.rect(self.SCREEN, color, pygame.Rect(drawX, drawY, thickness, thickness))

         #   radius += 1

        
