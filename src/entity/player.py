import arcade
from numpy import ndarray
from src.entity.entity import Entity, Movable

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
    def update(self, delta_time: float = 1 / 60) -> None:
        arrived = self._move_toward_target(delta_time)
        if arrived and self.dir != (0, 0):
            dx, dy = self.dir
            new_x = round(self._x) + dx
            new_y = round(self._y) + dy
            if self.can_move_to(new_x, new_y, self.scale):
                self._target = (float(new_x), float(new_y))
                if dx < 0:
                    self.texture = self.textures[4]
                elif dx > 0:
                    self.texture = self.textures[5]

    def die(self) -> None:
        self.respawn()

    def respawn(self) -> None:
        self._x, self._y = self.spawn_point
        self._target = None
        self.center_x = self._x
        self.center_y = self._y
