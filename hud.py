import pygame
import config


class Hud(pygame.sprite.Sprite):
    '''Счетчик в интерфейсе'''
    def __init__(
            self,
            center_x: int,
            center_y: int,
            scene,
            func,
            title: str,
            font_size: int
    ):
        super().__init__()
        self.scene = scene
        self.center_x = center_x
        self.center_y = center_y
        self.func = func
        self.title = title
        self.font_size = font_size
        self.color = config.HUD_COLOR
        self.font = pygame.font.Font(
            config.HUD_FONT,
            self.font_size,
        )
        self.image = None
        self.rect = None
        self.scene.all_sprites.add(self)

    def update(self):
        text = f'{self.title}: {self.func()}'
        self.image = self.font.render(text, True, self.color)
        self.rect = self.image.get_rect()
        self.rect.centerx = self.center_x
        self.rect.centery = self.center_y
