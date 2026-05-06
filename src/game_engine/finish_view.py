
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

    def on_draw(self) -> bool | None:
        self.clear()

        return None
