import pygame
from constants import SIZE_OF_PIN, SPRITE_CONFIG, COLOR


class Square(pygame.sprite.Sprite):
    def __init__(self, x, y, _type, size=SIZE_OF_PIN):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(SPRITE_CONFIG[_type][0].convert(), SPRITE_CONFIG[_type][1])
        self.rect = self.image.get_rect()
        self.image.set_colorkey(COLOR.WHITE.value)
        self.rect.centerx = x
        self.rect.centery = y

    def setPosition(self, coordinates):
        self.rect.centerx += coordinates[0]
        self.rect.centery += coordinates[1]
