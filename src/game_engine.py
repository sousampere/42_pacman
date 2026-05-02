import arcade


class GameEngineError(Exception):
    def __init__(self, msg: str = "") -> None:
        super().__init__(f"GameEngine error: {msg}")


class FontError(GameEngineError):
    def __init__(self, msg: str = "") -> None:
        super().__init__(f"Font error: {msg}")


class MenuView(arcade.View):
    """View of the menu (onboarding)"""

    def __init__(self, engine: "GameEngine") -> None:
        super().__init__()
        self.engine = engine
        self.background_color = (0, 8, 20)  # Soft black background
        self.sprite_list = arcade.SpriteList()

        # -- Load sprites --
        # Load play button :
        self.start_button = arcade.Sprite("assets/buttons/play.png", 0.1)
        self.start_button.change_x += self.engine.width / 2
        self.start_button.change_y += self.engine.height / 2
        self.start_button.center_x = self.engine.width / 2
        self.start_button.center_y = self.engine.height / 2 - self.engine.height * 0.2
        self.sprite_list.append(self.start_button)
        # Load background
        try:
            self.background = arcade.load_texture("assets/background/background_1.jpg")
        except (FileNotFoundError, PermissionError):
            self.background = None

    def on_draw(self) -> bool | None:
        """Method for drawing at screen"""
        self.clear()

        # Apply background
        if self.background is not None:
            rect = arcade.Rect(
                x=self.width / 2,
                y=self.height / 2,
                width=self.width,
                height=self.height,
                left=0,
                right=0,
                bottom=0,
                top=0,
            )
            arcade.draw_texture_rect(self.background, rect)

        # Apply a soft shadow on the screen
        arcade.draw_lbwh_rectangle_filled(
            0, 0, self.engine.width, self.engine.height, (0, 0, 0, 128)
        )

        # Write "Welcome to Pac-Man"
        arcade.draw_text(
            "Pac-Man",
            self.engine.width / 2,
            self.engine.height * 0.9,
            color=arcade.color.WHITE_SMOKE,
            font_size=42,
            anchor_x="center",
            anchor_y="center",
            font_name="Early GameBoy",
        )

        # Draw sprites
        self.sprite_list.draw()
        return None

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


class GameView(arcade.View):
    """View of the game (in-game)"""

    def __init__(self, engine: "GameEngine") -> None:
        super().__init__()
        self.engine = engine
        self.background_color = arcade.color.RED
        self.sprites: arcade.SpriteList[arcade.Sprite] = arcade.SpriteList()

        # -- Load sprites --
        # Player sprite
        self.circle = arcade.Sprite()
        self.circle.position = self.center
        self.sprites.append(self.circle)

    def on_draw(self) -> bool | None:
        self.clear()
        self.sprites.draw()

        return None

    def on_key_press(self, symbol: int, modifiers: int) -> bool | None:
        if symbol == arcade.key.ESCAPE:
            self.engine.switch_pause()
        if symbol == arcade.key.SPACE:
            self.circle.change_x -= 50

        return None

    def on_update(self, delta_time: float) -> bool | None:
        self.sprites.update()

        return None


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
            0, 0, self.engine.width, self.engine.height, (0, 0, 0, 128)
        )

        # Write "Paused..."
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
        """Keyboard interaction"""
        # Exit pause if escape is pressed
        if symbol == arcade.key.ESCAPE:
            self.engine.switch_game()

        return None


class FinishView(arcade.View):
    """View of the game (in-game)"""

    def __init__(self, engine: "GameEngine") -> None:
        super().__init__()
        self.engine = engine
        self.background_color = arcade.color.GRAY

    def on_draw(self) -> bool | None:
        self.clear()

        return None


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
