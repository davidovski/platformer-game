import pygame
import time

class SoundManager:
    def __init__(self, root="./assets/sounds"):
        self.root = root
        self.sounds = {}
        pygame.mixer.pre_init(44100, -16, 2, 2048)
        # pygame.mixer.music.set_volume(0.3)

    def get_manager(self):
        return self.sounds

    def load_sound(self, name):
        if name not in self.sounds:
            print("loaded sound: " + name)
            self.sounds[name] = pygame.mixer.Sound(self.root + "/" + name)
        return self.sounds[name]

    def play_sound(self, name):
        # print(name + " - " + str(time.time()))
        if name not in self.sounds:
            self.load_sound(name)
        self.sounds[name].play()
