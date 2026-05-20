import random

import numpy as np
import arcade
from numpy.typing import NDArray

from src.algorithms.heat_map import HeatMap
from src.entity.ghost import Ghost
from src.entity.pacgum import Pacgum
from src.entity.player import Player
from src.event_bus.event_bus import EventBus

PLAYER_SPEED: float = 0.28
GHOST_SPEED: float = 0.3


class GameState:
    def __init__(self, maze_data: tuple[NDArray, NDArray, int]) -> None:
        pts: NDArray = maze_data[1]
        self._pts = pts

        center_point = pts.mean(axis=0)
        distances = np.sum((pts - center_point) ** 2, axis=1)
        closest_point = tuple(pts[np.argmin(distances)].tolist())

        min_x, min_y = pts.min(axis=0)
        max_x, max_y = pts.max(axis=0)
        corners = [
            (min_x, min_y),
            (max_x, min_y),
            (min_x, max_y),
            (max_x, max_y),
        ]

        self.entity: arcade.SpriteList = arcade.SpriteList()
        self._init_pacgums(pts, closest_point, corners)
        self._init_ghosts(pts, corners)
        self._init_player(closest_point, pts)
        self._init_heatmaps(pts)

    def _init_pacgums(
        self,
        pts: NDArray,
        closest_point: tuple,
        corners: list,
    ) -> None:
        occupied = [closest_point] + corners
        pac_gum_pts = pts.copy()
        for pos in occupied:
            pac_gum_pts = pac_gum_pts[~np.all(pac_gum_pts == pos, axis=1)]

        total = random.randint(int((len(pts) - 5) * 0.6), len(pts) - 5)
        num = min(total, len(pac_gum_pts))
        indices = np.random.choice(len(pac_gum_pts), size=num, replace=False)

        self.pacgum: list[Pacgum] = []
        for spawn in pac_gum_pts[indices]:
            p = Pacgum(spawn)
            self.pacgum.append(p)
            self.entity.append(p)

    def _init_ghosts(self, pts: NDArray, corners: list) -> None:
        self.ghosts: list[Ghost] = []
        for i, corner in enumerate(corners):
            dist = np.sum((pts - corner) ** 2, axis=1)
            ghost_pos = tuple(pts[np.argmin(dist)].tolist())
            g = Ghost(ghost_pos, pts, GHOST_SPEED, i)
            self.ghosts.append(g)
            self.entity.append(g)

    def _init_player(self, closest_point: tuple, pts: NDArray) -> None:
        self.player = Player(closest_point, pts, PLAYER_SPEED)
        self.entity.append(self.player)

    def _init_heatmaps(self, pts: NDArray) -> None:
        self.heat_map_manager = HeatMap(pts)
        self._rand_target = [
            self._random_target(),
            self._random_target(),
        ]
        self.heat_map = [self.heat_map_manager.grid.copy() for _ in range(4)]
        self.heat_map[1] = self.heat_map_manager.update_heat_map(
            self._rand_target[0]
        )
        self.heat_map[3] = self.heat_map_manager.update_heat_map(
            self._rand_target[1]
        )

    def _random_target(self) -> tuple[int, int]:
        coord = np.random.default_rng().choice(self._pts)
        return (int(coord[0]), int(coord[1]))

    def _player_lookahead(self, steps: int = 4) -> tuple[int, int]:
        px, py = round(self.player._x), round(self.player._y)
        dx, dy = int(self.player.dir[0]), int(self.player.dir[1])
        if dx == 0 and dy == 0:
            return (px, py)
        pos = (px, py)
        for _ in range(steps):
            nxt = (pos[0] + dx, pos[1] + dy)
            if nxt in self.player._path_set:
                pos = nxt
            else:
                break
        return pos

    def update(
        self, delta_time: float, freeze_ghosts: bool, invincibility: bool
    ) -> None:
        self._update_heatmaps()
        self._check_ghost_collision(invincibility)
        self._check_pacgum_collision()
        self._update_ghosts(delta_time, freeze_ghosts)
        self.player.update()

        if len(self.pacgum) == 0:
            EventBus.broadcast_event("next_level")

    def _update_heatmaps(self) -> None:
        px, py = round(self.player._x), round(self.player._y)
        self.heat_map[0] = self.heat_map_manager.update_heat_map(
            self._rand_target[0]
        )
        self.heat_map[1] = self.heat_map_manager.update_heat_map((px, py))
        self.heat_map[2] = self.heat_map_manager.update_heat_map(
            self._player_lookahead(4)
        )
        self.heat_map[3] = self.heat_map_manager.update_heat_map(
            self._rand_target[1]
        )

    def _check_ghost_collision(self, invincibility: bool) -> None:
        player_pos = (round(self.player._x), round(self.player._y))
        ghost_positions = {(round(g._x), round(g._y)) for g in self.ghosts}
        if player_pos in ghost_positions:
            if not invincibility:
                self.player.die()
                EventBus.broadcast_event("remove_life")

    def _check_pacgum_collision(self) -> None:
        player_pos = (round(self.player._x), round(self.player._y))
        for p in self.pacgum[:]:
            if (round(p._x), round(p._y)) == player_pos:
                self.pacgum.remove(p)
                self.entity.remove(p)
                EventBus.broadcast_event("add_pacgum_point")

    def _update_ghosts(self, delta_time: float, freeze_ghosts: bool) -> None:
        if freeze_ghosts:
            return
        for idx, g in enumerate(self.ghosts):
            if idx == 0 and (g._x, g._y) == self._rand_target[0]:
                self._rand_target[0] = self._random_target()
            if idx == 3 and (g._x, g._y) == self._rand_target[1]:
                self._rand_target[1] = self._random_target()
            occupied = frozenset(
                pos
                for other in self.ghosts
                if other is not g
                for pos in (
                    [(round(other._target[0]), round(other._target[1]))]
                    if other._target is not None
                    else [(round(other._x), round(other._y))]
                )
            )
            g.update(
                delta_time,
                self.heat_map,
                self.heat_map_manager.max_x,
                self.heat_map_manager.max_y,
                occupied=occupied,
            )
