from socket import socket, AF_INET, SOCK_STREAM
import argparse
from time import time
from json import dumps, loads
from log.client_log_config import client_log


parser = argparse.ArgumentParser(description='JSON instant messaging client.')
parser.add_argument(
    '-addr',
    type=str,
    default="localhost",
    help='Server IP (default: localhost)'
)
parser.add_argument(
    '-port',
    type=int,
    default=7777,
    help='Server port (default: 7777)'
)
args = parser.parse_args()


class CustomClient:
    """Кастомный клиент"""

    def __init__(self, family: int, type_: int, timeout_: int) -> None:
        self.client = socket(family, type_)
        self.client.settimeout(timeout_)
        self.con = False

    def connect(self, address: str, port: int) -> None:
        """Подключение к серверу"""
        try:
            self.client.connect((address, port))  # подключение
        except Exception as err:
            client_log.exception(err)
        else:
            self.con = True
            client_log.info(f"Установлено соединение с сервером.")

    def disconnect(self) -> None:
        """отключение от сервера"""
        self.client.close()

    def __receive_msg(self) -> bytes:
        """Прием ответного сообщения"""
        return self.client.recv(1000000)

    @staticmethod
    def __validate_response(data):
        """Валидация ответного сообщения от сервера"""
        data = loads(data.decode('utf-8'))
        try:
            assert len(data) in [1, 2], "Не валидное количество полей"
            assert "response" in data, "Отсутствует поле response"
            assert isinstance(data["response"], int), "Поле response не числового типа"
            assert "alert" in data or "error" in data, "Присутствуют не валидные поля"
        except AssertionError as err:
            client_log.exception(err)
            return f"Не валидное сообщение от сервера, {str(err)}: {data}"
        else:
            return str(data)

    def send_message(self, mess: dict) -> str:
        """Отправка сообщения серверу"""
        if self.con:
            self.client.send(dumps(mess).encode('utf-8'))
            client_log.info(f"Отправлено сообщение: '{mess}'.")
            response_data = self.__receive_msg()
            response_msg = self.__validate_response(response_data)
            client_log.info(f"Получено сообщение: '{response_msg}'.")
            return response_msg
        else:
            client_log.error(f"Отправка сообщения невозможна, соединение с сервером небыло установленно.")
            return "Нет активного соединения."


if __name__ == "__main__":
    msg = {
        "action": "presence",
        "time": int(time()),
        "type": "status",
        "user": {
            "account_name": "Klark Charlz",
            "status": "Online"
        }
    }

    my_client = CustomClient(AF_INET, SOCK_STREAM, 10)
    my_client.connect(args.addr, args.port)
    # print(my_client.send_message(msg))
    my_client.send_message(msg)
    my_client.disconnect()
