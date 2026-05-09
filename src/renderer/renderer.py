from turtle import width
from typing import Any

import arcade
from numpy.typing import NDArray


class Renderer:
    def __init__(self) -> None:
        """Initialize the renderer"""
        self.cheat_mode: bool = False  # Cheat mode enabled or not
        self.fps = 0  # To calculate FPS\

        # Load maze related textures
        self.cheat_maze_wall_texture = arcade.load_texture(
            'assets/maze/cheat_mode_maze_wall.png')
        self.cheat_maze_path_texture = arcade.load_texture(
            'assets/maze/cheat_mode_maze_path.png')
        self.maze_wall_texture = arcade.load_texture(
            'assets/maze/maze_wall.png')
        self.maze_path_texture = arcade.load_texture(
            'assets/maze/maze_path.png')

        # Load logo title sprites
        self.logo_title_texture = arcade.load_texture(
            "assets/misc/logo-title.png"
        )  # Load logo title
        self.logo_title_texture_cheat = arcade.load_texture(
            "assets/misc/logo-title-cheat.png"
        )  # Load logo title

        # Load background texture
        self.bg_texture = arcade.load_texture(
            "assets/background/background_2.png"
        )  # Background texture
        self.bg_texture_cheat = arcade.load_texture(
            "assets/background/background_cheat.png"
        )  # Background cheat texture

        # Load icon textures
        self.life_texture = arcade.load_texture(
            "assets/misc/life.png")  # Lifes texture
        self.xp_texture = arcade.load_texture(
            "assets/misc/xp.png")  # XP texture
        self.lvl_texture = arcade.load_texture(
            "assets/misc/level.png"
        )  # XP texture

        self.maze_sprite_list: arcade.SpriteList[
            arcade.Sprite] = arcade.SpriteList()
        
        # List containing attributes (lifes, score, etc.)
        self.attributes_sprites: list[arcade.Rect] = []

        # Cache
        self._cached_window_size: tuple[int, int] = (-1, -1)

    def render_game(self, maze: NDArray[Any], path: NDArray[Any], lifes: int, entity_list: arcade.SpriteList) -> None:
        """Draws the game to the screen"""
        CONTROL_TEXT = 'Escape: Pause       Space: Cheat       R: Next lvl'

        window = arcade.get_window()
        tile_size = self.get_tile_size(maze, window)

        # Draw background
        bg_rect = self.get_background(window)
        if self.cheat_mode:
            arcade.draw_texture_rect(self.bg_texture_cheat, bg_rect)
            shadow = 220
        else:
            arcade.draw_texture_rect(self.bg_texture, bg_rect)
            shadow = 150

        # Apply a soft shadow on the screen
        arcade.draw_lbwh_rectangle_filled(
            0, 0, window.width, window.height, (0, 0, 0, shadow)
        )

        # Draw maze
        self.maze_sprite_list = self.build_maze_walls(maze, path, tile_size, window)
        self.maze_sprite_list.draw()

        maze_dimensions = self.calculate_maze_dimensions(maze)
        for e in entity_list:
            e.center_x = int(
                e._x * tile_size
                + window.width / 2
                - (tile_size * 2 * maze_dimensions[0]) / 2
            )
            e.center_y = int(
                e._y * tile_size
                + window.height / 2
                - (tile_size * 2 * maze_dimensions[1]) / 2
            )
        entity_list.draw()

        # Draw logo
        self.logo = self.create_logo(window)
        if self.cheat_mode:
            arcade.draw_texture_rect(self.logo_title_texture_cheat,
                                    self.logo)
        else:
            arcade.draw_texture_rect(self.logo_title_texture,
                                    self.logo)

        # Draw lifes
        self.draw_attribute(window,
                            self.life_texture,
                            self.logo.x + self.logo.width / 2 + window.width * 0.01,
                            self.logo.y,
                            lifes)

        # Draw XP
        self.draw_attribute(window,
                            self.xp_texture,
                            self.attributes_sprites[-1].x + 150,
                            self.logo.y,
                            99)

        # Draw level
        self.draw_attribute(window,
                            self.lvl_texture,
                            self.attributes_sprites[-1].x + 150,
                            self.logo.y,
                            '1')

        # Draw controls
        arcade.draw_text(
            CONTROL_TEXT,
            window.width / 2,
            window.height * 0.05,
            arcade.color.WHITE,
            16,
            font_name="Early GameBoy",
            anchor_x='center'
        )


    def draw_attribute(
        self,
        window: arcade.Window,
        icon: arcade.Texture,
        x: int,
        y: int,
        value: str | int = 0,
    ) -> None:
        placeholder = self.create_attribute_placeholder(
            window, x, y, 
        )
        arcade.draw_texture_rect(icon, placeholder)
        text_y = y
        arcade.draw_text(
            value,
            placeholder.x + placeholder.width / 2,
            text_y - (24 / 2),
            arcade.color.WHITE,
            24,
            font_name="Early GameBoy",
        )
        self.attributes_sprites.append(placeholder)

    def create_attribute_placeholder(
        self, window: arcade.Window, x: int, y: int, added_width: float = 0
    ) -> arcade.Rect:
        """Creates a layer that displays the lifes of the player"""
        resize_factor = 0.05
        width = window.height * resize_factor
        rect = arcade.Rect(
            x=x,
            y=y,
            width=width,
            height=window.height * resize_factor,
            left=0,
            right=0,
            bottom=0,
            top=0,
        )
        return rect

    def create_logo(self, window: arcade.Window) -> arcade.Rect:
        """Creates a layer that displays the logo of the game"""
        resize_factor = 0.15
        rect = arcade.Rect(
            x=window.width / 2,
            y=window.height * 0.93,
            width=self.logo_title_texture.width
            * ((window.height * resize_factor
                ) / self.logo_title_texture.height),
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
        self, walls: NDArray[Any], path: NDArray[Any], tile_size: int, window: arcade.Window
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
            self.save_blocs(self.cheat_maze_wall_texture, walls, tile_size, window, maze_dimensions)
            self.save_blocs(self.cheat_maze_path_texture, path, tile_size, window, maze_dimensions)
        else:
            self.save_blocs(self.maze_wall_texture, walls, tile_size, window, maze_dimensions)
            self.save_blocs(self.maze_path_texture, path, tile_size, window, maze_dimensions)

        self._cached_window_size = window.get_size()

        return self.maze_sprite_list

    def save_blocs(self, texture: arcade.Texture, coords: NDArray[Any],
                   tile_size: int, window: arcade.Window,
                   maze_dimensions: tuple[int, int]) -> None:
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