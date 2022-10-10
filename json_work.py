import json
from pprint import pprint


def read_orders():
    with open("temp/current_orders.json", "r") as f:
        return json.load(f)


def write_orders(orders):
    with open("temp/current_orders.json", "w") as write_file:
        json.dump(orders, write_file, ensure_ascii=False, indent=4)


def write_order(id, order):
    try:  # пытаемся загрузить словарь с заказами
        with open("temp/current_orders.json", "r") as f:
            orders = json.load(f)
        # pprint(orders)
        if str(id) in orders:
            temp = orders[str(id)]
            temp.append(order)
            orders[str(id)] = temp
        else:
            orders.update(order)
        write_orders(orders)
    except FileNotFoundError:  # если файла нет - создаем его и обновляем
        write_orders(order)


def get_order_no_by_tab_id(tab_id):
    orders = read_orders()
    return orders[str(tab_id)][0]['order_no']


def get_name_by_order_no(order_no):
    orders = read_orders()
    for key in orders:
        if orders[key][0]['order_no'] == order_no:
            return orders[key][0]['name']



