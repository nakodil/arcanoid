import pygame
from abc import ABC, abstractmethod
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
        self.tile_width = self.game.window_width // config.BLOCKS_IN_ROW
        self.tile_height = self.tile_width // 3

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
        self.sounds = {
            'gameover': pygame.mixer.Sound(
                config.SOUNDS_DIR / 'gameover.wav'
            ),
        }
        self.all_rackets = pygame.sprite.Group()
        racket_center = (
            int(self.game.window_width // 2),
            int(self.game.window_height * 0.9),
        )

        self.racket = RacketManual(
            self,
            racket_center,
            config.RACKETS_COLOR,
            pygame.K_a,
            pygame.K_d,
        )

        self.ball = Ball(self, config.BALL_COLOR, self.game.is_sound)

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

        self.all_drops = pygame.sprite.Group()

    def make_blocks(self):
        '''Создает блоки'''
        y = int(self.game.window_height * 0.15)
        for row_index in range(config.ROWS_OF_BLOCKS):
            x = 0
            for _ in range(config.BLOCKS_IN_ROW):
                Block(
                    self,
                    (x, y),
                    config.BLOCK_COLORS[row_index % len(config.BLOCK_COLORS)],
                )
                x += self.tile_width
            y += self.tile_height

    def render(self):
        '''Отрисовывает объекты на экране'''
        self.game.screen.fill(config.BG_COLOR)
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
        if self.game.is_sound:
            # FIXME: Этот звук почти не слышкно из-за звука потери мяча
            self.sounds['gameover'].play()
        self.game.scene = MenuScene(self.game, 'Проиграл')

    def win(self):
        # TODO: сыграть звук победы, загрузить следующий уровень
        self.game.scene = MenuScene(self.game, 'Выиграл')


class MenuScene(Scene):
    def __init__(self, game, title: str):
        super().__init__(game)
        self.title = title
        self.menu_options = [
            'ENTER - новая игра',
            'ESC - выход',
        ]
        self.font_size = self.game.font_size
        self.render_menu()

    def render_menu(self):
        '''Рисует все меню в центре экрана'''
        total_height = (len(self.menu_options) + 1) * self.font_size * 2
        start_y = (self.game.window_height - total_height) // 2

        # заголовок
        self.render_text(
            self.title,
            (self.game.window_width // 2, start_y),
            self.font_size * 2
        )

        # опции
        y = start_y + self.font_size * 3  # отступ от заголовка
        for option in self.menu_options:
            self.render_text(
                option, (self.game.window_width // 2, y), self.font_size
            )
            y += self.font_size * 2  # межстрочный отступ

    def render_text(self, text: str, coords: tuple, font_size: int):
        '''Рисует одну строчку текста'''
        font = pygame.font.Font(config.MENU_FONT, font_size)
        text_surface = font.render(text, True, config.MENU_COLOR)
        text_rect = text_surface.get_rect(center=coords)
        text_sprite = pygame.sprite.Sprite()
        text_sprite.image = text_surface
        text_sprite.rect = text_rect
        self.all_sprites.add(text_sprite)

    def handle_events(self):
        '''Реагирует на события в меню'''
        super().handle_events()
        if self.keys_pressed and self.keys_pressed[pygame.K_RETURN]:
            self.game.scene = GameplayScene(self.game)  # новая игра

    def render(self):
        self.game.screen.fill(config.BG_COLOR)
        self.all_sprites.draw(self.game.screen)
        pygame.display.flip()
