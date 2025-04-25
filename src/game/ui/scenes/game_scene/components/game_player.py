import pygame

from common.consts.screen_settings import CHIP_SIZE
from common.utils.file_manager import get_static_file_path
from game.commons.widget import UIWidget
from game.consts.screen_settings import SCREEN_HEIGHT, SCREEN_WIDTH, ZOOM
from game.ui.scenes.game_scene.components.map_field import MapField

class Bullet:
    def __init__(self, x, y, velocity):
        self.x = x
        self.y = y
        self.velocity = velocity
        self.surface = pygame.Surface((10, 10))
        self.surface.fill((255, 0, 0))

    def move(self):
        self.x += self.velocity[0]
        self.y += self.velocity[1]

    def draw(self, surface):
        surface.blit(self.surface, (self.x, self.y))

class GamePlayer:
    is_wasd = True
    def __init__(self, map_field: MapField):
        self.x = 0
        self.y = 0
        self.cd = 0
        self.cd_max = 3
        self.map_field = map_field
        img = pygame.image.load(get_static_file_path("character/down/0.png"))
        img = pygame.transform.scale(img, (img.get_width() * 1, img.get_height() * 1))
        self.surface = img.convert_alpha()

        self.bullets: list[Bullet] = []
    
    def is_in_wall(self, x, y):
        map_data = self.map_field.map_data
        x = int(x / (CHIP_SIZE * ZOOM)+ 0.5)
        y = int(y / (CHIP_SIZE * ZOOM)+ 1.5)
        if x < 0 or y < 0 or x >= map_data.size_x - 1 or y >= map_data.size_y - 1:
            return True
        chip_id = map_data.get_tile(x, y)
        chip = map_data.chipset.load_chip(chip_id)
        if chip is not None:
            if not chip.passable:
                return True
        return False

    def move(self):
        keys = pygame.key.get_pressed()
        movements = {
            True: {pygame.K_w: (0, -10), pygame.K_s: (0, 10), pygame.K_a: (-10, 0), pygame.K_d: (10, 0)},
            False: {pygame.K_UP: (0, -10), pygame.K_DOWN: (0, 10), pygame.K_LEFT: (-10, 0), pygame.K_RIGHT: (10, 0)}
        }
        for key, (dx, dy) in movements[GamePlayer.is_wasd].items():
            if keys[key]:
                self.x += dx
                self.y += dy

                if self.is_in_wall(self.x, self.y):
                    self.x -= dx
                    self.y -= dy

                self.x = max(0, min(self.x, SCREEN_WIDTH - self.surface.get_width()))
                self.y = max(0, min(self.y, SCREEN_HEIGHT - self.surface.get_height()))

        # マウスを押している間は弾を撃つ
        if pygame.mouse.get_pressed()[0]:
            # クールダウンが終わっている場合のみ弾を撃つ
            if self.cd == 0:
                self.cd = self.cd_max
                # マウスの位置を取得
                mouse_x, mouse_y = pygame.mouse.get_pos()
                self.shoot_bullet(mouse_x, mouse_y)
        # クールダウンを減らす
        if self.cd > 0:
            self.cd -= 1
    
    def set_position(self, position):
        self.x = position[0] * ZOOM * CHIP_SIZE
        self.y = position[1] * ZOOM * CHIP_SIZE
        
        
        
    def shoot_bullet(self, target_x=0, target_y=0):
        # Calculate normalized velocity vector
        dx, dy = target_x - self.x, target_y - self.y
        length = (dx ** 2 + dy ** 2) ** 0.5
        speed = 20  # Bullet speed
        velocity = (dx / length * speed, dy / length * speed) if length != 0 else (0, 0)

        # Add new bullet to the list
        self.bullets.append(Bullet(self.x + self.surface.get_width() // 2, self.y + self.surface.get_height() // 2, velocity))
        print(f"Bullet created at ({self.bullets[-1].x}, {self.bullets[-1].y}) with velocity {self.bullets[-1].velocity}")

    def draw(self):
        # self.view_surface.blit(self.surface, (self.x, self.y))
        self.map_field.view_surface.blit(self.surface, (self.x, self.y))

        # Update and draw bullets
        self.bullets = [bullet for bullet in self.bullets if not self._update_and_draw_bullet(bullet)]

    def _update_and_draw_bullet(self, bullet):
        bullet.move()
        if bullet.x < 0 or bullet.x > SCREEN_WIDTH or bullet.y < 0 or bullet.y > SCREEN_HEIGHT:
            return True  # Remove bullet if out of bounds
        # 壁
        if self.is_in_wall(bullet.x, bullet.y):
            return True
        bullet.draw(self.map_field.view_surface)
        return False
