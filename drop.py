import pygame


class Drop(pygame.sprite.Sprite):
    def __init__(self, scene, coords: tuple, color: tuple):
        super().__init__()
        self.scene = scene
        self.color = color
        self.image = pygame.Surface(
            (self.scene.tile_width, self.scene.tile_height)
        )
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.topleft = coords
        self.scene.all_sprites.add(self)
        self.scene.all_drops.add(self)
        self.bonus = 10
        self.speed = 5

    def move(self):
        self.rect.y += self.speed
        if self.rect.bottom > self.scene.game.window_height:
            self.kill()
            print('drop kill')

    def update(self):
        self.move()
        self.collide_rackets()

    def collide_rackets(self):
        rackets_hit = pygame.sprite.spritecollide(
            self, self.scene.all_rackets, False
        )
        if rackets_hit:
            self.kill()
            self.scene.ball.score += self.bonus
