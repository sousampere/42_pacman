from typing import Any

import arcade
from numpy import ndarray

from src.algorithms.algorithms import Algorithms
from src.entity.entity import Entity, Movable

WINDOWS_WIDTH: int = 800
WINDOWS_HEIGHT: int = 600


class Ghost(Entity, Movable):
    def __init__(
        self,
        spawn_point: tuple[int, int],
        maze_path: ndarray,
        speed: float,
        ghost_id: int,
    ) -> None:
        Entity.__init__(self, spawn_point)
        Movable.__init__(self, maze_path, speed)
        sheet = arcade.load_spritesheet("assets/entity/spritesheet.png")
        self.textures = sheet.get_texture_grid(
            size=(64, 64),
            columns=4,
            count=20,
        )
        self.texture = self.textures[ghost_id * 4]
        self._id: int = ghost_id
        self._is_dead: bool = False

    def update(
        self,
        delta_time: float = 1 / 60,
        *args: Any,
        heat_map: list[ndarray] | None = None,
        max_x: int = -1,
        max_y: int = -1,
        occupied: frozenset[tuple[int, int]] = frozenset(),
        **kwargs: Any,
    ) -> None:
        if heat_map is None:
            return
        arrived = self._move_toward_target(delta_time)
        if arrived:
            pos = (round(self._x), round(self._y))
            if self._is_dead and pos == self.spawn_point:
                self.respawn()
                return
            next_pos = Algorithms.process(
                pos,
                heat_map[self._id],
                max_x,
                max_y,
                excluded=occupied,
            )
            if next_pos is not None:
                self._target = (float(next_pos[0]), float(next_pos[1]))

    def die(self) -> None:
        self._is_dead = True
        self.switch_to_texture(3)

    def respawn(self) -> None:
        self._is_dead = False

    def switch_to_texture(self, id_textures: int) -> None:
        """Changes the texture of the player to textures"""
        self.texture = self.textures[self._id * 4 + id_textures]

    @property
    def is_dead(self) -> bool:
        return self._is_dead
