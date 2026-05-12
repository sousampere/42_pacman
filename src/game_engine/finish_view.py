import arcade

from typing import TYPE_CHECKING

from pubsub import pub

from src.leaderboard import Leaderboard, LeaderboardManager

if TYPE_CHECKING:
    from ..game_engine.game_engine import GameEngine


class FinishView(arcade.View):
    """View of the game (in-game)"""

    def __init__(self, engine: "GameEngine") -> None:
        super().__init__()
        self.engine = engine
        self.background_color = arcade.color.GRAY
        self.score = 0

        pub.subscribe(self.event_save_score, 'save_score')

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

    def on_key_press(self, symbol: int, modifiers: int) -> bool | None:
        if symbol == arcade.key.SPACE:
            pub.sendMessage('save_score',
                            username='REPLACE_ME', score=999,
                            target='data/leaderboard.json',
                            signature='SIGNATURE_EXAMPLE')

    def event_save_score(
            self,
            username: str,
            score: int,
            target: str,
            signature: str
    ) -> None:
        current_leaderboard = LeaderboardManager.load_leaderboard(target, signature=signature)
        LeaderboardManager.save_score(username, score, target, signature, current_leaderboard)
        return None