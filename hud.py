import pygame
import config


class Hud(pygame.sprite.Sprite):
    '''Табло для показа счета одного из игроков'''
    def __init__(self, center_x: int, center_y: int, scene, func):
        super().__init__()
        self.scene = scene
        self.center_x = center_x
        self.center_y = center_y
        self.func = func
        self.color = config.WHITE
        screen_width, screen_height = self.scene.game.screen.get_size()
        min_side = min(screen_width, screen_height)
        self.size = int(min_side * 0.03)
        self.font = pygame.font.Font(
            config.FONTS_DIR / 'PressStart2P-Regular.ttf', self.size
        )
        self.image = None
        self.rect = None
        self.scene.all_sprites.add(self)

    def update(self):
        self.image = self.font.render(str(self.func()), True, self.color)
        self.rect = self.image.get_rect()
        self.rect.centerx = self.center_x
        self.rect.centery = self.center_y
