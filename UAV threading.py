import threading
import time
import random


def th(x: int) -> None:
    print('thread %i' % x)
    time.sleep(random.randint(2, 7))
    print('thread stop %i' % x)


def main():
    for i in range(5):
        thread = threading.Thread(target=th, args=(i,))
        thread.start()


if __name__ == '__main__':
    main()
