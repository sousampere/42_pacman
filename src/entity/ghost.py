from typing import Callable

import arcade
from numpy import ndarray

from src.algorithms.algorithms import Algorithms
from src.entity.entity import Entity, Movable

SCALE: float = 0.5
LIVES: int = 3
WINDOWS_WIDTH: int = 800
WINDOWS_HEIGHT: int = 600


class Ghost(Entity, Movable):
    def __init__(
        self,
        spawn_point: tuple[int, int],
        maze_path: ndarray,
        speed: float,
        # chase_algorithm: Algorithms,
    ) -> None:
        Entity.__init__(self, spawn_point, SCALE)
        Movable.__init__(self, maze_path, speed)
        sheet = arcade.load_spritesheet("assets/entity/spritesheet.png")
        self.textures = sheet.get_texture_grid(
            size=(66, 66),
            columns=1,
            count=6,
        )
        self.texture = self.textures[0]
        self.__is_edible: bool = False
        # self._chase_algorithm: Callable = Algorithms.process
        self.move_cooldown = 0.0

    def move(self, direction: tuple[float, float]) -> None:
        dx, dy = direction
        new_x = dx
        new_y = dy

        if self.can_move_to(new_x, new_y, self.scale):
            self._y = new_y
            self._x = new_x
        else:
            self._x = round(self._x)
            self._y = round(self._y)
            self.cache_dir = (0, 0)

    def update(self, delta_time: float, heat_map, max_x, max_y) -> None:
        self.move_cooldown += delta_time

        if self.move_cooldown >= self.speed:
            next_case = Algorithms.process((int(self._x), int(self._y)), (int(self._x), int(self._y)), heat_map, max_x, max_y)
            print(next_case)
            self.move(next_case)
            self.move_cooldown = 0.0

    def die(self) -> None:
        if self.__is_edible:
            self.respawn()

    def respawn(self) -> None:
        self._x, self._y = self.spawn_point

        self.center_x = self._x
        self.center_y = self._y

    @property
    def is_edible(self) -> bool:
        return self.__is_edible

    @is_edible.setter
    def is_edible(self, value: bool) -> None:
        self.__is_edible = value
