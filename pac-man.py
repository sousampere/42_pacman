# Made by gtourdia & kebertra

import arcade

from src.config.config_loader import Config, ConfigError, ConfigLoader
from src.event_bus import cheat_manager
from src.game_engine.game_engine import (
    GameEngine,
    MenuView,
    GameView,
    PauseView,
    FinishView,
)
from src.game_engine.transition_view import TransitionView


def main():
    """Runs the game"""

    # Load config
    try:
        config = ConfigLoader.load_config("data/config.json")
    except ConfigError:
        print("[Error] Could not read your configuration file. Using default values.")
        levels = []
        for _ in range(10):
            levels.append({'width': 10, 'height': 10})
        config = Config(highscore_filename='data/leaderboard.json')

    # Load game engine
    engine = GameEngine(config)

    
    # Set different views
    engine.set_views(
        menu=MenuView(engine),
        game=GameView(config, engine),
        pause=PauseView(engine),
        finish=FinishView(engine),
        transition=TransitionView(engine)
    )

    # Start game engine
    engine.run()


if __name__ == "__main__":
    main()
