import asyncio


async def func1(x):
    await asyncio.sleep(3)
    print(x)


async def func2(y):
    await asyncio.sleep(2)
    print(y)


async def run():
    task1 = asyncio.create_task(func1(100))
    task2 = asyncio.create_task(func2(200))
    await asyncio.wait((task1, task2))


def main():
    asyncio.run(run())


if __name__ == '__main__':
    main()
