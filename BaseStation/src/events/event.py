from src.events.event_observer import EventObserver


class Event:
    def __init__(self, name: str, *data):
        self.name = name
        self.data = data

        self.trigger()

    def trigger(self):
        for observer in EventObserver.Observers:
            if self.name in observer.observables:
                observer.observables[self.name](*self.data)
