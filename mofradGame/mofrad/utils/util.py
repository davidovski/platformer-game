import pygame

def rot_center(image, angle):
    """rotate an image while keeping its center and size"""
    orig_rect = image.get_rect()
    rot_image = pygame.transform.rotate(image, angle)
    rot_rect = orig_rect.copy()
    rot_rect.center = rot_image.get_rect().center
    rot_image = rot_image.subsurface(rot_rect).copy()
    return rot_image


def playMusic(filename):
    m = pygame.mixer.Sound(filename)
    m.set_volume(0)
    m.play(-1)


def make_wall_rect_list(rect, ol, walls_only=True):
    wall_rect_list = []
    for w in ol:
        if not rect == w.rect:
            if walls_only:
                if w.wall:
                    wall_rect_list.append(w.rect)
            else:
                wall_rect_list.append(w.rect)
    return wall_rect_list

class Direction:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def right(self):
        if self.x > 0:
            return True
        return False

    def left(self):
        if self.x < 0:
            return True
        return False

    def up(self):
        if self.y > 0:
            return True
        return False

    def down(self):
        if self.y < 0:
            return True
        return False