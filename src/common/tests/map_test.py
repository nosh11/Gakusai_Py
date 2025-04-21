import pytest
from common.game_map import load_map_data

@pytest.mark.parametrize("map_name", ["test_map"])
def test_load_map_data(map_name):
    map_data = load_map_data(map_name)
    assert map_data is not None, "Map data should not be None"
    assert map_data.name == "test_map", "Map name should be 'test_map'"
    assert map_data.size_x == 10, "Map width should be 10"
    assert map_data.size_y == 10, "Map height should be 10"
    assert map_data.chips_map is not None, "Chips map should not be None"
    assert len(map_data.chips_map) == 10, "Chips map height should be 10"
    assert len(map_data.chips_map[0]) == 10, "Chips map width should be 10"
    assert map_data.entities == [], "Entities should be an empty list"
    assert map_data.chipset is not None, "Chipset should not be None"
    assert map_data.chipset.chipset_id == "plains", "Chipset name should be 'test_chipset'"
