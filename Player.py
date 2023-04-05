import random as rand
import math
import pygame
    
class Player:

    def __init__(self):

        self.thickness = 5
        self.spawnMargin = 200

        self.pos_x = rand.randint(1 + self.spawnMargin, 1280 - self.thickness - self.spawnMargin)
        self.pos_y = rand.randint(1 + self.spawnMargin, 720 - self.thickness - self.spawnMargin)

        self.firstSquareClear = True
        self.saveFirstRectangle = []

        self.pause = 0

        self.range = 20
        self.rangeMax = 200

        self.alpha = rand.randint(1, 4) * 90
        self.alphaChange = 3
        self.steerStrength = 5

        self.speed = 2
        self.color = "Red"
        self.previousPosition = []

        self.isAlive = True 


    def calcNewPosition(self):

        newPosition = []

        newPosition.append(self.pos_x + self.speed * math.cos(math.radians(self.alpha)))
        newPosition.append(self.pos_y + self.speed * math.sin(math.radians(self.alpha)))

        return newPosition
    
    def calcNewHeadPosition(self):

        newPosition = []

        newPosition.append(self.pos_x +  self.speed  * self.steerStrength * math.cos(math.radians(self.alpha)))
        newPosition.append(self.pos_y +  self.speed  * self.steerStrength * math.sin(math.radians(self.alpha)))

        return newPosition

    def updatePosition(self, x, y):

        self.pos_x = x
        self.pos_y = y

    def updatePause(self):
        self.pause += 1
        if self.pause >= self.rangeMax: self.pause = 0

    def checkIfCreatingPass(self):
        return self.pause in range(self.rangeMax - self.range, self.rangeMax)

    def addToPreviousPosition(self, pos_x, pos_y, alpha):

        if not self.checkIfCreatingPass():
            self.firstSquareClear = True
            self.clearPreviousPosition()
            return False

        if len(self.previousPosition) > 0: return True

        self.previousPosition = [pos_x, pos_y, alpha]
        return False


    def clearPreviousPosition(self):

        self.previousPosition.clear()
        return

    def handleInputForPlayer(self, input):

        if input[ord('a')]: 
            self.alpha -= self.alphaChange

        elif input[ord('d')]: 
            self.alpha += self.alphaChange
       
        return

    def checkIfPointIsInArea(self, point, squarePoint):

        angle = squarePoint[2]
        angle = angle % 360

        x = point[0]
        y = point[1]

        o = math.degrees(math.atan2(y, x))

        if angle >= o and angle <= (-1) * (180 - o): return False
        else: return True


    def movePlayerOnScreen(self, SCREEN, gameBackgroundColor):

        newPosition = self.calcNewPosition()
        newPositionHead = self.calcNewHeadPosition()

        self.updatePosition(newPosition[0], newPosition[1])
        self.updatePause()

        if self.addToPreviousPosition(newPositionHead[0], newPositionHead[1], self.alpha):
          
            for a in range(0, self.thickness):
                for b in range(0, self.thickness):                           
                    pygame.draw.rect(SCREEN, gameBackgroundColor, pygame.Rect(self.previousPosition[0] + a,  self.previousPosition[1] + b, 1, 1))

            if self.firstSquareClear == True:
                self.saveFirstRectangle = [self.previousPosition[0], self.previousPosition[1], self.previousPosition[2]]
              
            self.clearPreviousPosition()
            self.addToPreviousPosition(newPositionHead[0], newPositionHead[1], self.alpha)
            self.firstSquareClear = False

        if len(self.saveFirstRectangle) > 0:

            for a in range(0, self.thickness):
                    for b in range(0, self.thickness):

                        if self.checkIfPointIsInArea([self.saveFirstRectangle[0] + a, self.saveFirstRectangle[1] + b], self.saveFirstRectangle):
                            pygame.draw.rect(SCREEN, self.color, pygame.Rect(self.saveFirstRectangle[0] + a,  self.saveFirstRectangle[1] + b, 1, 1))

        if not self.checkIfCreatingPass():    
            self.saveFirstRectangle.clear()

        pygame.draw.rect(SCREEN, self.color, pygame.Rect(newPositionHead[0], newPositionHead[1], self.thickness, self.thickness))

       
        
        
