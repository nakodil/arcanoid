from abc import ABC, abstractmethod
import pygame


class Racket(ABC, pygame.sprite.Sprite):
    @abstractmethod
    def __init__(
            self,
            scene,
            center: tuple,
            color: tuple,
    ):
        super().__init__()
        self.scene = scene
        self.center = center
        self.color = color
        self.speed = 10
        self.image = pygame.Surface(
            (
                self.scene.tile_width,
                self.scene.tile_height // 2,
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


class RacketManual(Racket):
    def __init__(self, scene, center, color, key_left, key_right):
        super().__init__(scene, center, color)
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
