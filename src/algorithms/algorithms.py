import random 

from numpy import ndarray


class Algorithms:
    movements = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    @classmethod
    def process(
        cls,
        ghost_pos: tuple[float, float],
        target: tuple[float, float],
        heat_map: ndarray,
        max_x,
        max_y,
        excluded: frozenset[tuple[int, int]] = frozenset(),
    ) -> tuple[float, float]:

        best_move = None
        best_dist = float('inf')
        fallback_move = None
        fallback_dist = float('inf')

        for dx, dy in cls.movements:
            neighbour = (ghost_pos[0] + dx, ghost_pos[1] + dy)
            if 0 <= neighbour[0] < max_x and 0 <= neighbour[1] < max_y:
                dist_neighbour = heat_map[neighbour]
                if dist_neighbour == -1:
                    continue
                if dist_neighbour < fallback_dist:
                    fallback_dist = dist_neighbour
                    fallback_move = neighbour
                if neighbour not in excluded and dist_neighbour < best_dist:
                    best_dist = dist_neighbour
                    best_move = neighbour

        return best_move if best_move is not None else fallback_move
