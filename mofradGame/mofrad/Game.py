import pygame

from Player import Player
from assets.FontManager import FontManager
from assets.SoundManager import SoundManager
from inputs.InputController import InputController
from mofrad.assets.asset_manager import AssetManager
from mofrad.objects.Bee import Bee
from mofrad.objects.Wall import Wall


class Game:
    def __init__(self, asset_manager: AssetManager, screen_rect: pygame.Rect):
        self.screen_rect = screen_rect

        self.tile_size = 32
        self.objects = []
        self.level_name = ""
        self.offset = [0, 0]
        self.map_scroll = [0, 0]

        self.asset_manager = asset_manager
        self.font_manager = FontManager()
        self.font_manager.load("debug", "ComicSansMS", size=8)

        self.sound_manager = SoundManager(root="./assets")

        self.game_surface = pygame.Surface((screen_rect.width, screen_rect.height))
        self.hud_surface = pygame.Surface((screen_rect.width, screen_rect.height))
        self.hud_surface.set_colorkey((255, 0, 255))
        self.game_surface.set_colorkey((255, 0, 255))


        self.objects.append(Bee((7 * self.tile_size, 3 * self.tile_size), self.asset_manager, self))
        self.objects.append(Bee((8 * self.tile_size, 3 * self.tile_size), self.asset_manager, self))
        self.objects.append(Bee((7 * self.tile_size, 6 * self.tile_size), self.asset_manager, self))
        self.objects.append(Bee((8 * self.tile_size, 6 * self.tile_size), self.asset_manager, self))
        self.objects.append(Bee((7 * self.tile_size, 10 * self.tile_size), self.asset_manager, self))

        for x in range(0, 60):
            for y in range(0, 16):
                if y == 0 or x == 0 or y == 15 or x == 59:
                    self.add_wall(x, y)

        self.font = pygame.font.SysFont("ariel", 32)

        self.player = Player(self.asset_manager, self)
        self.player.set_position(4 * self.tile_size, 3 * self.tile_size)

    def add_wall(self, x, y):
        self.objects.append(Wall((x * self.tile_size, y * self.tile_size), self.asset_manager, self))

    def set_level(self, name):
        self.level_name = name

    def calculate_offset(self, focus: pygame.Rect):
        xpercent = 0.4
        xcenter = self.map_scroll[0] + self.screen_rect.centerx
        if focus.centerx < xcenter - self.screen_rect.width * (0.5 - xpercent):
            self.map_scroll[0] -= ((xcenter - self.screen_rect.width * (0.5 - xpercent)) - focus.centerx) * 0.5
        if focus.centerx > xcenter + self.screen_rect.width * (0.5 - xpercent):
            self.map_scroll[0] += (focus.centerx - xcenter - self.screen_rect.width * (0.5 - xpercent)) * 0.5

        ypercent = 0.1
        ycenter = self.map_scroll[1] + self.screen_rect.centery
        if focus.centery < ycenter - self.screen_rect.height * (0.5 - ypercent):
            self.map_scroll[1] -= ((ycenter - self.screen_rect.height * (0.5 - ypercent)) - focus.centery) * 0.5
        if focus.centery > ycenter + self.screen_rect.height * (0.5 - ypercent):
            self.map_scroll[1] += (focus.centery - ycenter - self.screen_rect.height * (0.5 - ypercent)) * 0.5

    def update(self, inputs: InputController):
        for i in range(len(self.objects) - 1, -1, -1):
            obj = self.objects[i]
            obj.update(self.objects, self.player)
            if obj.delete:
                del self.objects[i]
        self.player.update(self.objects, inputs, self.offset)
        self.calculate_offset(self.player.rect)
        self.offset = self.map_scroll

    def draw(self, surface: pygame.Surface, fps):
        surface.fill((100, 140, 255))

        self.game_surface.fill((255, 0, 255))


        self.hud_surface.fill((255, 0, 255))

        for i in range(len(self.objects) - 1, -1, -1):
            if len(self.objects) > i:
                obj = self.objects[i]
                obj.draw(self.game_surface, self.offset)

        self.player.draw(self.game_surface, self.offset)

        self.hud_surface.blit(self.font_manager.render("debug", str(int(fps)) + "fps"), (0, 0))
        surface.blit(self.game_surface.convert(), (0, 0))
        surface.blit(self.hud_surface.convert_alpha(), (0, 0))
