from dataclasses import dataclass, field
from typing import Any, List, Tuple

import yaml
from game.interface.game_interface import GameInterface
from common.util.yaml_factory import make_constructor, make_representer

class EventFunctionMeta(type):
    registry = {}

    def __new__(mcs, name, bases, attrs):
        cls = super().__new__(mcs, name, bases, attrs)
        if name != "EventFunction":
            tag = f"!{name}"
            EventFunctionMeta.registry[name.lower()] = cls
            yaml.add_representer(cls, make_representer(tag))
            yaml.add_constructor(tag, make_constructor(cls))
        return cls

class MapEventMeta(type):
    registry = {}

    def __new__(mcs, name, bases, attrs):
        cls = super().__new__(mcs, name, bases, attrs)
        if name != "MapEvent":
            tag = f"!{name}"
            MapEventMeta.registry[name.lower()] = cls
            yaml.add_representer(cls, make_representer(tag))
            yaml.add_constructor(tag, make_constructor(cls))
        return cls

@dataclass
class EventFunction(metaclass=EventFunctionMeta):
    function_type: str
    params: dict = field(default_factory=dict, init=False)

    def __init__(self, function_type: str, **kwargs: Any):
        self.function_type = function_type
        self.params = kwargs

    def execute(self, game_state: GameInterface, *args: Any, **kwargs: Any) -> None:
        raise NotImplementedError("This method should be overridden in subclasses")

@dataclass
class ChangeTileFunction(EventFunction):
    pos: Tuple[int, int]
    new_tile: int

    def __post_init__(self):
        self.function_type = "change_tile"
        self.params = {"pos": self.pos, "new_tile": self.new_tile}

    def execute(self, game_state: GameInterface, *args: Any, **kwargs: Any) -> None:
        map_interface = game_state.get_map()
        if map_interface.is_within(self.pos):
            map_interface.set_tile(self.pos, self.new_tile)
            print(f"Tile at {self.pos} changed to {self.new_tile}.")
        else:
            print(f"Position {self.pos} is out of bounds.")


@dataclass
class ShowMessageFunction(EventFunction):
    message: str

    def __post_init__(self):
        self.function_type = "show_message"
        self.params = {"message": self.message}

    def execute(self, *args: Any, **kwargs: Any) -> None:
        print(f"Message: {self.params['message']}")

@dataclass
class MapChangeFunction(EventFunction):
    pos: Tuple[int, int]
    new_map: str

    def __post_init__(self):
        self.function_type = "change_tile"
        self.params = {"pos": self.pos, "new_map": self.new_map}

    def execute(self, game_state: GameInterface, *args: Any, **kwargs: Any) -> None:
        game_state.transition_map(self.new_map)
        print(f"Map changed to {self.new_map} at position {self.pos}.")



@dataclass
class MapEvent(metaclass=MapEventMeta):
    event_type: str
    event_id: str
    event_name: str
    functions: List[EventFunction] = field(default_factory=list)

    def check(self, *args: Any, **kwargs: Any) -> bool:
        raise NotImplementedError("This method should be overridden in subclasses")
    
    def on_event(self, *args: Any, **kwargs: Any) -> None:
        for function in self.functions:
            function.execute(*args, **kwargs)

@dataclass
class PlayerStepOnEvent(MapEvent):
    pos: Tuple[int, int] = field(default_factory=tuple)

    def __post_init__(self):
        self.is_step_on = False
        self.event_type = "player_step_on"

    def check(self, player_pos: Tuple[int, int]) -> bool:
        if player_pos != self.pos:
            self.is_step_on = False
            return False
        if not self.is_step_on:
            self.is_step_on = True
            return True
        return False

@dataclass
class PeriodicEvent(MapEvent):
    interval: int = 0
    elapsed_time: int = 0

    def __post_init__(self):
        self.event_type = "periodic"

    def check(self, delta_time: int) -> None:
        self.elapsed_time += delta_time
        if self.elapsed_time >= self.interval:
            self.on_event()
            self.elapsed_time = 0