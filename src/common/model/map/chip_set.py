from dataclasses import dataclass, field

import yaml
from common.model.map.chip import Chip
from common.util.file_manager import get_resource_file_path, get_asset_file_path

@dataclass
class ChipSet:
    chipset_id: str
    chipset_image: str
    chips: dict[int, Chip] = field(default_factory=dict)

    def __post_init__(self):
        # チップセット画像のパスを取得
        self.chipset_image_path = get_asset_file_path(f'chipset\\{self.chipset_image}.png')

    def to_dict(self):
        return {
            'chipset_id': self.chipset_id,
            'chipset_image': self.chipset_image,
            'chips': {chip_id: chip.to_dict() for chip_id, chip in self.chips.items()}
        }
    
    @classmethod
    def from_dict(cls, data):
        chipset_id = data['chipset_id']
        chipset_image = data['chipset_image']
        chips = {int(chip_id): Chip.from_dict(chip) for chip_id, chip in data['chips'].items()}
        return cls(chipset_id, chipset_image, chips)

    def load_chip(self, chip_id: int) -> Chip:
        # 存在しない -> 新規作成
        if chip_id not in self.chips:
            chip = Chip(chip_id, True, -1, 0)
            self.chips[chip_id] = chip
        return self.chips[chip_id]
    
from common.util.yaml_factory import make_constructor, make_representer
# YAMLのシリアライズとデシリアライズのための関数を登録
yaml.add_representer(ChipSet, make_representer('!ChipSet'))
yaml.add_constructor('!ChipSet', make_constructor(ChipSet))

def load_chipset(chipset_id: str) -> ChipSet:
    """
    チップセットデータをYAMLファイルから読み込む関数
    :param chipset_id: チップセットのID
    :return: ChipSetオブジェクト
    """
    file_path = get_resource_file_path(f'chipset\\{chipset_id}.yaml')
    with open(file_path, 'r', encoding='utf-8') as file:
        data = yaml.safe_load(file)
        return ChipSet.from_dict(data)

def save_chipset(chipset: ChipSet) -> None:
    """
    チップセットデータをYAMLファイルに保存する関数
    :param chipset: 保存するChipSetオブジェクト
    """
    file_path = get_resource_file_path(f'chipset\\{chipset.chipset_id}.yaml')
    with open(file_path, 'w', encoding='utf-8') as file:
        data = chipset.to_dict()
        yaml.dump(data, file, default_flow_style=False, allow_unicode=True)


if __name__ == "__main__":
    # テスト用のチップセットデータを作成
    chipset = ChipSet(
        chipset_id="test_chipset",
        chipset_image="chip1",
        chips={}
    )
    # チップを追加
    chipset.load_chip(1)
    chipset.load_chip(2)

    # YAMLファイルに保存
    save_chipset(chipset)

    # YAMLファイルから読み込み
    loaded_chipset = load_chipset("test_chipset")
    print(loaded_chipset)