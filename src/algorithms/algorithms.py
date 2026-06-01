from numpy import ndarray


class Algorithms:
    movements = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    @classmethod
    def process(
        cls,
        ghost_pos: tuple[float, float],
        heat_map: ndarray,
        max_x: int,
        max_y: int,
        excluded: frozenset[tuple[int, int]] = frozenset(),
    ) -> tuple[float, float] | None:

        best_move: tuple[float, float] | None = None
        best_dist: float = float("inf")
        fallback_move: tuple[float, float] | None = None
        fallback_dist: float = float("inf")

        for dx, dy in cls.movements:
            neighbour = (ghost_pos[0] + dx, ghost_pos[1] + dy)
            nx, ny = int(neighbour[0]), int(neighbour[1])
            if 0 <= nx < max_x and 0 <= ny < max_y:
                dist_neighbour: int = int(heat_map[nx, ny])
                if dist_neighbour == -1:
                    continue
                if dist_neighbour < fallback_dist:
                    fallback_dist = float(dist_neighbour)
                    fallback_move = (float(nx), float(ny))
                if neighbour not in excluded \
                        and dist_neighbour < best_dist:
                    best_dist = float(dist_neighbour)
                    best_move = (float(nx), float(ny))

        return best_move if best_move is not None else fallback_move
