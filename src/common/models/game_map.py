__CHIPSIZE__ = 16  # チップのサイズ

from dataclasses import dataclass, field
from typing import List

import yaml
from common.models.map.chip_set import ChipSet, load_chipset
from common.models.map.entity import CEntity
from common.utils import get_resource_file_path
from common.utils.yaml_factory import make_constructor, make_representer

class InvalidMapDataError(Exception):
    def __init__(self, message: str):
        super().__init__(message)

@dataclass
class MapData:
    map_id: str
    chipset: ChipSet
    entities: List[CEntity] = field(default_factory=list)
    name: str = "Unnamed Map"
    size: tuple[int, int] = field(default_factory=lambda: (10, 10))
    chips_map: List[List[int]] = field(default_factory=lambda: [[0 for _ in range(10)] for _ in range(10)])
    init_pos: tuple[int, int] = field(default_factory=lambda: (0, 0))

    def to_dict(self):
        data = {
            'map_id': self.map_id,
            'chipset_id': self.chipset.chipset_id,
            'entities': [entity.to_dict() for entity in self.entities],
            'name': self.name,
            'size': list(self.size),
            'chips_map': self.chips_map,
            'init_pos': list(self.init_pos)
        }
        return data

    @classmethod
    def from_dict(cls, data):
        data['chipset'] = load_chipset(data['chipset_id'])
        del data['chipset_id']
        data['entities'] = [CEntity(**entity) for entity in data.get('entities', [])]
        data['size'] = tuple(data.get('size', (10, 10)))
        data['init_pos'] = tuple(data.get('init_pos', (0, 0)))
        return cls(**data)

    def is_within(self, pos: tuple[int, int]):
        return all(0 <= pos[i] < self.size[i] for i in range(2))

    def set_tile(self, pos: tuple[int, int], chip_id: int) -> bool:
        if self.is_within(pos):
            self.chips_map[pos[1]][pos[0]] = chip_id
            return True
        return False

    def get_tile(self, pos: tuple[int, int]) -> int | None:
        if self.is_within(pos):
            return self.chips_map[pos[1]][pos[0]]
        return None
        
    def resize(self, new_x, new_y):
        if new_x > self.size_x or new_y > self.size_y:
            # サイズを拡大する場合
            for y in range(self.size_y):
                self.chips_map[y].extend([0] * (new_x - self.size_x))
            self.chips_map.extend([[0] * new_x for _ in range(new_y - self.size_y)])
        else:
            # サイズを縮小する場合
            self.chips_map = [row[:new_x] for row in self.chips_map[:new_y]]
        self.size_x = new_x
        self.size_y = new_y

    # deprecated
    @property
    def size_x(self) -> int:
        return self.size[0]
    
    @property
    def size_y(self) -> int:
        return self.size[1]
    
    @size_x.setter
    def size_x(self, value: int) -> None:
        self.size = (value, self.size[1])

    @size_y.setter
    def size_y(self, value: int) -> None:
        self.size = (self.size[0], value)
    

yaml.add_representer(MapData, make_representer("!MapData"))
yaml.add_constructor("!MapData", make_constructor(MapData))

def load_map_data(map_id: str) -> MapData:
    """
    YAMLファイルからマップデータを読み込む関数
    :param map_id: 読み込むマップのID
    :return: MapDataオブジェクト
    """
    file_path = get_resource_file_path(f'map\\{map_id}.yaml')

    with open(file_path, 'r', encoding='utf-8') as f:
        map_data: MapData = yaml.load(f, Loader=yaml.FullLoader)
        if not isinstance(map_data, MapData):
            raise InvalidMapDataError(f"Invalid map data format for {map_id}. Expected MapData object.")
    return map_data

def save_map_data(map_data: MapData) -> None:
    """
    マップデータをYAMLファイルに保存する関数
    :param map_data: 保存するMapDataオブジェクト
    """
    file_path = get_resource_file_path(f'map\\{map_data.map_id}.yaml')

    with open(file_path, 'w', encoding='utf-8') as f:
        yaml.dump(map_data, f, default_flow_style=None, allow_unicode=True)  # allow_unicode=Trueで日本語を扱えるようにする