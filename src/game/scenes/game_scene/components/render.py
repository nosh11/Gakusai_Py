


import pygame

from game.consts.screen_settings import SCREEN_SIZE


"""
レンダリングを効率化する為、2つの座標空間を定義する。

1. ゲーム内座標空間: ゲーム内の座標を表す空間。(x, y)
2. スクリーン座標空間: スクリーン上の座標を表す空間。<X, Y> = (x * ZOOMED_CHIP, y * ZOOMED_CHIP)

基本的に、ゲーム内座標空間を使用する。
ゲーム内座標空間は、スクリーン座標空間に変換されて描画される。

スクリーン座標空間は、スクリーンの左上を原点とし、右下に向かって増加する座標系である。
ゲーム内座標空間は、ゲーム内の座標を表す空間であり、左上を原点とし、右下に向かって増加する座標系である。
"""

class GameSceneRender:
    def __init__(self, map_field, player):
        self.map_field = map_field
        self.player = player
        self.topleft = [0, 0]
        self.render_surface = pygame.Surface(SCREEN_SIZE)
        self.render_surface.fill((0, 0, 0, 0))
    
