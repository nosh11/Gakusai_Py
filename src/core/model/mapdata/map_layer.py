

from dataclasses import dataclass

from .chip_set import ChipSet


@dataclass
class MapLayer:
    chipset: ChipSet
    chip_array: list[list[int]]

    @classmethod
    def from_dict(cls, data: dict):
        data['chipset'] = ChipSet.from_dict(data['chipset'])
        data['chip_array'] = [list(row) for row in data['chip_array']]
        return cls(**data)