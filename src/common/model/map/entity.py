from dataclasses import dataclass, asdict, field
import yaml
from common.util.yaml_factory import make_constructor, make_representer

class CEntityMeta(type):
    registry = {}

    def __new__(mcs, name, bases, attrs):
        cls = super().__new__(mcs, name, bases, attrs)
        if name != "CEntity":
            tag = f"!{name}"
            CEntityMeta.registry[name.lower()] = cls
            yaml.add_representer(cls, make_representer(tag))
            yaml.add_constructor(tag, make_constructor(cls))
        return cls

@dataclass
class CEntity(metaclass=CEntityMeta):
    name: str = "unnamed entity"
    position: list[float, float] = field(default_factory=lambda: [0.0, 0.0])

@dataclass
class LivingCEntity(CEntity):
    max_health: int = 10

@dataclass
class ImageEntity(CEntity):
    image_id: str = "none"