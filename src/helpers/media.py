import pygame

freq = 44100  # audio CD quality
bitsize = -16  # unsigned 16 bit
channels = 2  # 1 is mono, 2 is stereo
buffer = 1024  # number of samples
pygame.mixer.init(freq, bitsize, channels, buffer)
pygame.mixer.music.set_volume(0.8)

paused = False


def play_midi(midi_filename):
    pygame.mixer.music.load(midi_filename)
    pygame.mixer.music.play()


def stop_midi():
    pygame.mixer.music.stop()


def pause_midi():
    global paused
    if paused:
        pygame.mixer.music.unpause()
        paused = False
    else:
        pygame.mixer.music.pause()
        paused = True
