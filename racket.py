from abc import ABC, abstractmethod
import config
import pygame


class Racket(ABC, pygame.sprite.Sprite):
    @abstractmethod
    def __init__(
            self,
            center: tuple,
            scene,
    ):
        super().__init__()
        self.scene = scene
        self.center = center
        self.color = config.WHITE
        self.speed = 10
        self.image = pygame.Surface(
            (
                self.scene.tile_size,
                int(self.scene.tile_size * 0.3),
            )
        )
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.goto_start()
        self.direction = 0
        self.scene.all_sprites.add(self)
        self.scene.all_rackets.add(self)

    def goto_start(self):
        self.rect.center = self.center

    def move(self):
        '''двигает ракетку'''
        pass

    def collide_borders(self):
        if self.rect.right > self.scene.game.window_width:
            self.rect.right = self.scene.game.window_width

        elif self.rect.left < 0:
            self.rect.left = 0

    def update(self):
        self.move()
        self.collide_borders()


class RacketAuto(Racket):
    def __init__(self, center, scene, delay):
        super().__init__(center, scene)
        self.delay = delay  # ms
        self.last_move = pygame.time.get_ticks()  # ms

    def move(self):
        if pygame.time.get_ticks() - self.last_move >= self.delay:
            if self.scene.ball.rect.centery < self.rect.centery:
                self.rect.centery -= self.speed
            elif self.scene.ball.rect.centery > self.rect.centery:
                self.rect.centery += self.speed
            self.last_move = pygame.time.get_ticks()


class RacketManual(Racket):
    def __init__(self, center, key_left, key_right, scene):
        super().__init__(center, scene)
        self.key_left = key_left
        self.key_right = key_right

    def move(self):
        if not self.scene.keys_pressed:
            self.direction = 0
            return

        if self.scene.keys_pressed[self.key_right]:
            self.rect.x += self.speed
            self.direction = 1
        elif self.scene.keys_pressed[self.key_left]:
            self.rect.x -= self.speed
            self.direction = -1
