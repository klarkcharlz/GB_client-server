from socket import socket, AF_INET, SOCK_STREAM
from socket import timeout as TimeoutError
from datetime import datetime
import argparse
from json import dumps, loads


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


class CustomServer:
    """Кастомный сервер"""

    def __init__(self, family: int, type_: int, interval: int, addr: str, port: int, max_clients: int) -> None:
        self.server = socket(family, type_)
        self.server.settimeout(interval)
        self.server.bind((addr, port))
        self.server.listen(max_clients)

    def run(self) -> None:
        """Запуск сервера"""
        print(f"{datetime.now()}: Запуск сервера")
        while True:
            try:
                client, address = self.server.accept()  # ловим подключение
            except TimeoutError:
                print(f"Клиентов не обнаружено")
            else:
                msg = {}
                try:
                    data = loads(client.recv(1000000).decode('utf-8'))  # принимаем данные
                except Exception as err:
                    print(f"{type(err)}\n{err}")
                    msg["error"] = "Message not JSON format."
                    msg["response"] = 400
                else:
                    print(f'Сообщение: {data}, было отправлено клиентом: {address}')

                    if isinstance(data, dict):

                        try:
                            assert "action" in data, "Отсутствует поле action."
                            assert data["action"] in ["presence", "prоbe", "msg", "quit", "authenticate", "join", "leave"],\
                                "Поле action содержит не допустимое значение."
                            assert len(data["action"]) < 16, "Поле action превышает максимальное значение в 16 символов"
                            assert "time" in data, "Отсутствует поле time."
                            assert isinstance(data["time"], int), "Поле time не валидного значения"
                        except AssertionError as err:
                            msg["error"] = str(err)
                            msg["response"] = 400
                        else:
                            msg["alert"] = "OK"
                            msg["response"] = 200
                    else:
                        msg["error"] = "Message not JSON format."
                        msg["response"] = 400
                client.send(dumps(msg).encode('utf-8'))  # отправляем данные обратно клиенту
                client.close()  # закрываем подключение


if __name__ == "__main__":
    my_serv = CustomServer(family=AF_INET,
                           type_=SOCK_STREAM,
                           interval=10,
                           addr=args.addr,
                           port=args.port,
                           max_clients=5)
    my_serv.run()
