
import arcade
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from ..game_engine.game_engine import GameEngine

class MenuView(arcade.View):
    """View of the menu (onboarding)"""

    def __init__(self, engine: "GameEngine") -> None:
        super().__init__()
        self.engine = engine
        self.background_color = (0, 8, 20)  # Soft black background
        self.sprite_list: arcade.SpriteList[arcade.Sprite] = arcade.SpriteList()

        # -- Load sprites --
        # Load play button :
        self.start_button = arcade.Sprite("assets/buttons/play.png", 0.1)
        self.sprite_list.append(self.start_button)
        # Load background
        try:
            self.background = arcade.load_texture("assets/background/background_1.jpg")
        except (FileNotFoundError, PermissionError):
            raise NotImplementedError('NOT IMPLEMENTED : Missing background')

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
            0, 0, self.window.width, self.window.height, (0, 0, 0, 128)
        )

        # Write "Welcome to Pac-Man"
        arcade.draw_text(
            "Pac-Man",
            self.window.width / 2,
            self.window.height * 0.9,
            color=arcade.color.WHITE_SMOKE,
            font_size=42,
            anchor_x="center",
            anchor_y="center",
            font_name="Early GameBoy",
        )

        self.start_button.center_x = self.window.width / 2
        self.start_button.center_y = self.window.height * 0.33

        # Draw sprites
        self.sprite_list.draw()
        return None
    
    def on_update(self, delta_time: float) -> bool | None:
        self.sprite_list.update()
        return super().on_update(delta_time)

    def on_key_press(self, symbol: int, modifiers: int) -> bool | None:
        """Keyboard interaction"""

        # Switch to GameView if space is hit
        if symbol == arcade.key.SPACE:
            self.engine.switch_game()

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
                self.engine.switch_game()

        return None

    def on_mouse_motion(self, x: int, y: int, dx: int, dy: int) -> bool | None:
        if self.start_button.collides_with_point((x,y)):
            c = self.window.get_system_mouse_cursor(self.window.CURSOR_HAND)
            self.start_button.scale = 0.105
            self.window.set_mouse_cursor(c)
        else:
            c = self.window.get_system_mouse_cursor(self.window.CURSOR_DEFAULT)
            self.start_button.scale = 0.1
            self.window.set_mouse_cursor(c)
        return super().on_mouse_motion(x, y, dx, dy)
