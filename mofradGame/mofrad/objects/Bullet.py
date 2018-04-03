from math import ceil

import pygame

from mofrad.assets.asset_manager import AssetManager
from mofrad.objects.GameObject import GameObject
from mofrad.utils import spritesheet
from mofrad.utils.util import make_wall_rect_list
from utils.vector import magnitude


class Bullet(GameObject):
    def __init__(self, pos, asset_manager : AssetManager, game):
        x = pos[0]
        y = pos[1]
        GameObject.__init__(self, rect=pygame.Rect(x, y, 8, 8), game=game)
        self.type = "bullet"
        self.shooter = ""
        self.direction = [0, 0]
        self.start_rect = pygame.Rect(x, y, 8, 8)

        game.sound_manager.play_sound("shoot.wav")

        self.images.append(asset_manager.get_asset("bullet.png"))
        self.remove_when_offscreen = True
        self.evil = False
        self.wall = False
        self.last_pos = [self.rect.x, self.rect.y]

    def on_hit(self, rct):
        if rct.colliderect(self.rect):
            return True
        return False

    def draw(self, surf: pygame.Surface, map_pos):
        pygame.draw.line(surf, (240, 190, 190), (self.rect.x - map_pos[0] + 4, self.rect.y - map_pos[1] + 2), (self.last_pos[0] - map_pos[0] + 4, self.last_pos[1] - map_pos[1] + 2), 1)
        GameObject.draw(self, surf, map_pos)
        # if not self.delete:

    def update(self, object_list, inputs):

        # GameObject.update(self, object_list, inputs)
        # times = abs(magnitude(self.direction))
        # for t in range(0, ceil(times)):
        self.last_pos = [self.rect.x, self.rect.y]
        times = 64.0
        p = [float(self.rect.x), float(self.rect.y)]
        for i in range(0, int(times)):
            move_rect = pygame.Rect(p[0], p[1], self.rect.width, self.rect.height)
            move_rect.move(self.direction[0] / times, self.direction[1] / times)

            hit = False
            for obj in object_list:
                if not obj.type == self.shooter and not obj.type == self.type:
                    if obj.on_hit(move_rect):
                        self.delete = True
                        hit = True
            if hit:
                break
            p[0] += self.direction[0] / times
            p[1] += self.direction[1] / times
        self.rect.x = p[0]
        self.rect.y = p[1]
        pass
