from random import uniform, randint
from numpy import round
import matplotlib
import matplotlib.pyplot as plt
from math import pi, sin, sqrt, atan2, cos
matplotlib.use('TkAgg')


def get_gps_data(string: str) -> dict:
    d = string.split(',')
    return {'time': float(d[1]), 'lon': float(d[2]), 'lat': float(d[4]), 'height': float(d[9])}


def deg_to_rad(deg) -> float:
    return deg * pi / 180


def dist_ab(lat1, lon1, lat2, lon2) -> float:
    earth_r = 6371

    dlat = deg_to_rad(lat2-lat1)
    dlon = deg_to_rad(lon2-lon1)

    lat1 = deg_to_rad(lat1)
    lat2 = deg_to_rad(lat2)

    a = sin(dlat/2)**2 + sin(dlon/2)**2 * cos(lat1) * cos(lat2)
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    return earth_r * c


lat = 5546.95900
lon = 03740.69200
h = 142.0
t = 102030.000
list_data_gps = []
for i in range(15):
    lat += uniform(1.0, 1.5)
    lon += uniform(1.0, 1.5)
    h += uniform(-10.0, 20.0)
    t += randint(5, 20)
    s = '$GNGGA,'
    s += str(round(t, 3)) + '00,'
    s += str(round(lat, 5)) + ',N,'
    s += str(round(lon, 5)) + ',E,1,08,2.0,'
    s += str(round(h, 1)) + ',M,0.0,M,,*'
    list_data_gps.append(s)

gps_data = []
for data in list_data_gps:
    gps_data.append(get_gps_data(data))

time_data = list(map(lambda x: x['time'], gps_data))
height_data = list(map(lambda x: x['height'], gps_data))
lon_data = list(map(lambda x: x['lon'], gps_data))
lat_data = list(map(lambda x: x['lat'], gps_data))

plt.plot(time_data, height_data)
plt.title('h(t)')
plt.show()

fig = plt.figure(figsize=(8, 8))
ax_3d = fig.add_subplot(projection='3d')
ax_3d.plot(lon_data, lat_data, height_data)
plt.show()

all_dist = 0
for i in range(len(lon_data)-1):
    all_dist += dist_ab(lat_data[i], lon_data[i], lat_data[i+1], lon_data[i+1])

print(f'All distance: {all_dist}')
