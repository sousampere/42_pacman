# Made by gtourdia & kebertra

from src.config.config_loader import ConfigError, ConfigLoader
from src.game_engine.game_engine import GameEngine, MenuView, GameView, PauseView, FinishView


def main():
    """Runs the game"""

    # Load config
    try:
        config = ConfigLoader.load_config('data/config.json')
    except ConfigError:
        print('[Error] Could not read your configuration file. Aborting.')
        exit(1)

    # Load game engine
    engine = GameEngine(config)

    # Set different views
    engine.set_views(
        menu=MenuView(engine),
        game=GameView(config, engine),
        pause=PauseView(engine),
        finish=FinishView(engine),
    )

    # Start game engine
    engine.run()


if __name__ == "__main__":
    main()
