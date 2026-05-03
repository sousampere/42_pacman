
import arcade


class PauseView(arcade.View):
    """View of the pause"""

    def __init__(self, engine: "GameEngine") -> None:
        super().__init__()
        self.engine = engine
        self.background_color = arcade.color.GRAY

    def on_draw(self) -> bool | None:
        self.clear()

        # Draw the screen of the GameView
        self.engine.game_view.on_draw()

        # Apply a soft shadow on the screen
        arcade.draw_lbwh_rectangle_filled(
            0, 0, self.window.width, self.window.height, (0, 0, 0, 128)
        )

        # Write "Paused..."
        arcade.draw_text(
            "Paused...",
            self.window.width / 2,
            self.window.height / 2,
            color=arcade.color.WHITE_SMOKE,
            font_size=24,
            anchor_x="center",
            anchor_y="center",
            font_name="Early GameBoy",
        )
        return None

    def on_key_press(self, symbol: int, modifiers: int) -> bool | None:
        """Keyboard interaction"""
        # Exit pause if escape is pressed
        if symbol == arcade.key.ESCAPE:
            self.engine.switch_game()

        return None
