from pubsub import pub
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from ..game_engine.game_engine import GameEngine


class EventBus:
    @classmethod
    def initialize(cls, game_engine: "GameEngine") -> None:
        """Initialize events"""
        # Init view switching
        pub.subscribe(game_engine.switch_game, "switch_game")
        pub.subscribe(game_engine.switch_menu, "switch_menu")
        pub.subscribe(game_engine.switch_pause, "switch_pause")
        pub.subscribe(game_engine.switch_finish, "switch_finish")

        # Init finish view events
        pub.subscribe(game_engine.finish_view.event_save_score, "save_score")

        # Init score events
        pub.subscribe(
            game_engine.score_manager.event_add_pacgum_point,
            "add_pacgum_point",
        )

        # Init cheat events
        pub.subscribe(
            game_engine.cheat_manager.event_enable_cheat_mode, "enable_cheat"
        )
        pub.subscribe(
            game_engine.cheat_manager.event_toggle_invincibility,
            "toggle_invincibility",
        )
        pub.subscribe(
            game_engine.cheat_manager.event_toggle_freeze_ghosts,
            "toggle_freeze_ghosts",
        )

        # Init game manager events (state changes)
        pub.subscribe(game_engine.game_manager.event_add_life, "add_life")
        pub.subscribe(game_engine.game_manager.event_remove_life, "remove_life")
        pub.subscribe(game_engine.game_manager.event_next_level, "next_level")

        # Init GameEngine events
        pub.subscribe(game_engine.event_next_level, "next_level")
        pub.subscribe(game_engine.event_reload_views, "reload_views")
        pub.subscribe(game_engine.event_toggle_fullscreen, "toggle_fullscreen")
        pub.subscribe(game_engine.event_game_over, "game_over")
        pub.subscribe(game_engine.switch_finish, "switch_finish")

    @staticmethod
    def broadcast_event(event: str, **kwargs: Any) -> None:
        pub.sendMessage(event, **kwargs)
