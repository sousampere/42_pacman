from src.event_bus.event_bus import EventBus
import time

class GameManager:
    def __init__(self, lives: int, total_levels: int, game_time: int) -> None:
        self.__lives: int = lives
        self.__level: int = 1
        self.__current_maze: int = 0
        self.__total_levels: int = total_levels
        self.__start_time: int = int(time.time())

    def event_add_life(self) -> None:
        self.__lives += 1

    def event_remove_life(self) -> None:
        self.__lives -= 1
        if self.__lives <= 0:
            EventBus.broadcast_event("game_over")

    def event_next_level(self) -> None:
        self.__current_maze += 1
        self.__level += 1
        if self.__current_maze >= self.__total_levels:
            EventBus.broadcast_event("switch_finish")

    def event_reset_start_time(self) -> None:
        self.__start_time = int(time.time())

    @property
    def lives(self) -> int:
        return self.__lives

    @property
    def level(self) -> int:
        return self.__level

    @property
    def current_maze(self) -> int:
        return self.__current_maze
    
    @property
    def start_time(self) -> int:
        return self.__start_time