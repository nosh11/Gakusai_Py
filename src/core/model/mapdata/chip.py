from dataclasses import dataclass

import yaml

@dataclass
class Chip:
    id: int = 0
    passable: bool = True
    durability: int = -1
    layer: int = 0

    def to_dict(self):
        return self.__dict__
    
    @classmethod
    def from_dict(cls, data):
        return cls(**data)
    
from util import make_constructor, make_representer
# YAMLのシリアライズとデシリアライズのための関数を登録
yaml.add_representer(Chip, make_representer('!Chip'))
yaml.add_constructor('!Chip', make_constructor(Chip))