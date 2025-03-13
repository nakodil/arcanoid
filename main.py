# Звуки с https://sfxr.me/
import pygame
import config
from scene import MenuScene


class Game:
    '''Игра'''
    def __init__(self) -> None:
        pygame.init()
        pygame.mixer.init()  # зачем?
        display_info = pygame.display.Info()
        self.window_width = display_info.current_w
        self.window_height = display_info.current_h
        self.screen = pygame.display.set_mode(
            (self.window_width, self.window_height)
        )
        self.scene = MenuScene(self, 'новая игра')
        self.keys_pressed = None
        self.is_running = True
        self.clock = pygame.time.Clock()

    def main_loop(self) -> None:
        '''
        сбор событий
        обновление (объектов)
        рендер (отрисовка)
        '''
        while self.is_running:
            self.scene.handle_events()
            self.scene.update()
            self.scene.render()
            self.clock.tick(config.FPS)
        pygame.quit()


if __name__ == '__main__':
    game = Game()
    game.main_loop()
