import arcade
from numpy import ndarray
from src.entity.entity import Entity, Movable
import time

from src.event_bus import cheat_manager

SCALE: float = 0.5
LIVES: int = 3
WINDOWS_WIDTH: int = 800
WINDOWS_HEIGHT: int = 600


class Player(Entity, Movable):
    def __init__(
        self,
        spawn_point: tuple[int, int],
        maze_path: ndarray,
        speed: float,
        cheat_enabled: bool,
    ):
        Entity.__init__(self, spawn_point, SCALE)
        Movable.__init__(self, maze_path, speed)
        sheet = arcade.load_spritesheet("assets/entity/spritesheet.png")
        self.textures = sheet.get_texture_grid(
            size=(64, 64),
            columns=4,
            count=20,
        )

        # init player textures
        self.right_texture = self.textures[18]
        self.left_texture = self.right_texture.flip_horizontally()
        self.right_texture_closed = self.textures[19]
        self.left_texture_closed = self.right_texture_closed.flip_horizontally()
        self.texture = self.right_texture

        if cheat_enabled:
            self.switch_to_cheat_texture()

        # sprite change timer accumulation
        self.__animation_time: int = 0

    def update(self, delta_time: float = 1 / 60) -> None:
        arrived = self._move_toward_target(delta_time)
        if arrived and self.dir != (0, 0):
            dx, dy = self.dir
            new_x = round(self._x) + dx
            new_y = round(self._y) + dy

            # Reset animation timer
            self.__animation_time += 1
            if self.__animation_time >= 2:
                self.__animation_time = 0

            if self.can_move_to(new_x, new_y, self.scale):
                self._target = (float(new_x), float(new_y))
                if dx < 0:
                    if self.__animation_time > 1 / 2:
                        self.texture = self.left_texture
                    else:
                        self.texture = self.left_texture_closed
                if dx > 0:
                    if self.__animation_time > 1 / 2:
                        self.texture = self.right_texture
                    else:
                        self.texture = self.right_texture_closed
                if dy > 0:
                    if self.__animation_time > 1 / 2:
                        self.texture = self.left_texture.flip_diagonally()
                    else:
                        self.texture = self.left_texture_closed.flip_diagonally()
                if dy < 0:
                    if self.__animation_time > 1 / 2:
                        self.texture = self.right_texture.flip_diagonally()
                    else:
                        self.texture = self.right_texture_closed.flip_diagonally()

    def die(self) -> None:
        self.respawn()

    def respawn(self) -> None:
        self._x, self._y = self.spawn_point
        self._target = None
        self.center_x = self._x
        self.center_y = self._y

    def switch_to_cheat_texture(self) -> None:
        """Changes the texture of the player to cheat textures"""
        self.right_texture = self.textures[16]
        self.left_texture = self.right_texture.flip_horizontally()
        self.right_texture_closed = self.textures[17]
        self.left_texture_closed = self.right_texture_closed.flip_horizontally()
        self.texture = self.right_texture
