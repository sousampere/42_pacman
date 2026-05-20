from typing import Any

import arcade
from numpy.typing import NDArray

from src.entity.ghost import Ghost
from src.entity.pacgum import Pacgum
from src.entity.player import Player
from src.entity.super_pacgum import SuperPacgum


class Renderer:
    def __init__(self) -> None:
        """Initialize the renderer"""
        self.cheat_mode: bool = False  # Cheat mode enabled or not
        self.fps = 0  # To calculate FPS\

        # Load maze related textures
        self.cheat_maze_wall_texture = arcade.load_texture(
            "assets/maze/cheat_mode_maze_wall.png"
        )
        self.cheat_maze_path_texture = arcade.load_texture(
            "assets/maze/cheat_mode_maze_path.png"
        )
        self.maze_wall_texture = arcade.load_texture(
            "assets/maze/maze_wall.png"
        )
        self.maze_path_texture = arcade.load_texture(
            "assets/maze/maze_path.png"
        )

        # Load logo title sprites
        self.logo_title_texture = arcade.load_texture(
            "assets/misc/logo-title.png"
        )  # Load logo title
        self.logo_title_texture_cheat = arcade.load_texture(
            "assets/misc/logo-title-cheat.png"
        )  # Load logo title

        # Load background texture
        self.bg_texture = arcade.load_texture(
            "assets/background/background_5.png"
        )  # Background texture
        self.bg_texture_cheat = arcade.load_texture(
            "assets/background/background_cheat.png"
        )  # Background cheat texture

        # Load icon textures
        self.life_texture = arcade.load_texture(
            "assets/misc/life.png"
        )  # Lifes texture
        self.xp_texture = arcade.load_texture(
            "assets/misc/xp.png"
        )  # XP texture
        self.lvl_texture = arcade.load_texture(
            "assets/misc/level.png"
        )  # XP texture
        self.time_texture = arcade.load_texture(
            "assets/misc/time.png"
        )  # Time texture

        self.maze_sprite_list: arcade.SpriteList[arcade.Sprite] = (
            arcade.SpriteList()
        )

        # List containing attributes (lifes, score, etc.)
        self.attributes_sprites: list[arcade.Rect] = []

        # Cache
        self._cached_window_size: tuple[int, int] = (-1, -1)

    def render_game(
        self,
        maze: NDArray[Any],
        path: NDArray[Any],
        entity_list: arcade.SpriteList[Player | Ghost | Pacgum | SuperPacgum],
        lifes: int,
        time: int,
        xp: int,
        level: int,
        fps: int,
        game_view: "GameView"
    ) -> None:
        """Draws the game to the screen"""
        window = arcade.get_window()

        attributes: list[dict[str, arcade.Texture | str]] = []

        tile_size = self.get_tile_size(maze, window)

        # Draw background
        bg_rect = self.get_background(window)
        if self.cheat_mode:
            arcade.draw_texture_rect(self.bg_texture_cheat, bg_rect)
            shadow = 220
        else:
            arcade.draw_texture_rect(self.bg_texture, bg_rect)
            shadow = 200

        # Apply a soft shadow on the screen
        arcade.draw_lbwh_rectangle_filled(
            0, 0, window.width, window.height, (0, 0, 0, shadow)
        )

        # Draw maze
        self.maze_sprite_list = self.build_maze_walls(
            maze, path, tile_size, window
        )
        self.maze_sprite_list.draw()

        maze_dimensions = self.calculate_maze_dimensions(maze)
        for e in entity_list:
            if isinstance(e, Pacgum):
                e.size = (int(tile_size*0.5), int(tile_size*0.5))
            else:
                e.size = (tile_size, tile_size)
            e.center_x = (int(
                e._x * tile_size
                + window.width / 2
                - (tile_size * 2 * maze_dimensions[0]) / 2
            ))
            e.center_y = int(
                e._y * tile_size
                + window.height / 2
                - (tile_size * 2 * maze_dimensions[1]) / 2
            )
        entity_list.draw()

        # Draw logo
        self.logo = self.create_logo(window)
        if self.cheat_mode:
            arcade.draw_texture_rect(self.logo_title_texture_cheat, self.logo)
        else:
            arcade.draw_texture_rect(self.logo_title_texture, self.logo)

        # Draw attributes
        attributes.append({"texture": self.life_texture, "value": str(lifes)})
        attributes.append({"texture": self.xp_texture, "value": str(xp)})
        attributes.append({"texture": self.lvl_texture, "value": str(level)})
        attributes.append({"texture": self.time_texture, "value": str(time)})
        self.draw_attributes(self.logo, attributes, window)


        # Draw controls
        control_list: list[tuple[str, bool]] = []
        if self.cheat_mode:
            control_list.append(("Escape: Pause", False))
            control_list.append(("1:Invincibility", game_view.invincibility))
            control_list.append(("2:Get a life", False))
            control_list.append(("3:Complete lvl", False))
            control_list.append(("4:Freeze ghosts", game_view.freeze_ghosts))
        else:
            control_list.append(("Escape: Pause", False))
        
        font_size: int = int(min(window.height / 100, window.width / 100))
        texts = []
        for i, control_text in enumerate(control_list):
            if (len(control_list) == 1):
                x = window.width / 2
            else:
                x = window.width / 2 + (window.width * 0.2) * i - (len(control_text) * (window.width * 0.2))
            text_obj = arcade.Text(
                control_text[0],
                x,
                window.height * (0.05 - 1 * 0.03),
                arcade.color.GREEN if control_text[1] else arcade.color.WHITE,
                font_size,
                font_name="Early GameBoy",
                anchor_x="center",
            )
            texts.append(text_obj)
        for text in texts:
            text.draw()

        font_size: int = int(window.height / 50)
        fps_text = arcade.Text(
            f"FPS: {int(fps)}",
            10,
            window.height - 10 - 18,
            (50, 255, 50),
            font_size,
            font_name="Early GameBoy",
        )
        fps_text.draw()

    def draw_attributes(
        self,
        logo_rect: arcade.Rect,
        attributes: list[dict[str, arcade.Texture | str]],
        window: arcade.Window,
    ) -> None:
        """Draw attributes to the screen"""
        for index, attribute in enumerate(attributes):
            # Draw pair attributes to the right
            if index % 2 == 0:
                x = (
                    window.width / 2
                    + logo_rect.width / 2
                    + window.width * 0.03
                    + window.width * index / 15
                )
            else:
                x = (
                    window.width / 2
                    - logo_rect.width / 2
                    - window.width * 0.03
                    - window.width * index / 15
                )
            sprite_size: int = int(window.height / 20)
            attrib_rect = arcade.Rect(
                x=x,
                y=logo_rect.y,
                width=sprite_size,
                height=sprite_size,
                left=0,
                right=0,
                bottom=0,
                top=0,
            )
            arcade.draw_texture_rect(attribute["texture"], attrib_rect)
            text_size: int = int(window.height / 50)
            text = arcade.Text(
                text=attribute["value"],
                x=attrib_rect.x + attrib_rect.width,
                y=attrib_rect.y,
                font_size=text_size,
                font_name="Early GameBoy",
                # anchor_x="center",
                anchor_y="center",
                color=arcade.color.WHITE,
            )
            text.draw()

    def create_logo(self, window: arcade.Window) -> arcade.Rect:
        """Creates a layer that displays the logo of the game"""
        resize_factor = 0.15
        rect = arcade.Rect(
            x=window.width / 2,
            y=window.height * 0.93,
            width=self.logo_title_texture.width
            * (
                (window.height * resize_factor)
                / self.logo_title_texture.height
            ),
            height=window.height * resize_factor,
            left=0,
            right=0,
            bottom=0,
            top=0,
        )
        return rect

    def calculate_maze_dimensions(self, maze: NDArray[Any]) -> tuple[int, int]:
        """Refresh the self.maze_dimensions according to the current maze"""
        x = maze[:, 0].max()
        y = maze[:, 1].max()
        return (int(x / 2), int(y / 2))

    def build_maze_walls(
        self,
        walls: NDArray[Any],
        path: NDArray[Any],
        tile_size: int,
        window: arcade.Window,
    ) -> arcade.SpriteList[arcade.Sprite]:
        """Returns a list of sprites corresponding to each bloc composing the
        given maze.

        The sprites have a size of (tile_size) which is calculated depending
        on the window dimensions,
        so that the maze always let at least a 20% margin on each window side
        """
        if self._cached_window_size == window.get_size():
            return self.maze_sprite_list
        maze_dimensions = self.calculate_maze_dimensions(walls)

        self.maze_sprite_list = arcade.SpriteList()
        if self.cheat_mode:
            self.save_blocs(
                self.cheat_maze_wall_texture,
                walls,
                tile_size,
                window,
                maze_dimensions,
            )
            self.save_blocs(
                self.cheat_maze_path_texture,
                path,
                tile_size,
                window,
                maze_dimensions,
            )
        else:
            self.save_blocs(
                self.maze_wall_texture,
                walls,
                tile_size,
                window,
                maze_dimensions,
            )
            self.save_blocs(
                self.maze_path_texture,
                path,
                tile_size,
                window,
                maze_dimensions,
            )

        self._cached_window_size = window.get_size()

        return self.maze_sprite_list

    def save_blocs(
        self,
        texture: arcade.Texture,
        coords: NDArray[Any],
        tile_size: int,
        window: arcade.Window,
        maze_dimensions: tuple[int, int],
    ) -> None:
        xs = (
            coords[:, 0] * tile_size
            + window.width / 2
            - (tile_size * 2 * maze_dimensions[0]) / 2
        ).astype(int)
        ys = (
            coords[:, 1] * tile_size
            + window.height / 2
            - (tile_size * 2 * maze_dimensions[1]) / 2
        ).astype(int)

        for x, y in zip(xs, ys):
            bloc = arcade.Sprite(texture, 1, x, y)
            bloc.width = tile_size
            bloc.height = tile_size
            self.maze_sprite_list.append(bloc)

    def get_tile_size(self, maze: NDArray[Any], window: arcade.Window) -> int:
        """Return an adapted tile size for the window size"""
        maze_dimensions = self.calculate_maze_dimensions(maze)
        max_x = maze_dimensions[0] * 2 + 1
        max_y = maze_dimensions[1] * 2 + 1

        tile_size = min(window.width / max_x, window.height / max_y) * 0.8

        return min(30, int(tile_size))

    def get_background(self, window: arcade.Window) -> arcade.Rect:
        # Apply background
        rect = arcade.Rect(
            x=window.width / 2,
            y=window.height / 2,
            width=window.width,
            height=window.height,
            left=0,
            right=0,
            bottom=0,
            top=0,
        )
        return rect

    def reset_cache(self) -> None:
        self._cached_window_size = (-1, -1)
