from abc import ABCMeta, abstractmethod


class Observable:
    def __init__(self):
        self.observers: list[Observer] = []

    def add_observer(self, observer):
        self.observers.append(observer)

    def remove_observer(self, observer):
        self.observers.remove(observer)

    def notify_observers(self, *args, **kwargs):
        for observer in self.observers:
            observer.update(self, *args, **kwargs)

class Observer:
    def update(self, o: Observable, id, *args, **kwargs):
        pass