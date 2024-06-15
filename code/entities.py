import pygame, math, random
from support import import_folder

class Bed(pygame.sprite.Sprite):
    def __init__(self, pos, group) -> None:
        super().__init__(group)
        self.image = pygame.transform.scale(pygame.image.load('img/bed.png'), (200, 200))
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
    
    def move(self,dt):
        pass

    def update(self, dt):
        pass
        #self.move(dt)




bullet_speed = {"up": (0, -1, 90), 
                "down": (0, 1, 270), 
                "right": (1, 0, 0), 
                "left": (-1, 0, 180)}

class Mob(pygame.sprite.Sprite):
    def __init__(self, pos, group, name, scale, speed) -> None:
        super().__init__(group)

        # 移動特性
        self.speed = speed
        self.velocity = (0, 0)

        self.import_assets(name, scale)
        self.status = "down"
        self.frame_index = 0

        self.image = self.animations[self.get_status()][self.frame_index]
        self.rect = self.image.get_rect()
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
            # horizontal movement
            self.pos.x += self.velocity[0] * self.speed * dt
            self.rect.centerx = self.pos.x

            # vertical movement
            self.pos.y += self.velocity[1] * self.speed * dt
            self.rect.centery = self.pos.y

        elif self.moving <= 0:
            self.status = random.choice(list(bullet_speed.keys()))
            self.velocity = tuple(bullet_speed[self.status][:2])
            self.moving = 1000

    def update(self, dt):
        self.move(dt)
        self.animate(dt)
        self.moving -= 1
class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos, group, d: str):
        super().__init__(group)
        self.spd = bullet_speed[d]
        self.image = pygame.transform.rotate(pygame.image.load('img/bullet.png'),self.spd[2])
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.hp = 1000
    def move(self,dt):
        self.rect.x += self.spd[0]
        self.rect.y += self.spd[1]

    def update(self, dt):
        self.move(dt)
        self.hp -= 1
        if self.hp <= 0:
            self.kill()
