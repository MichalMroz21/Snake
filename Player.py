import random as rand
import math
import pygame
    
class Player:

    def __init__(self):

        self.thickness = 5

        self.pos_x = rand.randint(1, 1280 - self.thickness)
        self.pos_y = rand.randint(1, 720 - self.thickness)

        self.pause = 0

        self.range = 20
        self.rangeMax = 180

        self.alpha = 90
        self.alphaChange = 3
        self.alphaDistancedLeft = False
        self.alphaDistancedRight = False
        self.alphaHead = self.alpha

        self.speed = 2
        self.color = "Red"
        self.headColor = "Red"
        self.previousPositions = []


    def calcNewPosition(self):

        newPosition = []

        newPosition.append(self.pos_x + self.speed * math.cos(math.radians(self.alpha)))
        newPosition.append(self.pos_y + self.speed * math.sin(math.radians(self.alpha)))

        return newPosition
    
    def calcNewHeadPosition(self):

        newPosition = []

        newPosition.append(self.pos_x + self.thickness * self.speed * math.cos(math.radians(self.alphaHead)))
        newPosition.append(self.pos_y + self.thickness * self.speed * math.sin(math.radians(self.alphaHead)))

        return newPosition

    def rotatePointByDegrees(self, pos_x, pos_y, alpha):
        ox = pos_x + self.thickness/2
        oy = pos_y + self.thickness/2

        ret_points = []
        ret_points.append(math.cos(math.radians(alpha)) * (pos_x - ox) - math.sin(math.radians(alpha)) * (pos_y - oy) + ox)
        ret_points.append(math.sin(math.radians(alpha)) * (pos_x - ox) + math.cos(math.radians(alpha)) * (pos_y - oy) + oy)

        return ret_points


    def updatePosition(self, x, y):

        self.pos_x = x
        self.pos_y = y


    def updatePause(self):
        self.pause += 1
        if self.pause >= self.rangeMax: self.pause = 0

    def checkIfInRange(self):
        if self.pause not in range(self.rangeMax - self.range, self.rangeMax): 
            self.clearPreviousPositions()
            return True
        else: 
            return False

    def addToPreviousPositions(self, pos_x, pos_y, alpha):
        if self.checkIfInRange(): return False

        if len(self.previousPositions) == 1: return True

        self.previousPositions.append([pos_x, pos_y, alpha])
        return False


    def clearPreviousPositions(self):

        self.previousPositions.clear()
        return

    def useInputForPlayer(self, input):

        if input[ord('a')]: 

            self.alpha -= self.alphaChange
            self.alphaHead -= self.alphaChange

            if self.alphaDistancedLeft == False:
                self.alphaHead -= self.alphaChange * 2
                self.alphaDistancedLeft = True

        elif input[ord('d')]: 

            self.alpha += self.alphaChange
            self.alphaHead += self.alphaChange

            if self.alphaDistancedRight == False:
                self.alphaHead += self.alphaChange * 2 
                self.alphaDistancedRight = True
        else:
            self.alphaHead = self.alpha
            self.alphaDistancedRight = False
            self.alphaDistancedLeft = False

        return

    def movePlayerOnScreen(self, SCREEN, gameBackgroundColor):

        newPosition = self.calcNewPosition()
        newPositionHead = self.calcNewHeadPosition()

        self.updatePosition(newPosition[0], newPosition[1])
        self.updatePause()

        if self.addToPreviousPositions(newPositionHead[0], newPositionHead[1], self.alpha):
            for i in self.previousPositions:
                    
                for a in range(0, self.thickness):
                    for b in range(0, self.thickness):
                        pygame.draw.rect(SCREEN, gameBackgroundColor, pygame.Rect(i[0] + a, i[1] + b, 1, 1))
                
            self.clearPreviousPositions()
            self.addToPreviousPositions(newPositionHead[0], newPositionHead[1], self.alpha)

        pygame.draw.rect(SCREEN, self.headColor, pygame.Rect(newPositionHead[0], newPositionHead[1], self.thickness, self.thickness))

        if self.checkIfInRange(): pygame.draw.rect(SCREEN, self.color, pygame.Rect(newPosition[0], newPosition[1], self.thickness, self.thickness))
        
        
