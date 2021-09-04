import json
from datetime import datetime


def write_order_to_json(item: str, quantity: int, price: float, buyer: str, date: datetime):
    new_orders = {
        "item": item,
        "quantity": quantity,
        "price": price,
        "buyer": buyer,
        "date": date
    }

    if isinstance(new_orders["date"], datetime):
        new_orders["date"] = new_orders["date"].isoformat()

    with open('orders.json', 'r') as f:
        old_json_data = json.load(f)
        old_json_data["orders"].append(new_orders)

    with open('orders.json', 'w') as f:
        json.dump(old_json_data, f, indent=4)


if __name__ == "__main__":
    write_order_to_json("PC", 2, 3200.20, "Nik Nikolson", datetime.now())
