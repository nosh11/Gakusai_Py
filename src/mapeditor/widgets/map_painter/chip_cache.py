from mapeditor.widgets.map_painter.chipset_image import get_chip_image

class SharedImageCache:
    """画像キャッシュを共有するためのクラス"""
    _cache = {}

    @classmethod
    def get_image(cls, chipset, tile_id):
        if tile_id not in cls._cache:
            cls._cache[tile_id] = get_chip_image(chipset, tile_id)
        return cls._cache[tile_id]

    @classmethod
    def clear_cache(cls):
        cls._cache.clear()