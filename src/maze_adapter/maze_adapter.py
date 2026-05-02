from copy import deepcopy
import hashlib

from mazegenerator.mazegenerator import MazeGenerator  # type: ignore

DEFAULT_SEED: int = 42
DEFAULT_NB_LEVEL: int = 30
DEFAULT_SIGNATURE: str = "2020350501004290"


class MazeAdapter:
    """
    Facade over MazeGenerator that handles single and multi-level maze
    generation.

    Supports two generation strategies:
    - Story mode: seeds are derived deterministically from a signature via a
    SHA-256
      hash chain, ensuring full reproducibility across runs sharing the same
      signature.
    - Direct mode: generate a single maze from an explicit seed via get_maze().

    The first level is always generated with the initial seed (default 42).
    """

    def __init__(
        self,
        size: tuple[int, int],
        nb_level: int = DEFAULT_NB_LEVEL,
        signature: str = DEFAULT_SIGNATURE,
        seed: int = DEFAULT_SEED,
    ) -> None:
        """
        Initialize the MazeAdapter.

        Args:
            size: Grid dimensions as (width, height).
            nb_level: Total number of levels to generate in story mode.
            signature: Initial string used to seed the SHA-256 hash chain.
            seed: Seed for the first level. Defaults to 42 as per project spec.
        """
        self.__seed = seed
        self.__maze_gen: MazeGenerator = MazeGenerator(
            size, exit_cell=(1, 1), seed=seed
        )
        self.__nb_level: int = nb_level
        self.__initial_signature: str = signature

    def __hash_to_int(self, hex_str: str) -> int:
        """
        Convert a SHA-256 hex digest to a 32-bit unsigned integer.

        Args:
            hex_str: A hexadecimal string (e.g.
            from hashlib.sha256().hexdigest()).

        Returns:
            An integer in [0, 2**32).
        """
        return int(hex_str, 16) % (2**32)

    def get_multiple_maze(self) -> list[tuple[list[list[int]], int]]:
        """
        Generate a sequence of maze levels using the story mode hash chain.

        The first level uses the initial seed. Each subsequent level derives
        its seed
        by repeatedly hashing the previous SHA-256 digest, starting from the
        initial
        signature. Seeds are reduced to 32-bit integers via __hash_to_int().

        Returns:
            A list of (maze, seed) tuples, one per level. Each maze is a deep
            copy
            of the grid at generation time, represented as a 2D list of
            integers.
        """
        level_list = []
        current_hash = hashlib.sha256(
            self.__initial_signature.encode()
        ).hexdigest()

        level_list.append((deepcopy(self.get_maze(self.__seed)), self.__seed))
        for _ in range(self.__nb_level - 1):
            seed_int = self.__hash_to_int(current_hash)
            self.__maze_gen.generate(seed_int)
            level_list.append((deepcopy(self.__maze_gen.maze), seed_int))
            current_hash = hashlib.sha256(current_hash.encode()).hexdigest()

        return level_list

    def get_maze(self, seed: int = DEFAULT_SEED) -> list[list[int]]:
        """
        Generate a single maze from an explicit seed.

        Note: This method mutates the internal MazeGenerator state. Calling it
        between get_multiple_maze() iterations will break level continuity.

        Args:
            seed: The RNG seed to use for generation.

        Returns:
            A deep copy of the generated maze as a 2D list of integers.
        """
        self.__maze_gen.generate(seed)
        return deepcopy(self.__maze_gen.maze)


# maze_gen = MazeAdapter((20, 20))

# for row in maze_gen.get_multiple_maze():
#     for r in row[0]:
#         print(list(map(hex, r)))
#     print(row[1], "\n")
