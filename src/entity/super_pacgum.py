import arcade

from src.entity.entity import Collectible, Entity
from src.entity.pacgum import Pacgum



class SuperPacgum(Pacgum):
    def __init__(self, spawn_point: tuple[int, int]) -> None:
        Entity.__init__(self, spawn_point)
        Collectible.__init__(self)
        self.texture = arcade.load_texture("assets/entity/super_pacgum.png")
