
import yaml

class Model:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    @classmethod
    def from_dict(cls, data):
        return cls(data['name'], data['age'])

    def to_dict(self):
        return {'name': self.name, 'age': self.age}


def make_constructor(cls: type[Model]):
    def constructor(loader: yaml.Loader, node: str):
        data = loader.construct_mapping(node, deep=True)
        return cls.from_dict(data)
    return constructor

def make_representer(tag: str):
    def representer(dumper: yaml.Dumper, data: Model):
        return dumper.represent_mapping(tag, data.to_dict())
    return representer