import random as rand
import math
import pygame
    
class Player:

    def __init__(self, color, SCREEN_WIDTH, SCREEN_HEIGHT):

        self.thickness = 5
        self.spawnMargin = 200

        self.pos_x = rand.randint(1 + self.spawnMargin, SCREEN_WIDTH - self.thickness - self.spawnMargin)
        self.pos_y = rand.randint(1 + self.spawnMargin, SCREEN_HEIGHT - self.thickness - self.spawnMargin)

        self.firstSquareClear = True
        self.saveFirstRectangle = []

        self.pause = 0

        self.range = 20
        self.rangeMax = 200

        self.alpha = rand.randint(1, 4) * 90
        self.alphaChange = 4
        self.steerStrength = 1

        self.speed = 3
        self.color = color
        self.previousPosition = []

        self.isAlive = True 
        self.previousHeadPositions = [[(-1, -1) for x in range(self.thickness)] for y in range(self.thickness)]


    def calcNewPosition(self):

        newPosition = []

        newPosition.append(self.pos_x + self.speed * math.cos(math.radians(self.alpha)))
        newPosition.append(self.pos_y + self.speed * math.sin(math.radians(self.alpha)))

        return newPosition
    
    def calcNewHeadPosition(self):

        newPosition = []

        newPosition.append(self.pos_x +  self.speed * self.steerStrength * math.cos(math.radians(self.alpha)))
        newPosition.append(self.pos_y +  self.speed * self.steerStrength * math.sin(math.radians(self.alpha)))

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

    def clearSaveFirstRectangle(self):
        self.saveFirstRectangle.clear()

    def handleInputForPlayer(self, input):

        if self.isAlive:

            if input[ord('a')]: 
                self.alpha -= self.alphaChange

            elif input[ord('d')]: 
                self.alpha += self.alphaChange
       

    def checkIfPointIsInArea(self, point, squarePoint):

        angle = squarePoint[2]
        angle = angle % 360

        x = point[0]
        y = point[1]

        o = math.degrees(math.atan2(y, x))

        if angle >= o and angle <= (-1) * (180 - o): return False
        else: return True


    def movePlayerOnScreen(self, SCREEN, gameBackgroundColor, boardFill):

        if self.isAlive:

            newPosition = self.calcNewPosition()
            newPositionHead = self.calcNewHeadPosition()

            self.updatePosition(newPosition[0], newPosition[1])
            self.updatePause()

            if self.addToPreviousPosition(newPositionHead[0], newPositionHead[1], self.alpha):
          
                for a in range(0, self.thickness):
                    for b in range(0, self.thickness):                           
                        pygame.draw.rect(SCREEN, gameBackgroundColor, pygame.Rect(self.previousPosition[0] + a,  self.previousPosition[1] + b, 1, 1))
                        boardFill[(int)(self.previousPosition[1]) + b][(int)(self.previousPosition[0]) + a] = 0


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
                                boardFill[(int)(self.saveFirstRectangle[1]) + b][(int)(self.saveFirstRectangle[0]) + a] = 1

            if not self.checkIfCreatingPass():    
                self.clearSaveFirstRectangle()

            pygame.draw.rect(SCREEN, self.color, pygame.Rect(newPositionHead[0], newPositionHead[1], self.thickness, self.thickness))
            for a in range(0, self.thickness):
                for b in range(0, self.thickness):
                    if boardFill[(int)(newPositionHead[1]) + b][(int)(newPositionHead[0]) + a] == 1 and not any( ((int)(newPositionHead[1]) + b, (int)(newPositionHead[0] + a)) in sublist for sublist in self.previousHeadPositions):
                        self.isAlive = False
                        print("death")
                        return
                   
                   
            for a in range(0, self.thickness):
                for b in range(0, self.thickness):
                    boardFill[(int)(newPositionHead[1]) + b][(int)(newPositionHead[0]) + a] = 1

            for a in range(0, self.thickness):
                for b in range(0, self.thickness):
                    self.previousHeadPositions[b][a] = ((int)(newPositionHead[1]) + b, (int)(newPositionHead[0]) + a)
       
        
        
