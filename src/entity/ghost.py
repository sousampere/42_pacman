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
        ghost_id: int,
        cheat_enabled: bool = False,
    ) -> None:
        Entity.__init__(self, spawn_point, SCALE)
        Movable.__init__(self, maze_path, speed)
        sheet = arcade.load_spritesheet("assets/entity/spritesheet.png")
        self.textures = sheet.get_texture_grid(
            size=(64, 64),
            columns=5,
            count=12,
        )
        self.texture = self.textures[ghost_id * 3]
        self.__is_edible: bool = False
        self._id: int = ghost_id
        self._is_dead: bool = False
        if cheat_enabled:
            self.switch_to_cheat_texture()

    def update(
        self,
        heat_map,
        max_x,
        max_y,
        occupied: frozenset[tuple[int, int]],
        delta_time: float = 1 / 60,
    ) -> None:
        arrived = self._move_toward_target(delta_time)
        if arrived:
            pos = (round(self._x), round(self._y))
            if self._is_dead and pos == self.spawn_point:
                self.respawn()
                return
            next_pos = Algorithms.process(
                pos,
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

    def respawn(self) -> None:
        self._is_dead = False
        self._x, self._y = self.spawn_point
        self.center_x = self._x
        self.center_y = self._y

    @property
    def is_edible(self) -> bool:
        return self.__is_edible

    @is_edible.setter
    def is_edible(self, value: bool) -> None:
        self.__is_edible = value

    def switch_to_cheat_texture(self) -> None:
        """Changes the texture of the player to cheat textures"""
        self.texture = self.textures[self._id + 4]
