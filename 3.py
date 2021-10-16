"""
Определить, какие из слов «attribute», «класс», «функция», «type»
невозможно записать в байтовом типе.
"""

str_variables = ["attribute", "класс", "функция", "type"]

for string in str_variables:
    try:
        print(bytes(string, 'ascii'))
    except UnicodeEncodeError as err:
        print(f"Строку '{string}' невозможно преобразовать в байты.\n"
              f"{type(err)}\n{err}")

"""
Невозможно представить 'класс' и 'функция',
т.к. эти переменные содержат не ASCII символы.
"""