

class MapInterface:
    def is_within(self, pos: tuple[int, int]) -> bool:
        """
        Check if the given position is within the map boundaries.
        """
        raise NotImplementedError("This method should be overridden in subclasses")

    def set_tile(self, pos: tuple[int, int], chip_id: int) -> bool:
        """
        Set the tile at the given position to the specified chip ID.
        """
        raise NotImplementedError("This method should be overridden in subclasses")