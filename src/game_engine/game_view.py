
from src.renderer.renderer import Renderer

from ..maze_adapter.maze_adapter import MazeAdapter

import arcade

class NotImplementedError(Exception):
    def __init__(self, msg: str = '') -> None:
        super().__init__(f'NOT IMPLEMENTED ERROR: {msg}')

class GameView(arcade.View):
    """View of the game (in-game)"""

    def __init__(self, engine: "GameEngine") -> None:
        """Initialize the view"""
        super().__init__()
        self.engine = engine  # GameEngine to access engine variables

        # Scene setup
        self.background_color = arcade.color.BLACK  # Default background color
        self.levels = self.engine.config.level  # Array of levels from the config
        self.maze_list : list[tuple[list[list[int]]]] = MazeAdapter().get_multiple_maze(self.levels)  # List of generated mazes
        self.level = 0  # Current level


    def on_draw(self) -> bool | None:
        """Function to draw on the screen"""
        self.clear() # Clear previous frame

        # Initialize renderer
        renderer = Renderer()

        # Render game from Rendere
        renderer.render_game(self.maze_list[0][0])

        return None

    def on_key_press(self, symbol: int, modifiers: int) -> bool | None:
        """Keyboard interactions events"""
        if symbol == arcade.key.ESCAPE:
            self.engine.switch_pause()

        return None

    def on_update(self, delta_time: float) -> bool | None:
        """ Update sprites """
        self.entities.update()
        return None

    def on_resize(self, width: int, height: int) -> bool | None:
        """ Function executed when the window is resized """

        # Resize player
        self.player.width = self.get_tile_size()
        self.player.height = self.get_tile_size()
        return super().on_resize(width, height)
