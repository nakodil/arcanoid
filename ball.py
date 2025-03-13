import config
import pygame
import math


class Ball(pygame.sprite.Sprite):
    def __init__(self, scene, is_sound):
        super().__init__()
        self.scene = scene
        self.is_sound = is_sound
        self.velocity_x = 0
        self.velocity_y = 0
        self.angle = 0
        self.color = config.GREEN
        self.speed = 10
        self.score = 0
        self.hp = 3

        width = int(self.scene.tile_size * 0.3)
        height = int(self.scene.tile_size * 0.3)

        self.image = pygame.Surface((width, height))
        self.image.fill(self.color)
        self.rect = self.image.get_rect()

        self.goto_start()
        if self.is_sound:
            self.sounds = {
                'collide': pygame.mixer.Sound(config.SOUNDS_DIR / 'collide.wav'),
                'lose': pygame.mixer.Sound(config.SOUNDS_DIR / 'lose.wav'),
                'win': pygame.mixer.Sound(config.SOUNDS_DIR / 'win.wav'),
            }
        self.scene.all_sprites.add(self)

    def goto_start(self):
        self.rect.midbottom = self.scene.racket.rect.midtop
        self.angle = 0

    def move(self):
        self.velocity_x = math.cos(math.radians(self.angle - 90))
        self.velocity_y = math.sin(math.radians(self.angle - 90))
        self.rect.x += self.velocity_x * self.speed
        self.rect.y += self.velocity_y * self.speed

    def collide_borders(self):
        '''Столкновения с границами экрана с учетом правильного отражения'''
        if self.rect.left < 0 or self.rect.right > self.scene.game.window_width:
            self.angle = (360 - self.angle) % 360
            if self.is_sound:
                self.sounds['collide'].play()
        elif self.rect.top < 0:
            self.angle = (180 - self.angle) % 360
            if self.is_sound:
                self.sounds['collide'].play()

    def collide_rackets(self):
        '''Столкновения с ракетками'''
        rackets_hit = pygame.sprite.spritecollide(
            self, self.scene.all_rackets, False
        )
        if rackets_hit:
            racket_hit = rackets_hit[0]
            self.angle = (180 - self.angle) % 360
            self.angle += 15 * racket_hit.direction
            self.rect.bottom = racket_hit.rect.top
            if self.is_sound:
                self.sounds['collide'].play()

    def collide_blocks(self):
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

    def update(self):
        self.move()
        self.check_lose()
        self.collide_borders()
        self.collide_rackets()
        self.collide_blocks()

    def check_lose(self) -> None:
        '''Мяч ушел вниз'''
        if self.rect.bottom <= self.scene.game.window_height:
            return
        self.hp -= 1
        if self.hp <= 0:
            self.scene.loose()
        self.scene.racket.goto_start()
        if self.is_sound:
            self.sounds['lose'].play()
        self.goto_start()


if __name__ == '__main__':
    from main import Game
    ball = Ball(Game())
