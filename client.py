from socket import socket, AF_INET, SOCK_STREAM
import argparse
from time import time
from json import dumps

timeout_ = 10
parser = argparse.ArgumentParser(description='JSON instant messaging client.')
parser.add_argument('addr', type=str, help='Server IP')
parser.add_argument(
    '-port',
    type=int,
    default=7777,
    help='Server port (default: 7777)'
)
args = parser.parse_args()

client = socket(AF_INET, SOCK_STREAM)  # обьект клиент
# AF_INET -указывает, что создаваемый сокет будет сетевым
# SOCK_STREAM -указывает на то, что сокет работает с TCP-пакетами
client.settimeout(timeout_)  # таймаут подключения

if __name__ == "__main__":
    client.connect((args.addr, args.port))  # подключение

    msg = {
        "action": "presence",
        "time": int(time()),
        "type": "status",
        "user": {
            "account_name": "Klark Charlz",
            "status": "Online"
        }
    }

    client.send(dumps(msg).encode('utf-8'))  # отправка сообщения по сети через сокет на сервер
    data = client.recv(1000000)  # прием ответного сообщения

    print('Сообщение от сервера: ', data.decode('utf-8'), ', длиной ', len(data), ' байт')

    client.close()  # закрываем соединение
