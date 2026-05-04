
from arcade.shape_list import ShapeElementList, create_rectangle_filled

from ..maze_adapter.maze_adapter import MazeAdapter

import arcade

class GameView(arcade.View):
    """View of the game (in-game)"""

    def __init__(self, engine: "GameEngine") -> None:
        """Initialize the view"""
        self.engine = engine  # GameEngine to access engine variables

        # Scene setup
        self.background_color = arcade.color.BLACK  # Default
        self.MAZE_DIMENSIONS = (40, 14)
        self.maze = MazeAdapter(self.MAZE_DIMENSIONS).get_multiple_maze()[0]
        self.previous_frame_dimensions = (self.window.width, self.window.height)
        self.level = 0

        # Sprites setup
        self.sprites: arcade.SpriteList[arcade.Sprite] = arcade.SpriteList()
        self.cell_sprite = arcade.load_texture('assets/maze/bloc.png')
        self.maze_blocs = arcade.SpriteList()

        # -- Load sprites --
        # Player sprite
        self.circle = arcade.Sprite('assets/maze/bloc.png')
        self.circle.position = self.window.center
        self.sprites.append(self.circle)


    def get_maze(self, level: int) -> list[list[int]]:
        """ WIP, This function will generate maze"""
        return self.maze[0]

    def on_draw(self) -> bool | None:
        """Function to draw on the screen"""
        self.clear() # Clear previous frame
        self.sprites.draw() # Display all sprites from the self.sprites list

        # Draw all the sprites on the screen
        if (self.previous_frame_dimensions != (self.window.width, self.window.height)
            or len(self.maze_blocs) == 0):
            self.previous_frame_dimensions = (self.window.width, self.window.height)
            self.maze_blocs = arcade.SpriteList()
            coords = self.get_walls_blocs_coords()
            for coord in coords:
                # Get the most optimal tile size
                if (self.MAZE_DIMENSIONS[0] > self.MAZE_DIMENSIONS[1]):
                    tile_size = (self.window.width / (self.MAZE_DIMENSIONS[0] * 2)) * 0.7
                else:
                    tile_size = (self.window.height / (self.MAZE_DIMENSIONS[1] * 2)) * 0.7
                bloc = arcade.Sprite(
                    self.cell_sprite,
                    1,
                    coord[0] * tile_size + self.window.width/2 - (tile_size * 2 * self.MAZE_DIMENSIONS[0]) / 2,
                    coord[1] * tile_size + self.window.height/2 - (tile_size * 2 * self.MAZE_DIMENSIONS[1]) / 2
                    )
                bloc.width = tile_size
                bloc.height = tile_size
                self.maze_blocs.append(bloc)

        # Draw maze blocs
        self.maze_blocs.draw()

        return None

    def on_key_press(self, symbol: int, modifiers: int) -> bool | None:
        """Keyboard interactions events"""
        if symbol == arcade.key.ESCAPE:
            self.engine.switch_pause()
        if symbol == arcade.key.SPACE:
            self.circle.change_x -= 10
        if symbol == arcade.key.R:
            self.level += 1
            self.maze = MazeAdapter(self.MAZE_DIMENSIONS).get_multiple_maze()[self.level]
            self.maze_blocs = arcade.SpriteList()
            print(f'level {self.level}')

        return None

    def on_update(self, delta_time: float) -> bool | None:
        """ Update sprites """
        self.sprites.update()

        return None

    def on_resize(self, width: int, height: int) -> bool | None:
        print(width, height)
        return super().on_resize(width, height)

    def get_walls_blocs_coords(self) -> list[tuple[int, int]]:
        """Returns a list of walls coords from the engine's maze"""
        maze = self.get_maze(self.level)
        coords: set[tuple[int, int]] = set()  # List of coords of all wall blocs (x,y)

        # Scan each cell
        for y, row in enumerate(maze[::-1]):  # reverse read due to for loop
                for x, cell in enumerate(row):
                    if cell & 4:  # 4 because the maze is read in reversed because of for loop
                        # Top wall
                        coords.add(((x * 2), (y * 2)))
                        coords.add(((x * 2) + 1, (y * 2)))
                        coords.add(((x * 2) + 2, (y * 2)))
                    if cell & 2:
                        # Right wall
                        coords.add(((x * 2) + 2, (y * 2)))
                        coords.add(((x * 2) + 2, (y * 2) + 1))
                        coords.add(((x * 2) + 2, (y * 2) + 2))
                    if cell & 1:  # 1 because the maze is read in reversed because of for loop
                        # Bottom wall
                        coords.add(((x * 2), (y * 2) + 2))
                        coords.add(((x * 2) + 1, (y * 2) + 2))
                        coords.add(((x * 2) + 2, (y * 2) + 2))
                    if cell & 8:
                        # Left wall
                        coords.add(((x * 2), (y * 2)))
                        coords.add(((x * 2), (y * 2) + 1))
                        coords.add(((x * 2), (y * 2) + 2))
                    if cell == 15:
                        # Left wall
                        coords.add(((x * 2) + 1, (y * 2) + 1))
                # # break

        # Return as list
        return list(coords)

