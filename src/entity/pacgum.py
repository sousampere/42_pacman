import arcade

from src.entity.entity import Collectible, Entity

SCALE: float = 1
SCORE: int = 50


class Pacgum(Entity, Collectible):
    def __init__(self, spawn_point: tuple[int, int]) -> None:
        arcade.Sprite.__init__(self, "assets/entity/pacgum.png", scale=SCALE)
        Entity.__init__(self, spawn_point)
        Collectible.__init__(self, score=SCORE)
        self.center_x = self._x
        self.center_y = self._y

    def activate_power(self):
        return super().activate_power()
