import pygame
import sys

from mofrad.utils.util import Direction


class InputController:
    def __init__(self):
        self.keys = pygame.key.get_pressed()
        self.last_keys = pygame.key.get_pressed()
        self.mouse = MouseState(False, [0,0])

    def update(self):
        self.last_keys = self.keys

        self.keys = pygame.key.get_pressed()

        self.mouse.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONUP:
                self.mouse.set_down(False)
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.mouse.set_down(True)
            if event.type == pygame.MOUSEMOTION:
                self.mouse.set_position(pygame.mouse.get_pos())

    def move_pad(self):
        x = 0
        y = 0
        if self.keys[pygame.K_a] or self.keys[pygame.K_LEFT]:
            x = -1
        if self.keys[pygame.K_d] or self.keys[pygame.K_RIGHT]:
            x = 1

        if self.keys[pygame.K_w] or self.keys[pygame.K_UP]:
            y = 1
        if self.keys[pygame.K_s] or self.keys[pygame.K_DOWN]:
            y = -1
        return Direction(x, y)

    def shooting(self):
        return self.keys[pygame.K_SPACE] or self.mouse.down or self.keys[pygame.K_l]

    def end_shooting(self):
        return (not self.keys[pygame.K_SPACE] and self.last_keys[pygame.K_SPACE]) or (not self.mouse.down and self.mouse.last_down) or (not self.keys[pygame.K_l] and self.last_keys[pygame.K_l])

    def sprint(self):
        if self.keys[pygame.K_LSHIFT]:
            return True
        return False

    def ducked(self):
        if self.keys[pygame.K_s] or self.keys[pygame.K_DOWN]:
            return True
        return False

    def start_ducked(self):
        if self.keys[pygame.K_s] and not self.last_keys[pygame.K_s]:
            return True
        if self.keys[pygame.K_DOWN] and not self.last_keys[pygame.K_DOWN]:
            return True
        return False

    def end_ducked(self):
        if not self.keys[pygame.K_s] and self.last_keys[pygame.K_s]:
            return True
        if not self.keys[pygame.K_DOWN] and self.last_keys[pygame.K_DOWN]:
            return True
        return False

    def jump(self):
        return self.jump_start()

    def jump_start(self):
        if self.keys[pygame.K_w] and not self.last_keys[pygame.K_w]:
            return True
        # if self.keys[pygame.K_SPACE] and not self.last_keys[pygame.K_SPACE]:
        #     return True
        if self.keys[pygame.K_UP] and not self.last_keys[pygame.K_UP]:
            return True
        return False

    def jump_end(self):
        if not self.keys[pygame.K_w] and self.last_keys[pygame.K_w]:
            return True
        # if not self.keys[pygame.K_SPACE] and self.last_keys[pygame.K_SPACE]:
        #     return True
        if not self.keys[pygame.K_UP] and self.last_keys[pygame.K_UP]:
            return True
        return False

class MouseState:
    def __init__(self, down, position):
        self.down = down
        self.last_down = down
        self.last_position = position
        self.position = position

    def update(self):
        self.last_down = self.down
        self.last_position = self.position

    def set(self, down, position):
        self.down = down
        self.position = position

    def set_down(self, down):
        self.down = down

    def set_position(self, position):
        self.position = position

