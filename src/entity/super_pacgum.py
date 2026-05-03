import arcade

from src.entity.entity import Collectible, Entity
from src.entity.pacgum import Pacgum

SCALE: float = 0.02
SCORE: int = 500


class SuperPacgum(Pacgum):
    def __init__(self, spawn_point: tuple[int, int]) -> None:
        arcade.Sprite.__init__(self, "assets/entity/super_pacgum.png", scale=SCALE)
        Entity.__init__(self, spawn_point)
        Collectible.__init__(self, score=SCORE)
        self.center_x = self._x
        self.center_y = self._y

    def activate_power(self):
        print("ULTIMATE POWAAAA")
