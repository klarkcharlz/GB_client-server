import yaml

test_data = {
    "list": [1, 2, 3],
    "int": 4,
    "dict": {
        4: "€"
    }
}

with open('data.yaml', 'w') as f:
    yaml.dump(test_data, f, default_flow_style=False, allow_unicode=True)

with open('data.yaml') as f:
    print(f.read())

"""
Данные совпадают, 
но благодаря "default_flow_style=False" данные записались в характерном для yaml стиле.

Почему запись в файл произвелась по ключам в обратном порядке?
"""