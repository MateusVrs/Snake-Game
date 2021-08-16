import pygame


class Body():
    def __init__(self, display, x, y, width, height, border=25):
        self.x, self.y = x, y
        self.w, self.h = width, height
        self.mainDisplay = display
        self.border = border

    def createBody(self):
        pygame.draw.rect(self.mainDisplay, '#32C49F',
                         (self.x, self.y, self.w, self.h),
                         border_radius=20, width=self.border)
