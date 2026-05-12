
import arcade
from numpy import ndarray

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
        # self._chase_algorithm: Algorithms = chase_algorithm

    def move(self, direction: tuple[float, float]) -> None:
        # dx, dy = self._chase_algorithm.process(
        #     (self.center_x, self.center_y), direction
        # )

        # self._x += dx * self.speed
        # self._y += dy * self.speed
        # if dx < 0:
        #     self.texture = self.textures[0]
        #     self.angle = 0
        # elif dx > 0:
        #     self.texture = self.textures[0]
        #     self.angle = 0
        # elif dy > 0:
        #     self.texture = self.textures[0]
        #     self.angle = -90
        # elif dy < 0:
        #     self.texture = self.textures[0]
        #     self.angle = -90
        pass

    def update(self, delta_time: float = 1 / 60) -> None:
        if self.right > WINDOWS_WIDTH:
            self._x = WINDOWS_WIDTH - self.width / 2
        if self.left < 0:
            self._x = self.width / 2
        if self.top > WINDOWS_HEIGHT:
            self._y = WINDOWS_HEIGHT - self.height / 2
        if self.bottom < 0:
            self._y = self.height / 2

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
