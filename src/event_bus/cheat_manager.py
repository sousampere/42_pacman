class CheatManager:
    def __init__(self) -> None:
        self.__cheat_mode: bool = False
        self.__invincibility: bool = False
        self.__freeze_ghosts: bool = False

    def event_enable_cheat_mode(self) -> None:
        self.__cheat_mode = True

    def event_toggle_invincibility(self) -> None:
        self.__invincibility = not self.__invincibility

    def event_toggle_freeze_ghosts(self) -> None:
        self.__freeze_ghosts = not self.__freeze_ghosts

    @property
    def cheat_mode(self) -> bool:
        return self.__cheat_mode

    @property
    def invincibility(self) -> bool:
        return self.__invincibility

    @property
    def freeze_ghosts(self) -> bool:
        return self.__freeze_ghosts
