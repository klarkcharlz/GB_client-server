"""
Каждое из слов «class», «function», «method»
записать в байтовом типе
без преобразования в последовательность кодов
(не используя методы encode и decode) и определить тип,
содержимое и длину соответствующих переменных.
"""

bytes_string = [b"class", b"function", b"method"]

[print(f"Variable '{string}' is type: {type(string)} has len {len(string)}") for string in bytes_string]
