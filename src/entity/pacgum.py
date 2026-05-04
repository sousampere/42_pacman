import arcade

from src.entity.entity import Collectible, Entity

SCALE: float = 1
SCORE: int = 50


class Pacgum(Entity, Collectible):
    def __init__(self, spawn_point: tuple[int, int]) -> None:
        Entity.__init__(self, spawn_point, SCALE)
        Collectible.__init__(self, score=SCORE)
        self.texture = arcade.load_texture("assets/entity/pacgum.png")

    def activate_power(self):
        return super().activate_power()
