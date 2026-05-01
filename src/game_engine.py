import arcade


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

    def on_draw(self) -> bool | None:
        self.clear()
        return super().on_draw()

    def on_key_press(self, symbol: int, modifiers: int) -> bool | None:
        if symbol == arcade.key.ESCAPE:
            self.engine.switch_pause()
        return super().on_key_press(symbol, modifiers)


class PauseView(arcade.View):
    """View of the pause"""

    def __init__(self, engine: "GameEngine") -> None:
        super().__init__()
        self.engine = engine
        self.background_color = arcade.color.GRAY

    def on_draw(self) -> bool | None:
        self.clear()
        return super().on_draw()

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
        self.window = arcade.Window(width=1280, height=720, title="Pac-Man")
        self.maze_adapter = None
        self.config_data = None

    def set_views(
        self, menu: MenuView, game: GameView, pause: PauseView, finish: FinishView
    ) -> None:
        self.menu_view = menu
        self.game_view = game
        self.pause_view = pause
        self.finish_view = finish

    def switch_menu(self) -> None:
        self.window.show_view(self.menu_view)

    def switch_game(self) -> None:
        self.window.show_view(self.game_view)

    def switch_pause(self) -> None:
        self.window.show_view(self.pause_view)

    def switch_finish(self) -> None:
        self.window.show_view(self.finish_view)

    @staticmethod
    def run() -> None:
        arcade.run()
        return None
