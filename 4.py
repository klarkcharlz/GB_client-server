"""
Преобразовать слова
«разработка», «администрирование», «protocol», «standard»
из строкового представления в байтовое
и выполнить обратное преобразование (используя методы encode и decode).
"""

string_variables = ["разработка", "администрирование", "protocol", "standard"]

[print(string.encode('utf-8').decode('utf-8')) for string in string_variables]
