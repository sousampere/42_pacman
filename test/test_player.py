import numpy as np

from src.entity.player import Player


class TestPlayer:
    def test_player_initialization(self) -> None:
        maze = np.array([(100, 100), (100, 101)])
        player = Player(
            spawn_point=(100, 100),
            maze_path=maze,
            speed=1,
            cheat_enabled=False,
        )
        assert player._x == 100.0
        assert player._y == 100.0
