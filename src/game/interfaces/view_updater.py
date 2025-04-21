from abc import ABCMeta, abstractmethod

class ViewUpdater(metaclass=ABCMeta):
    @abstractmethod
    def update(self) -> bool:
        pass