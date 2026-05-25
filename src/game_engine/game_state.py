import numpy as np
import arcade
from numpy.typing import NDArray

from src.algorithms.heat_map import HeatMap
from src.entity.ghost import Ghost
from src.entity.pacgum import Pacgum
from src.entity.player import Player
from src.entity.super_pacgum import SuperPacgum
from src.event_bus import cheat_manager, game_manager
from src.event_bus.event_bus import EventBus

PLAYER_SPEED: float = 0.28
GHOST_SPEED: float = 0.3


class GameState:
    def __init__(
        self,
        maze_data: tuple[NDArray, NDArray, int],
        cheat_mng: cheat_manager.CheatManager,
        game_mng: game_manager.GameManager,
    ) -> None:
        pts: NDArray = maze_data[1]
        self._pts = pts
        self.cheat_mng = cheat_mng
        self.game_mng = game_mng

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
        self._init_ghosts_super_pacgum(pts, corners)
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

        total = int((len(pts) - 5) * 0.6)
        num = min(total, len(pac_gum_pts))
        indices = np.random.choice(len(pac_gum_pts), size=num, replace=False)

        self.pacgum: list[Pacgum] = []
        for spawn in pac_gum_pts[indices]:
            p = Pacgum(spawn)
            self.pacgum.append(p)
            self.entity.append(p)

    def _init_ghosts_super_pacgum(self, pts: NDArray, corners: list) -> None:
        self.ghosts: list[Ghost] = []
        self.super_pacgum: list[SuperPacgum] = []
        for i, corner in enumerate(corners):
            dist = np.sum((pts - corner) ** 2, axis=1)
            ghost_pos = tuple(pts[np.argmin(dist)].tolist())
            p = SuperPacgum(ghost_pos)
            self.super_pacgum.append(p)
            self.entity.append(p)
            g = Ghost(
                ghost_pos, pts, GHOST_SPEED, i, self.cheat_mng.cheat_mode
            )
            self.ghosts.append(g)
            self.entity.append(g)

    def _init_player(self, closest_point: tuple, pts: NDArray) -> None:
        self.player = Player(
            closest_point, pts, PLAYER_SPEED, self.cheat_mng.cheat_mode
        )
        self.entity.append(self.player)

    def _init_heatmaps(self, pts: NDArray) -> None:
        self.heat_map_manager = HeatMap(pts)
        self._rand_target = [
            self._random_target(),
            self._random_target(),
        ]

        # One slot per ghost (index == ghost._id)
        self.heat_map = [self.heat_map_manager.grid.copy() for _ in range(4)]

        # Static spawn heatmaps: each ghost navigates back to its own spawn
        self._spawn_heat_maps = [
            self.heat_map_manager.update_heat_map(g.spawn_point)
            for g in self.ghosts
        ]

        init_pos: tuple[int, int] = (
            round(self.player._x),
            round(self.player._y),
        )
        init_lookahead: tuple[int, int] = self._player_lookahead(4)

        self.heat_map[0] = self.heat_map_manager.update_heat_map(
            self._rand_target[0]
        )
        self.heat_map[1] = self.heat_map_manager.update_heat_map(init_pos)
        self.heat_map[2] = self.heat_map_manager.update_heat_map(
            init_lookahead
        )
        self.heat_map[3] = self.heat_map_manager.update_heat_map(
            self._rand_target[1]
        )

        self._last_player_pos: tuple[int, int] = init_pos
        self._last_lookahead: tuple[int, int] = init_lookahead
        self._last_is_edible: bool = False
        self._last_ghost_dead: list[bool] = [False] * len(self.ghosts)

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
        player_pos = (px, py)
        lookahead = self._player_lookahead(4)

        player_moved = player_pos != self._last_player_pos
        lookahead_changed = lookahead != self._last_lookahead
        edible_changed = self.game_mng.is_edible != self._last_is_edible
        any_revived = any(
            self._last_ghost_dead[i] and not g._is_dead
            for i, g in enumerate(self.ghosts)
        )
        force = edible_changed or any_revived

        if self.game_mng.is_edible:
            if player_moved or force:
                flee_map = self.heat_map_manager.update_flee_map(player_pos)
                for i, g in enumerate(self.ghosts):
                    if not g._is_dead:
                        self.heat_map[i] = flee_map
        else:
            if not self.ghosts[0]._is_dead:
                self.heat_map[0] = self.heat_map_manager.update_heat_map(
                    self._rand_target[0]
                )
            if not self.ghosts[3]._is_dead:
                self.heat_map[3] = self.heat_map_manager.update_heat_map(
                    self._rand_target[1]
                )
            if not self.ghosts[1]._is_dead and (player_moved or force):
                self.heat_map[1] = self.heat_map_manager.update_heat_map(
                    player_pos
                )
            if not self.ghosts[2]._is_dead and (lookahead_changed or force):
                self.heat_map[2] = self.heat_map_manager.update_heat_map(
                    lookahead
                )

        for i, g in enumerate(self.ghosts):
            if g._is_dead:
                self.heat_map[i] = self._spawn_heat_maps[i]

        self._last_player_pos = player_pos
        self._last_lookahead = lookahead
        self._last_is_edible = self.game_mng.is_edible
        self._last_ghost_dead = [g._is_dead for g in self.ghosts]

    def _check_ghost_collision(self, invincibility: bool) -> None:
        player_pos = (round(self.player._x), round(self.player._y))
        for g in self.ghosts:
            if (round(g._x), round(g._y)) != player_pos or g._is_dead:
                continue
            if self.game_mng.is_edible:
                g.die()
            elif not invincibility:
                self.player.die()
                EventBus.broadcast_event("remove_life")

    def _check_pacgum_collision(self) -> None:
        player_pos = (round(self.player._x), round(self.player._y))
        for p in self.pacgum[:]:
            if (round(p._x), round(p._y)) == player_pos:
                self.pacgum.remove(p)
                self.entity.remove(p)
                EventBus.broadcast_event("add_pacgum_point")
                EventBus.broadcast_event("play_pacgum_sound")
        for p in self.super_pacgum[:]:
            if (round(p._x), round(p._y)) == player_pos:
                self.super_pacgum.remove(p)
                self.entity.remove(p)
                EventBus.broadcast_event("add_super_pacgum_point")
                EventBus.broadcast_event("is_edible")

    def _update_ghosts(self, delta_time: float, freeze_ghosts: bool) -> None:
        if freeze_ghosts:
            return
        for idx, g in enumerate(self.ghosts):
            if (
                idx == 0
                and (g._x, g._y) == self._rand_target[0]
                and not self.game_mng.is_edible
            ):
                self._rand_target[0] = self._random_target()
            if (
                idx == 3
                and (g._x, g._y) == self._rand_target[1]
                and not self.game_mng.is_edible
            ):
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
                self.heat_map,
                self.heat_map_manager.max_x,
                self.heat_map_manager.max_y,
                occupied,
                delta_time,
            )
