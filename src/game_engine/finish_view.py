import arcade

from typing import TYPE_CHECKING

from arcade import text
from pubsub import pub

from src.event_bus.event_bus import EventBus
from src.leaderboard import LeaderboardManager

if TYPE_CHECKING:
    from ..game_engine.game_engine import GameEngine


class FinishView(arcade.View):
    """View of the game (in-game)"""

    def __init__(self, engine: "GameEngine") -> None:
        super().__init__()
        self.engine = engine
        self.background_color = arcade.color.GRAY
        self.score = 0
        self.username: str = '---------'

        pub.subscribe(self.event_save_score, "save_score")

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
            "Game Over !",
            self.window.width / 2,
            self.window.height * 0.9,
            color=arcade.color.WHITE_SMOKE,
            font_size=42,
            anchor_x="center",
            anchor_y="center",
            font_name="Early GameBoy",
        )
        
        username_text = arcade.Text(
            self.username,
            self.window.width / 2,
            200,
            color=arcade.color.WHITE_SMOKE,
            font_size=42,
            anchor_x="center",
            anchor_y="center",
            font_name="Early GameBoy",
        )
        username_text.draw()

        return None

    def on_key_press(self, symbol: int, modifiers: int) -> bool | None:
        """Keyboard interaction"""

        # Switch to GameView if space is hit

        return None

    def on_key_press(self, symbol: int, modifiers: int) -> bool | None:
        if symbol == arcade.key.SPACE:
            EventBus.broadcast_event(
                "save_score",
                username="REPLACE_ME",
                score=999,
                target="data/leaderboard.json",
                signature="SIGNATURE_EXAMPLE",
            )

        # Entering username
        if ((symbol >= arcade.key.A and symbol <= arcade.key.Z)
            and len(self.username) <= 9):
            self.username = (self.username.replace('-', '') + chr(symbol)).ljust(9, '-')
        if ((symbol >= arcade.key.NUM_0 and symbol <= arcade.key.NUM_9) and len(self.username) <= 9):
            self.username = (self.username.replace('-', '') + str(symbol - arcade.key.NUM_0)).ljust(9, '-')
        if symbol == arcade.key.BACKSPACE:
            self.username = self.username.replace('-', '')[:-1].ljust(9, '-')

        # 
        if symbol == arcade.key.SPACE:
            EventBus.broadcast_event(
                "save_score",
                username="REPLACE_ME",
                score=999,
                target="data/leaderboard.json",
                signature="SIGNATURE_EXAMPLE",
            )

    def event_save_score(
        self, username: str, score: int, target: str, signature: str
    ) -> None:
        current_leaderboard = LeaderboardManager.load_leaderboard(
            target, signature=signature
        )
        LeaderboardManager.save_score(
            username, score, target, signature, current_leaderboard
        )
        return None
