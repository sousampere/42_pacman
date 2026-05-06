from curses import window

import arcade
from arcade import draw

from src.maze_adapter.maze_adapter import MazeAdapter

class Renderer:
    def __init__(self) -> None:
        """Initialize the renderer"""
        self.maze_bloc_texture = arcade.load_texture('assets/maze/bloc.png')  # Load bloc texture
        self.logo_title_texture = arcade.load_texture('assets/misc/logo-title.png')  # Load logo title
        self.life_texture = arcade.load_texture('assets/misc/life.png')  # Lifes texture
        self.xp_texture = arcade.load_texture('assets/misc/xp.png')  # XP texture
        self.fps = 0  # To calculate FPS
        self.maze_adapter = MazeAdapter()
        pass

    def render_game(self, maze: list[list[int]], lifes: int = 42) -> None:
        """Draws the game to the screen"""
        window = arcade.get_window()
        HUD_x = int(self.calculate_maze_dimensions(maze)[0] * self.get_tile_size(maze) + window.width / 2)

        # Draw maze
        maze_blocs = self.build_maze_walls(maze)
        maze_blocs.draw()

        # Draw logo
        logo = self.create_logo()
        arcade.draw_texture_rect(self.logo_title_texture, logo)

        # Draw lifes
        self.draw_attribute(self.life_texture, HUD_x, lifes, 0)

        # Draw XP
        self.draw_attribute(self.xp_texture, HUD_x, lifes, -(window.height * 0.05))

    def draw_attribute(self, icon: arcade.Texture, HUD_x: int, value: str | int = 0, added_height: int = 0) -> None:
        window = arcade.get_window()
        placeholder = self.create_attribute_placeholder(int(HUD_x), added_height)
        arcade.draw_texture_rect(icon, placeholder)
        text_x = placeholder.x + window.width * 0
        text_y = window.height * 0.7 + added_height - (24 / 2)
        arcade.draw_text(value, text_x, text_y, arcade.color.WHITE, 24, font_name='Early GameBoy')
        pass

    def create_attribute_placeholder(self, HUD_x: int, added_height: int = 0) -> arcade.Rect:
        """Creates a layer that displays the lifes of the player"""
        window = arcade.get_window()
        resize_factor = 0.05
        width = self.logo_title_texture.width * ((window.height * resize_factor) / self.logo_title_texture.height)
        rect = arcade.Rect(
            x=HUD_x + width / 2,
            y=window.height * 0.7 + added_height,
            width=(self.logo_title_texture.width) / (self.logo_title_texture.height / (window.height * resize_factor)),
            height=window.height * resize_factor,
            left=0,
            right=0,
            bottom=0,
            top=0
        )
        return rect

    def create_logo(self) -> arcade.Rect:
        """Creates a layer that displays the logo of the game"""
        window = arcade.get_window()
        resize_factor = 0.15
        rect = arcade.Rect(
            x=window.width / 2,
            y=window.height * 0.93,
            width=self.logo_title_texture.width * ((window.height * resize_factor) / self.logo_title_texture.height),
            height=window.height * resize_factor,
            left=0,
            right=0,
            bottom=0,
            top=0
        )
        return rect

    def calculate_maze_dimensions(self, maze: list[list[int]]) -> tuple[int, int]:
        """Refresh the self.MAZE_DIMENSIONS according to the current maze"""
        MAZE_DIMENSIONS = (len(maze[0]), len(maze))
        return MAZE_DIMENSIONS

    def build_maze_walls(self, maze: list[list[int]]) -> arcade.SpriteList[arcade.Sprite]:
        """Returns a list of sprites corresponding to each bloc composing the given maze.

        The sprites have a size of (tile_size) which is calculated depending on the window dimensions,
        so that the maze always let at least a 20% margin on each window side"""
        # Draw all the sprites on the screen
        maze_blocs: arcade.SpriteList[arcade.Sprite] = arcade.SpriteList()
        coords = self.maze_adapter.get_walls_blocs_coords(maze)
        MAZE_DIMENSIONS = self.calculate_maze_dimensions(maze)
        window = arcade.get_window()
        for coord in coords:
            # Calculate tile size that will be OK for the current window size
            tile_size = self.get_tile_size(maze)

            # Create sprite with a good tile size
            bloc = arcade.Sprite(
                self.maze_bloc_texture,
                1,
                coord[0] * tile_size + window.width/2 - (tile_size * 2 * MAZE_DIMENSIONS[0]) / 2,
                coord[1] * tile_size + window.height/2 - (tile_size * 2 * MAZE_DIMENSIONS[1]) / 2
                )
            bloc.width = tile_size
            bloc.height = tile_size
            maze_blocs.append(bloc)

        return maze_blocs

    def get_tile_size(self, maze: list[list[int]]) -> int:
        """ Return an adapted tile size for the window size"""
        # Get maze dimensions
        MAZE_DIMENSIONS = self.calculate_maze_dimensions(maze)
        max_x = MAZE_DIMENSIONS[0] * 2 + 1
        max_y = MAZE_DIMENSIONS[1] * 2 + 1

        # Get window dimensions
        window = arcade.get_window()

        # Calculate tile size so that the maze takes max (multiplicator)% of height/width
        tile_size = min(
            window.width / max_x,
            window.height / max_y
        ) * 0.8

        return int(tile_size)
