import csv
import re


files_name = ["info_1.txt", "info_2.txt", "info_2.txt"]
csv_file = "data.csv"


def get_data(files: list) -> list:
    os_prod_list, os_name_list, os_code_list, os_type_list = [], [], [], []
    main_data = ['Изготовитель системы', 'Название ОС', 'Код продукта', 'Тип системы']
    for file in files:

        with open(file, 'r', encoding='1251') as f:
            text = f.read()
            os_prod_list.append(re.findall(r'.*Изготовитель системы:(.*)', text)[0].strip())
            os_name_list.append(re.findall(r'.*Название ОС:(.*)', text)[0].strip())
            os_code_list.append(re.findall(r'.*Код продукта:(.*)', text)[0].strip())
            os_type_list.append(re.findall(r'.*Тип системы:(.*)', text)[0].strip())

    return [main_data, os_prod_list, os_name_list, os_code_list, os_type_list]


def write_to_csv(file: list) -> None:
    data = get_data(files_name)
    headers, data = data[0], data[1:]
    with open(file, 'w') as f:
        csv_f = csv.writer(f, quoting=csv.QUOTE_NONNUMERIC)
        csv_f.writerow(headers)
        for i in range(len(data[0])):
            csv_f.writerow(list(map(lambda l: l[i], data)))


if __name__ == "__main__":
    write_to_csv(csv_file)
