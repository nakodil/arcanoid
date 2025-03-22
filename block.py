import pygame
import random
import config
from drop import Drop


class Block(pygame.sprite.Sprite):
    def __init__(self, scene, coords: tuple, color: tuple):
        super().__init__()
        self.scene = scene
        self.coords = coords
        self.color = color
        self.image = pygame.Surface(
            (self.scene.tile_width, self.scene.tile_height)
        )
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.topleft = self.coords
        self.scene.all_sprites.add(self)
        self.scene.all_blocks.add(self)
        self.bonus = 1

        pygame.draw.rect(
            self.image,
            config.WHITE,
            self.image.get_rect(),
            1
        )

    def destroy(self):
        self.scene.ball.score += self.bonus
        self.kill()
        if not self.scene.all_blocks:
            self.scene.win()
            return
        if random.randint(1, 10) == 1:  # TODO: fix chance
            Drop(self.scene, self.rect.center, config.DROP_COLOR)
