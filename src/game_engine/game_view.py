import numpy as np
from numpy.typing import NDArray
from pubsub import pub

from src.entity.ghost import Ghost
from src.entity.player import Player
from src.renderer.renderer import Renderer

from ..maze_adapter.maze_adapter import MazeAdapter
from ..config.config_loader import Config
from typing import TYPE_CHECKING

import arcade


class NotImplementedError(Exception):
    def __init__(self, msg: str = "") -> None:
        super().__init__(f"NOT IMPLEMENTED ERROR: {msg}")


if TYPE_CHECKING:
    from ..game_engine.game_engine import GameEngine


class GameView(arcade.View):
    """View of the game (in-game)"""

    def __init__(self, config: Config, engine: "GameEngine") -> None:
        """Initialize the view"""
        super().__init__()
        self.window = arcade.get_window()
        self.config = config
        self.engine = engine


        # Scene setup
        self.current_maze = 0
        self.levels: list[dict[str, int]] = (
            self.config.level
        )  # Array of levels from the config
        self.maze_list: list[
            tuple[NDArray, NDArray, int]
        ] = MazeAdapter().get_multiple_maze(
            self.levels
        )  # List of generated mazes
        self.renderer = Renderer()  # Initialize renderer

        # Init variables that will be displayed
        self.lives = config.lives
        self.level = 1  # Current level
        self.xp = 0  # Current xp
        self.time = config.max_time  # Current xp

        self.entity = self.init_entity()

        pub.subscribe(self.event_enable_cheat_mode, 'enable_cheat')
        pub.subscribe(self.event_next_level, 'next_level')

    def init_entity(self) -> arcade.SpriteList:
        entity: arcade.SpriteList = arcade.SpriteList()
        pts = self.maze_list[self.current_maze][1]

        center_point = pts.mean(axis=0)
        distances = np.sum((pts - center_point)**2, axis=1)
        closest_point = tuple(pts[np.argmin(distances)].tolist())
        self.player = Player(closest_point, pts, 0.25)
        entity.append(self.player)

        min_x, min_y = pts.min(axis=0)
        max_x, max_y = pts.max(axis=0)

        corners = [
            (min_x, min_y), (max_x, min_y), 
            (min_x, max_y), (max_x, max_y)
        ]

        self.ghosts = []
        for corner in corners:
            dist_to_corner = np.sum((pts - corner)**2, axis=1)
            ghost_pos = tuple(pts[np.argmin(dist_to_corner)].tolist())
            
            ghost = Ghost(ghost_pos, pts, 0.25)
            self.ghosts.append(ghost)
            entity.append(ghost)

        return entity

    def on_draw(self) -> bool | None:
        """Function to draw on the screen"""
        self.clear()  # Clear previous frame)
        self.window.set_mouse_cursor(
            self.window.get_system_mouse_cursor(self.window.CURSOR_DEFAULT)
        )

        # Render game from Rendere
        walls, paths, seed = self.maze_list[self.current_maze]
        self.renderer.render_game(walls, paths, self.entity, self.lives, self.time, self.xp, self.level)

        fps_text = f"FPS: {int(self.fps)}"
        font_size: int = int(self.window.height / 50)
        arcade.draw_text(fps_text, 10, self.window.height - 10 - 18,
                         (50, 255, 50), font_size, font_name="Early GameBoy")

        return None

    def on_key_press(self, symbol: int, modifiers: int) -> bool | None:
        """Keyboard interactions events"""
        # if self.on_key_press.history is None:
        #     self.on_key_press.history = []
        # else if:
        #     self.on_key_press.history.append('')

        if symbol == arcade.key.ESCAPE:
            pub.sendMessage('switch_pause')

        # Dev feature to go to cheat mode
        if symbol == arcade.key.SPACE:
            pub.sendMessage('enable_cheat')

        # Dev feature to swich maze
        if symbol == arcade.key.R:
            pub.sendMessage('next_level')

        return None

    def on_update(self, delta_time: float) -> bool | None:
        """Update sprites"""
        if delta_time > 0:
            self.fps = 1 / delta_time
        return None

    def on_resize(self, width: int, height: int) -> bool | None:
        """Function executed when the window is resized"""

        return super().on_resize(width, height)

    def event_enable_cheat_mode(self) -> None:
        """Turn on cheat mode and reset cache"""
        self.renderer.cheat_mode = True
        self.renderer.reset_cache()

    def event_next_level(self) -> None:
        """Switch to next level"""
        self.current_maze += 1
        self.level += 1
        self.entity = self.init_entity()
        self.renderer.reset_cache()

        # Check if end of level
        if self.level == len(self.maze_list):
            pub.sendMessage('switch_finish')