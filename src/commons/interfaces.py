from abc import ABC, abstractmethod

class ViewUpdater(ABC):
    @abstractmethod
    def update(self) -> bool:
        pass