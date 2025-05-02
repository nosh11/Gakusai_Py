from dataclasses import dataclass
import yaml

from common.util.file_manager import get_user_data_file_path

@dataclass
class Achievement:
    name: str = ""
    description: str = ""
    unlocked: bool = False



@dataclass
class PlayerBase:
    id: int = 0
    name: str = ""
    level: int = 0
    experience: int = 0
    coins: int = 0
    items: list[str] = None
    achievements: list[Achievement] = None
    settings: dict[str, bool] = None

    def set_position(self, pos: tuple[int, int]):
        """
        Set the player's position.
        :param pos: A tuple containing the x and y coordinates.
        """
        raise NotImplementedError("This method should be overridden in subclasses")

    def get_position(self) -> tuple[int, int]:
        """
        Get the player's position.
        :return: A tuple containing the x and y coordinates.
        """
        raise NotImplementedError("This method should be overridden in subclasses")

    @classmethod
    def from_dict(cls, data: dict):
        data['id'] = int(data.get('id', 0))
        data['achievements'] = [Achievement(**achievement) for achievement in data.get('achievements', [])]
        data['items'] = data.get('items', [])
        return cls(**data)
    
    def to_dict(self) -> dict:
        data = {
            'id': self.id,
            'name': self.name,
            'level': self.level,
            'experience': self.experience,
            'coins': self.coins,
            'items': self.items or [],
            'achievements': [achievement.__dict__ for achievement in self.achievements] if self.achievements else [],
            'settings': self.settings or {},
        }
        return data

    def save(self):
        # save by yaml
        import yaml
        with open(get_user_data_file_path(str(self.id)), "w") as file:
            yaml.dump(self.to_dict(), file)
        print("User data saved successfully.")
        
        # ...existing code...
    @classmethod
    def load(cls, id=0):
        try:
            path = get_user_data_file_path(f"{id}.yaml")
            path = path.replace("\\", "/")
            with open(path, "r") as file:
                data = yaml.load(file, Loader=yaml.FullLoader)
            if data is None:
                data = {}
            return cls.from_dict(data)
        except Exception:
            return cls()