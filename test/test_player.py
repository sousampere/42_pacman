from src.entity.player import Player


class TestPlayer:
    def test_player_move_down(self):
        player = Player(spawn_point=(100, 100), speed=1)
        player.move((0, 1))

        assert player._x == 100
        assert player._y == 101
