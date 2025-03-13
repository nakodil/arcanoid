import pygame
from abc import ABC, abstractmethod
import math
import config
from ball import Ball
from racket import RacketManual, RacketAuto
from hud import Hud
from block import Block, BonusBlock


class Scene(ABC):
    '''Игровая сцена'''
    @abstractmethod
    def __init__(self, game):
        self.game = game
        self.keys_pressed = None
        self.all_sprites = pygame.sprite.Group()
        self.tile_size = math.gcd(
            self.game.window_width,
            self.game.window_height
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
    def __init__(self, game, mode: str):
        super().__init__(game)
        self.all_rackets = pygame.sprite.Group()
        racket_center = (
            int(self.game.window_width // 2),
            int(self.game.window_height * 0.9),
        )

        # ракетка
        if mode == 'human':
            self.racket = RacketManual(
                racket_center,
                pygame.K_a,
                pygame.K_d,
                self
            )
        else:
            self.racket = RacketAuto(
                racket_center,
                self,
                20
            )

        self.ball = Ball(self)

        # табло - очки
        Hud(
            int(self.game.window_width * 0.2),
            int(self.game.window_height * 0.05),
            self,
            lambda: self.ball.score
        )

        # табло - жизни
        Hud(
            int(self.game.window_width * 0.8),
            int(self.game.window_height * 0.05),
            self,
            lambda: self.ball.hp
        )

        self.all_blocks = pygame.sprite.Group()
        self.make_blocks()

    def make_blocks(self):
        '''Создает блоки'''
        y = self.tile_size
        for row_index in range(config.ROWS_OF_BLOCKS):
            x = 0
            for _ in range(self.game.window_width // self.tile_size):
                if row_index % 2:
                    Block(self, (x, y))
                else:
                    BonusBlock(self, (x, y))
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
            5
        )
        pygame.draw.line(
            self.game.screen,
            config.WHITE,
            (self.game.window_width // 2, 0),
            (self.game.window_width // 2, self.game.window_height),
            5
        )

    def loose(self):
        self.game.scene = MenuScene(self.game, 'Проиграл')

    def win(self):
        self.game.scene = MenuScene(self.game, 'Выиграл')


class MenuScene(Scene):
    def __init__(self, game, title: str):
        super().__init__(game)
        MenuLines(
            self,
            title,
            '1 - человек',
            '2 - компьютер',
            'ESC - выход',
        )

    def handle_events(self):
        super().handle_events()
        if self.keys_pressed[pygame.K_1]:
            self.game.scene = GameplayScene(self.game, 'human')
        elif self.keys_pressed[pygame.K_2]:
            self.game.scene = GameplayScene(self.game, 'pc')

    def render(self):
        self.game.screen.fill(config.BLACK)
        self.all_sprites.draw(self.game.screen)
        pygame.display.flip()


class TextLine(pygame.sprite.Sprite):
    def __init__(self, text_line: str, coords: tuple):
        super().__init__()
        self.font = pygame.font.Font(None, 100)  # FIXME: magic number!
        self.image = self.font.render(text_line, True, config.WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = coords


class MenuLines:
    # TODO: рисовать линии на отдельной поверхности
    def __init__(self, scene, *lines):
        x = scene.game.window_width // 2
        y = 100
        for line in lines:
            text_line = TextLine(line, (x, y))
            scene.all_sprites.add(text_line)
            y += 100  # TODO: рассчитать отступ относительно размера шрифта
