import _thread as thread
import pygame
from pygame.rect import Rect

from mofrad.Game import *
from mofrad.assets.asset_manager import AssetManager
from mofrad.inputs.InputController import InputController


class Main:
    def __init__(self):
        pygame.init()
        scale = 0.8
        size = (int(960 * scale), int(510 * scale))
        self.screen = pygame.display.set_mode(size, pygame.HWSURFACE)
        self.screen_rect = Rect(0, 0, size[0], size[1])
        self.clock = pygame.time.Clock()
        self.tick_clock = pygame.time.Clock()

        self.asset_manager = AssetManager()
        self.inputs = InputController()

        self.game = Game(self.asset_manager, self.screen_rect)
        self.draw_thread = thread.start_new_thread(self.draw_loop, ("draw", 60))

        pygame.mouse.set_visible(False)

    def start(self):
        while True:
            self.update()
            self.inputs.update()

    def update(self):
        self.game.update(self.inputs)
        self.tick_clock.tick(30)
        pass

    def draw_loop(self, thread_name, speed):
        print("starting " + thread_name)
        while True:
            self.draw()
            self.clock.tick(speed)

    def draw(self):
        color = (0, 0, 0)
        self.screen.fill(color)

        self.game.draw(surface=self.screen, fps=self.clock.get_fps())
        pygame.display.flip()
