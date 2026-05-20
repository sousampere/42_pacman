
class ScoreManager:
    def __init__(self, pacgum_pts: int, super_pacgum_pts: int) -> None:
        self.__pacgum_pts: int = pacgum_pts
        self.__super_pacgum_pts: int = super_pacgum_pts
        self.__xp: int = 0

    def event_add_pacgum_point(self) -> None:
        self.__xp += self.__pacgum_pts

    @property
    def xp(self) -> int:
        return self.__xp
