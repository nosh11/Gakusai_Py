from abc import ABCMeta, abstractmethod

from pygame import Surface

class ViewUpdater(metaclass=ABCMeta):
    @abstractmethod
    def update(self) -> bool:
        pass