from tkinter import font

import arcade


class GameEngineError(Exception):
    pass


class FontError(GameEngineError):
    pass


class MenuView(arcade.View):
    """View of the menu (onboarding)"""

    def __init__(self, engine: "GameEngine") -> None:
        super().__init__()
        self.engine = engine
        self.background_color = arcade.color.AQUA

    def on_draw(self) -> bool | None:
        self.clear()
        return super().on_draw()

    def on_key_press(self, symbol: int, modifiers: int) -> bool | None:
        if symbol == arcade.key.SPACE:
            self.engine.switch_game()
        return super().on_key_press(symbol, modifiers)


class GameView(arcade.View):
    """View of the game (in-game)"""

    def __init__(self, engine: "GameEngine") -> None:
        super().__init__()
        self.engine = engine
        self.background_color = arcade.color.RED
        self.sprites: arcade.SpriteList[arcade.Sprite] = arcade.SpriteList()

        # Player sprite
        self.circle = arcade.Sprite()
        self.circle.position = self.center
        self.sprites.append(self.circle)

    def on_draw(self) -> bool | None:
        self.clear()
        self.sprites.draw()
        return super().on_draw()

    def on_key_press(self, symbol: int, modifiers: int) -> bool | None:
        if symbol == arcade.key.ESCAPE:
            self.engine.switch_pause()
        if symbol == arcade.key.SPACE:
            self.circle.change_x -= 50
        return super().on_key_press(symbol, modifiers)

    def on_update(self, delta_time: float) -> bool | None:
        self.sprites.update()
        return super().on_update(delta_time)


class PauseView(arcade.View):
    """View of the pause"""

    def __init__(self, engine: "GameEngine") -> None:
        super().__init__()
        self.engine = engine
        self.background_color = arcade.color.GRAY


    def on_draw(self) -> bool | None:
        self.clear()
        super().on_draw()

        # Draw the screen of the GameView
        self.engine.game_view.on_draw()

        # Apply a soft shadow on the screen
        arcade.draw_lbwh_rectangle_filled(
            0, 0, self.engine.width, self.engine.height, (0, 0, 0, 128)
        )

        # Write "Paused..."
        start_x = 0
        start_y = 100
        arcade.draw_text(
            "Paused...",
            self.engine.width / 2,
            self.engine.height / 2,
            color=arcade.color.WHITE_SMOKE,
            font_size=24,
            anchor_x="center",
            anchor_y="center",
            font_name="Early GameBoy",
        )
        return None

    def on_key_press(self, symbol: int, modifiers: int) -> bool | None:
        if symbol == arcade.key.ESCAPE:
            self.engine.switch_game()
        return super().on_key_press(symbol, modifiers)


class FinishView(arcade.View):
    """View of the game (in-game)"""

    def __init__(self, engine: "GameEngine") -> None:
        super().__init__()
        self.engine = engine
        self.background_color = arcade.color.GRAY

    def on_draw(self) -> bool | None:
        self.clear()
        return super().on_draw()


class GameEngine:
    """Game Engine that orchestrate different views and their data"""

    def __init__(self) -> None:
        self.width = 1280
        self.height = 720
        self.window = arcade.Window(
            width=self.width, height=self.height, title="Pac-Man"
        )
        self.maze_adapter = None
        self.config_data = None
        self.is_configured = False  # Set to True when Views added
        try:
            self.pixel_font = arcade.load_font("assets/fonts/Early GameBoy.ttf")
        except (FileNotFoundError, PermissionError):
            pass

    def set_views(
        self, menu: MenuView, game: GameView, pause: PauseView, finish: FinishView
    ) -> None:
        """Initialize the menu, game, pause and finish views."""
        self.menu_view = menu
        self.game_view = game
        self.pause_view = pause
        self.finish_view = finish

        # Switch to menu view by default
        self.switch_menu()

        # Save configuration as done to enable starting the game
        self.is_configured = True

    def switch_menu(self) -> None:
        """Change the current to the menu view"""
        self.window.show_view(self.menu_view)

    def switch_game(self) -> None:
        """Change the current to the game view"""
        self.window.show_view(self.game_view)

    def switch_pause(self) -> None:
        """Change the current to the pause view"""
        self.window.show_view(self.pause_view)

    def switch_finish(self) -> None:
        """Change the current view to the finish view"""
        self.window.show_view(self.finish_view)

    def run(self) -> None:
        """Run the game after"""
        if not self.is_configured:
            raise GameEngineError(
                "Tried to run the game without configuring all game views"
            )
        arcade.run()
        return None
