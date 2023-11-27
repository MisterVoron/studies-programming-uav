import matplotlib.pyplot as plt
import numpy as np
import random


def length_ab(ax: int, ay: int, az: int, bx: int, by: int, bz: int) -> float:
    return round(((bx - ax)**2 + (by - ay)**2 + (bz - az)**2) ** 0.5, 2)


def fly_time(fly_speed, bst, length_start_end) -> tuple:
    time = 0
    time += fly_speed / bst
    time_boost = time
    lngth = (bst * time**2) / 2
    time *= 2
    lngth *= 2
    lngth = length_start_end - lngth
    time += lngth / fly_speed
    return time, time_boost


def angle(ax: int, ay: int, bx: int, by: int) -> float:
    return 90 - np.degrees(np.arctan((by - ay) / (bx - ax)))


a_x, a_y, a_z = random.randint(0, 5), random.randint(0, 5), random.randint(0, 5)
b_x, b_y, b_z = random.randint(5, 20), random.randint(5, 20), random.randint(5, 20)
min_speed, max_speed = 0, 10
length = length_ab(a_x, a_y, a_z, b_x, b_y, b_z)
boost = random.randint(1, 5)

print(f"A({a_x}, {a_y}, {a_z})")
print(f"B({b_x}, {b_y}, {b_z})")
print(f'Длина от точки до точки {length_ab(a_x, a_y, a_z, b_x, b_y, b_z)}')
print(f'Время полёта {fly_time(max_speed, boost, length)}')
print(f'Угол направления {angle(a_x, a_y, b_x, b_y)}')

x = [a_x]
y = [a_y]
z = [a_z]
v = [0]
t = 0

ab_vect = [b_x-a_x, b_y-a_y, b_z-a_z]

while (x[-1] <= b_x) and (y[-1] <= b_y) and (z[-1] <= b_z):
    x.append(ab_vect[0]*t + a_x)
    y.append(ab_vect[1]*t + a_y)
    z.append(ab_vect[2]*t + a_z)
    t += 0.1

fig = plt.figure(figsize=(8, 8))
ax_3d = fig.add_subplot(projection='3d')
ax_3d.plot(x, y, z)
plt.show()

print("End flying")
