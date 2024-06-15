import pygame
from settings import *

def change_brightness(image, brighten):
    # 画像をコピーして、変更後の画像を保持
    new_image = image.copy()
    # 画像の幅と高さを取得
    width, height = new_image.get_size()
    
    # ピクセルごとに明度を変更
    for x in range(width):
        for y in range(height):
            # ピクセルの色を取得
            r, g, b, a = new_image.get_at((x, y))
            # 明度を変更し、新しい値を0から255の範囲にクリップ
            r = max(0, min(255, r + brighten))
            g = max(0, min(255, g + brighten))
            b = max(0, min(255, b + brighten))
            # 新しい色を設定
            new_image.set_at((x, y), (r, g, b, a))
    
    return new_image

def text_button(img, font, text):
    new_img = img.copy()
    text_surface = font.render(text,True,(255,255,255))
    pos = ((new_img.get_rect().size[0]-text_surface.get_rect().size[0])//2,
           (new_img.get_rect().size[1]-text_surface.get_rect().size[1])//2)
    new_img.blit(text_surface, pos)
    return new_img
class Button:
    def __init__(self, x, y, image, scale, text=None):
        width = image.get_width()
        height = image.get_height()
        self.img = pygame.transform.scale(image, (int(width*scale),int(height*scale)))
        if text:
            self.img = text_button(self.img, pygame.font.Font('font/TsukimiRounded-Medium.ttf', 32), text)
        self.image = self.img
        self.image_brighten = change_brightness(self.img, 50)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False

    def draw(self):
        action = False
        pos = pygame.mouse.get_pos()
        collide = self.rect.collidepoint(pos)
        if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
            self.clicked = True
            action = collide
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False
        if collide:
            self.image = self.image_brighten
        else:
            self.image = self.img
        pygame.display.get_surface().blit(self.image, (self.rect.x, self.rect.y))
        return action