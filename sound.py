import pygame
import threads

class Sound:
    def __init__(self, filename):
        """
        Create a sound from a file
        """
        if not pygame.mixer.get_init():
            pygame.mixer.init()
        self.sound_file = pygame.mixer.Sound(filename)
    

def play_sound(sound: Sound):
    """
    Play the sound
    """
    sound.sound_file.play()

def play_sound_forever(sound: Sound):
    """
    Play the sound forever
    """
    sound.sound_file.play(-1)

def play_until_done(sound: Sound):
    """
    Play the sound and wait until it is done
    """
    threads.thread_operation("play_until_done")
    sound.sound_file.play()
    while pygame.mixer.get_busy():
        threads.wait()

def stop_sound(sound: Sound):
    """
    Stop the sound
    """
    sound.sound_file.stop()

def set_volume(sound: Sound, volume: float):
    """
    Set the volume of the sound
    """
    sound.sound_file.set_volume(volume)