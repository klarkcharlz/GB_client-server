"""
Создать текстовый файл test_file.txt,
заполнить его тремя строками:
«сетевое программирование», «сокет», «декоратор».
Проверить кодировку файла по умолчанию.
Принудительно открыть файл в формате Unicode и вывести его содержимое.
"""

with open("test_file.txt", "r") as f:
    print(f.encoding)

with open("test_file.txt", "r", encoding='utf-8') as f:
    print(f.read())
