import pygame
import time
import random as rand
import math
import sys 
from threading import Thread

class PlayerAnimator():

    def __init__(self, player):
        
        self.player = player


    def animateDeath(self, boardFill, colorBoard, particleAmountMin, particleAmountMax):
        
        circle_center = (self.player.pos_x, self.player.pos_y)

        screenWidth = self.player.screenWidth
        screenHeight = self.player.screenHeight
        screen = self.player.screen

        playerColor = self.player.color
        gameBackgroundColor = self.player.gameBackgroundColor
        thickness = self.player.thickness

        playerSpeed = self.player.speed
        FPS = self.player.FPS

        MAX_TRANSPARENCY = 255

        particlesAmount = rand.randint(particleAmountMin, particleAmountMax)
        particlesAlphas = []
        particlesSizes = []
        particlesTransparency = []
        particlesMaxRadiuses = []
        particlesVelocities = []

        baseRadius = (screenWidth * screenHeight)/2 / (thickness * 1.5) / (1280 * 720 / (1280 + 720))
        previousAlpha = 0

        for i in range(0, particlesAmount):

            particlesAlphas.append(rand.randint(0 + round(previousAlpha/2), 360))
            particlesSizes.append(rand.randint(round(thickness / 2), round(thickness / 1.5)))

            particlesTransparency.append(rand.uniform(MAX_TRANSPARENCY / 2, MAX_TRANSPARENCY))
            particlesMaxRadiuses.append(rand.uniform(baseRadius, baseRadius * 1.75))
            particlesVelocities.append(rand.uniform(playerSpeed/2, playerSpeed * 1.5))

            previousAlpha = particlesAlphas[-1]

        maxRadius = max(particlesMaxRadiuses)

        previousRadiuses = [0 for radius in range(0, particlesAmount)]
        particleRadiuses = [1 for particle in range(0, particlesAmount)]
        finalClears = [False for particle in range(0, particlesAmount)]

        clock = pygame.time.Clock() 

        while False in finalClears:
        
            i = 0
            for alpha, size, transparency in zip(particlesAlphas, particlesSizes, particlesTransparency):

                if previousRadiuses[i] != 0 and finalClears[i] == False:

                    xPrev = previousRadiuses[i] * math.cos(math.radians(alpha)) + circle_center[0]
                    yPrev = previousRadiuses[i] * math.sin(math.radians(alpha)) + circle_center[1]

                    for a in range(0, size):
                        for b in range(0, size):
                        
                            y = round(yPrev) + b
                            x = round(xPrev) + a

                            if(x >= screenWidth or x < 0 or y < 0 or y >= screenHeight): continue

                            if(boardFill[y][x] != 1):

                                pygame.draw.rect(screen, gameBackgroundColor, pygame.Rect(x, y, 1, 1))

                            else:

                                pygame.draw.rect(screen, colorBoard[y][x], pygame.Rect(x, y, 1, 1))


                if particleRadiuses[i] >= particlesMaxRadiuses[i]:
                    finalClears[i] = True
                    previousRadiuses[i] = particleRadiuses[i]
                    i += 1
                    continue


                xTop = particleRadiuses[i] * math.cos(math.radians(alpha)) + circle_center[0]
                yTop = particleRadiuses[i] * math.sin(math.radians(alpha)) + circle_center[1]

                for a in range(0, size):
                        for b in range(0, size):
                        
                            y = round(yTop) + b
                            x = round(xTop) + a

                            if(x >= screenWidth or x < 0 or y < 0 or y >= screenHeight): continue

                            s = pygame.Surface((1, 1))
                            s.set_alpha(transparency)
                            s.fill(playerColor)

                            screen.blit(s, (x, y))            


                previousRadiuses[i] = particleRadiuses[i]
                particleRadiuses[i] += particlesVelocities[i]
                i += 1

                pygame.display.update()

            clock.tick(FPS)




