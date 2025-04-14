from commons.observe import Observable

class GameData(Observable):
    def __init__(self):
        super().__init__()
        self.__user_name = ""
        self.__user_score = 0
        self.__user_level = 1

    def get_user_name(self) -> str:
        return self.__user_name
    def set_user_name(self, name: str) -> None:
        self.__user_name = name
        self.notify_observers()

    def get_user_score(self) -> int:
        return self.__user_score
    def set_user_score(self, score: int) -> None:
        self.__user_score = score
        self.notify_observers()

    def get_user_level(self) -> int:
        return self.__user_level
    def set_user_level(self, level: int) -> None:
        self.__user_level = level 
        self.notify_observers()