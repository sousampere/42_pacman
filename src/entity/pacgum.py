import arcade

from src.entity.entity import Collectible, Entity


class Pacgum(Entity, Collectible):
    def __init__(self, spawn_point: tuple[int, int]) -> None:
        Entity.__init__(self, spawn_point)
        Collectible.__init__(self)
        self.texture = arcade.load_texture("assets/entity/pacgum.png")

    def activate_power(self) -> None:
        pass
