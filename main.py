# Звуки с https://sfbgames.itch.io/chiptone
import pygame
import sound_device_test
import config
from scene import MenuScene


class Game:
    '''Игра'''
    def __init__(self) -> None:
        pygame.display.init()
        pygame.font.init()

        self.is_sound = sound_device_test.is_sound()
        if self.is_sound:
            pygame.mixer.init()
            pygame.mixer.music.load(config.SOUNDS_DIR / 'music.wav')
            pygame.mixer.music.set_volume(0.3)
            pygame.mixer.music.play(loops=-1)

        # FIXME: использовать главный дисплей, если их несколько
        display_info = pygame.display.Info()

        self.window_width = display_info.current_w
        self.window_height = display_info.current_h
        self.font_size = int(
            min(self.window_width, self.window_height) * 0.03
        )
        self.screen = pygame.display.set_mode(
            (self.window_width, self.window_height)
        )
        self.scene = MenuScene(self, 'Арканоид')
        self.keys_pressed = None
        self.is_running = True
        self.clock = pygame.time.Clock()

    def main_loop(self) -> None:
        '''
        Главный цикл игры:
            сбор событий
            обновление объектов
            рендер
            ожидание тика FPS
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
