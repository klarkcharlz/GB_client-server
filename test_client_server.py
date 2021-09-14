from multiprocessing import Process
from time import time
from socket import AF_INET, SOCK_STREAM
from unittest import TestCase, main

from client import CustomClient
from server import CustomServer


class TestClientServerApplication(TestCase):
    def setUp(self):
        # предварительная настройка
        self.test_client = CustomClient(AF_INET, SOCK_STREAM, 10)
        self.test_serv = CustomServer(family=AF_INET,
                                      type_=SOCK_STREAM,
                                      interval=10,
                                      addr='',
                                      port=8888,
                                      max_clients=5)
        self.server_run = Process(target=self.test_serv.run, daemon=True)
        self.server_run.start()
        self.test_client.connect("localhost", 8888)

    def tearDown(self):
        # завершающие действия
        self.test_client.disconnect()
        self.server_run.terminate()

    def test_presence(self):
        self.assertEqual(self.test_client.send_message({
            "action": "presence",
            "time": int(time()),
            "type": "status",
            "user": {
                "account_name": "Klark Charlz",
                "status": "Online"
            }
        }), 'Сообщение от сервера: {"response": 200, "alert": "OK"}, длиной: 32 байт.')


if __name__ == "__main__":
    main()
