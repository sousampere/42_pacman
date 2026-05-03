# Made by gtourdia & kebertra

from src.game_engine.game_engine import GameEngine, MenuView, GameView, PauseView, FinishView


def main():
    """Runs the game"""
    # Load game engine
    engine = GameEngine()

    # Set different views
    engine.set_views(
        menu=MenuView(engine),
        game=GameView(engine),
        pause=PauseView(engine),
        finish=FinishView(engine),
    )

    # Start game engine
    engine.run()


if __name__ == "__main__":
    main()
