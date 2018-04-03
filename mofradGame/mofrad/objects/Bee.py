import random
from mofrad.objects.GameObject import *
from mofrad.utils.util import make_wall_rect_list


class Bee(GameObject):
    def __init__(self, pos, asset_manager, game):
        x = pos[0]
        y = pos[1]
        GameObject.__init__(self, pygame.Rect(x, y, 32, 20), game)
        self.move_step = 4
        self.type = "bee"
        self.health = 10
        self.direction = [self.move_step, 0]
        self.start_rect = pygame.Rect(x, y, 32, 32)
        self.images.append(pygame.transform.flip(asset_manager.get_asset("enemy_right_32_0.png"), True, False))
        self.images.append(pygame.transform.flip(asset_manager.get_asset("enemy_right_32_1.png"), True, False))
        self.images.append(asset_manager.get_asset("enemy_right_32_0.png"))
        self.images.append(asset_manager.get_asset("enemy_right_32_1.png"))
        self.images.append(asset_manager.get_asset("eyes.png"))
        self.images.append(pygame.transform.flip(asset_manager.get_asset("eyes.png"), True, False))
        self.drone = False
        self.evil = True

    def update(self, object_list, player):
        wall_rect_list  = make_wall_rect_list(self.rect, object_list)

        if self.drone:
            if player["rect"].x > self.rect.x + 2:
                self.direction[0] = self.move_step
            elif player["rect"].x < self.rect.x - 2:
                self.direction[0] = -self.move_step
            elif player["rect"].y > self.rect.y:
                self.direction[1] = self.move_step * 1.2
                self.direction[0] = 0
            elif player["rect"].y < self.rect.y:
                self.direction[1] = -self.move_step * 1.2
                self.direction[0] = 0
            else:
                self.direction[1] = 0
                self.direction[0] = 0

        enemy_move_rect = self.rect.move(self.direction[0], self.direction[1])
        if enemy_move_rect.collidelist(wall_rect_list) != -1 or random.randint(0, 60) == self.alpha % 60:
            random_direction = random.randint(0, 3)
            if random_direction == 0:
                self.direction = [0, self.move_step]  # down
            elif random_direction == 1:
                self.direction = [0, -self.move_step]  # up
            elif random_direction == 2:
                self.direction = [self.move_step, 0]  # right
            elif random_direction == 3:
                self.direction = [-self.move_step, 0]  # left
        else:
            self.rect = enemy_move_rect

    def draw(self, surf, map_pos):
        calculated = self.rect.move(-map_pos[0], -map_pos[1])
        if not self.is_on_screen(calculated, surf, map_pos):
            return
        if not self.flash:
            frame = self.rect.centerx // 8 % 2
            if self.direction[0] > 0:
                frame_start = 2
            else:
                frame_start = 0
            surf.blit(self.images[frame_start + frame], calculated)
        else:
            self.flash = False