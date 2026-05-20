from abc import ABC, abstractmethod

import arcade
from numpy import ndarray


class Entity(arcade.Sprite, ABC):
    def __init__(self, spawn_point: tuple[int, int], scale: float) -> None:
        arcade.Sprite.__init__(self, scale=scale)
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
        speed: float
    ) -> None:
        self.maze_path = maze_path
        self._path_set: frozenset[tuple[int, int]] = frozenset(
            (int(x), int(y)) for x, y in maze_path
        )
        self.dir: tuple[float, float] = (0, 0)
        self.speed: float = speed
        self._target: tuple[float, float] | None = None
        self._x: float
        self._y: float

    def can_move_to(self, x: float, y: float, size: tuple[int, int]) -> bool:
        return (round(x + size[0]), round(y + size[1])) in self._path_set and (
            round(x - size[0]),
            round(y - size[1]),
        ) in self._path_set

    def _move_toward_target(self, delta_time: float) -> bool:
        """Interpolates toward _target. Returns True when arrived."""
        if self._target is None:
            return True
        tx, ty = self._target
        step = delta_time / self.speed
        dx = tx - self._x
        dy = ty - self._y
        dist = (dx ** 2 + dy ** 2) ** 0.5
        if dist <= step:
            self._x, self._y = float(tx), float(ty)
            self._target = None
            return True
        self._x += dx / dist * step
        self._y += dy / dist * step
        return False


class Collectible(ABC):
    def __init__(self, score: int = 0) -> None:
        self.__score: int = score
        self.__already_collect: bool = False

    def collect(self) -> bool:
        if not self.__already_collect:
            self.__already_collect = True
            return True
        return False

    @abstractmethod
    def activate_power(self) -> None:
        pass

    @property
    def score(self) -> int:
        return self.__score
