'''
Проблема 1:
pygame.init() инициализирует ВСЕ модули, в том числе - микшер;
если в ОС нет АКТИВНЫХ устройств, то инициализация занимает много времени

Проблема 2:
если в ОС нет АКТИВНЫХ устройств, то микшер не будет инициализирован,
и при попытке сыграть звук будет ошибка
pygame.error: WASAPI can't find requested audio endpoint: Element not found.

Решение обеих:
инициализировать модули по отдельности;
перед инициализацией микшера проверить, может ли ОС проиграть звук
'''

import pyaudio


def is_sound() -> bool:
    p = pyaudio.PyAudio()
    try:
        stream = p.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=44100,
            output=True
        )
        stream.close()
        return True
    except OSError:
        return False
    finally:
        p.terminate()
