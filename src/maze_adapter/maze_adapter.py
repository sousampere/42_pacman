from mazegenerator.mazegenerator import MazeGenerator  # type: ignore

DEFAULT_SEED: int = 42
DEFAULT_NB_LEVEL: int = 10
DEFAULT_SIGNATURE: str = "2020350501004290"


class MazeAdapterError(Exception):
    def __init__(self, msg) -> None:
        super().__init__(f"Maze Adapter Error: {msg}")


class MazeAdapter:

    def __init__(
        self,
        signature: str = DEFAULT_SIGNATURE,
        nb_level: int = DEFAULT_NB_LEVEL,
    ) -> None:
        self.__initial_signature: str = signature
        self.__nb_level: int = nb_level

    def __hash_to_int(self, hex_str: str) -> int:
        try:
            res = int(hex_str, 16) % (2**32)
        except ValueError as e:
            raise MazeAdapterError(str(e))
        return res

    def get_maze(
        self, size: tuple[int, int], seed: int = DEFAULT_SEED
    ) -> list[list[int]]:
        try:
            maze = MazeGenerator(size=size, seed=seed)
        except RecursionError as e:
            raise MazeAdapterError(str(e))
        return maze.maze

    def get_multiple_maze(
        self, levels: list[dict[str, int]], seed: int = DEFAULT_SEED
    ):
        maze_list = []
        for i, level in enumerate(levels):
            size = (level.get("width", 20), level.get("height", 10))
            if i != 0:
                seed += self.__hash_to_int(self.__initial_signature)
            maze_list.append((self.get_maze(size, seed), seed))
        return maze_list

    def get_walls_blocs_coords(self, maze: list[list[int]]) -> list[tuple[int, int]]:
        """Returns a list of walls coords from the engine's maze"""
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

# maze_gen = MazeAdapter(DEFAULT_SIGNATURE, 10)

# # 14*10 min
# levels = [
#     {"width": 145, "height": 100},
#     {"width": 20, "height": 10},
#     {"width": 20, "height": 10},
#     {"width": 20, "height": 10},
#     {"width": 20, "height": 10},
#     {"width": 20, "height": 10},
# ]
# maze = maze_gen.get_multiple_maze(levels, 42)
# for m in maze:
#     print(m[0])
#     print(m[1])
#     print()
