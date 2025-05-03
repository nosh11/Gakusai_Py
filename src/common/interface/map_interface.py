from abc import ABC, abstractmethod

class MapInterface(ABC):
    @abstractmethod
    def is_within_wall(self, pos: tuple[int, int]) -> bool:
        pass

    @abstractmethod
    def set_tile(self, pos: tuple[int, int], chip_id: int) -> bool:
        pass