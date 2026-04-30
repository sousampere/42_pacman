import arcade
from src.entity.entity import Entity, Movable


class Player(arcade.Sprite, Entity, Movable):
    def __init__(self, spawn_point: tuple[int, int], speed: float = 10):
        arcade.Sprite.__init__(
            self, "assets/entity/Pacman_base.png", scale=0.5
        )
        Entity.__init__(self, spawn_point)
        Movable.__init__(self, speed)
        self.textures_dir = {
            "left": arcade.load_texture("assets/entity/Pacman_base_left.png"),
            "right": arcade.load_texture("assets/entity/Pacman_base.png"),
        }
        self.center_x = self._x
        self.center_y = self._y

    def move(self, direction: tuple[float, float]) -> None:
        dx, dy = direction
        self._x += dx * self.speed
        self._y += dy * self.speed
        if dx < 0:
            self.texture = self.textures_dir["left"]
            self.angle = 0
        elif dx > 0:
            self.texture = self.textures_dir["right"]
            self.angle = 0
        elif dy > 0:
            self.texture = self.textures_dir["right"]
            self.angle = -90
        elif dy < 0:
            self.texture = self.textures_dir["left"]
            self.angle = -90

    def update(self, delta_time: float = 1 / 60):
        self.center_x = self._x
        self.center_y = self._y
        if self.right > 800:
            self._x = 800 - self.width / 2
        if self.left < 0:
            self._x = self.width / 2
        if self.top > 600:
            self._y = 600 - self.height / 2
        if self.bottom < 0:
            self._y = self.height / 2
