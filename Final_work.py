class Kopter:
    """Базовый класс квадрокоптера:
    x, y - начальные координаты
    h - начальная высота
    yaw - начальный угол рысканья
    v - начальная скорость"""

    def __init__(self, x: int, y: int, h=0, yaw=0, v=0):
        self.x = x
        self.y = y
        self.h = h
        self.yaw = yaw
        self.v = v

    def get_xy(self) -> tuple:
        return self.x, self.y

    def set_xy(self, x: int, y: int):
        self.x = x
        self.y = y

    def get_h(self) -> float:
        return self.h

    def set_h(self, h: float):
        self.h = h

    def get_yaw(self) -> float:
        return self.yaw

    def set_yaw(self, yaw: float):
        self.yaw = yaw

    def get_v(self) -> int:
        return self.v

    def set_v(self, v: int):
        self.v = v


print(Kopter.__doc__)
my_kopter = Kopter(x=5, y=10)
print(my_kopter.get_xy())
my_kopter.set_xy(x=10, y=10)
print(my_kopter.get_xy())
