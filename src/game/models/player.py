from dataclasses import dataclass

from pygame import Vector2

from core.model.player import PlayerBase

@dataclass
class Player(PlayerBase):
    pos: Vector2 = Vector2(0, 0)

    def set_position(self, pos: tuple[float, float]):
        self.pos.x = pos[0]
        self.pos.y = pos[1]
        
    def get_position(self) -> tuple[float, float]:
        return self.pos.x, self.pos.y