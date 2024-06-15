import pygame, math
from support import import_folder
from entities import Bullet


# 銃のステータス：
#   火力：貫通する敵の数
#   弾速：玉の速さ


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, group) -> None:
        super().__init__(group)
        self.group = group

        # 移動特性
        self.direction = pygame.math.Vector2()
        self.speed = 300

        self.import_assets()
        self.status = "down"
        self.frame_index = 0

        self.image = self.animations[self.get_status()][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = pos

        self.pos = pygame.math.Vector2(self.rect.center)

        self.ct = 0

    def import_assets(self):
        self.animations = {'up': [],'down': [],'left': [],'right': [],
                            'right_idle':[],'left_idle':[],'up_idle':[],'down_idle':[]}

        for animation in self.animations.keys():
            full_path = 'graphics/character/' + animation
            self.animations[animation] = import_folder(full_path, (50, 100))

    def animate(self,dt):
        self.frame_index += 8 * dt
        status = self.get_status()
        if self.frame_index >= len(self.animations[status]):
            self.frame_index = 0
        self.image = self.animations[status][int(self.frame_index)]
    
    def shot(self):
        Bullet(self.pos, self.group, self.status)
        self.ct = 0
    
    def get_status(self) -> str:
        if self.direction.magnitude() > 0:
            return self.status
        else:
            return self.status + "_idle"

    def input(self):
        keys = pygame.key.get_pressed()
        st = True

        if keys[pygame.K_SPACE]:
            st = False
            if self.ct >= 20:
                self.shot()

        if keys[pygame.K_UP]:
            self.direction.y = -1
            if st:
                self.status = "up"
        elif keys[pygame.K_DOWN]:
            self.direction.y = 1
            if st:
                self.status = "down"
        else:
            self.direction.y = 0

        if keys[pygame.K_RIGHT]:
            self.direction.x = 1
            if st:
                self.status = "right"
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
            if st:
                self.status = "left"
        else:
            self.direction.x = 0


    def move(self,dt):

        # normalizing a vector 
        if self.direction.magnitude() > 0:
            self.direction = self.direction.normalize()

        # horizontal movement
        self.pos.x += self.direction.x * self.speed * dt
        self.rect.centerx = self.pos.x

        # vertical movement
        self.pos.y += self.direction.y * self.speed * dt
        self.rect.centery = self.pos.y


    def update(self, dt):
        self.input()
        self.move(dt)
        self.animate(dt)
        self.ct += 1
