import pygame
from pygame.math import Vector2
from common.utils.file_manager import get_static_file_path
from game.consts.screen_settings import SCREEN_SIZE, ZOOM, ZOOMED_CHIP
from game.ui.scenes.game_scene.components.map_field import MapField

class Bullet:
    def __init__(self, x, y, velocity: Vector2):
        self.pos = Vector2(x, y)
        self.velocity = velocity  # chips/tick
        self.surface = pygame.Surface((10, 10))
        self.surface.fill((255, 0, 0))

    def move(self):
        self.pos += self.velocity

    def draw(self, surface, map_field_topleft):
        pos = self.pos * ZOOMED_CHIP - Vector2(map_field_topleft)
        surface.blit(self.surface, (int(pos.x), int(pos.y)))

class GamePlayer:
    is_wasd = True

    def __init__(self, display_surface, map_field: MapField):
        self.pos = Vector2(0.0, 0.0)
        self.cd = 0
        self.cd_max = 3
        self.move_speed = 0.3
        self.display_surface: pygame.Surface = display_surface
        self.map_field = map_field
        img = pygame.image.load(get_static_file_path("character/down/0.png"))
        img = pygame.transform.scale(img, (int(img.get_width() * ZOOM / 2), int(img.get_height() * ZOOM / 2)))
        self.surface = img.convert_alpha()
        self.offset = Vector2(-1.5, -2.5)
        self.bullets: list[Bullet] = []

    def is_in_wall(self, x: int, y: int) -> bool:
        map_data = self.map_field.map_data
        if x < 0 or y < 0 or x >= map_data.size_x - 1 or y >= map_data.size_y - 1:
            return True
        chip_id = map_data.get_tile(x, y)
        chip = map_data.chipset.load_chip(chip_id)
        return chip is not None and not chip.passable

    def move(self):
        keys = pygame.key.get_pressed()
        movements = {
            True: {pygame.K_w: Vector2(0, -1), pygame.K_s: Vector2(0, 1), pygame.K_a: Vector2(-1, 0), pygame.K_d: Vector2(1, 0)},
            False: {pygame.K_UP: Vector2(0, -1), pygame.K_DOWN: Vector2(0, 1), pygame.K_LEFT: Vector2(-1, 0), pygame.K_RIGHT: Vector2(1, 0)}
        }
        for key, v in movements[GamePlayer.is_wasd].items():
            if keys[key]:
                new_pos = self.pos + v * self.move_speed
                if not self.is_in_wall(int(new_pos.x), int(new_pos.y)) and all(
                        0 <= new_pos[i] < self.map_field.map_data.size[i] - 1 for i in range(2)):
                    self.pos = new_pos
                    self.update_map_field_topleft()
        if pygame.mouse.get_pressed()[0] and self.cd == 0:
            self.cd = self.cd_max
            if len(self.bullets) < 20:
                self.shoot_bullet()
        if self.cd > 0:
            self.cd -= 1

    def update_map_field_topleft(self):
        topleft = [
            max(0, min(self.map_field.screen_size[i] - SCREEN_SIZE[i] - ZOOMED_CHIP,
                       self.pos[i] * ZOOMED_CHIP - SCREEN_SIZE[i] // 2))
            for i in range(2)
        ]
        self.map_field.update_topleft(topleft)

    def set_position(self, position):
        self.pos = Vector2(position)

    def shoot_bullet(self):
        target_pos = Vector2(pygame.mouse.get_pos())
        pos = Vector2(self.blit_local_pos)
        dxdy = target_pos - pos
        length = dxdy.length()
        speed = 0.1
        velocity = dxdy.normalize() * speed if length != 0 else Vector2(0, 0)
        bullet = Bullet(self.pos.x + self.offset.x, self.pos.y + self.offset.y, velocity)
        self.bullets.append(bullet)

    @property
    def blit_local_pos(self):
        map_field_pos = Vector2(self.map_field.current_topleft)
        pos = (self.pos + self.offset) * ZOOMED_CHIP - map_field_pos
        return [int(pos.x), int(pos.y)]

    def draw(self):
        self.display_surface.blit(self.surface, self.blit_local_pos)
        self.bullets = [bullet for bullet in self.bullets if not self._update_and_draw_bullet(bullet)]

    def _update_and_draw_bullet(self, bullet):
        bullet.move()
        # if (bullet.x < 0 or bullet.y < 0 or 
        #     bullet.x >= self.map_field.map_data.size_x - 1 or bullet.y >= self.map_field.map_data.size_y - 1):
        #     return True
        if (bullet.pos.x < 0 or bullet.pos.y < 0 or 
            bullet.pos.x >= self.map_field.map_data.size_x - 1 or bullet.pos.y >= self.map_field.map_data.size_y - 1):
            return True
        bullet.draw(self.map_field.view_surface, self.map_field.current_topleft)
        return False