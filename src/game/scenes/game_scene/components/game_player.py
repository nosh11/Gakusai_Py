import pygame
from pygame.math import Vector2
from core.interface.player_interface import PlayerInterface
from core.model.player import PlayerBase
from util import get_asset_file_path
from game.consts.screen_settings import SCREEN_SIZE, ZOOM, ZOOMED_CHIP
from game.scenes.game_scene.components.map_field import MapField
class Bullet:
    def __init__(self, x, y, velocity: Vector2):
        self.pos = Vector2(x, y)
        self.velocity = velocity
        self.surface = pygame.Surface((10, 10))
        self.surface.fill((255, 0, 0))

    def move(self):
        self.pos += self.velocity

    def draw(self, surface, map_field_topleft):
        pos = self.pos * ZOOMED_CHIP - Vector2(map_field_topleft)
        surface.blit(self.surface, (int(pos.x), int(pos.y)))


class GamePlayer:
    is_wasd = True

    def __init__(self, display_surface: pygame.Surface, map_field: MapField, player: PlayerInterface):
        self.player = player
        self.pos = Vector2(0.0, 0.0)
        self.move_speed = 0.3
        self.display_surface: pygame.Surface = display_surface
        self.map_field = map_field
        img = pygame.image.load(get_asset_file_path("character/down/0.png"))
        img = pygame.transform.scale(img, (int(img.get_width() * ZOOM / 2), int(img.get_height() * ZOOM / 2)))
        self.surface = img.convert_alpha()
        self.offset = Vector2(0, 0)
        # Gun now handles bullets, so they are removed from GamePlayer
        self.gun_panel = Gun(self.display_surface, self)

    def is_in_wall(self, x: int, y: int) -> bool:
        map_data = self.map_field.map_data
        if x < 0 or y < 0 or x >= map_data.size[0] - 1 or y >= map_data.size[1] - 1:
            return True
        chip_id = map_data.get_tile((x, y))
        if (chip_id is None):
            return False
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
                if not self.is_in_wall(int(new_pos.x + 0.5), int(new_pos.y + 1.5)) and all(
                        0 <= new_pos[i] < self.map_field.map_data.size[i] - 1 for i in range(2)):
                    self.pos = new_pos
                    self.update_map_field_topleft()
        if pygame.mouse.get_pressed()[0]:
            self.gun_panel.shoot()

    def update_map_field_topleft(self):
        topleft = [
            max(0, min(self.map_field.screen_size[i] - SCREEN_SIZE[i] - ZOOMED_CHIP, self.pos[i] * ZOOMED_CHIP - SCREEN_SIZE[i] // 2))
            for i in range(2)
        ]
        self.map_field.update_topleft((topleft[0], topleft[1]))

    def set_position(self, pos: tuple[int, int]):
        self.pos = Vector2(pos[0], pos[1])
        self.update_map_field_topleft()

    @property
    def blit_local_pos(self):
        map_field_pos = Vector2(self.map_field.current_topleft)
        pos = (self.pos + self.offset) * ZOOMED_CHIP - map_field_pos
        return [int(pos.x), int(pos.y)]

    def draw(self):
        self.display_surface.blit(self.surface, self.blit_local_pos)
        self.gun_panel.draw()


class Gun:
    def __init__(self, display_surface, player: GamePlayer):
        self.display_surface = display_surface
        self.player = player

        # Load the gun image and scale it
        image_size = (ZOOMED_CHIP // 2, ZOOMED_CHIP // 2)
        self.image = pygame.Surface((ZOOMED_CHIP // 2, ZOOMED_CHIP // 2))
        self.image.fill((255, 255, 255))
        self.image = pygame.transform.scale(self.image, image_size)

        # Initialize cooldown and bullets
        self.cd = 0
        self.cd_max = 3
        self.bullets: list[Bullet] = []

    def shoot(self):
        if self.cd == 0: #and len(self.bullets) < 20:
            self.cd = self.cd_max
            pos = Vector2(self.player.pos) + self.direction
            dxdy = Vector2(pygame.mouse.get_pos()) - Vector2(self.player.blit_local_pos)
            speed = 0.5
            velocity = dxdy.normalize() * speed if dxdy.length() != 0 else Vector2(0, 0)
            self.bullets.append(Bullet(pos.x, pos.y, velocity))
    
    def update_pos(self):
        direction = Vector2(pygame.mouse.get_pos()) - Vector2(self.player.blit_local_pos)
        self.direction = direction.normalize() if direction.length() != 0 else Vector2(0, 0)

    def draw(self):
        self.update_pos()
        self.update_bullets()
        self.display_surface.blit(self.image, self.player.blit_local_pos + self.direction * ZOOMED_CHIP)

    def update_bullets(self):
        if self.cd > 0:
            self.cd -= 1

        # Update and draw bullets
        new_bullets = []
        for bullet in self.bullets:
            bullet.move()
            if (bullet.pos.x < 0 or bullet.pos.y < 0 or 
                bullet.pos.x >= self.player.map_field.map_data.size_x - 1 or bullet.pos.y >= self.player.map_field.map_data.size_y - 1 or
                self.player.is_in_wall(int(bullet.pos.x + 0.5), int(bullet.pos.y + 0.5))):
                continue
            bullet.draw(self.player.map_field.view_surface, self.player.map_field.current_topleft)
            new_bullets.append(bullet)
        self.bullets = new_bullets