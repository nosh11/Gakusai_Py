import pygame, math
from support import import_folder
from entities import *
from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, group, name="apple") -> None:
        super().__init__(group)
        self.group: pygame.sprite.Group = group
        self.name = name

        self.bullet_group = pygame.sprite.Group()
        self.apple_group: pygame.sprite.Group = pygame.sprite.Group()
        self.display_surface = pygame.display.get_surface()

        self.direction = pygame.math.Vector2()
        self.speed = 350

        self.import_assets()
        self.status = "down"
        self.frame_index = 0

        self.image = self.animations[self.get_status()][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = pos

        self.pos = pygame.math.Vector2(self.rect.center)

        self.space = False
        self.can_move = True

        self.score = 0
        self.high_score = 0
        self.font = pygame.font.Font('font/unifont.otf', 32)

        self.timer = 0

        self.ct = 0

        Apple(self.apple_group, name="dame")

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
        Bullet(self.pos, self.bullet_group, d=self.status)
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
            if self.ct >= 0.5:
                self.shot()
            if not self.space:
                self.space = True
                for sprite in self.group.sprites():
                    if pygame.sprite.collide_circle(self,sprite):
                        if isinstance(sprite, Mob):
                            sprite.speak()
        else:
            self.space = False
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
        current_pos = self.rect.center

        dx = self.direction.x * self.speed * dt
        #dy = 0
        self.pos.x += dx
        self.rect.centerx = self.pos.x
        if not(0 < self.pos.x < SCREEN_WIDTH) or (len(pygame.sprite.spritecollide(self, self.group, False)) >= 2):
            if self.can_move:
                self.pos.x = current_pos[0]
                self.rect.centerx = current_pos[0]
        #self.pos.y += dy
        #self.rect.centery = self.pos.y
        #if not(0 < self.pos.y < SCREEN_HEIGHT) or (len(pygame.sprite.spritecollide(self, self.group, False)) >= 2):
            #if self.can_move:
                #self.pos.y = current_pos[1]
                #self.rect.centery = current_pos[1]



    def update(self, dt):
        self.input()
        self.move(dt)
        self.animate(dt)


        bullet_list = list(self.bullet_group.spritedict.keys())
        bullet_list.append(self)
        for a in self.apple_group.spritedict.keys():
            skip = False
            for b in bullet_list:
                if math.sqrt((a.rect.centerx-b.rect.centerx)**2+(a.rect.centery-b.rect.centery)**2)<=50:
                    a.repos()
                    b.hp = 0
                    if a.name == "apple":
                        self.score += 1
                        if self.score > self.high_score:
                            self.high_score = self.score
                    elif a.name == "dame":
                        self.score = 0
                    skip = True
                    break
            
            if not skip and a.rect.centery > SCREEN_HEIGHT + 50:
                a.repos()
                if a.name == "apple":
                    self.score = 0
                elif a.name == "dame":
                    self.score += 1
                    if self.score > self.high_score:
                        self.high_score = self.score

        if len(self.apple_group) < 3:
            self.timer += dt
            if self.timer >= 2:
                print("Apple Spawned!")
                Apple(self.apple_group)
                self.timer = 0
        self.apple_group.draw(self.display_surface)
        self.apple_group.update(dt)
        

        self.display_surface.blit(self.font.render(f"SCORE: {self.score}",True,(0,0,0)),(SCREEN_WIDTH//2, 10))
        self.display_surface.blit(self.font.render(f"HIGHSCORE: {self.high_score}",True,(0,0,0)),(SCREEN_WIDTH//2, 50))

        self.bullet_group.draw(self.display_surface)
        self.bullet_group.update(dt)
        self.ct += dt
