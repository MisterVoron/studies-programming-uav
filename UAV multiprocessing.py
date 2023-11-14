import multiprocessing


def greetings(x: int) -> None:
    print('Hello', x + 1)


def main():
    cpu_count = multiprocessing.cpu_count()
    procs = []
    for i in range(cpu_count):
        proc = multiprocessing.Process(target=greetings, args=(i,))
        proc.start()
        procs.append(proc)
    for proc in procs:
        proc.join()


if __name__ == '__main__':
    main()
