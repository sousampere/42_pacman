from src.entity.player import Player
import pytest


class TestPlayer:
    player = Player(spawn_point=(0, 0), speed=2)
