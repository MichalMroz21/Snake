import pygame


class TextBox:
    def __init__(self, x, y, width, height, color, color_picked, font, initial_text, text_id):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.colorPicked = color_picked
        self.text = str(initial_text)
        self.font = font

        self.text_id = text_id

        self.TEXT_SURFACE = self.font.render(self.text.upper(), True, (255, 255, 255))
        self.TEXT_WIDTH, self.TEXT_HEIGHT = self.font.size(self.text.upper())

        self.TEXT_RECT = pygame.Rect(self.x, self.y, self.width, self.height)

    def update(self):

        self.TEXT_SURFACE = self.font.render(self.text.upper(), True, (255, 255, 255))
        self.TEXT_WIDTH, self.TEXT_HEIGHT = self.font.size(self.text.upper())

    def draw_not_picked_rectangle(self, screen):
        pygame.draw.rect(screen, self.color, self.TEXT_RECT, 2)

    def draw_picked_rectangle(self, screen):
        pygame.draw.rect(screen, self.colorPicked, self.TEXT_RECT, 2)

    def blit_text(self, screen):
        screen.blit(self.TEXT_SURFACE, (self.TEXT_RECT.x + self.width / 2 - self.TEXT_WIDTH / 2, self.TEXT_RECT.y + self.height / 2 - self.font.get_height() / 2))

    def check_if_clicked(self, mouse_pos_x, mouse_pos_y):
        if (self.TEXT_RECT.x <= mouse_pos_x <= self.TEXT_RECT.x + self.TEXT_RECT.width and
                self.TEXT_RECT.y <= mouse_pos_y <= self.TEXT_RECT.y + self.TEXT_RECT.height):

            return self.text_id

        else: return None

    def add_to_text(self, char):
        self.text += char

    def pop_back_text(self):
        self.text = self.text[:-1]

    def set_text(self, text):
        self.text = str(text)