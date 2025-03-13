import pyaudio


def is_sound():
    p = pyaudio.PyAudio()
    try:
        stream = p.open(format=pyaudio.paInt16, channels=1, rate=44100, output=True)
        stream.close()
        return True
    except OSError:
        return False
    finally:
        p.terminate()
