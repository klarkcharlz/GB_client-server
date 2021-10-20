import json
from datetime import datetime


def write_order_to_json(item: str, quantity: int, price: float, buyer: str, date: datetime) -> None:
    """
    Внесение информации о заказе в json файл
    :param item: продукт
    :param quantity: количество
    :param price: цена
    :param buyer: покупатель
    :param date: дата оформления заказа
    :return: None, результат работы функции запись в json файл
    """
    new_orders = {
        "item": item,
        "quantity": quantity,
        "price": price,
        "buyer": buyer,
        "date": date
    }

    if isinstance(new_orders["date"], datetime):
        # json не поддерживает python тип datetime, необходимо преобразование
        new_orders["date"] = new_orders["date"].isoformat()

    with open('orders.json', 'r') as f:
        # сначала считаем то что уже есть для дозаписи
        old_json_data = json.load(f)
        old_json_data["orders"].append(new_orders)

    with open('orders.json', 'w') as f:
        # запись в json файл
        json.dump(old_json_data, f, indent=4)


if __name__ == "__main__":
    ORDERS = [
        {"item": "PC",
         "quantity": 3,
         "price": 1000,
         "buyer": "Nik Nik",
         "date": datetime.now(),
         },
        {"item": "SSD",
         "quantity": 5,
         "price": 2000,
         "buyer": "Mike Mik",
         "date": datetime.now(),
         },
        {"item": "HHD",
         "quantity": 22,
         "price": 10000,
         "buyer": "Max Maxi",
         "date": datetime.now(),
         },
    ]

    for order in ORDERS:
        write_order_to_json(**order)
