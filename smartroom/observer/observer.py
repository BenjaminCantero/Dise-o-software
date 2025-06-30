from typing import Any, Protocol, List

class Observer(Protocol):
    def update(self, event: str, data: Any) -> None:
        ...

class Subject:
    def __init__(self):
        self._observers: List[Observer] = []

    def attach(self, observer: Observer) -> None:
        self._observers.append(observer)

    def detach(self, observer: Observer) -> None:
        self._observers.remove(observer)

    def notify(self, event: str, data: Any) -> None:
        for observer in self._observers:
            observer.update(event, data)