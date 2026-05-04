import arcade

from src.entity.entity import Collectible, Entity
from src.entity.pacgum import Pacgum

SCALE: float = 0.02
SCORE: int = 500


class SuperPacgum(Pacgum):
    def __init__(self, spawn_point: tuple[int, int]) -> None:
        Entity.__init__(self, spawn_point, SCALE)
        Collectible.__init__(self, score=SCORE)
        self.texture = arcade.load_texture("assets/entity/super_pacgum.png")

    def activate_power(self):
        print("ULTIMATE POWAAAA")
