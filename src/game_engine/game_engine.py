import arcade

from src.config.config_loader import Config
from src.event_bus.event_bus import EventBus
from src.event_bus.score_manager import ScoreManager
from src.event_bus.cheat_manager import CheatManager
from src.event_bus.game_manager import GameManager
from src.maze_adapter.maze_adapter import MazeAdapter
from src.game_engine.game_state import GameState
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
            width=self.width,
            height=self.height,
            title="Pac-Man",
            resizable=True,
            update_rate=1 / 61,
        )
        self.config = config
        self.window.set_minimum_size(720, 480)
        self.maze_adapter = None
        self.config_data = None
        self.is_configured = False  # Set to True when Views added
        self.score_manager = ScoreManager(
            config.pacgum_points, config.super_pacgum_points
        )
        self.cheat_manager = CheatManager()
        self.game_manager = GameManager(config.lives, len(config.level))
        self.maze_list = MazeAdapter().get_multiple_maze(config.level)
        self.game_state = GameState(
            self.maze_list[self.game_manager.current_maze]
        )
        try:
            arcade.load_font("assets/fonts/Early GameBoy.ttf")
        except (FileNotFoundError, PermissionError):
            pass

    def set_views(
        self,
        menu: MenuView,
        game: GameView,
        pause: PauseView,
        finish: FinishView,
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

        # Reload event bus
        self.event_bus = EventBus()
        self.event_bus.initialize(self)

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
        self.finish_view.score = self.score_manager.xp
        self.window.show_view(self.finish_view)

    def event_game_over(self) -> None:
        self.finish_view.end_game_status = "Game Over :L"
        self.switch_finish()

    def event_next_level(self) -> None:
        if self.game_manager.current_maze < len(self.maze_list):
            self.game_state = GameState(
                self.maze_list[self.game_manager.current_maze]
            )

    def run(self) -> None:
        """Run the game after"""
        if not self.is_configured:
            raise GameEngineError(
                "Tried to run the game without configuring all game views"
            )
        arcade.run()
        return None

    def event_reload_views(self) -> None:
        self.score_manager = ScoreManager(
            self.config.pacgum_points, self.config.super_pacgum_points
        )
        self.cheat_manager = CheatManager()
        self.game_manager = GameManager(
            self.config.lives, len(self.config.level)
        )
        self.maze_list = MazeAdapter().get_multiple_maze(self.config.level)
        self.game_state = GameState(
            self.maze_list[self.game_manager.current_maze]
        )
        self.set_views(
            menu=MenuView(self),
            game=GameView(self.config, self),
            pause=PauseView(self),
            finish=FinishView(self),
        )

    def event_toggle_fullscreen(self) -> None:
        """Toggle full screen when event is triggered"""
        if self.window.fullscreen:
            self.window.set_fullscreen(False)
        else:
            self.window.set_fullscreen(True)
        self.window.set_minimum_size(720, 480)
