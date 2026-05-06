
from src.renderer.renderer import Renderer

from ..maze_adapter.maze_adapter import MazeAdapter
from ..config.config_loader import Config
from typing import TYPE_CHECKING

import arcade

class NotImplementedError(Exception):
    def __init__(self, msg: str = '') -> None:
        super().__init__(f'NOT IMPLEMENTED ERROR: {msg}')

if TYPE_CHECKING:
    from ..game_engine.game_engine import GameEngine

class GameView(arcade.View):
    """View of the game (in-game)"""

    def __init__(self, config: Config, engine: "GameEngine") -> None:
        """Initialize the view"""
        super().__init__()
        self.window = arcade.get_window()

        # Scene setup
        self.config = config
        self.engine = engine
        self.background_color = arcade.color.BLACK  # Default background color
        self.levels: list[dict[str, int]] = self.config.level  # Array of levels from the config
        self.maze_list : list[tuple[list[list[int]], int]] = MazeAdapter().get_multiple_maze(self.levels)  # List of generated mazes
        self.renderer = Renderer()  # Initialize renderer
        self.level = 0  # Current level


    def on_draw(self) -> bool | None:
        """Function to draw on the screen"""
        self.clear() # Clear previous frame
        self.window.set_mouse_cursor(self.window.get_system_mouse_cursor(self.window.CURSOR_DEFAULT))

        # Render game from Rendere
        self.renderer.render_game(self.maze_list[0][0])

        fps_text = f"FPS: {int(self.fps)}"
        arcade.draw_text(fps_text, 10, 10, arcade.color.WHITE, 18)

        return None

    def on_key_press(self, symbol: int, modifiers: int) -> bool | None:
        """Keyboard interactions events"""
        if symbol == arcade.key.ESCAPE:
            self.engine.switch_pause()

        return None

    def on_update(self, delta_time: float) -> bool | None:
        """ Update sprites """
        if delta_time > 0:
            self.fps = 1 / delta_time
        return None

    def on_resize(self, width: int, height: int) -> bool | None:
        """ Function executed when the window is resized """

        return super().on_resize(width, height)
