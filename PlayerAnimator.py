import pygame
import time
import random as rand
import math
from threading import Thread

class PlayerAnimator():

    def __init__(self, player, animationSpeed):
        
        self.player = player
        self.globalAnimationSpeed = animationSpeed


    def animateDeath(self, boardFill):
        
        radius = 1
        previousRadius = 0
        circle_center = (self.player.pos_x, self.player.pos_y)
        maxRadius = rand.randint(20, 30)

        particlesAmount = rand.randint(5, 10)
        particlesAlphas = []

        for i in range(0, particlesAmount):
            particlesAlphas.append(rand.randint(0, 360))

        clock = pygame.time.Clock() 

        while radius <= maxRadius:

            for i in particlesAlphas:

                if previousRadius != 0:

                    xPrev = previousRadius * math.cos(math.radians(i)) + circle_center[0]
                    yPrev = previousRadius * math.sin(math.radians(i)) + circle_center[1]

                    #if(boardFill[(int)(yPrev)][(int)(xPrev)] != 1):
                    pygame.draw.rect(self.player.SCREEN, self.player.gameBackgroundColor, pygame.Rect(xPrev, yPrev, self.player.thickness, self.player.thickness))


                x = radius * math.cos(math.radians(i)) + circle_center[0]
                y = radius * math.sin(math.radians(i)) + circle_center[1]

                pygame.draw.rect(self.player.SCREEN, self.player.color, pygame.Rect(x, y, self.player.thickness, self.player.thickness))


            previousRadius = radius
            radius += self.player.speed/10.0

            pygame.display.update()
            clock.tick(self.player.FPS)


        for i in particlesAlphas:

            if previousRadius != 0:

                xPrev = previousRadius * math.cos(math.radians(i)) + circle_center[0]
                yPrev = previousRadius * math.sin(math.radians(i)) + circle_center[1]

                #if(boardFill[(int)(yPrev)][(int)(xPrev)] != 1):
                pygame.draw.rect(self.player.SCREEN, self.player.gameBackgroundColor, pygame.Rect(xPrev, yPrev, self.player.thickness, self.player.thickness))






