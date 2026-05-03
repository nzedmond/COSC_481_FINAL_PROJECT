from pyray import *
from constants import *
from screen_manager import ScreenManager, Resources


def main():
    init_window(SCREEN_WIDTH, SCREEN_HEIGHT, b"Crossing Kabgayi - The Escape")
    init_audio_device()
    set_target_fps(60)

    res = Resources()
    manager = ScreenManager(res)

    while not window_should_close():
        res.update_audio()
        manager.update(get_frame_time())
        manager.draw()

    res.unload()
    close_audio_device()
    close_window()


if __name__ == "__main__":
    main()
