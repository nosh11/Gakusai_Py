import pygame, random
from support import import_folder
from settings import *

class Bed(pygame.sprite.Sprite):
    def __init__(self, pos, group_nocollide, group) -> None:
        super().__init__(group_nocollide)
        self.image = pygame.transform.scale(pygame.image.load('img/bed.png'), (200, 200))
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        self.collide = CollideBox(group,(pos[0]+20,pos[1]+80),(150,120))
    def move(self,dt):
        pass
    def update(self, dt):
        pass
class CollideBox(pygame.sprite.Sprite):
    def __init__(self, group, center, size) -> None:
        super().__init__(group)
        s = pygame.Surface(size)
        s.set_alpha(128)
        self.image = s
        self.rect = self.image.get_rect()
        self.rect.topleft = center
    def move(self,dt):
        pass
    def update(self, dt):
        pass

class Mob(pygame.sprite.Sprite):
    def __init__(self, pos, group, name, scale, speed) -> None:
        super().__init__(group)

        self.name = name

        self.group = group

        # 移動特性
        self.speed = speed
        self.velocity = (0, 0)

        self.import_assets(name, scale)
        self.status = "down"
        self.frame_index = 0

        self.image = self.animations[self.get_status()][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.size = (50, 50)
        self.rect.topleft = pos

        self.pos = pygame.math.Vector2(self.rect.center)

        self.moving = 1000
    
    def import_assets(self, name, scale):
        self.animations = {'up': [],'down': [],'left': [],'right': [],
                            'right_idle':[],'left_idle':[],'up_idle':[],'down_idle':[]}

        for animation in self.animations.keys():
            full_path = f'graphics/mobs/{name}/' + animation
            self.animations[animation] = import_folder(full_path, scale)

    def animate(self,dt):
        self.frame_index += 8 * dt
        if self.frame_index >= len(self.animations[self.get_status()]):
            self.frame_index = 0
        self.image = self.animations[self.get_status()][int(self.frame_index)]

    def get_status(self) -> str:
        if sum(self.velocity) > 0:
            return self.status
        else:
            return self.status + "_idle"
    
    def move(self,dt):
        if self.moving >= 750:
            current_pos = self.rect.center

            # horizontal movement
            self.pos.x += self.velocity[0] * self.speed * dt
            self.rect.centerx = self.pos.x

            # vertical movement
            self.pos.y += self.velocity[1] * self.speed * dt
            self.rect.centery = self.pos.y

            c = not(0 < self.pos.x < SCREEN_WIDTH) or not(0 < self.pos.y < SCREEN_HEIGHT)
            if (len(pygame.sprite.spritecollide(self, self.group, False)) >= 2) or c:
                self.pos.x, self.pos.y = current_pos
                self.rect.center = current_pos

        elif self.moving <= 0:
            self.status = random.choice(list(bullet_speed.keys()))
            self.velocity = tuple(bullet_speed[self.status][:2])
            self.moving = 1000

    def update(self, dt):
        self.move(dt)
        self.animate(dt)
        self.moving -= 1
class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos, group, d: str, status: dict):
        super().__init__(group)
        self.spd = bullet_speed[d]
        self.image = pygame.transform.rotate(pygame.image.load('img/bullet.png'),self.spd[2])
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.status = status
        self.hp = 1000
    def move(self,dt):
        self.rect.x += self.spd[0] * self.status["bullet_speed"]
        self.rect.y += self.spd[1] * self.status["bullet_speed"]

    def update(self, dt):
        self.move(dt)
        self.hp -= 1
        if self.hp <= 0:
            self.kill()
