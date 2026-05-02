import arcade
from src.entity.entity import Entity, Movable

SCALE: float = 0.5
LIVES: int = 3
WINDOWS_WIDTH: int = 800
WINDOWS_HEIGHT: int = 600


class Player(Entity, Movable):
    def __init__(self, spawn_point: tuple[int, int], speed: float = 10):
        arcade.Sprite.__init__(
            self, scale=SCALE
        )
        Entity.__init__(self, spawn_point)
        Movable.__init__(self, speed)
        sheet = arcade.load_spritesheet("assets/entity/pacman.png")
        self.textures = sheet.get_texture_grid(
            size=(128, 128),
            columns=5,
            count=5,
        )
        self.texture = self.textures[0]
        self.center_x = self._x
        self.center_y = self._y
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
        self.center_x = self._x
        self.center_y = self._y
        if self.right > WINDOWS_WIDTH:
            self._x = WINDOWS_WIDTH - self.width / 2
            self.die()  # test
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
