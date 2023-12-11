import asyncio
import csv
import mlrose
import cv2
import matplotlib
from matplotlib import pyplot as plt
from mavsdk import System
from mavsdk.offboard import PositionNedYaw, VelocityNedYaw
from mavsdk.offboard import AccelerationNed, OffboardError
from mavsdk.telemetry import LandedState
import numpy as np
import six
import sys
sys.modules['sklearn.externals.six'] = six
matplotlib.use("TkAgg")


class Kopter:
    """Базовый класс квадрокоптера:
    x, y - начальные координаты
    h - начальная высота
    yaw - начальный угол рысканья
    v - начальная скорость"""

    def __init__(self, x: int, y: int, h=10, yaw=0, v=0):
        self.drone = System()

        async def init():
            await self.drone.connect(system_address="udp://:14540")

            # Wait for the drone to connect
            print("Waiting for drone to connect...")
            async for state in self.drone.core.connection_state():
                if state.is_connected:
                    print("-- Connected to drone!")
                    break

        asyncio.run(init())
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

    def takeoff(self):
        # Wait for the drone to have a global position estimate
        print("Waiting for drone to have a global position estimate...")
        for health in self.drone.telemetry.health():
            if health.is_global_position_ok and health.is_home_position_ok:
                print("-- Global position estimate OK")
                break

        # Arm the drone
        print("-- Arming")
        self.drone.action.arm()

        # Set the initial setpoint
        print("-- Setting initial setpoint")
        startSetpoint = PositionNedYaw(0.0, 0.0, 0.0, 0.0)
        self.drone.offboard.set_position_ned(startSetpoint)

        # Start offboard mode
        print("-- Starting offboard")
        try:
            self.drone.offboard.start()
        except OffboardError as error:
            print(f"Starting offboard mode failed with error code:"
                  f" {error._result.result}")
            print("-- Disarming")
            self.drone.action.disarm()
            return

    def land(self):
        print("-- Landing")
        self.drone.action.land()

        for state in self.drone.telemetry.landed_state():
            if state == LandedState.ON_GROUND:
                break

        print("-- Stopping offboard")
        try:
            self.drone.offboard.stop()
        except Exception as error:
            print(f"Stopping offboard mode failed with error: {error}")

        print("-- Disarming")
        self.drone.action.disarm()

    def go2xy(self, x, y, h, yaw, vx, vy, vz):
        self.drone.offboard.set_position_velocity_ned(
            PositionNedYaw(*[x, y, h], yaw_deg=yaw),
            VelocityNedYaw(*[vx, vy, vz], yaw_deg=yaw)
        )


# ключевая точка для съемки (x, y)
key_point = [42, 42]

print(Kopter.__doc__)

# создаем экземпляр коптера
my_kopter = Kopter(x=0, y=0)

# инициализируем
my_kopter.takeoff()

# читаем маршрут
waypoints = []
points = []

with open("data.csv", newline="") as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        waypoints.append((float(row["t"]),
                          float(row["px"]),
                          float(row["py"]),
                          float(row["pz"]),
                          float(row["vx"]),
                          float(row["vy"]),
                          float(row["vz"]),
                          float(row["ax"]),
                          float(row["ay"]),
                          float(row["az"]),
                          float(row["yaw"]),
                          int(row["mode"])))

        points.append((float(row["px"]), float(row["py"])))

# оптимизируем маршрут
# фитнесс-функция оптимизации
fitness_func = mlrose.TravellingSales(coords=points)
# Проблема: минимизация/максимизация
problem = mlrose.TSPOpt(length=len(points), fitness_fn=fitness_func, maximize=False)

# запуск генетического алгоритма для решения задачи
best_path, best_lenght = mlrose.genetic_alg(problem=problem, random_state=3)

print(best_path, best_lenght)
best_path = list(best_path) * 2
best_path = best_path[best_path.index(0)+1:best_path.index(0)+len(points)+1]

# летим по маршруту
for point in best_path:
    if waypoints[point][1] == key_point[0] and waypoints[point][2] == key_point[1]:
        # съемака ключевой точки
        img = cv2.imread("cars3.jpg")
        # обработка изображения
        img_color = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        xml_data = cv2.CascadeClassifier("cars.xml")
        detecting = xml_data.detectMultiScale(img_color, minSize=(70, 70), scaleFactor=1.05)
        detect = len(detecting)
        if detect != 0:
            for (a, b, widht, height) in detecting:
                cv2.rectangle(img_color, (a, b), (a + height, b + widht), (0, 255, 0), 3)

        cv2.imshow('avto', img_color)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    # летим дальше
    my_kopter.go2xy(x=waypoints[point][1],
                    y=waypoints[point][2],
                    h=waypoints[point][3],
                    yaw=waypoints[point][10],
                    vx=waypoints[point][4],
                    vy=waypoints[point][5],
                    vz=waypoints[point][6])

# посадка
my_kopter.land()
