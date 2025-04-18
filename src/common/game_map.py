__CHIPSIZE__ = 16  # チップのサイズ

from common.utils.file_manager import get_static_file_path
from src.common.utils import get_resource_file_path


class Chip:
    def __init__(self, id: int, passable: bool, durability: int, layer: int, **kwargs):
        """
        チップの基本情報を表現するクラス
        :param passable: 通行可能かどうか
        :param durability: 耐久値 (-1: イミュータブル, 0以上: 壊れるまでの攻撃回数)
        :param layer: レイヤー (数値が高いほど上に表示)
        """
        self.id: int = id
        self.passable = passable
        self.durability = durability
        self.layer = layer

class ChipSet:
    def __init__(self, chipset_image: str, chips: dict[int, Chip]):
        """
        チップセットを表現するクラス
        :param chipset_image: チップセット画像のIDまたはパス
        :param chips: チップのリスト
        """
        self.chipset_image = chipset_image
        self.chips = chips
    
    @property
    def chipset_image_path(self) -> str:
        """
        チップセット画像のパスを取得するプロパティ
        :return: チップセット画像のパス
        """
        return get_static_file_path(f'chipset\\{self.chipset_image}.png')
        

class Entity:
    def __init__(self, type: str, name: str, position: list, **kwargs):
        """
        エンティティ (敵やオブジェクト) を表現するクラス
        :param entity_type: エンティティの種類 (enemy, other)
        :param name: エンティティの名前
        :param init_x: 初期位置のX座標
        :param init_y: 初期位置のY座標
        """
        self.entity_type = type
        self.name = name
        self.position = position  # [x, y]のリスト形式で位置を保持

class MapData:
    def __init__(self, name: str, chipset: ChipSet, size_x: int, size_y: int, chips_map: list[list[int]], entities: list[Entity]):
        """
        マップデータを表現するクラス
        :param name: マップの名前
        :param chipset: 使用するチップセット
        :param size_x: マップの横幅
        :param size_y: マップの縦幅
        :param chips_map: チップIDの2次元配列 (size_y × size_x)
        :param entities: マップ上のエンティティのリスト
        """
        self.name = name
        self.chipset = chipset
        self.size_x = size_x
        self.size_y = size_y
        self.chips_map = chips_map
        self.entities = entities

    def get_tile(self, x: int, y: int) -> Chip:
        """
        指定した座標のチップを取得するメソッド
        :param x: X座標
        :param y: Y座標
        :return: 指定した座標のチップ
        """
        if 0 <= x < self.size_x and 0 <= y < self.size_y:
            chip_id = self.chips_map[y][x]
            return self.chipset.chips[chip_id]
        else:
            raise IndexError("指定された座標がマップの範囲外です。")


# exception
class InvalidMapDataError(Exception):
    """無効なマップデータエラー"""
    def __init__(self, message: str):
        super().__init__(message)




def load_map_data(map_id: str) -> MapData:
    """
    YAMLファイルからマップデータを読み込む関数
    :param file_path: 読み込むYAMLファイルのパス
    :return: MapDataオブジェクト
    """
    import yaml
    file_path = get_resource_file_path(f'map\\{map_id}.yml')

    with open(file_path, 'r', encoding='utf-8') as f:
        map_data_yaml = yaml.safe_load(f)


        try:
            # チップセットの読み込み
            chipset = load_chipset(map_data_yaml['chipset'])

            # エンティティの読み込み
            entities = [Entity(**entity) for entity in map_data_yaml['entities']]

            # マップデータの読み込み
            map_data = MapData(
                name=map_data_yaml['name'],
                chipset=chipset,
                size_x=map_data_yaml['size_x'],
                size_y=map_data_yaml['size_y'],
                chips_map=map_data_yaml['chips_map'],
                entities=entities
            )
        except KeyError as e:
            raise InvalidMapDataError(f"無効なマップデータ: {e}")

    return map_data

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
            chipset_image=chipset_yaml['chipset_image'],
            chips={chip['id']: Chip(**chip) for chip in chipset_yaml['chips']}
        )

    return chipset