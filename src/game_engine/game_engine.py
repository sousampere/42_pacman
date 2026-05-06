import arcade

from src.config.config_loader import Config
from .menu_view import MenuView
from .game_view import GameView
from .pause_view import PauseView
from .finish_view import FinishView

class GameEngineError(Exception):
    def __init__(self, msg: str = "") -> None:
        super().__init__(f"GameEngine error: {msg}")


class FontError(GameEngineError):
    def __init__(self, msg: str = "") -> None:
        super().__init__(f"Font error: {msg}")


class GameEngine:
    """Game Engine that orchestrate different views and their data"""

    def __init__(self, config: Config) -> None:
        self.width = 1280
        self.height = 720
        self.window = arcade.Window(
            width=self.width, height=self.height, title="Pac-Man", resizable=True
        )
        self.config = config
        # self.window.set_minimum_size(1920, 1080)
        self.maze_adapter = None
        self.config_data = None
        self.is_configured = False  # Set to True when Views added
        try:
            arcade.load_font("assets/fonts/Early GameBoy.ttf")
        except (FileNotFoundError, PermissionError):
            pass

    def set_views(
        self, menu: MenuView, game: GameView, pause: PauseView, finish: FinishView
    ) -> None:
        """Initialize the menu, game, pause and finish views."""
        self.menu_view = menu
        self.game_view = game
        self.pause_view = pause
        self.finish_view = finish

        # Switch to menu view by default
        self.switch_menu()

        # Save configuration as done to enable starting the game
        self.is_configured = True

    def switch_menu(self) -> None:
        """Change the current to the menu view"""
        self.window.show_view(self.menu_view)

    def switch_game(self) -> None:
        """Change the current to the game view"""
        self.window.show_view(self.game_view)

    def switch_pause(self) -> None:
        """Change the current to the pause view"""
        self.window.show_view(self.pause_view)

    def switch_finish(self) -> None:
        """Change the current view to the finish view"""
        self.window.show_view(self.finish_view)

    def run(self) -> None:
        """Run the game after"""
        if not self.is_configured:
            raise GameEngineError(
                "Tried to run the game without configuring all game views"
            )
        arcade.run()
        return None
