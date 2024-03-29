class Button:

    def __init__(self, image, pos, text_input, font, base_color, hovering_color):

        self.image = image
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.font = font
        self.base_color, self.hovering_color = base_color, hovering_color
        self.text_input = text_input
        self.text = self.font.render(self.text_input, True, self.base_color)

        self.imageIsText = False

        if self.image is None:
            self.image = self.text
            self.imageIsText = True

        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

    def update(self, screen):

        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

        if self.image is not None:
            screen.blit(self.image, self.rect)

        screen.blit(self.text, self.text_rect)

    def check_for_input(self, position):

        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top,
                                                                                          self.rect.bottom):
            return True

        return False

    def change_text(self, text):
        self.text_input = text
        self.text = self.font.render(self.text_input, True, self.base_color)

        if self.imageIsText:
            self.image = self.font.render(self.text_input, True, self.base_color)

    def change_color(self, position):

        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top,
                                                                                          self.rect.bottom):
            self.text = self.font.render(self.text_input, True, self.hovering_color)
            if self.imageIsText:
                self.image = self.font.render(self.text_input, True, self.hovering_color)

        else:
            self.text = self.font.render(self.text_input, True, self.base_color)
            if self.imageIsText:
                self.image = self.font.render(self.text_input, True, self.base_color)

