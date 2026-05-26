import time

import arcade

from src.event_bus.event_bus import EventBus


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

        try:
            self.background = arcade.load_texture(
                "assets/background/background_2.png"
            )
        except (FileNotFoundError, PermissionError):
            raise NotImplementedError("NOT IMPLEMENTED : Missing background")

    def on_draw(self) -> bool | None:
        window = arcade.get_window()
        self.clear()

        # Create background
        if self.background is not None:
            rect = arcade.Rect(
                x=self.window.width / 2,
                y=self.window.height / 2,
                width=self.window.width,
                height=self.window.height,
                left=0,
                right=0,
                bottom=0,
                top=0,
            )
            arcade.draw_texture_rect(self.background, rect)

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
