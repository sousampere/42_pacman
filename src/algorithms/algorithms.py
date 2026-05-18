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
        max_y
    ) -> tuple[float, float]:

        best_move = None
        best_dist = float('inf')

        for dx, dy in cls.movements:
            neighbour = (ghost_pos[0] + dx, ghost_pos[1] + dy)
            # On vérifie que le neighbour est bien sur la carte
            if 0 <= neighbour[0] < max_x and 0 <= neighbour[1] < max_y:
                dist_neighbour = heat_map[neighbour]
                # Si c'est un chemin (-1 = mur) et que c'est plus près de Pacman
                if dist_neighbour != -1 and dist_neighbour < best_dist:
                    best_dist = dist_neighbour
                    best_move = neighbour

        return best_move
