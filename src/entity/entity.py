from abc import ABC, abstractmethod

import arcade


class Entity(arcade.Sprite, ABC):
    def __init__(self, spawn_point: tuple[int, int]) -> None:
        self.spawn_point: tuple[int, int] = spawn_point
        self._x: float = float(spawn_point[0])
        self._y: float = float(spawn_point[1])

    @property
    def x(self) -> float:
        return self._x

    @property
    def y(self) -> float:
        return self._y


class Movable(ABC):
    def __init__(
        self,
        speed: float = 0.0,
    ) -> None:
        self.speed: float = speed

    @abstractmethod
    def move(self, direction: tuple[float, float]) -> None:
        pass

    @property
    def get_speed(self) -> float:
        return self.speed


class Collectible(ABC):
    def __init__(self, score: int = 0) -> None:
        self.score: int = score

    @abstractmethod
    def collect(self):
        pass

    @property
    def get_score(self) -> int:
        return self.score
