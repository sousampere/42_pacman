class Algorithms:
    def __init__(self, maze: list[list[int]]) -> None:
        pass

    def process(
        self, my_pos: tuple[float, float], target: tuple[float, float]
    ) -> tuple[float, float]:
        dx, dy = my_pos
        tx, ty = target
        rx = 1
        ry = 1
        if tx - dx < 0:
            rx = -1
        if ty - dy < 0:
            ry = -1
        return (rx, ry)