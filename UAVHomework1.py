from numpy import random
import matplotlib.pyplot as plp


def get_data_gyro(x0: int) -> list:
    result = []
    for _ in range(100):
        data = random.normal(x0, 2, 7)
        data = median_sort(data)
        result.append(data)
    return result


def median_sort(data) -> int:
    result = sorted(data)[3]
    return result


def main():
    def pid(err) -> float:
        nonlocal i
        nonlocal e
        p = kp * err
        i = i + ki * err
        d = kd * (err - e)
        e = err
        return p + i + d

    p, i, d = 0, 0, 0
    kp, ki, kd = 1.3, 0.23, 0.002
    e = 0
    x0 = 5
    data = get_data_gyro(x0)
    correct = []
    for j in range(100):
        correct.append(x0 + pid(data[j] - x0))
    x = [l for l in range(100)]
    plp.plot(x, data, x, correct)
    plp.show()


if __name__ == '__main__':
    main()
