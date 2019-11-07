import pygame

GREY = (200, 200, 200)
BLACK = (0,   0,   0)
GREEN = (76, 153,   0)

class Button:
    def __init__(self, x, y, text, canvas, fnt, speed):
        self.x = x
        self.y = y
        self.size = 60
        self.text = text
        self.canvas = canvas
        self.active = False
        self.font = pygame.font.SysFont(fnt, 15)
        self.text_x = self.font.size(text)[0]/2
        self.text_y = self.font.size(text)[1]/2
        self.rect = None
        self.speed = speed

    def show(self):
        colour = GREEN if self.active else GREY

        button = pygame.Rect(self.x, self.y, self.size, self.size)
        pygame.draw.rect(self.canvas, colour, button)

        label = self.font.render(self.text, 24, BLACK)
        self.canvas.blit(label, (self.x + self.size/2 - self.text_x, self.y + self.size/2 - self.text_y))

        self.rect = button
        return button

