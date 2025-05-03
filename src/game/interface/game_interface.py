from common.interface.map_interface import MapInterface
from common.interface.player_interface import PlayerInterface
from common.model.player import PlayerBase

class GameInterface:
    def __init__(self, map_data: MapInterface, player: PlayerInterface):
        self.__map: MapInterface = map_data
        self.__player: PlayerInterface = player

    def get_map(self) -> MapInterface:
        return self.__map
    
    def get_player(self) -> PlayerInterface:
        return self.__player

    def get_player_pos(self) -> tuple[float, float]:
        raise NotImplementedError("This method should be overridden in subclasses")
    
    def set_player_pos(self, pos: tuple[int, int]) -> None:
        raise NotImplementedError("This method should be overridden in subclasses")
    
    def transition_map(self, map_id: str) -> None:
        raise NotImplementedError("This method should be overridden in subclasses")