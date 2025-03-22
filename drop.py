import pygame


class Drop(pygame.sprite.Sprite):
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
        self.scene.all_drops.add(self)
        self.speed = 5

    def move(self):
        self.rect.y += self.speed
        if self.rect.bottom > self.scene.game.window_height:
            self.kill()
            print('drop kill')

    def update(self):
        self.move()
