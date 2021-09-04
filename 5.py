"""
Выполнить пинг веб-ресурсов
yandex.ru, youtube.com
и преобразовать результаты из байтовового в строковый тип на кириллице.
"""

import subprocess
import locale


def_coding = locale.getpreferredencoding()
# print(def_coding)

ping = ["yandex.ru", "youtube.com"]

command = ["ping", "-c", "4"]

for url in ping:
    subproc_command = subprocess.Popen([*command, url], stdout=subprocess.PIPE)
    print(f"Result command {' '.join([*command, url])}:\n")
    for line in subproc_command.stdout:
        print(line.decode(def_coding).encode('utf-8').decode('utf-8'))
    else:
        print()
