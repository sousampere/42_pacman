# Made with <3 by gtourdia & kebertra

from src.config.config_loader import Config, ConfigError, ConfigLoader
from src.game_engine.game_engine import GameEngine
from src.game_engine.menu_view import MenuView
from src.game_engine.game_view import GameView
from src.game_engine.pause_view import PauseView
from src.game_engine.finish_view import FinishView
from src.game_engine.transition_view import TransitionView
import sys


def main() -> None:
    """Runs the game"""

    if (len(sys.argv) != 2):
        print(
            "No configuration file given in input. "
            "Please provide as an argument."
        )
        exit(1)

    # Load config
    try:
        config = ConfigLoader.load_config(sys.argv[1])
    except ConfigError as e:
        print(
            f"[Warning] Could not read your configuration file ({e}). "
            "Using default values."
        )
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
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print('\033c\033[0;32m[Info] Quitting Pacman. See you soon 🤠\033[0m')
