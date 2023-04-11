import random as rand
import math
import pygame

from threading import Thread
from collections import deque 
from Mixer import Mixer
from PlayerAnimator import PlayerAnimator

class Player:

    def __init__(self, color, SCREEN_WIDTH, SCREEN_HEIGHT, left, right, gameBackgroundColor, SCREEN, FPS):
        
        self.thickness = 5 #max 20, small optimization problems for more, collision problems for more, default: 5
        self.spawnMargin = 200

        self.SCREEN_WIDTH = SCREEN_WIDTH
        self.SCREEN_HEIGHT = SCREEN_HEIGHT
        self.SCREEN = SCREEN

        self.FPS = FPS

        self.pos_x = rand.randint(1 + self.spawnMargin, self.SCREEN_WIDTH - self.thickness - self.spawnMargin)
        self.pos_y = rand.randint(1 + self.spawnMargin, self.SCREEN_HEIGHT - self.thickness - self.spawnMargin) #todo: make so players cant spawn on each other

        self.firstSquareClear = True
        self.saveFirstRectangle = []

        self.pause = 0

        self.range = 15 + round(math.sqrt(2) * self.thickness)
        self.rangeMax = 200

        self.alpha = rand.randint(1, 4) * 90
        self.alphaChange = 3 #should work for 90, default: 3, max 90 test for others
        self.steerStrength = 1 #this is prob not needed, so can be left at 1

        self.speed = 1.75 #default: 1.75 no max test for speed
        self.color = color
        self.gameBackgroundColor = gameBackgroundColor
        self.previousPosition = []

        self.left = left;
        self.right = right;

        self.isAlive = True 

        self.previousHeadPositionsMaxSize = 0
        self.updatePreviousHeadPositionsMaxSize()

        self.previousHeadPositionsMap = [[0 for x in range(SCREEN_WIDTH)] for y in range(SCREEN_HEIGHT)] 
        self.previousHeadPositions = deque()

        self.playerVolume = 0.5
        self.mixer = Mixer(self.playerVolume)
        self.animator = PlayerAnimator(self)
        

    def updatePreviousHeadPositionsMaxSize(self):

        alpha = self.alphaChange % 90 if self.alphaChange != 90 else 90

        self.previousHeadPositionsMaxSize = self.thickness * math.sqrt(2) * math.cos(math.radians(alpha)) + 1 #how many rectangles to consider as previous in collision

    def calcNewPosition(self):

        newPosition = []

        newPosition.append(self.pos_x + self.speed * math.cos(math.radians(self.alpha)))
        newPosition.append(self.pos_y + self.speed * math.sin(math.radians(self.alpha)))

        return newPosition
    
    def calcNewHeadPosition(self):

        newPosition = []

        newPosition.append(self.pos_x + self.speed * self.steerStrength * math.cos(math.radians(self.alpha)))
        newPosition.append(self.pos_y + self.speed * self.steerStrength * math.sin(math.radians(self.alpha)))

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

            if input[ord(self.left)]: 
                self.alpha -= self.alphaChange

            elif input[ord(self.right)]: 
                self.alpha += self.alphaChange

    def death(self, boardFill, colorBoard):

        self.mixer.playSoundEffect(self.mixer.SoundBoard.death)

        self.animator.animateDeath(boardFill, colorBoard)

    def checkIfPointIsInArea(self, point, squarePoint):

        angle = squarePoint[2]
        angle = angle % 360

        x = point[0]
        y = point[1]

        o = math.degrees(math.atan2(y, x))

        if angle >= o and angle <= (-1) * (180 - o): return False
        else: return True


    def managePreviousHeadPositions(self, newPositionHead):

        self.updatePreviousHeadPositionsMaxSize()

        tempHeadPositions = [[-1 for x in range(self.thickness)] for y in range(self.thickness)] 

        while(len(self.previousHeadPositions) >= self.previousHeadPositionsMaxSize):

            removedPreviousRectangle = self.previousHeadPositions.popleft()

            for i in removedPreviousRectangle:
                for j in i:
                    self.previousHeadPositionsMap[j[0]][j[1]] = 0

        for a in range(0, self.thickness):
                for b in range(0, self.thickness):

                    x = (int)(newPositionHead[0]) + a
                    y = (int)(newPositionHead[1]) + b

                    tempHeadPositions[b][a] = (y, x)
                    self.previousHeadPositionsMap[y][x] = 1

        self.previousHeadPositions.append(tempHeadPositions)


    def movePlayerOnScreen(self, SCREEN, SCREEN_WIDTH, SCREEN_HEIGHT, boardFill, colorBoard):

        if self.isAlive:

            newPosition = self.calcNewPosition()
            newPositionHead = self.calcNewHeadPosition()

            self.updatePosition(newPosition[0], newPosition[1])
            self.updatePause()

            if self.addToPreviousPosition(newPositionHead[0], newPositionHead[1], self.alpha):
          
                for a in range(0, self.thickness):
                    for b in range(0, self.thickness):
                        
                        y = self.previousPosition[1] + b
                        x = self.previousPosition[0] + a

                        pygame.draw.rect(SCREEN, self.gameBackgroundColor, pygame.Rect(x, y, 1, 1))
                        boardFill[(int)(y)][(int)(x)] = 0
                        colorBoard[(int(y))][(int)(x)] = self.gameBackgroundColor


                if self.firstSquareClear == True:
                    self.saveFirstRectangle = [self.previousPosition[0], self.previousPosition[1], self.previousPosition[2]]
              
                self.clearPreviousPosition()
                self.addToPreviousPosition(newPositionHead[0], newPositionHead[1], self.alpha)
                self.firstSquareClear = False

            if len(self.saveFirstRectangle) > 0:

                for a in range(0, self.thickness):
                        for b in range(0, self.thickness):

                            y = self.saveFirstRectangle[1] + b
                            x = self.saveFirstRectangle[0] + a

                            if self.checkIfPointIsInArea([x, y], self.saveFirstRectangle):

                                pygame.draw.rect(SCREEN, self.color, pygame.Rect(x, y, 1, 1))
                                boardFill[(int)(y)][(int)(x)] = 1
                                colorBoard[(int(y))][(int)(x)] = self.color


            if not self.checkIfCreatingPass():    
                self.clearSaveFirstRectangle()

            pygame.draw.rect(SCREEN, self.color, pygame.Rect(newPositionHead[0], newPositionHead[1], self.thickness, self.thickness))

            for a in range(0, self.thickness):
                for b in range(0, self.thickness):

                    y = (int)(newPositionHead[1]) + b
                    x = (int)(newPositionHead[0]) + a

                    if (y >= SCREEN_HEIGHT or y < 0 or x >= SCREEN_WIDTH or x < 0) or (boardFill[y][x] == 1 and not self.previousHeadPositionsMap[y][x]):

                        self.isAlive = False
                        Thread(target = self.death, args = (boardFill, colorBoard)).start()
                        return
            
            #this has to be below death check
            for a in range(0, self.thickness):
                for b in range(0, self.thickness):
                    boardFill[(int)(newPositionHead[1]) + b][(int)(newPositionHead[0]) + a] = 1
                    colorBoard[(int)(newPositionHead[1]) + b][(int)(newPositionHead[0]) + a] = self.color

            self.managePreviousHeadPositions(newPositionHead)
       
        
        
