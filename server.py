from socket import socket, AF_INET, SOCK_STREAM
from socket import timeout as TimeoutError
from select import select
import argparse
from json import dumps, loads

from log_conf.server_log_config import server_log
from decos import Log

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
    default=7775,
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
        self.all_clients = []
        self.wait = 0
        self.clients_read = []
        self.clients_write = []

    @staticmethod
    @Log(server_log)
    def read_requests(read_clients):
        responses = {}
        for sock in read_clients:
            msg = {}
            try:
                data = loads(sock.recv(1000000).decode('utf-8'))  # принимаем данные
            except Exception as err:
                server_log.error("Принято сообщение неверного формата.")
                server_log.exception(err)
            else:
                server_log.info(f'Сообщение: {data}, было отправлено клиентом: {sock}')
                if isinstance(data, dict):
                    if data.get("type", None) == 1:
                        try:
                            assert "action" in data, "Отсутствует поле action."
                            assert data["action"] in ["presence", "prоbe", "msg", "quit", "authenticate", "join",
                                                      "leave"], \
                                "Поле action содержит не допустимое значение."
                            assert len(data["action"]) < 16, "Поле action превышает максимальное значение в 16 символов"
                            assert "time" in data, "Отсутствует поле time."
                            assert isinstance(data["time"], int), "Поле time не валидного значения"
                        except AssertionError as err:
                            server_log.error("Принят не валидный JSON.")
                            server_log.exception(err)
                            msg["error"] = str(err)
                            msg["response"] = 400
                        else:
                            msg["alert"] = "OK"
                            msg["response"] = 200
                            msg["message"] = data.get("message", "Nos message")
                            responses[sock] = msg
        return responses

    @staticmethod
    @Log(server_log)
    def write_responses(requests, clients_write, all_clients):
        listeners = []  # список слушателей
        msgs = []  # список сообщений для отправки

        for sock in requests:
            if requests[sock]:
                listeners.append(sock)
                msgs.append(requests[sock])

        for msg in msgs:
            for listener in clients_write:
                if listener not in requests.keys():
                    try:
                        if listener == '':
                            raise Exception
                        response_msg = dumps(msg).encode('utf-8')
                        listener.send(response_msg)
                    except Exception as err:
                        server_log.exception(err)
                        server_log.info(f"Клиент {sock} отключился")
                        sock.close()
                        all_clients.remove(sock)
                    else:
                        server_log.info(f"Клиенту {sock} отправлено ответное сообщение: '{response_msg}'.")

    @Log(server_log)
    def run(self) -> None:
        """Запуск сервера"""
        server_log.warning("Запуск сервера")
        while True:
            try:
                client, address = self.server.accept()  # ловим подключение
                server_log.info(f"Установлено соединение с клиентом: {address}.")
            except TimeoutError:
                server_log.info("Клиентов не обнаружено")
            else:
                self.all_clients.append(client)
            finally:
                try:
                    clients_read, clients_write, errors = select(self.all_clients, self.all_clients, [], self.wait)
                except Exception as err:
                    server_log.exception(err)
                else:
                    print(clients_read)
                    print(clients_write)
                    requests = self.read_requests(clients_read)
                    if requests:
                        self.write_responses(requests, clients_write, self.all_clients)


if __name__ == "__main__":
    my_serv = CustomServer(family=AF_INET,
                           type_=SOCK_STREAM,
                           interval=0.5,
                           addr=args.addr,
                           port=args.port,
                           max_clients=5)
    my_serv.run()
