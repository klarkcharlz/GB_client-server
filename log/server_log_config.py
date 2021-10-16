import logging
from logging.handlers import TimedRotatingFileHandler

# Определить формат сообщений
# дата уровень имя сообщение
format = logging.Formatter('%(asctime)s %(levelname)-10s %(name)s %(message)s')

# Создать обработчик, который выводит сообщения в файл
server_log_hand = logging.FileHandler('logs/server.log')
server_log_hand.setFormatter(format)

time_handler = TimedRotatingFileHandler("logs/backup/server/server.log",
                                        when='d',
                                        interval=1,
                                        backupCount=5)

# Создать регистратор
server_log = logging.getLogger('server')
server_log.setLevel(logging.INFO)
server_log.addHandler(server_log_hand)
server_log.addHandler(time_handler)
