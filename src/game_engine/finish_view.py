import arcade

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..game_engine.game_engine import GameEngine


class FinishView(arcade.View):
    """View of the game (in-game)"""

    def __init__(self, engine: "GameEngine") -> None:
        super().__init__()
        self.engine = engine
        self.background_color = arcade.color.GRAY
        self.score = 0

        try:
            self.background = arcade.load_texture(
                "assets/background/background_2.png")
        except (FileNotFoundError, PermissionError):
            raise NotImplementedError("NOT IMPLEMENTED : Missing background")

    def on_draw(self) -> bool | None:
        self.clear()

        # Apply background
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

        # Apply a soft shadow on the screen
        arcade.draw_lbwh_rectangle_filled(
            0, 0, self.window.width, self.window.height, (0, 0, 0, 128)
        )

        # Write "Welcome to Pac-Man"
        arcade.draw_text(
            f"Game Over !",
            self.window.width / 2,
            self.window.height * 0.9,
            color=arcade.color.WHITE_SMOKE,
            font_size=42,
            anchor_x="center",
            anchor_y="center",
            font_name="Early GameBoy",
        )

        return None
