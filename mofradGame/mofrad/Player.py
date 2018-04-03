import random
from enum import Enum

import pygame

from assets.asset_manager import AssetManager
from inputs.InputController import InputController
from objects.Bullet import Bullet
from objects.GameObject import GameObject
from utils.spritesheet import spritesheet
from utils.util import make_wall_rect_list
from utils.vector import Vector, normalize, magnitude


class Player(GameObject):
    def __init__(self, asset_manager: AssetManager, game):
        self.game = game
        self.asset_manager = asset_manager
        self.rect = pygame.Rect((64, 0, 28, 63))
        GameObject.__init__(self, rect=self.rect, game=game)
        self.type = "player"
        sheet = spritesheet("playerwalking.png", asset_manager)
        self.images_walking_right = [sheet.image_at((0, 0, 32, 64)),
                                     sheet.image_at((32, 0, 32, 64)),
                                     sheet.image_at((64, 0, 32, 64)),
                                     sheet.image_at((96, 0, 32, 64))]

        self.images_standing_right = [sheet.image_at((0, 64, 32, 64))]
        self.images_ducking_right = [sheet.image_at((32, 64, 32, 32))]
        self.images_sliding_right = [sheet.image_at((0, 64, 32, 64))]


        self.images_walking_left = [pygame.transform.flip(sheet.image_at((0, 0, 32, 64)), True, False),
                                    pygame.transform.flip(sheet.image_at((32, 0, 32, 64)), True, False),
                                    pygame.transform.flip(sheet.image_at((64, 0, 32, 64)), True, False),
                                    pygame.transform.flip(sheet.image_at((96, 0, 32, 64)), True, False)]

        self.images_standing_left = [pygame.transform.flip(sheet.image_at((0, 64, 32, 64)), True, False)]
        self.images_ducking_left = [pygame.transform.flip(sheet.image_at((32, 64, 32, 32)), True, False)]
        self.images_sliding_left = [pygame.transform.flip(sheet.image_at((0, 64, 32, 64)), True, False)]


        self.speed = 4
        self.on_ground = False
        self.velocity = Vector(0, 0)

        self.jumps = 0
        self.max_jumps = 999
        self.ducked = False

        self.state = PlayerState.STANDING
        self.looking = Looking.MIDDLE

        self.sliding = False

        self.gun = Gun()

        self.crosshair_image = asset_manager.get_asset("crosshair.png")

        self.mp = [0, 0]


    def set_position(self, x, y):
        self.rect.x = x
        self.rect.y = y

    def move(self, x, y):
        self.rect.x += x
        self.rect.y += y

    def draw(self, surf: pygame.Surface, map_pos):
        calculated = self.rect.move(-map_pos[0], -map_pos[1])
        if not self.is_on_screen(calculated, surf, map_pos):
            return
        if not self.flash:
            self.alpha += 1
            animation = self.images_standing_right
            if self.looking == Looking.RIGHT:
                if self.state == PlayerState.WALKING:
                    animation = self.images_walking_right
                if self.state == PlayerState.RUNNING:
                    animation = self.images_walking_right
                if self.state == PlayerState.JUMPING:
                    animation = self.images_walking_right
                if self.state == PlayerState.SLIDING:
                    animation = self.images_sliding_right
                if self.state == PlayerState.DUCKED:
                    animation = self.images_ducking_right
                if self.state == PlayerState.STANDING:
                    animation = self.images_standing_right

            if self.looking == Looking.LEFT:
                if self.state == PlayerState.WALKING:
                    animation = self.images_walking_left
                if self.state == PlayerState.RUNNING:
                    animation = self.images_walking_left
                if self.state == PlayerState.JUMPING:
                    animation = self.images_walking_left
                if self.state == PlayerState.SLIDING:
                    animation = self.images_sliding_left
                if self.state == PlayerState.DUCKED:
                    animation = self.images_ducking_left
                if self.state == PlayerState.STANDING:
                    animation = self.images_standing_left

            surf.blit(animation[int(self.rect.x / 8) % len(animation)], calculated)

        else:
            self.flash = False
        surf.blit(self.crosshair_image, [self.mp[0] - 8 - map_pos[0], self.mp[1] - 8 - map_pos[1]])
        return

    def update(self, object_list, inputs: InputController, map_pos):
        jump_strength = 12
        gravity = -0.9
        drag = 1

        self.mp = [inputs.mouse.position[0], inputs.mouse.position[1]]
        self.mp[0] += float(map_pos[0])
        self.mp[1] += float(map_pos[1])
        self.mp[1] += self.gun.recoil
        self.mp[0] += self.gun.side_recoil

        move_rect = pygame.Rect(self.rect.x, self.rect.y, self.rect.width, self.rect.height)

        if inputs.start_ducked() and not self.ducked:
            self.ducked = True
            self.rect.y += 32
            self.rect.height -= 32

        if not inputs.ducked() and self.ducked:
            move_rect.y -= 32
            move_rect.height += 32
            if move_rect.collidelist(make_wall_rect_list(move_rect, object_list)) == -1:
                self.rect.y -= 32
                self.rect.height += 32
                self.ducked = False

        move_rect = pygame.Rect(self.rect.x, self.rect.y, self.rect.width, self.rect.height)

        if self.ducked:
            jump_strength /= 2

        if self.on_ground:
            self.jumps = 0

        if inputs.jump() and self.jumps < self.max_jumps:
            self.velocity.y = -jump_strength
            self.jumps += 1

        self.velocity.y -= gravity

        move_rect.y += self.velocity.y
        if move_rect.collidelist(make_wall_rect_list(move_rect, object_list)) == -1:
            self.set_position(move_rect.x, move_rect.y)
            self.on_ground = False
        else:
            if self.velocity.y > 0:
                self.on_ground = True
            self.velocity.y = 1

        move_rect = pygame.Rect(self.rect.x, self.rect.y, self.rect.width, self.rect.height)

        speed = self.speed
        if inputs.sprint():
            speed *= 2
            self.sliding = True

        if self.ducked:
            speed /= 2

        if inputs.move_pad().left():
            self.velocity.x = -speed
        elif inputs.move_pad().right():
            self.velocity.x = speed
        else:
            if inputs.sprint():
                self.sliding = True
            drg = drag
            if not self.on_ground:
                drg = drag * 0.8
            if self.velocity.x > drg:
                self.velocity.x -= drg
            elif self.velocity.x < -drg:
                self.velocity.x += drg
            else:
                self.velocity.x = 0
        if abs(self.velocity.x) < 0.1:
            self.sliding = False

        move_rect.x += self.velocity.x
        if move_rect.collidelist(make_wall_rect_list(move_rect, object_list)) == -1:
            self.set_position(move_rect.x, move_rect.y)
        else:
            self.sliding = False

        if self.ducked:
            self.state = PlayerState.DUCKED
        elif not self.on_ground:
            self.state = PlayerState.JUMPING
        elif inputs.move_pad().left() or inputs.move_pad().right():
            self.state = PlayerState.WALKING
            if inputs.sprint():
                self.state = PlayerState.RUNNING
        elif self.sliding:
            self.state = PlayerState.SLIDING
        else:
            self.state = PlayerState.STANDING

        if self.velocity.x > 0:
            self.looking = Looking.RIGHT
        elif self.velocity.x < 0:
            self.looking = Looking.LEFT



        self.gun.bullet_cool_down -= 1
        if inputs.shooting():
            if self.gun.bullet_cool_down < 0:

                if self.gun.ammo > 0:
                    self.gun.ammo -= 1
                    if self.gun.recoil < self.gun.max_recoil:
                        self.gun.recoil -= self.gun.recoil_amount
                    self.gun.side_recoil = random.randint(-self.gun.recoil_amount, self.gun.recoil_amount)
                    self.gun.bullet_cool_down = self.gun.bullet_max_cool_down

                    position = [self.rect.center[0], self.rect.center[1]]
                    bullet = Bullet(position, self.asset_manager, self.game)

                    if self.looking == Looking.RIGHT:
                        position[0] += 8
                        # bullet.direction = [strength, 0]
                    if self.looking == Looking.LEFT:
                        position[0] -= 8
                        # bullet.direction = [-strength, 0]

                    v = [self.mp[0] - (position[0]), self.mp[1] - (position[1])]
                    v[0] += random.randint(-100, 100) / 100
                    v[1] += random.randint(-100, 100) / 100

                    m = float(magnitude(v))
                    v[0] = float(v[0] / m) * self.gun.strength
                    v[1] = float(v[1] / m) * self.gun.strength
                    bullet.direction[0] = v[0]
                    bullet.direction[1] = v[1]

                    # print(str(bullet.direction))
                    bullet.rect.x = position[0]
                    bullet.rect.y = position[1]

                    bullet.shooter = self.type
                    object_list.append(bullet)
                else:

                    self.game.sound_manager.play_sound("failed_shot.wav")
        else:
            if self.gun.recoil < 0:
                self.gun.recoil += self.gun.recoil_reset
            if self.gun.side_recoil < 0:
                self.gun.side_recoil += self.gun.side_recoil_reset

        if inputs.end_shooting():
            if self.gun.ammo < 1:
                self.gun.ammo = self.gun.max_ammo
                self.gun.bullet_cool_down = 12
                self.game.sound_manager.play_sound("reload.wav")
        pass


class PlayerState(Enum):
    STANDING = "STANDING"
    DUCKED = "DUCKED"
    JUMPING = "JUMPING"
    WALKING = "WALKING"
    RUNNING = "RUNNING"
    SLIDING = "SLIDING"


class Looking(Enum):
    LEFT = "LEFT"
    MIDDLE = "MIDDLE"
    RIGHT = "RIGHT"


class Gun:
    def __init__(self):
        self.max_ammo = 16
        self.ammo = self.max_ammo
        self.bullet_max_cool_down = 1
        self.bullet_cool_down = self.bullet_max_cool_down
        self.strength = 64.0
        self.recoil = 0.0
        self.recoil_amount = 4
        self.recoil_reset = 2

        self.side_recoil = 0
        self.side_recoil_amount = 4
        self.side_recoil_reset = 16

        self.max_recoil = 64
