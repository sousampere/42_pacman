# Made by gtourdia & kebertra

import arcade

from src.config.config_loader import ConfigError, ConfigLoader
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
        print("[Error] Could not read your configuration file. Aborting.")
        exit(1)

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
