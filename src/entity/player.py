import arcade
from numpy import ndarray
from src.entity.entity import Entity, Movable
from typing import Optional

SCALE: float = 0.5
LIVES: int = 3
WINDOWS_WIDTH: int = 800
WINDOWS_HEIGHT: int = 600


class Player(Entity, Movable):
    def __init__(
        self,
        spawn_point: tuple[int, int],
        maze_path: ndarray,
        speed: float
    ):
        Entity.__init__(self, spawn_point, SCALE)
        Movable.__init__(self, maze_path, speed)
        sheet = arcade.load_spritesheet("assets/entity/spritesheet.png")
        self.textures = sheet.get_texture_grid(
            size=(66, 66),
            columns=1,
            count=6,
        )
        self.texture = self.textures[4]
        self._lives: int = LIVES
        self.move_cooldown = 0.0

    def move(self, direction: tuple[float, float]) -> None:
        dx, dy = direction
        new_x = self._x + dx
        new_y = self._y + dy

        if self.can_move_to(new_x, new_y, self.scale):
            if direction[0] == 0:
                self._y = new_y
            if direction[1] == 0:
                self._x = new_x
        else:
            self._x = round(self._x)
            self._y = round(self._y)
            self.cache_dir = (0, 0)

        if dx < 0:
            self.texture = self.textures[4]
        elif dx > 0:
            self.texture = self.textures[5]

    def update(self, delta_time: float = 1 / 60) -> None:
        self.move_cooldown += delta_time

        if self.move_cooldown >= self.speed:
            self.move(self.dir)
            self.move_cooldown = 0.0

    def die(self) -> None:
        self.respawn()

    def respawn(self) -> None:
        self._x, self._y = self.spawn_point

        self.center_x = self._x
        self.center_y = self._y
