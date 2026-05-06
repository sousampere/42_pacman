import numpy as np

from mazegenerator.mazegenerator import MazeGenerator  # type: ignore
from numpy.typing import NDArray

DEFAULT_SEED: int = 42
DEFAULT_NB_LEVEL: int = 10
DEFAULT_SIGNATURE: str = "2020350501004290"


class MazeAdapterError(Exception):
    def __init__(self, msg: str = "") -> None:
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
    ) -> tuple[NDArray, NDArray]:
        try:
            maze = MazeGenerator(size=size, seed=seed)
        except RecursionError as e:
            raise MazeAdapterError(str(e))
        return self.get_walls_amd_path_coords(np.array(maze.maze))

    def get_multiple_maze(
        self, levels: list[dict[str, int]], seed: int = DEFAULT_SEED
    ):
        maze_list: list[tuple[NDArray, NDArray, int]] = []
        for i, level in enumerate(levels):
            size = (level.get("width", 20), level.get("height", 10))
            if i != 0:
                seed += self.__hash_to_int(self.__initial_signature)
            wall, path = self.get_maze(size, seed)
            maze_list.append((wall, path, seed))
        return maze_list

    def get_walls_amd_path_coords(
        self, maze: NDArray
    ) -> tuple[NDArray, NDArray]:
        m = maze[::-1]
        h, w = m.shape

        iy, ix = np.indices((h * 2 + 1, w * 2 + 1))
        allcoords = np.column_stack((ix.ravel(), iy.ravel()))

        wall_rules = [
            (1, [(0, 2), (1, 2), (2, 2)]),
            (2, [(2, 0), (2, 1), (2, 2)]),
            (4, [(0, 0), (1, 0), (2, 0)]),
            (8, [(0, 0), (0, 1), (0, 2)]),
            (15, [(1, 1)]),
        ]
        all_segments = []
        for bit, offsets in wall_rules:
            condition = (m == bit) if bit == 15 else (m & bit)
            ys, xs = np.where(condition)
            if ys.size > 0:
                for dx, dy in offsets:
                    all_segments.append(
                        np.column_stack((xs * 2 + dx, ys * 2 + dy))
                    )

        wall_coords = np.unique(np.concatenate(all_segments), axis=0)

        def row_diff(A, B):
            A = np.ascontiguousarray(A).astype(np.int32)
            B = np.ascontiguousarray(B).astype(np.int32)

            dt = np.dtype([("f0", A.dtype), ("f1", A.dtype)])

            struct_A = A.view(dt)
            struct_B = B.view(dt)

            mask = np.isin(struct_A, struct_B, invert=True)

            return A[mask.ravel()]

        path_coords = row_diff(allcoords, wall_coords)

        return wall_coords, path_coords
