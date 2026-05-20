import arcade
from typing import TYPE_CHECKING

from src.event_bus.event_bus import EventBus
from src.leaderboard import LeaderboardManager

if TYPE_CHECKING:
    from ..game_engine.game_engine import GameEngine


class MenuView(arcade.View):
    """View of the menu (onboarding)"""

    def __init__(self, engine: "GameEngine") -> None:
        super().__init__()
        self.engine = engine
        self.background_color = (0, 8, 20)  # Soft black background
        self.sprite_list: arcade.SpriteList[arcade.Sprite] = (
            arcade.SpriteList()
        )

        # -- Load sprites --
        # Load play button :
        self.start_button = arcade.Sprite("assets/buttons/play.png", 0.1)
        self.sprite_list.append(self.start_button)
        # Load background
        try:
            self.background = arcade.load_texture(
                "assets/background/background_4.png"
            )
        except (FileNotFoundError, PermissionError):
            raise NotImplementedError("NOT IMPLEMENTED : Missing background")
        self.leaderboard = LeaderboardManager.load_leaderboard(
            self.engine.config.highscore_filename, self.engine.config.signature
        )

        # Create a player sprite that will be at the bottom
        sheet = arcade.load_spritesheet("assets/entity/spritesheet.png")
        self.textures = sheet.get_texture_grid(
            size=(66, 66),
            columns=1,
            count=6,
        )
        self.player_texture: arcade.Texture = self.textures[4]
        self.player_texture = arcade.Texture.flip_horizontally(
            self.player_texture
        )
        self.player_pos = 0
        self.player_direction = 1

    def on_draw(self) -> bool | None:
        """Method for drawing at screen"""
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
            0, 0, self.window.width, self.window.height, (0, 0, 0, 200)
        )

        # Write "Welcome to Pac-Man"
        title_text = arcade.Text(
            "Pac-Man",
            self.window.width / 2,
            self.window.height * 0.9,
            color=arcade.color.WHITE_SMOKE,
            font_size=min(self.window.width * 0.05, self.window.height * 0.05),
            anchor_x="center",
            anchor_y="center",
            font_name="Early GameBoy",
        )
        title_text.draw()

        # Print leaderboard
        texts: list[arcade.Text] = []
        self.leaderboard.scores = sorted(
            self.leaderboard.scores, key=lambda s: s["score"], reverse=True
        )
        self.leaderboard.scores = self.leaderboard.scores[:10]
        for index, score in enumerate(self.leaderboard.scores):
            match index:
                case 0:
                    color = arcade.color.GOLD
                case 1:
                    color = arcade.color.SILVER
                case 2:
                    color = arcade.color.BRONZE
                case _:
                    color = arcade.color.GRAY

            texts.append(
                arcade.Text(
                    f"{index + 1}. {score['username']} - {score['score']}",
                    self.window.width / 2,
                    title_text.bottom
                    - self.window.height / 10
                    - (self.window.height / 20) * index,
                    color=color,
                    font_size=min(
                        self.window.width * 0.02, self.window.height * 0.02
                    ),
                    anchor_x="center",
                    anchor_y="center",
                    font_name="Early GameBoy",
                )
            )
        for text in texts:
            text.draw()

        self.start_button.center_x = self.window.width / 2
        self.start_button.center_y = self.window.height * 0.33

        if len(texts) != 0:
            self.start_button.center_y = texts[-1].y - self.start_button.height
        else:
            self.start_button.center_y = (
                self.window.height / 2 + self.start_button.height
            )

        # Draw sprites
        self.sprite_list.draw()

        # Draw player
        player_rect = arcade.Rect(
            x=self.player_pos + self.player_texture.width / 2,
            y=0 + self.player_texture.height / 2,
            width=self.player_texture.width,
            height=self.player_texture.height,
            left=0,
            right=0,
            bottom=0,
            top=0,
        )
        arcade.draw_texture_rect(self.player_texture, player_rect)

        return None

    def on_update(self, delta_time: float) -> bool | None:
        self.sprite_list.update()

        # Bottom player movement
        self.player_pos += 3 * self.player_direction
        if self.player_pos > self.window.width:
            self.player_direction = -1
            self.player_texture = arcade.Texture.flip_horizontally(
                self.player_texture
            )
        if self.player_pos < -self.player_texture.width:
            self.player_direction = 1
            self.player_texture = arcade.Texture.flip_horizontally(
                self.player_texture
            )
        return super().on_update(delta_time)

    def on_key_press(self, symbol: int, modifiers: int) -> bool | None:
        """Keyboard interaction"""

        # Switch to GameView if space is hit
        if symbol == arcade.key.SPACE:
            EventBus.broadcast_event("switch_game")

        if symbol == arcade.key.F11:
            EventBus.broadcast_event("toggle_fullscreen")

        return None

    def on_mouse_press(
        self, x: int, y: int, button: int, modifiers: int
    ) -> bool | None:
        """Mouse interaction"""
        # Get list of sprite hit by mouse
        hits = arcade.get_sprites_at_point((x, y), self.sprite_list)

        for sprite in hits:
            # Start button interraction
            if sprite == self.start_button:
                EventBus.broadcast_event("switch_game")

        return None

    def on_mouse_motion(self, x: int, y: int, dx: int, dy: int) -> bool | None:
        """Detect collision of the mouse with the start button, and
        change the cursor if the mouse overlaps the start button"""
        if self.start_button.collides_with_point((x, y)):
            c = self.window.get_system_mouse_cursor(self.window.CURSOR_HAND)
            self.start_button.scale = 0.105
            self.window.set_mouse_cursor(c)
        else:
            c = self.window.get_system_mouse_cursor(self.window.CURSOR_DEFAULT)
            self.start_button.scale = 0.1
            self.window.set_mouse_cursor(c)
        return super().on_mouse_motion(x, y, dx, dy)

    def on_show_view(self) -> None:
        # Refresh leaderboard
        self.leaderboard = LeaderboardManager.load_leaderboard(
            self.engine.config.highscore_filename, self.engine.config.signature
        )
