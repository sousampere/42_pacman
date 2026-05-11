from abc import ABC, abstractmethod

import arcade
from numpy import ndarray


class Entity(arcade.Sprite, ABC):
    def __init__(self, spawn_point: tuple[int, int], scale) -> None:
        arcade.Sprite.__init__(
            self, scale=scale
        )
        self.spawn_point: tuple[int, int] = spawn_point
        self._x: float = float(spawn_point[0])
        self._y: float = float(spawn_point[1])
        self.center_x = self._x
        self.center_y = self._y

    @property
    def x(self) -> float:
        return self._x

    @property
    def y(self) -> float:
        return self._y


class Movable(ABC):
    def __init__(
        self,
        maze_path: ndarray,
        speed: float = 0.0,
    ) -> None:
        self.speed: float = speed
        self.maze_path = maze_path
        self._path_set: frozenset[tuple[int, int]] = frozenset(
            (int(x), int(y)) for x, y in maze_path
        )

    def can_move_to(self, x: float, y: float) -> bool:
        return (round(x), round(y)) in self._path_set

    @abstractmethod
    def move(self, direction: tuple[float, float]) -> None:
        pass

    @property
    def get_speed(self) -> float:
        return self.speed


class Collectible(ABC):
    def __init__(self, score: int = 0) -> None:
        self.__score: int = score
        self.__already_collect: bool = False

    def collect(self):
        if not self.__already_collect:
            self.__already_collect = True
            return True
        return False

    @abstractmethod
    def activate_power(self):
        pass

    @property
    def score(self) -> int:
        return self.__score
