import arcade
from src.entity.entity import Entity, Movable


class Player(arcade.Sprite, Entity, Movable):
    def __init__(self, spawn_point: tuple[int, int], speed: float = 10):
        super().__init__("assets/entity/Pacman_base.png", scale=0.5)

        Entity.__init__(self, spawn_point)
        Movable.__init__(self, speed)

        self.textures_dir = {
            "left": arcade.load_texture("assets/entity/Pacman_base_left.png"),
            "right": arcade.load_texture("assets/entity/Pacman_base.png"),
        }
        self.center_x, self.center_y = spawn_point

    def move(self, direction: tuple[float, float]):
        dx, dy = direction
        self.change_x = dx * self.speed
        self.change_y = dy * self.speed

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
        super().update()

        if self.right > 800:
            self.right = 800
            self.change_x = 0

        elif self.left < 0:
            self.left = 0
            self.change_x = 0

        if self.top > 600:
            self.top = 600
            self.change_y = 0

        elif self.bottom < 0:
            self.bottom = 0
            self.change_y = 0
