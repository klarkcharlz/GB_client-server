import logging


# Определить формат сообщений
# дата уровень имя сообщение
format = logging.Formatter('%(asctime)s  %(levelname)-10s  %(name)s  %(message)s')

# Создать обработчик, который выводит сообщения в файл
client_log_hand = logging.FileHandler('logs/client.log')
client_log_hand.setFormatter(format)

# Создать регистратор
client_log = logging.getLogger('client')
client_log.setLevel(logging.INFO)
client_log.addHandler(client_log_hand)
