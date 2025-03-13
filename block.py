import pygame


class Block(pygame.sprite.Sprite):
    def __init__(self, scene, coords: tuple, color: tuple):
        super().__init__()
        self.scene = scene
        self.color = color
        self.image = pygame.Surface(
            (self.scene.tile_size, self.scene.tile_size)
        )
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.topleft = coords
        self.scene.all_sprites.add(self)
        self.scene.all_blocks.add(self)
        self.bonus = 1

    def destroy(self):
        self.scene.ball.score += self.bonus
        self.kill()
        if not self.scene.all_blocks:
            self.scene.win()
