import pygame

from mofrad.assets.asset_manager import AssetManager
from mofrad.objects.GameObject import GameObject
from mofrad.utils import spritesheet
from mofrad.utils.util import make_wall_rect_list


class Wall(GameObject):
    def __init__(self, pos, asset_manager : AssetManager, game):
        x = pos[0]
        y = pos[1]
        GameObject.__init__(self, rect=pygame.Rect(x, y, 32, 32), game=game)
        self.type = "wall"
        self.direction = [0, 0]
        self.start_rect = pygame.Rect(x, y, 32, 32)

        sheet = spritesheet.spritesheet('tilesheet.png', asset_manager)
        self.images.append(sheet.image_at((64, 32, 32, 32)))

        self.evil = False
        self.wall = True

    def on_hit(self, rct):
        if rct.colliderect(self.rect):
            return True
        return False

    def update(self, object_list, inputs):
        pass
