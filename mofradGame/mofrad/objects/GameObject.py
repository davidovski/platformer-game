import pygame

from inputs.InputController import InputController
from utils.util import make_wall_rect_list


class GameObject:
    def __init__(self, rect, game):

        self.rect = pygame.Rect(rect[0], rect[1], rect[2], rect[3])
        self.images = []
        self.alpha = 0
        self.health = 1
        self.direction = [1, 0]
        self.flash = False

        self.wall = False
        self.evil = False
        self.delete = False
        self.remove_when_offscreen = False
        return self

    def is_on_screen(self, rect, surf: pygame.Surface, map_pos):
        rect = self.rect.move(-map_pos[0], -map_pos[1])
        if rect.right < 0 or rect.left > surf.get_width() or rect.bottom < 0 or rect.top > surf.get_height():
            if self.remove_when_offscreen:
                self.delete = True
            return False
        return True

    def draw(self, surf: pygame.Surface, map_pos):
        calculated = self.rect.move(-map_pos[0], -map_pos[1])
        if not self.is_on_screen(calculated, surf, map_pos):
            return
        if not self.flash:
            self.alpha += 1
            surf.blit(self.images[self.alpha % len(self.images)], calculated)
        else:
            self.flash = False
        return

    def update(self, object_list, player):
        move_rect = pygame.Rect(self.rect.x, self.rect.y, self.rect.width, self.rect.height)
        move_rect.move(self.direction[0], self.direction[1])
        if move_rect.collidelist(make_wall_rect_list(self.rect, object_list)) == -1:
            self.rect.move(self.direction[0], self.direction[1])
        pass

    def on_hit(self, rct):
        if rct.colliderect(self.rect):
            self.health -= 1
            self.flash = True
            if self.health < 0:
                self.delete = True
            return True
        return False