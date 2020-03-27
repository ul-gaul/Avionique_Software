import abc


class EventObserver:
    __metaclass__ = abc.ABCMeta

    Observers = []

    def __init__(self):
        self.Observers.append(self)
        self.observables = {}

    def observe(self, event_name: str, callback):
        self.observables[event_name] = callback
