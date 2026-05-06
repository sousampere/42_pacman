import arcade

from src.maze_adapter.maze_adapter import MazeAdapter

class Renderer:
    def __init__(self) -> None:
        self.maze_bloc_texture = arcade.load_texture('assets/maze/bloc.png')  # Load bloc texture
        self.maze_adapter = MazeAdapter()
        pass

    def render_game(self, maze: list[list[int]]) -> None:
        """Draws the game to the screen"""

        maze_blocs = self.build_maze_walls(maze)
        maze_blocs.draw()

    def calculate_maze_dimensions(self, maze: list[list[int]]) -> tuple[int, int]:
        """Refresh the self.MAZE_DIMENSIONS according to the current maze"""
        MAZE_DIMENSIONS = (len(maze[0]), len(maze))
        return MAZE_DIMENSIONS

    def build_maze_walls(self, maze: list[list[int]]) -> arcade.SpriteList[arcade.Sprite]:
        """Re-calculate the maze blocs position depending on the window resolution
        and save the result in self.maze_blocs"""
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

        # Calculate tile size so that the maze takes max 60% of height/width
        tile_size = min(
            window.width / max_x,
            window.height / max_y
        ) * 0.6

        return int(tile_size)
