import time
from typing import TYPE_CHECKING

import arcade

from src.event_bus.event_bus import EventBus

if TYPE_CHECKING:
    from ..game_engine.game_engine import GameEngine


class TransitionView(arcade.View):
    def __init__(self, engine: "GameEngine") -> None:
        super().__init__()
        self.engine = engine
        self.background_color = arcade.color.BLACK
        self.text = "Transition"
        self.transition_end_time = time.time() + 2
        self.event_after_transition = (
            "switch_menu"  # Event executed after transition
        )

    def on_draw(self) -> bool | None:
        window = arcade.get_window()
        self.clear()

        self.engine.game_view.on_draw()

        # Apply a soft shadow on the screen
        arcade.draw_lbwh_rectangle_filled(
            0, 0, self.window.width, self.window.height, (0, 0, 0, 150)
        )

        remaining_seconds = int(self.transition_end_time - time.time())
        # Write transition text
        text = arcade.Text(
            self.text,
            window.width / 2,
            window.height / 2,
            arcade.color.WHITE,
            font_size=min(self.window.width * 0.05, self.window.height * 0.05),
            anchor_x="center",
            anchor_y="center",
            font_name="Early GameBoy",
        )
        text_time = arcade.Text(
            f"{remaining_seconds}",
            window.width / 2,
            window.height / 3,
            arcade.color.YELLOW,
            font_size=min(self.window.width * 0.05, self.window.height * 0.05),
            anchor_x="center",
            anchor_y="center",
            font_name="Early GameBoy",
        )

        text.draw()
        text_time.draw()
        return None

    def on_update(self, delta_time: float) -> bool | None:
        if time.time() >= self.transition_end_time:
            # Execute event if time is elapsed
            EventBus.broadcast_event(self.event_after_transition)
        return None

    def on_key_press(self, symbol: int, modifiers: int) -> bool | None:
        if symbol == arcade.key.F11:
            EventBus.broadcast_event('toggle_fullscreen')
        return super().on_key_press(symbol, modifiers)
