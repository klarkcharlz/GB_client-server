from socket import socket, AF_INET, SOCK_STREAM, timeout
from datetime import datetime
import argparse
from json import dumps


max_clients = 5
timeout_ = 10

parser = argparse.ArgumentParser(description='JSON instant messaging client.')
parser.add_argument(
    '-addr',
    type=str,
    default='',
    help='Server IP (default: '')'
)
parser.add_argument(
    '-port',
    type=int,
    default=7777,
    help='Server IP (default: 7777)'
)
args = parser.parse_args()

server = socket(AF_INET, SOCK_STREAM)  # обьект сервер
# AF_INET -указывает, что создаваемый сокет будет сетевым
# SOCK_STREAM -указывает на то, что сокет работает с TCP-пакетами
server.settimeout(timeout_)  # таймаут подключения
server.bind((args.addr, args.port))  # запуск
server.listen(max_clients)  # максимальное число клиентов

if __name__ == "__main__":
    print(f"{datetime.now()}: Запуск сервера")
    while True:
        try:
            client, address = server.accept()  # ловим подключение
        except timeout:
            print(f"Клиентов не обнаружено")
        else:
            data = client.recv(1000000)  # принимаем данные

            print('Сообщение: ', data.decode('utf-8'), ', было отправлено клиентом: ', address)

            msg = {
                "response": 200,
                "alert": "OK"
            }

            client.send(dumps(msg).encode('utf-8'))  # отправляем данные обратно клиенту
            client.close()  # закрываем подключение
