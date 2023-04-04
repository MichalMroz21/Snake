import random as rand
import math
    
class Player:

    def __init__(self):

        self.thickness = 5
        self.headThickness = (5 * self.thickness)/6 
        self.pos_x = rand.randint(1, 1280 - self.thickness)
        self.pos_y = rand.randint(1, 720 - self.thickness)
        self.pause = 0
        self.range = 20
        self.rangeMax = 180
        self.alpha = 90
        self.speed = 1
        self.color = "Red"
        self.headColor = "Green"
        self.previousPositions = []


    def calcNewPosition(self):

        newPosition = []

        newPosition.append(self.pos_x + self.speed * math.cos(math.radians(self.alpha)))
        newPosition.append(self.pos_y + self.speed * math.sin(math.radians(self.alpha)))

        return newPosition

    def calcNewHeadPosition(self):

        newPosition = []

        newPosition.append(self.pos_x + self.thickness * self.speed * math.cos(math.radians(self.alpha)))
        newPosition.append(self.pos_y + self.thickness * self.speed * math.sin(math.radians(self.alpha)))

        return newPosition

    def updatePosition(self, x, y):

        self.pos_x = x
        self.pos_y = y


    def updatePause(self):
        self.pause += 1
        if self.pause >= self.rangeMax: self.pause = 0

    def checkIfInRange(self):
        return self.pause not in range(self.rangeMax - self.range, self.rangeMax)

    def addToPreviousPositions(self, pos_x, pos_y):
        self.previousPositions.append([pos_x, pos_y])

        return len(self.previousPositions) == self.thickness

    def clearPreviousPositions(self):

        self.previousPositions.clear()
        return


        
        
