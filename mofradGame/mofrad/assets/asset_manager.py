import pygame
import os

class AssetManager:
    def __init__(self, root="./assets"):
        self.root = root
        self.assets = {}

    def get_manager(self):
        return self.assets

    def load_asset(self,name):
        self.assets[name] = pygame.image.load(self.root + "/" + name).convert()

    def get_asset(self, name):
        if not name in self.assets:
            self.assets[name] = pygame.image.load(self.root + "/" + name).convert_alpha()
        return self.assets[name]