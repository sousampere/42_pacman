from collections import deque

import numpy as np
from numpy import ndarray


class HeatMap:
    def __init__(self, coords_array: ndarray) -> None:
        self.max_x = int(np.max(coords_array[:, 0])) + 1
        self.max_y = int(np.max(coords_array[:, 1])) + 1

        self.grid = np.full((self.max_x, self.max_y), -1, dtype=np.int32)
        for x, y in coords_array:
            self.grid[x, y] = 999999

        self.heat_map_cache: dict[tuple[int, int], ndarray] = {}

    def update_heat_map(self, pos: tuple[int, int]) -> ndarray:
        if pos in self.heat_map_cache:
            return self.heat_map_cache[pos]

        heat_map = self.grid.copy()

        try:
            if heat_map[pos] == -1:
                return heat_map
        except IndexError:
            return heat_map

        heat_map[pos] = 0
        file = deque([pos])
        movements = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        while file:
            cx, cy = file.popleft()
            actual_dist = heat_map[cx, cy]

            for dx, dy in movements:
                nx, ny = cx + dx, cy + dy

                if 0 <= nx < self.max_x and 0 <= ny < self.max_y:
                    if heat_map[nx, ny] > actual_dist + 1:
                        heat_map[nx, ny] = actual_dist + 1
                        file.append((nx, ny))

        self.heat_map_cache[pos] = heat_map
        return heat_map

    def update_flee_map(self, pos_pacman: tuple[int, int]) -> ndarray:
        regular = self.update_heat_map(pos_pacman)
        reachable = (regular >= 0) & (regular < 999999)
        if not np.any(reachable):
            return regular
        max_dist = int(regular[reachable].max())
        flee_map = regular.copy()
        flee_map[reachable] = max_dist - regular[reachable]
        return flee_map
