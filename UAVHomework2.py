import ftplib
import filecmp
import asyncio


async def push_item(ftp_connection: ftplib.FTP, item_path: str) -> None:
    with open(file=item_path, mode='rb') as file:
        await asyncio.sleep(1)
        ftp_connection.storbinary(cmd=' '.join(('STOR', item_path)), fp=file, blocksize=1024)


async def receive_item(ftp_connection: ftplib.FTP, item_path: str, receive_path: str) -> None:
    with open(file=receive_path, mode='wb') as file:
        await asyncio.sleep(1)
        ftp_connection.retrbinary(cmd=' '.join(('RETR', item_path)), callback=file.write)


async def async_run():
    ftp = connection()
    task1 = push_item(ftp, 'UAVHomework1.py')
    task2 = receive_item(ftp, 'UAVHomework1.py',
                         r'D:\Program Files\JetBrains\PythonProjects\studies-programming-uav\instance.py')
    await task1
    await task2
    ftp.close()


def connection() -> ftplib.FTP:
    host = '192.168.1.69'
    user = 'user'
    passwd = 'user'
    ftp = ftplib.FTP(host=host, user=user, passwd=passwd)
    return ftp


def main():
    asyncio.run(async_run())
    if filecmp.cmp('UAVHomework1.py', 'instance.py'):
        print('Files are identical')
    else:
        print('Files are different')


if __name__ == '__main__':
    main()
