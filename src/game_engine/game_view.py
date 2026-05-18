import random

import numpy as np
from numpy.typing import NDArray

from src.entity.ghost import Ghost
from src.entity.pacgum import Pacgum
from src.entity.player import Player
from src.event_bus.event_bus import EventBus
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
        self.key_history: list[int] = []

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

        # Init cheat toggle variables
        self.cheat_mode = False
        self.invincibility = False
        self.freeze_ghosts = False

        self.entity = self.init_entity()

    def init_entity(self) -> arcade.SpriteList:
        entity: arcade.SpriteList = arcade.SpriteList()
        pts = self.maze_list[self.current_maze][1]

        center_point = pts.mean(axis=0)
        distances = np.sum((pts - center_point) ** 2, axis=1)
        closest_point = tuple(pts[np.argmin(distances)].tolist())

        min_x, min_y = pts.min(axis=0)
        max_x, max_y = pts.max(axis=0)

        corners = [
            (min_x, min_y),
            (max_x, min_y),
            (min_x, max_y),
            (max_x, max_y),
        ]

        self.ghosts: list[Ghost] = []
        for corner in corners:
            dist_to_corner = np.sum((pts - corner) ** 2, axis=1)
            ghost_pos = tuple(pts[np.argmin(dist_to_corner)].tolist())

            ghost = Ghost(ghost_pos, pts, 1)
            self.ghosts.append(ghost)
            entity.append(ghost)

        total_pacgum = random.randint(
            int((len((pts) - 5) * 0.6)), (len(pts) - 5))
        occupied_positions = [closest_point]
        occupied_positions.extend(corners)

        pac_gum_pts = pts.copy()

        for pos in occupied_positions:
            mask = ~np.all(pac_gum_pts == pos, axis=1)
            pac_gum_pts = pac_gum_pts[mask]

        num_to_spawn = min(total_pacgum, len(pac_gum_pts))

        indices = np.random.choice(
            len(pac_gum_pts), size=num_to_spawn, replace=False)
        pac_gum_spawn = pac_gum_pts[indices]
        self.pacgum = []
        for spawn in pac_gum_spawn:
            pacgum = Pacgum(spawn)
            self.pacgum.append(pacgum)
            entity.append(pacgum)

        self.player = Player(closest_point, pts, 0.3)
        entity.append(self.player)

        return entity

    def on_draw(self) -> bool | None:
        """Function to draw on the screen"""
        self.clear()  # Clear previous frame)
        self.window.set_mouse_cursor(
            self.window.get_system_mouse_cursor(self.window.CURSOR_DEFAULT)
        )

        # Render game from Rendere
        walls, paths, seed = self.maze_list[self.current_maze]
        self.renderer.render_game(
            walls,
            paths,
            self.entity,
            self.lives,
            self.time,
            self.xp,
            self.level,
        )

        fps_text = f"FPS: {int(self.fps)}"
        font_size: int = int(self.window.height / 50)
        arcade.draw_text(
            fps_text,
            10,
            self.window.height - 10 - 18,
            (50, 255, 50),
            font_size,
            font_name="Early GameBoy",
        )

        return None

    def on_key_press(self, symbol: int, modifiers: int) -> bool | None:
        """Keyboard interactions events"""
        KONAMI_CODE: list[int] = [
            arcade.key.UP,
            arcade.key.UP,
            arcade.key.DOWN,
            arcade.key.DOWN,
            arcade.key.LEFT,
            arcade.key.RIGHT,
            arcade.key.LEFT,
            arcade.key.RIGHT,
            arcade.key.A,
            arcade.key.B,
        ]

        # Check knoami code
        self.key_history.append(symbol)
        if KONAMI_CODE[: len(self.key_history)] == self.key_history:
            if self.key_history == KONAMI_CODE:
                EventBus.broadcast_event("enable_cheat")
        else:
            self.key_history = []

        if symbol == arcade.key.ESCAPE:
            EventBus.broadcast_event("switch_pause")

        # Dev feature to skip current level
        if symbol == arcade.key.NUM_3 and self.cheat_mode:
            EventBus.broadcast_event("next_level")

        # Dev feature to switch easily to finish view
        if symbol == arcade.key.NUM_1:
            EventBus.broadcast_event("switch_finish", score=1)
        if symbol == arcade.key.UP:
            self.player.dir = (0, 1)
        if symbol == arcade.key.DOWN:
            self.player.dir = (0, -1)
        if symbol == arcade.key.LEFT:
            self.player.dir = (-1, 0)
        if symbol == arcade.key.RIGHT:
            self.player.dir = (1, 0)

        return None

    def on_update(self, delta_time: float) -> bool | None:
        """Update sprites"""
        if delta_time > 0:
            self.fps = 1 / delta_time
        self.player.update()
        if self.player.position in [g.position for g in self.ghosts]:
            self.player.die()
            EventBus.broadcast_event('remove_life')
        for p in self.pacgum:
            if p.position == self.player.position:
                self.pacgum.remove(p)
                self.entity.remove(p)
                EventBus.broadcast_event('add_pacgum_point')
        if len(self.pacgum) == 0:
            self.event_next_level()
        return None

    def on_resize(self, width: int, height: int) -> bool | None:
        """Function executed when the window is resized"""

        return super().on_resize(width, height)

    def event_enable_cheat_mode(self) -> None:
        """Turn on cheat mode and reset cache"""
        self.renderer.cheat_mode = True
        self.cheat_mode = True
        self.renderer.reset_cache()

    def event_next_level(self) -> None:
        """Switch to next level"""
        self.current_maze += 1
        self.level += 1
        self.entity = self.init_entity()
        self.renderer.reset_cache()

        # Check if end of level
        if self.level == len(self.maze_list):
            EventBus.broadcast_event("switch_finish", score=self.xp)

    def event_add_pacgum_point(self) -> None:
        """Add a pacgum point to the player"""
        self.xp += self.config.pacgum_points

    def event_add_life(self) -> None:
        """Adds a life to the player"""
        self.lives += 1

    def event_remove_life(self) -> None:
        """Removes a life to the player"""
        self.lives -= 1

    def event_toggle_freeze_ghosts(self) -> None:
        """Toggle freezing the ghosts"""
        if self.freeze_ghosts:
            self.freeze_ghosts = False
        else:
            self.freeze_ghosts = True

    def event_toggle_invincibility(self) -> None:
        """Toggles the invincibility of the player"""
        if self.invincibility:
            self.invincibility = False
        else:
            self.invincibility = True
