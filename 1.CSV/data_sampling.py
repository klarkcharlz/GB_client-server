import csv
import re


def get_data(files: list, headers: list) -> list:
    """
    Парсинг данных из текстовых файлов
    :param files: список файлов на открытие
    :param headers: заголовки, необходимые данные
    :return: список списков с данными
    """
    os_prod_list, os_name_list, os_code_list, os_type_list = [], [], [], []
    for file in files:
        with open(file, 'r', encoding='1251') as f:
            text = f.read()
            os_prod_list.append(re.findall(r'.*Изготовитель системы:(.*)', text)[0].strip())
            os_name_list.append(re.findall(r'.*Название ОС:(.*)', text)[0].strip())
            os_code_list.append(re.findall(r'.*Код продукта:(.*)', text)[0].strip())
            os_type_list.append(re.findall(r'.*Тип системы:(.*)', text)[0].strip())

    return [headers, os_prod_list, os_name_list, os_code_list, os_type_list]


def write_to_csv(file: list, csv_file: str, headers: list) -> None:
    """
    Запись распарсенных данных из текстовых файлов в csv файл
    :param file: список файлов на парсинг
    :param csv_file: файл куда будут записаны распарсенные данные
    :param headers: заголовки, необходимые поля для поиска
    :return: None, результат работы функции - запись в файл
    """
    data = get_data(file, headers)
    headers, data = data[0], data[1:]
    with open(csv_file, 'w') as f:
        csv_f = csv.writer(f, quoting=csv.QUOTE_NONNUMERIC)
        csv_f.writerow(headers)
        for i in range(len(data[0])):
            csv_f.writerow(list(map(lambda l: l[i], data)))


if __name__ == "__main__":
    FILES_NAME = ["info_1.txt", "info_2.txt", "info_2.txt"]  # файлы на открытие
    CSV_FILE = "data.csv"  # файл для записи
    HEADERS = ['Изготовитель системы', 'Название ОС', 'Код продукта', 'Тип системы']  # то что будем вытаскивать

    write_to_csv(FILES_NAME, CSV_FILE, HEADERS)
