import random as rand
import math
    
class Player:

    def __init__(self):

        self.thickness = 5
        self.headThickness = 5

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

        newPosition.append(self.pos_x + self.headThickness * self.speed * math.cos(math.radians(self.alphaHead)))
        newPosition.append(self.pos_y + self.headThickness * self.speed * math.sin(math.radians(self.alphaHead)))

        return newPosition

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

    def addToPreviousPositions(self, pos_x, pos_y):
        if self.checkIfInRange(): return False

        if len(self.previousPositions) == 1: return True

        self.previousPositions.append([pos_x, pos_y])
        return False


    def clearPreviousPositions(self):

        self.previousPositions.clear()
        return


        
        
