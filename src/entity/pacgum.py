import arcade

from src.entity.entity import Collectible, Entity

SCALE: int = 1
SCORE: int = 50


class Pacgum(Entity, Collectible):
    def __init__(self, spawn_point: tuple[int, int]) -> None:
        arcade.Sprite.__init__(self, "assets/entity/pacgum.png", scale=SCALE)
        Entity.__init__(self, spawn_point)
        Collectible.__init__(self, score=SCORE)
        self.center_x = self._x
        self.center_y = self._y

        self.__already_collect: bool = False

    def collect(self):
        if not self.__already_collect:
            self.__already_collect = True
            self.remove_from_sprite_lists()
            return True
        return False
