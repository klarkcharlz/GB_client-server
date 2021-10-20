import yaml

TEST_DATA = {
    "list": [1, 2, 3],
    "int": 4,
    "dict": {
        4: "€"
    }
}

with open('data.yaml', 'w') as f:
    # запись в файл
    yaml.dump(TEST_DATA, f, default_flow_style=False, allow_unicode=True)

with open('data.yaml') as f:
    # чтение
    f_n_content = yaml.safe_load(f)
    print(f_n_content)
    print(f_n_content == TEST_DATA)  # данные совпадают, но ключи в обратном порядке

"""
Данные совпадают, 
Почему запись в файл произвелась по ключам в обратном порядке?
"""