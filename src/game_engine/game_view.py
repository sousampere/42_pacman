import arcade

from src.event_bus.event_bus import EventBus
from src.renderer.renderer import Renderer

from ..config.config_loader import Config
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..game_engine.game_engine import GameEngine

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


class GameView(arcade.View):
    """View of the game (in-game)"""

    def __init__(self, config: Config, engine: "GameEngine") -> None:
        super().__init__()
        self.window = arcade.get_window()
        self.engine = engine
        self.key_history: list[int] = []
        self.renderer = Renderer()
        self.config = config
        self.fps = 0

    def on_draw(self) -> bool | None:
        self.clear()
        if self.window.current_view == self:
            self.window.set_mouse_cursor(
                self.window.get_system_mouse_cursor(self.window.CURSOR_DEFAULT)
            )
        walls, paths, _ = self.engine.maze_list[
            self.engine.game_manager.current_maze
        ]
        cheat = self.engine.cheat_manager
        remaining_time: int = self.engine.game_state.remaining_time

        if remaining_time == 0:
            EventBus.broadcast_event("game_over")
        self.renderer.render_game(
            walls,
            paths,
            self.engine.game_state.entity,
            self.engine.game_manager.lives,
            remaining_time,
            self.engine.score_manager.xp,
            self.engine.game_manager.level,
            self.fps,
            cheat.cheat_mode,
            cheat.invincibility,
            cheat.freeze_ghosts,
        )
        return None

    def on_key_press(self, symbol: int, modifiers: int) -> bool | None:
        # Check Konami code
        self.key_history.append(symbol)
        if KONAMI_CODE[: len(self.key_history)] == self.key_history:
            if self.key_history == KONAMI_CODE:
                EventBus.broadcast_event("enable_cheat")
        else:
            self.key_history = []

        if symbol == arcade.key.ESCAPE:
            EventBus.broadcast_event("switch_pause")

        # Cheat shortcuts
        if self.engine.cheat_manager.cheat_mode:
            if symbol == arcade.key.NUM_1 or symbol == arcade.key.KEY_1:
                EventBus.broadcast_event("toggle_invincibility")
            if symbol == arcade.key.NUM_2 or symbol == arcade.key.KEY_2:
                EventBus.broadcast_event("add_life")
            if symbol == arcade.key.NUM_3 or symbol == arcade.key.KEY_3:
                EventBus.broadcast_event("next_level")
                EventBus.broadcast_event("next_engine_level")
                EventBus.broadcast_event("reset_time")
            if symbol == arcade.key.NUM_4 or symbol == arcade.key.KEY_4:
                EventBus.broadcast_event("toggle_freeze_ghosts")

        # Movement
        if symbol == arcade.key.UP \
                or symbol == arcade.key.W:
            self.engine.game_state.player.dir = (0, 1)
        if symbol == arcade.key.DOWN \
                or symbol == arcade.key.S:
            self.engine.game_state.player.dir = (0, -1)
        if symbol == arcade.key.LEFT \
                or symbol == arcade.key.A:
            self.engine.game_state.player.dir = (-1, 0)
        if symbol == arcade.key.RIGHT \
                or symbol == arcade.key.D:
            self.engine.game_state.player.dir = (1, 0)

        if symbol == arcade.key.F11:
            EventBus.broadcast_event("toggle_fullscreen")

        return None

    def on_update(self, delta_time: float) -> bool | None:
        if delta_time > 0:
            self.fps = round(1 / delta_time)
        cheat = self.engine.cheat_manager
        self.engine.game_state.update(
            delta_time, cheat.freeze_ghosts, cheat.invincibility
        )
        return None

    def on_show_view(self) -> None:
        EventBus.broadcast_event("reset_time")
