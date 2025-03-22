import config
import pygame
import math


class Ball(pygame.sprite.Sprite):
    '''Мяч'''
    def __init__(self, scene, color: tuple, is_sound: bool):
        super().__init__()
        self.scene = scene
        self.color = color
        self.is_sound = is_sound
        self.velocity_x = 0
        self.velocity_y = 0
        self.angle = 0
        self.speed = 10
        self.score = 0
        self.hp = 3

        width = int(self.scene.tile_height * 0.3)
        height = int(self.scene.tile_height * 0.3)

        self.image = pygame.Surface((width, height))
        self.image.fill(self.color)
        self.rect = self.image.get_rect()

        self.goto_start()
        if self.is_sound:
            self.sounds = {
                'collide': pygame.mixer.Sound(
                    config.SOUNDS_DIR / 'collide.wav'
                ),
                'lose': pygame.mixer.Sound(
                    config.SOUNDS_DIR / 'lose.wav'
                ),
                'win': pygame.mixer.Sound(
                    config.SOUNDS_DIR / 'win.wav'
                ),
            }
        self.scene.all_sprites.add(self)

    def goto_start(self) -> None:
        self.rect.midbottom = self.scene.racket.rect.midtop
        self.angle = 0

    def move(self) -> None:
        self.velocity_x = math.cos(math.radians(self.angle - 90))
        self.velocity_y = math.sin(math.radians(self.angle - 90))
        self.rect.x += self.velocity_x * self.speed
        self.rect.y += self.velocity_y * self.speed

    def collide_borders(self) -> None:
        '''Столкновения с границами экрана'''
        if (
            self.rect.left < 0
            or self.rect.right > self.scene.game.window_width
        ):
            self.angle = (360 - self.angle) % 360
            if self.is_sound:
                self.sounds['collide'].play()
        elif self.rect.top < 0:
            self.angle = (180 - self.angle) % 360
            if self.is_sound:
                self.sounds['collide'].play()

    def collide_rackets(self) -> None:
        '''
        Столкновения с ракетками:
        мяч столкнулся с левой третью ракетки - поворачивается влево;
        мяч столкнулся с правой третью ракетки - поворачивается вправо;
        мяч столкнулся с центральной третью ракетки - поворачивается вверх.
        '''
        rackets_hit = pygame.sprite.spritecollide(
            self, self.scene.all_rackets, False
        )
        if not rackets_hit:
            return

        racket_hit = rackets_hit[0]
        collision_point = self.rect.centerx - racket_hit.rect.left
        racket_width = racket_hit.rect.width
        if collision_point < racket_width / 3:
            self.angle = -15
        elif collision_point > 2 * racket_width / 3:
            self.angle = 15
        else:
            self.angle = 0
        self.rect.bottom = racket_hit.rect.top - 1  # отлепить мяч от ракетки

        if self.is_sound:
            self.sounds['collide'].play()

    def collide_blocks(self) -> None:
        '''Столкновения с блоками'''
        blocks_hit = pygame.sprite.spritecollide(
            self, self.scene.all_blocks, False
        )
        if blocks_hit:
            for block in blocks_hit:
                if self.is_sound:
                    self.sounds['win'].play()
                block.destroy()
            self.angle = (180 - self.angle) % 360

    def update(self) -> None:
        self.move()
        self.check_lose()
        self.collide_borders()
        self.collide_rackets()
        self.collide_blocks()

    def check_lose(self) -> None:
        '''Мяч ушел за нижнюю границу экрана'''
        if self.rect.bottom <= self.scene.game.window_height:
            return
        self.hp -= 1
        if self.hp <= 0:
            self.scene.loose()
        self.scene.racket.goto_start()
        if self.is_sound:
            self.sounds['lose'].play()
        self.goto_start()
