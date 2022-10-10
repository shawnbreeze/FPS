# from pprint import pprint
from datetime import timedelta
from typing import List

import db
from settings import *


def time_sum(time: List[str]) -> timedelta:
    """
    Calculates time from list of time hh:mm:ss format
    """

    return sum(
        [
            timedelta(hours=int(ms[0]), minutes=int(ms[1]), seconds=int(ms[2]))
            for t in time
            for ms in [t.split(":")]
        ],
        timedelta(),
    )

##
def weight_1m(width: float, fold: float, thickness, k: float):
    if isinstance(fold, str) or not fold:
        fold = 0
    elif fold is None:
        fold = 0
    w = width + (fold * 2)
    return (w * thickness * k) / 50


def weight_1pc(width, fold, thickness, height, k):
    meter = weight_1m(width, fold, thickness, k)
    return meter * (height/100)


def weight_deviation(params: tuple, roll_lenght: int, roll_weight: float):  # params tuple = (width, fold, thickness, density_factor)
    width = params[0]
    fold = params[1]
    if isinstance(fold, str): fold = 0
    thickness = params[2]
    density_factor = params[3]
    meter1 = weight_1m(width, fold, thickness, density_factor)
    ideal_weight = meter1 * roll_lenght/1000
    deviation = ((roll_weight/ideal_weight)-1)*100
    deviation = round(deviation, 1)
    return deviation


def order_meterage(order):
    # pprint(order)
    width = order['width']
    thickness = order['thickness']
    height = order['height']
    fold = order['fold']
    k = order['density_factor']
    quantity = order['quantity']
    meas_unit = order['meas_unit']
    waste_percent = order['waste_percent']
    if meas_unit == 'м' or meas_unit == 'пог.м':
        if waste_percent == '' or not waste_percent:
            return int((quantity*WASTE_PERCENTAGE)/100)
        else:
            return int((quantity*float(1+waste_percent/100))/100)
    elif meas_unit == 'шт':
        if waste_percent == '' or not waste_percent:
            return int((quantity*float(height)*WASTE_PERCENTAGE)/100)
        else:
            return int((quantity*float(height)*float(1+waste_percent/100))/100)
    elif meas_unit == 'кг':
        meter = weight_1m(width, fold, thickness, k)
        if waste_percent == '' or not waste_percent:
            return int((quantity*1000/meter)*WASTE_PERCENTAGE)
        else:
            return int(((quantity*1000/meter)*float(1+waste_percent/100))/100)


def order_weight(order):
    width = order['width']
    thickness = order['thickness']
    height = order['height']
    fold = order['fold']
    if isinstance(fold, str):
        fold = 0
    k = order['density_factor']
    quantity = order['quantity']
    meas_unit = order['meas_unit']
    waste_percent = order['waste_percent'] if order['waste_percent'] else 0
    if meas_unit == 'кг':
        if waste_percent == '' or not waste_percent:
            return quantity*WASTE_PERCENTAGE
        else:
            return quantity*float(1+waste_percent/100)
    if meas_unit == 'шт':
        weight_1pc_ = weight_1pc(width, fold, thickness, height, k)
        # print(order['name'], weight_1pc_)
        # print(f'width {width}, height {height}, fold {fold}, thickness {thickness}, k {k}\n')
        if waste_percent == '':
            return (quantity*weight_1pc_*WASTE_PERCENTAGE)/1000
        else:
            return quantity * weight_1pc_ * float(1 + waste_percent / 100) / 1000
    if meas_unit == 'м' or meas_unit == 'пог.м':
        weight_1m_ = weight_1m(width, fold, thickness, k)
        if waste_percent == '' or not waste_percent:
            return quantity*weight_1m_*WASTE_PERCENTAGE
        else:
            return quantity*weight_1m_*float(1+waste_percent/100)


def multi_order_weight(order_no):
    total_weight_list = []
    positions_names = db.get_position_names(order_no)
    for position in positions_names:
        order_fields = db.get_order_fields(order_no, position[0])
        weight = order_weight(order_fields)
        total_weight_list.append(weight)
    return sum(total_weight_list)


def multi_order_meterage(order_no):
    total_meterage_list = []
    positions_names = db.get_position_names(order_no)
    for position in positions_names:
        order_fields = db.get_order_fields(order_no, position[0])
        meterage = order_meterage(order_fields)
        total_meterage_list.append(meterage)
    return sum(total_meterage_list)
