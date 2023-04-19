import pygame


class TextBox():
    def __init__(self, x, y, width, height, color, colorPicked, font, initialText, id):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.colorPicked = colorPicked
        self.text = initialText
        self.font = font

        self.text_id = id

        self.TEXT_SURFACE = self.font.render(self.text.upper(), True, (255, 255, 255))
        self.TEXT_WIDTH, self.TEXT_HEIGHT = self.font.size(self.text.upper())

        self.TEXT_RECT = pygame.Rect(self.x, self.y, self.width, self.height)

    def update(self):

        self.TEXT_SURFACE = self.font.render(self.text.upper(), True, (255, 255, 255))
        self.TEXT_WIDTH, self.TEXT_HEIGHT = self.font.size(self.text.upper())

    def drawNotPickedRectangle(self, screen):
        pygame.draw.rect(screen, self.color, self.TEXT_RECT, 2)

    def drawPickedRectangle(self, screen):
        pygame.draw.rect(screen, self.colorPicked, self.TEXT_RECT, 2)

    def blitText(self, screen):
        screen.blit(self.TEXT_SURFACE, (self.TEXT_RECT.x + self.width / 2 - self.TEXT_WIDTH / 2, self.TEXT_RECT.y + self.height / 2 - self.font.get_height() / 2))

    def checkIfClicked(self, mousePosX, mousePosY):
        if mousePosX >= self.TEXT_RECT.x and mousePosX <= self.TEXT_RECT.x + self.TEXT_RECT.width and mousePosY >= self.TEXT_RECT.y and mousePosY <= self.TEXT_RECT.y + self.TEXT_RECT.height:
            return self.text_id

        else: return None

    def addToText(self, char):
        self.text += char

    def popBackText(self):
        self.text = self.text[:-1]

    def setText(self, text):
        self.text = text