import arcade


class SoundManager:
    def __init__(self) -> None:
        self.menu_music = arcade.load_sound(
            "assets/sfx/menu_music.wav", streaming=True
        )
        self.game_music = arcade.load_sound(
            "assets/sfx/game_music.wav", streaming=True
        )
        self.end_screen_music = arcade.load_sound(
            "assets/sfx/end_screen.wav", streaming=True
        )
        self.die_sound = arcade.load_sound("assets/sfx/die.wav")
        self.pacgum_sound = arcade.load_sound("assets/sfx/pacgum.wav")
        self.super_pacgum_sound = arcade.load_sound(
            "assets/sfx/super_pacgum.wav"
        )
        self.ghost_death = arcade.load_sound("assets/sfx/ghost_death.wav")
        self.transition_sound = arcade.load_sound("assets/sfx/transition.wav")
        self.music_player = None

    def event_play_menu_music(self, speed: float = 1) -> None:
        """Starts playing the menu music"""
        self.event_stop_music()
        self.music_player = arcade.play_sound(
            self.menu_music, speed=speed, loop=True, volume=0.8
        )

    def event_play_game_music(self, speed: float = 1) -> None:
        """Starts playing the game music"""
        self.event_stop_music()
        self.music_player = arcade.play_sound(
            self.game_music, speed=speed, loop=True, volume=0.6
        )

    def event_play_end_music(self, speed: float = 1) -> None:
        """Starts playing the game music"""
        self.event_stop_music()
        self.music_player = arcade.play_sound(
            self.end_screen_music, speed=speed, loop=True, volume=0.6
        )

    def event_stop_music(self) -> None:
        """Stops music if playing"""
        if self.music_player is not None:
            arcade.stop_sound(self.music_player)

    def event_play_die_sound(self) -> None:
        """Plays a dying sound"""
        try:
            arcade.play_sound(self.die_sound, volume=0.8)
        except RuntimeError:
            # Ignore error if sound already playng
            pass

    def event_play_pacgum_sound(self) -> None:
        """Plays a pacgum sound"""
        try:
            arcade.play_sound(self.pacgum_sound, volume=100)
        except RuntimeError:
            # Ignore error if sound already playng
            pass

    def event_play_super_pacgum_sound(self) -> None:
        """Plays a super pacgum sound"""
        try:
            arcade.play_sound(self.super_pacgum_sound, volume=3)
        except RuntimeError:
            # Ignore error if sound already playng
            pass

    def event_play_ghost_death_sound(self) -> None:
        """Plays a ghost death sound"""
        try:
            arcade.play_sound(self.ghost_death, volume=0)
        except RuntimeError:
            # Ignore error if sound already playng
            pass

    def event_play_transition_sound(self) -> None:
        """Plays a transition sound"""
        try:
            arcade.play_sound(self.transition_sound, volume=100)
        except RuntimeError:
            # Ignore error if sound already playng
            pass
