import pytest

from src.common.game_map import load_map_data

"""
テストデータ:
    - マップ名: test_map
    - チップセット: test_chipset
    - サイズ: 10x10
    - チップマップ: 2次元配列 (10x10)
    - エンティティ: 空のリスト

"""


@pytest.mark.parametrize("map_name", ["test_map"])
def test_load_map_data(map_name):
    map_data = load_map_data(map_name)
    assert map_data is not None, "Map data should not be None"

