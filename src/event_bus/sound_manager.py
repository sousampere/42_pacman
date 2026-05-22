
import arcade


class SoundManager:
    def __init__(self) -> None:
        self.menu_music = arcade.load_sound('assets/sfx/menu_music.wav')
        self.game_music = arcade.load_sound('assets/sfx/game_musix.wav', streaming=True)
        self.music_player = None

    def event_play_menu_music(self, speed: float = 1) -> None:
        """Starts playing the menu music"""
        self.event_stop_music()
        self.music_player = arcade.play_sound(self.menu_music, speed=speed, loop=True, pan=1)

    def event_play_game_music(self, speed: float = 1) -> None:
        """Starts playing the game music"""
        self.event_stop_music()
        self.music_player = arcade.play_sound(self.game_music, speed=speed, loop=True)

    def event_stop_music(self) -> None:
        """Stops music if playing"""
        if self.music_player is not None:
            arcade.stop_sound(self.music_player)