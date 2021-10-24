from socket import socket, AF_INET, SOCK_STREAM
import argparse
from time import time
from json import dumps, loads

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

    def connect(self, address: str, port: int) -> None:
        """Подключение к серверу"""
        self.client.connect((address, port))  # подключение

    def disconnect(self) -> None:
        """отключение от сервера"""
        self.client.close()

    def __receive_msg(self) -> bytes:
        """Прием ответного сообщения"""
        return self.client.recv(1000000)

    @staticmethod
    def __validate_response(data):
        """Валидация ответного сообщения от сервера"""
        try:
            data = loads(data.decode('utf-8'))
        except Exception as err:
            print(f"{type(err)}\n{err}")
            return "Message not JSON format."
        else:
            if isinstance(data, dict):
                try:
                    assert len(data) in [1, 2], "Не валидное количество полей"
                    assert "response" in data, "Отсутствует поле response"
                    assert isinstance(data["response"], int), "Поле response не числового типа"
                    assert "alert" in data or "error" in data, "Присутствуют не валидные поля"
                except AssertionError as err:
                    return f"Не валидное сообщение от сервера, {str(err)}: {data}"
                else:
                    return f"Валидное сообщение от сервера: {data}"
            else:
                return "Message not JSON format."

    def send_message(self, mess: dict) -> str:
        """Отправка сообщения серверу"""
        self.client.send(dumps(mess).encode('utf-8'))
        response_data = self.__receive_msg()
        return self.__validate_response(response_data)


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
    print(my_client.send_message(msg))
    my_client.disconnect()
