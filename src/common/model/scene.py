

from dataclasses import dataclass


@dataclass
class TransitionType:
    
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description


@dataclass
class SceneBase:
    name: str

    def __repr__(self):
        return f"SceneBase(name={self.name}, description={self.description})"