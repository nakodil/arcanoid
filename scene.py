import pygame
from abc import ABC, abstractmethod
import math
import config
from ball import Ball
from racket import RacketManual
from hud import Hud
from block import Block


class Scene(ABC):
    '''Игровая сцена'''
    @abstractmethod
    def __init__(self, game):
        self.game = game
        self.font_size = self.game.font_size
        self.keys_pressed = None
        self.all_sprites = pygame.sprite.Group()
        self.tile_size = int(
            math.gcd(self.game.window_width, self.game.window_height) * 0.5
        )

    def handle_events(self):
        '''Обрабатывает события'''
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game.is_running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.game.is_running = False

        self.keys_pressed = pygame.key.get_pressed()

    def update(self):
        self.all_sprites.update()

    def render(self):
        pass


class GameplayScene(Scene):
    '''Сцена игрового процесса'''
    def __init__(self, game):
        super().__init__(game)
        self.all_rackets = pygame.sprite.Group()
        racket_center = (
            int(self.game.window_width // 2),
            int(self.game.window_height * 0.9),
        )

        self.racket = RacketManual(
            racket_center,
            pygame.K_a,
            pygame.K_d,
            self
        )

        self.ball = Ball(self, self.game.is_sound)

        Hud(
            int(self.game.window_width * 0.1),
            int(self.game.window_height * 0.05),
            self,
            lambda: self.ball.score,
            'очки',
            self.font_size
        )

        Hud(
            int(self.game.window_width * 0.9),
            int(self.game.window_height * 0.05),
            self,
            lambda: self.ball.hp,
            'жизни',
            self.font_size
        )

        self.all_blocks = pygame.sprite.Group()
        self.make_blocks()

    def make_blocks(self):
        '''Создает блоки'''
        y = self.tile_size * 2
        for row_index in range(config.ROWS_OF_BLOCKS):
            x = 0
            for _ in range(self.game.window_width // self.tile_size):
                Block(
                    self,
                    (x, y),
                    config.BLOCK_COLORS[row_index % len(config.BLOCK_COLORS)],
                )
                x += self.tile_size
            y += self.tile_size

    def render(self):
        '''Отрисовывает объекты на экране'''
        self.game.screen.fill(config.BLACK)
        if config.IS_DEBUG:
            self.draw_lines()
        self.all_sprites.draw(self.game.screen)
        pygame.display.flip()

    def draw_lines(self):
        pygame.draw.line(
            self.game.screen,
            config.GREEN,
            (0, self.game.window_height // 2),
            (self.game.window_width, self.game.window_height // 2),
            5,
        )
        pygame.draw.line(
            self.game.screen,
            config.WHITE,
            (self.game.window_width // 2, 0),
            (self.game.window_width // 2, self.game.window_height),
            5,
        )

    def loose(self):
        self.game.scene = MenuScene(self.game, 'Проиграл')

    def win(self):
        self.game.scene = MenuScene(self.game, 'Выиграл')


class MenuScene(Scene):
    '''Сцена меню'''
    def __init__(self, game, title: str):
        super().__init__(game)
        MenuLines(
            self,
            self.font_size,
            title,
            'ENTER - новая игра',
            'ESC - выход',
        )

    def handle_events(self):
        super().handle_events()
        if self.keys_pressed[pygame.K_RETURN]:
            self.game.scene = GameplayScene(self.game)

    def render(self):
        self.game.screen.fill(config.BLACK)
        self.all_sprites.draw(self.game.screen)
        pygame.display.flip()


class MenuLines:
    # TODO: рисовать линии на отдельной поверхности
    def __init__(self, scene, font_size, title, *lines):
        x = scene.game.window_width // 2
        y = 100
        title = TextLine(title, (x, y), font_size)  # заголовок меню
        scene.all_sprites.add(title)
        for line in lines:  # пункты меню
            y += 100  # TODO: рассчитать отступ относительно размера шрифта
            menu_line = TextLine(line, (x, y), font_size)
            scene.all_sprites.add(menu_line)


class TextLine(pygame.sprite.Sprite):
    def __init__(self, text_line: str, coords: tuple, font_size):
        super().__init__()
        self.font = pygame.font.Font(config.MENU_FONT, font_size)
        self.image = self.font.render(text_line, True, config.MENU_COLOR)
        self.rect = self.image.get_rect()
        self.rect.center = coords
