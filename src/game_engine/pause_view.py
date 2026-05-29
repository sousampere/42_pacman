import arcade
from typing import TYPE_CHECKING

from src.event_bus.event_bus import EventBus

if TYPE_CHECKING:
    from ..game_engine.game_engine import GameEngine


class PauseView(arcade.View):
    """View of the pause"""

    def __init__(self, engine: "GameEngine") -> None:
        super().__init__()
        self.engine = engine
        self.background_color = arcade.color.GRAY

        # Sprite for menu button
        self.sprite_list: arcade.SpriteList[arcade.Sprite] = arcade.SpriteList()
        self.menu_btn = arcade.Sprite("assets/buttons/menu.png", 0.1)
        self.sprite_list.append(self.menu_btn)


    def on_draw(self) -> bool | None:
        self.clear()

        # Draw the screen of the GameView
        self.engine.game_view.on_draw()

        # Apply a soft shadow on the screen
        arcade.draw_lbwh_rectangle_filled(
            0, 0, self.window.width, self.window.height, (0, 0, 0, 128)
        )

        # Write "Paused..."
        text = arcade.Text(
            "Paused...",
            self.window.width / 2,
            self.window.height / 2,
            color=arcade.color.WHITE_SMOKE,
            font_size=24,
            anchor_x="center",
            anchor_y="center",
            font_name="Early GameBoy",
        )
        text.draw()

        # Exit button placement
        self.menu_btn.center_x = self.window.width - 10 - self.menu_btn.width
        self.menu_btn.center_y = self.window.height - 10 - self.menu_btn.height
        self.sprite_list.draw()

        return None

    def on_key_press(self, symbol: int, modifiers: int) -> bool | None:
        """Keyboard interaction"""
        # Exit pause if escape is pressed
        if symbol == arcade.key.ESCAPE:
            self.engine.switch_game()
        if symbol == arcade.key.F11:
            EventBus.broadcast_event('toggle_fullscreen')

        return None

    def on_show_view(self) -> None:
        EventBus.broadcast_event("stop_music")
        return super().on_show_view()

    def on_mouse_press(
        self, x: int, y: int, button: int, modifiers: int
    ) -> bool | None:
        """Mouse interaction"""
        # Get list of sprite hit by mouse
        hits = arcade.get_sprites_at_point((x, y), self.sprite_list)

        for sprite in hits:
            if sprite == self.menu_btn:
                EventBus.broadcast_event('switch_menu')
                EventBus.broadcast_event('reload_views')

        return None
    
    def on_mouse_motion(self, x: int, y: int, dx: int, dy: int) -> bool | None:
        """Detect collision of the mouse with the menu button, and
        change the cursor if the mouse overlaps the menu button"""
        if self.menu_btn.collides_with_point((x, y)):
            c = self.window.get_system_mouse_cursor(self.window.CURSOR_HAND)
            self.menu_btn.scale = 0.105
            self.window.set_mouse_cursor(c)
        else:
            c = self.window.get_system_mouse_cursor(self.window.CURSOR_DEFAULT)
            self.menu_btn.scale = 0.1
            self.window.set_mouse_cursor(c)
