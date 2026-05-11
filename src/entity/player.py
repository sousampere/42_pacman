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
        speed: float = 10,
    ):
        Entity.__init__(self, spawn_point, SCALE)
        Movable.__init__(self, maze_path, speed)
        sheet = arcade.load_spritesheet("assets/entity/spritesheet.png")
        self.textures = sheet.get_texture_grid(
            size=(396, 66),
            columns=1,
            count=6,
        )
        self.texture = self.textures[4]
        self._lives: int = LIVES

    def move(self, direction: tuple[float, float]) -> None:
        dx, dy = direction
        self._x += dx * self.speed
        self._y += dy * self.speed
        if dx < 0:
            self.texture = self.textures[0]
            self.angle = 0
        elif dx > 0:
            self.texture = self.textures[0]
            self.angle = 0
        elif dy > 0:
            self.texture = self.textures[0]
            self.angle = -90
        elif dy < 0:
            self.texture = self.textures[0]
            self.angle = -90

    def update(self, delta_time: float = 1 / 60):
        if self.right > WINDOWS_WIDTH:
            self._x = WINDOWS_WIDTH - self.width / 2
        if self.left < 0:
            self._x = self.width / 2
        if self.top > WINDOWS_HEIGHT:
            self._y = WINDOWS_HEIGHT - self.height / 2
        if self.bottom < 0:
            self._y = self.height / 2

    def die(self) -> None:
        self._lives -= 1
        if self._lives == 0:
            raise NotImplementedError("GAME OVER A IMPLEMENTER")
        self.respawn()

    def respawn(self) -> None:
        self._x, self._y = self.spawn_point

        self.center_x = self._x
        self.center_y = self._y
