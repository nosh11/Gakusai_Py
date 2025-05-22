
from abc import ABCMeta, abstractmethod
import yaml

class Model:
    @classmethod
    @abstractmethod
    def from_dict(cls, data: dict) -> 'Model':
        pass
    
    @abstractmethod
    def to_dict(self) -> dict:
        pass


def make_constructor(cls: type[Model]):
    def constructor(loader: yaml.Loader, node: yaml.MappingNode):
        data = loader.construct_mapping(node, deep=True)
        return cls.from_dict(data)
    return constructor

def make_representer(tag: str):
    def representer(dumper: yaml.Dumper, data: Model):
        return dumper.represent_mapping(tag, data.to_dict())
    return representer