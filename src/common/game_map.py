__CHIPSIZE__ = 16  # チップのサイズ

from common.utils.file_manager import get_static_file_path
from common.utils import get_resource_file_path


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
    def __init__(self, chipset_id, chipset_image: str, chips: dict[int, Chip]):
        """
        チップセットを表現するクラス
        :param chipset_image: チップセット画像のIDまたはパス
        :param chips: チップのリスト
        """
        self.chipset_id = chipset_id
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
    def __init__(self, entity_type: str, name: str, position: list, **kwargs):
        """
        エンティティ (敵やオブジェクト) を表現するクラス
        :param entity_type: エンティティの種類 (enemy, other)
        :param name: エンティティの名前
        :param init_x: 初期位置のX座標
        :param init_y: 初期位置のY座標
        """
        self.entity_type = entity_type
        self.name = name
        self.position = position  # [x, y]のリスト形式で位置を保持

class MapData:
    def __init__(self, map_id: str, path: str, name: str, chipset: ChipSet, size_x: int, size_y: int, chips_map: list[list[int]], entities: list[Entity]):
        """
        マップデータを表現するクラス
        :param name: マップの名前
        :param chipset: 使用するチップセット
        :param size_x: マップの横幅
        :param size_y: マップの縦幅
        :param chips_map: チップIDの2次元配列 (size_y × size_x)
        :param entities: マップ上のエンティティのリスト
        """
        self.map_id = map_id
        self.path = path
        self.name = name
        self.chipset = chipset
        self.size_x = size_x
        self.size_y = size_y
        self.chips_map = chips_map
        self.entities = entities
    
    def set_tile(self, x: int, y: int, chip_id: int) -> None:
        """
        指定した座標にチップをセットするメソッド
        :param x: X座標
        :param y: Y座標
        :param chip_id: セットするチップのID
        """
        if 0 <= x < self.size_x and 0 <= y < self.size_y:
            self.chips_map[y][x] = chip_id
        else:
            raise IndexError("指定された座標がマップの範囲外です。")

    def get_tile(self, x: int, y: int) -> int:
        """
        指定した座標のチップを取得するメソッド
        :param x: X座標
        :param y: Y座標
        :return: 指定した座標のチップ
        """
        if 0 <= x < self.size_x and 0 <= y < self.size_y:
            chip_id = self.chips_map[y][x]
            return chip_id
        else:
            raise IndexError("指定された座標がマップの範囲外です。")
        
    def resize(self, new_x, new_y):
        """
        マップのサイズを変更するメソッド
        :param new_x: 新しいX座標
        :param new_y: 新しいY座標
        """
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
                map_id=map_id,
                path=file_path,
                name=map_data_yaml['name'],
                chipset=chipset,
                size_x=map_data_yaml['size_x'],
                size_y=map_data_yaml['size_y'],
                chips_map=map_data_yaml['chips_map'],
                entities=entities
            )
        except KeyError as e:
            raise InvalidMapDataError(f"無効なマップデータ: {e}")
        except Exception as e:
            raise InvalidMapDataError(f"マップデータの読み込み中にエラーが発生しました: {e}")

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
            chipset_id=chipset_id,
            chipset_image=chipset_yaml['chipset_image'],
            chips={chip['id']: Chip(**chip) for chip in chipset_yaml['chips']}
        )

    return chipset


def save_map_data(map_data: MapData) -> None:
    """
    マップデータをYAMLファイルに保存する関数
    :param map_data: 保存するMapDataオブジェクト
    """
    import yaml
    file_path = map_data.path

    with open(file_path, 'w', encoding='utf-8') as f:
        yaml_data = {
            'name': map_data.name,
            'chipset': map_data.chipset.chipset_id,
            'size_x': map_data.size_x,
            'size_y': map_data.size_y,
            'chips_map': map_data.chips_map,
            'entities': [entity.__dict__ for entity in map_data.entities]
        }

        yaml.dump(yaml_data, f, allow_unicode=True, default_flow_style=None)
        print(f"マップデータを保存しました: {file_path}")