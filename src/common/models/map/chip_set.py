from common.models.map.chip import Chip
from common.utils.file_manager import get_resource_file_path, get_static_file_path


class ChipSet:
    def __init__(self, chipset_id, chipset_image: str, chips: dict[int, Chip]):
        """
        チップセットを表現するクラス
        :param chipset_image: チップセット画像のIDまたはパス
        :param chips: チップのリスト
        """
        self.chipset_id = chipset_id
        self.chipset_image_id = chipset_image
        self.chips = chips

    def load_chip(self, chip_id: int) -> Chip:
        # 存在しない -> 新規作成
        if chip_id not in self.chips:
            chip = Chip(chip_id, True, -1, 0)
            self.chips[chip_id] = chip
        return self.chips[chip_id]

    
    @property
    def chipset_image_path(self) -> str:
        """
        チップセット画像のパスを取得するプロパティ
        :return: チップセット画像のパス
        """
        return get_static_file_path(f'chipset\\{self.chipset_image_id}.png')

def load_chipset(chipset_id: str) -> ChipSet:
    """
    チップセットを読み込む関数
    :param chipset_id: 読み込むチップセットのID
    :return: ChipSetオブジェクト
    """
    import yaml
    file_path = get_resource_file_path(f'chipset\\{chipset_id}.yml')
    print("file_path:", file_path)

    with open(file_path, 'r', encoding='utf-8') as f:
        chipset_yaml = yaml.safe_load(f)

        # チップセットの読み込み
        chipset = ChipSet(
            chipset_id=chipset_id,
            chipset_image=chipset_yaml['chipset_image'],
            chips={chip['id']: Chip(**chip) for chip in chipset_yaml['chips']}
        )

    return chipset


def save_chipset(chipset: ChipSet) -> None:
    """
    チップセットをYAMLファイルに保存する関数
    :param chipset: 保存するチップセット
    :param file_path: 保存先のファイルパス
    """
    import yaml
    file_path = get_resource_file_path(f'chipset\\{chipset.chipset_id}.yml')

    with open(file_path, 'w', encoding='utf-8') as f:
        yaml.dump({
            'chipset_image': chipset.chipset_image_id,
            'chips': [chip.__dict__ for chip in chipset.chips.values()]
        }, f, allow_unicode=True)