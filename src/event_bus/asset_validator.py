
from PIL import Image, UnidentifiedImageError
import wave


class AssetValidationError(Exception):
    def __init__(self, msg: str = "") -> None:
        super().__init__(f"Asset validation error: {msg}")


class AssetValidator:
    @staticmethod
    def validate_assets() -> bool:
        images = [
            'assets/misc/xp.png',
            'assets/misc/time.png',
            'assets/misc/logo-title.png',
            'assets/misc/logo-title-cheat.png',
            'assets/misc/life.png',
            'assets/misc/level.png',

            'assets/maze/maze_wall.png',
            'assets/maze/maze_path.png',
            'assets/maze/cheat_mode_maze_path.png',
            'assets/maze/cheat_mode_maze_wall.png',

            'assets/entity/pacgum.png',
            'assets/entity/super_pacgum.png',
            'assets/entity/spritesheet.png',

            'assets/buttons/exit.png',
            'assets/buttons/menu.png',
            'assets/buttons/play.png',

            'assets/background/background_2.png',
            'assets/background/background_3.png',
            'assets/background/background_4.png',
            'assets/background/background_5.png',
            'assets/background/background_cheat.png',
        ]

        sfx = [
            'assets/sfx/die.wav',
            'assets/sfx/end_screen.wav',
            'assets/sfx/game_music.wav',
            'assets/sfx/ghost_death.wav',
            'assets/sfx/menu_music.wav',
            'assets/sfx/pacgum.wav',
            'assets/sfx/super_pacgum.wav',
            'assets/sfx/transition.wav',
        ]

        AssetValidator.verify_images(*images)
        AssetValidator.verify_sound(*sfx)
        return True

    @staticmethod
    def verify_images(*args: str) -> bool:
        """Load the given images as PIL Image to check its
        validity."""
        for file in args:
            try:
                # Try triggering an error
                with Image.open(file, 'r'):
                    pass
            except (FileNotFoundError, PermissionError, OSError):
                raise AssetValidationError(
                    f'Image {file} not accessible. '
                    'Please provide the '
                    'asset and start again')
            except (UnidentifiedImageError, ValueError,
                    TypeError, IsADirectoryError):
                raise AssetValidationError(
                    f'Image {file} is invalid. '
                    'Please provide a valid '
                    'asset and start again.')
        return True

    @staticmethod
    def verify_sound(*args: str) -> bool:
        for file in args:
            try:
                # Try triggering an error
                with wave.open(file, 'rb') as wav_file:
                    if wav_file.getnframes() == 0:
                        raise wave.Error('Invalid audio file.')
            except (FileNotFoundError, PermissionError, OSError):
                raise AssetValidationError(
                    f'Sound {file} not accessible. '
                    'Please provide the '
                    'asset and start again')
            except (wave.Error,
                    TypeError, IsADirectoryError):
                raise AssetValidationError(
                    f'Sound {file} is invalid. '
                    'Please provide a valid '
                    'asset and start again.')
        return True
