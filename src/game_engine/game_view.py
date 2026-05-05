
from src.entity.player import Player

from ..maze_adapter.maze_adapter import MazeAdapter

import arcade

class NotImplementedError(Exception):
    def __init__(self, msg: str = '') -> None:
        super().__init__(f'NOT IMPLEMENTED ERROR: {msg}')

class GameView(arcade.View):
    """View of the game (in-game)"""

    def __init__(self, engine: "GameEngine") -> None:
        """Initialize the view"""
        super().__init__()
        self.engine = engine  # GameEngine to access engine variables

        # Scene setup
        self.background_color = arcade.color.BLACK  # Default background color
        self.levels = self.engine.config.level  # Array of levels from the config
        self.maze_list = MazeAdapter().get_multiple_maze(self.levels)  # List of generated mazes
        self.level = 0  # Current level
        self.calculate_maze_dimensions()

        # Sprites setup
        self.entities: arcade.SpriteList[arcade.Sprite] = arcade.SpriteList() # List of entities
        self.maze_bloc_texture = arcade.load_texture('assets/maze/bloc.png')  # Load bloc texture
        self.maze_blocs = arcade.SpriteList()  # List of maze blocs

        # -- Load sprites --
        # Player sprite
        tile_size = self.get_tile_size()
        self.player = Player((
            tile_size + self.window.width/2 - (tile_size * 2 * self.MAZE_DIMENSIONS[0]) / 2,
            tile_size + self.window.height/2 - (tile_size * 2 * self.MAZE_DIMENSIONS[1]) / 2), 1)
        self.player.width = self.get_tile_size() # Set player width and height
        self.player.height = self.get_tile_size()
        self.entities.append(self.player)

        # Initial build of the walls (refreshed for every window resize or new level)
        self.build_maze_walls()


    def on_draw(self) -> bool | None:
        """Function to draw on the screen"""
        self.clear() # Clear previous frame
        self.entities.draw() # Display all sprites from the self.sprites list

        # Draw maze blocs
        self.maze_blocs.draw()

        return None

    def on_key_press(self, symbol: int, modifiers: int) -> bool | None:
        """Keyboard interactions events"""
        if symbol == arcade.key.ESCAPE:
            self.engine.switch_pause()

        # Go to next level
        if symbol == arcade.key.R:
            self.level += 1
            if self.level > len(self.levels):
                raise NotImplementedError('All levels finished')
            self.maze_blocs = arcade.SpriteList()
            self.build_maze_walls()
            print(f'level {self.level}')

        return None

    def on_update(self, delta_time: float) -> bool | None:
        """ Update sprites """
        self.entities.update()
        return None

    def on_resize(self, width: int, height: int) -> bool | None:
        """ Function executed when the window is resized """
        # Recalculate the maze blocs position/scale
        self.build_maze_walls()

        # Resize player
        self.player.width = self.get_tile_size()
        self.player.height = self.get_tile_size()
        return super().on_resize(width, height)
    
    def calculate_maze_dimensions(self) -> None:
        """Refresh the self.MAZE_DIMENSIONS according to the current maze"""
        self.MAZE_DIMENSIONS = (len(self.maze_list[self.level][0][0]), len(self.maze_list[self.level][0]))
        return None
    
    def get_maze(self, level: int) -> list[list[int]]:
        """ WIP, This function will generate maze"""
        self.MAZE_DIMENSIONS = (len(self.maze_list[self.level][0][0]), len(self.maze_list[self.level][0]))
        return self.maze_list[self.level][0]

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

        # Return as list
        return list(coords)

    def build_maze_walls(self) -> None:
        """Re-calculate the maze blocs position depending on the window resolution
        and save the result in self.maze_blocs"""
        # Draw all the sprites on the screen
        self.maze_blocs = arcade.SpriteList()
        coords = self.get_walls_blocs_coords()
        for coord in coords:


            # Get the most optimal tile size
            if (self.MAZE_DIMENSIONS[0] > self.MAZE_DIMENSIONS[1]):
                tile_size = (self.window.width / (self.MAZE_DIMENSIONS[0] * 2)) * 0.2
            else:
                tile_size = (self.window.height / (self.MAZE_DIMENSIONS[1] * 2)) * 0.2

            tile_size = self.get_tile_size()

            # Draw sprite
            bloc = arcade.Sprite(
                self.maze_bloc_texture,
                1,
                coord[0] * tile_size + self.window.width/2 - (tile_size * 2 * self.MAZE_DIMENSIONS[0]) / 2,
                coord[1] * tile_size + self.window.height/2 - (tile_size * 2 * self.MAZE_DIMENSIONS[1]) / 2
                )
            bloc.width = tile_size
            bloc.height = tile_size
            self.maze_blocs.append(bloc)

        return None
    
    def get_tile_size(self) -> int:
        """ Return an adapted tile size for the window size"""
        # Get the most optimal tile size
        max_x = self.MAZE_DIMENSIONS[0] * 2 + 1
        max_y = self.MAZE_DIMENSIONS[1] * 2 + 1
        tile_size = min(
            self.window.width / max_x,
            self.window.height / max_y
        ) * 0.6

        return tile_size