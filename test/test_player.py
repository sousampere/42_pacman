from src.entity.player import Player
import pytest


class TestPlayer:
    def test_player_initial_position(self) -> None:
        player = Player(spawn_point=(0, 0))

        player.move((0,1))

        assert player.center_y == 1
        assert player.center_x == 0
