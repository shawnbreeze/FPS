import sqlite3
# from pprint import pprint
import time
from calculations import time_sum
from pprint import pprint
# from PyQt5.QtWidgets import QApplication
from settings import *
from datetime import timedelta, datetime

conn = sqlite3.connect("d:/FPS DB/data_.db")
cursor = conn.cursor()


def db_read(func):

    def wrapper(*args, **kwargs):
        start = time.time()
        return_value = func(*args, **kwargs)
        end = time.time()
        # print('READ  '+func.__name__+' - время выполнения: {} мс'.format(int(end-start)*1000))
        return return_value
    return wrapper


def db_write(func):

    def wrapper(*args, **kwargs):
        start = time.time()
        return_value = func(*args, **kwargs)
        end = time.time()
        # print('WRITE '+func.__name__+' - время выполнения: {} мс'.format(int(end - start)*1000))
        return return_value
    return wrapper


@db_read
def get_users():
    sql = f"""SELECT * FROM users"""
    cursor.execute(sql)
    result = cursor.fetchall()
    return result


@db_read
def is_roll_waste(roll_id: int):
    sql = f"""SELECT is_waste FROM rolls WHERE roll_id='{roll_id}'"""
    cursor.execute(sql)
    result = cursor.fetchone()[0]
    return result == 1


@db_read
def is_roll_edge(roll_id: int):
    sql = f"""SELECT is_edge FROM rolls WHERE roll_id='{roll_id}'"""
    cursor.execute(sql)
    result = cursor.fetchone()[0]
    return result == 1


@db_read
def is_roll_scrap(roll_id: int):
    sql = f"""SELECT is_scrap FROM rolls WHERE roll_id='{roll_id}'"""
    cursor.execute(sql)
    result = cursor.fetchone()[0]
    return result == 1


@db_write
def set_roll_as_waste(roll_id):
    sql = f"""UPDATE rolls SET is_waste='1' WHERE roll_id='{roll_id}'"""
    cursor.execute(sql)
    conn.commit()


@db_read
def get_user_id_by_name(name):
    sql = f"""SELECT user_id FROM users WHERE name='{name}'"""
    cursor.execute(sql)
    result = cursor.fetchone()[0]
    return result


@db_read
def get_user_name_by_id(user_id):
    sql = f"""SELECT name FROM users WHERE user_id='{user_id}'"""
    cursor.execute(sql)
    result = cursor.fetchone()[0]
    return result


@db_read
def get_comment(roll_id):
    sql = f"""SELECT comment FROM rolls WHERE roll_id='{roll_id}'"""
    cursor.execute(sql)
    result = cursor.fetchone()
    return result[0]


@db_write
def update_comment(roll_id, new_comment):
    sql = f"""UPDATE rolls SET comment='{new_comment}' WHERE roll_id={roll_id}"""
    cursor.execute(sql)
    conn.commit()


@db_read
def login(user, password):
    sql = f"""SELECT password FROM users WHERE name='{user}'"""
    cursor.execute(sql)
    result = cursor.fetchone()[0]
    return result == password


@db_read
def get_extruders():
    sql = f"""SELECT * FROM extruders"""
    cursor.execute(sql)
    result = cursor.fetchall()
    return result

@db_read
def get_extr_ids_list():
    sql = f"""SELECT extr_id FROM extruders WHERE in_repair='0'"""
    cursor.execute(sql)
    result = cursor.fetchall()
    return [x[0] for x in result]


@db_read
def get_all_extr_ids_list():
    sql = f"""SELECT extr_id FROM extruders"""
    cursor.execute(sql)
    result = cursor.fetchall()
    return [x[0] for x in result]


@db_read
def get_extr_orders():
    sql = f"""SELECT order_no, name, extr_id FROM orders WHERE extr_id !='' AND state='{EXTRUSION_STATE[0]}'"""
    cursor.execute(sql)
    result = cursor.fetchall()
    return result


@db_read
def get_busy_extrs_dict(extr_ids: list):
    sql = f"""SELECT extr_id FROM orders WHERE extr_id !=''"""
    cursor.execute(sql)
    extr_dict = {}
    extr_set = set(cursor.fetchall())
    extr_set = {x[0] for x in extr_set}
    for extr_id in extr_ids:
        extr_dict.update({extr_id: extr_id in extr_set})
    return extr_dict


@db_read
def get_busy_extrs_dict_1s():
    sql = f"""SELECT extr_id, current_order FROM extruders"""
    cursor.execute(sql)
    extr_dict = {}
    result = cursor.fetchall()
    for extr in result:
        extr_dict.update({extr[0]: extr[1] is not None})
    return extr_dict


@db_read
def get_order_fields(order_no, position):
    table = 'orders_' if CONNECT_1C else 'orders'
    sql = f"""SELECT * FROM {table} WHERE order_no='{order_no}' AND name='{position}'"""
    output_obj = cursor.execute(sql)
    results = cursor.fetchall()
    for row in results:
        row_as_dict = {output_obj.description[i][0]: row[i] for i in range(len(row))}
    return row_as_dict


@db_read
def get_order_params_by_no_and_name(order_no, name):
    table = 'orders_' if CONNECT_1C else 'orders'
    sql = f"""SELECT * FROM {table} WHERE order_no='{order_no}' AND name='{name}'"""
    output_obj = cursor.execute(sql)
    results = cursor.fetchall()
    for row in results:
        row_as_dict = {output_obj.description[i][0]: row[i] for i in range(len(row))}
    return row_as_dict


@db_read
def get_position_names(order_no):
    table = 'orders_' if CONNECT_1C else 'orders'
    sql = f"""SELECT name FROM {table} WHERE order_no='{order_no}'"""
    cursor.execute(sql)
    result = cursor.fetchall()
    return result


@db_read
def get_rolls_for_table(order_no):
    sql = f"""SELECT * FROM rolls WHERE order_no='{order_no}'"""
    cursor.execute(sql)
    result = cursor.fetchall()
    return result


@db_read
def is_multi_order(order_no):
    table = 'orders_' if CONNECT_1C else 'orders'
    sql = f"""SELECT * FROM {table} WHERE order_no='{order_no}'"""
    cursor.execute(sql)
    result = cursor.fetchall()
    return False if len(result) == 1 else True


@db_write
def clear_orders():
    cursor.execute("""DELETE FROM orders""")
    conn.commit()


@db_write
def write_orders(orders):
    clear_orders()
    sql = ''
    for x in orders:
        query = "INSERT into orders " + str(tuple(x.keys())) + " VALUES" + str(tuple(x.values())) + ";"
        sql += query
    with open('sql', 'w') as f:
        f.write(sql)
    cursor.executescript(sql)
    conn.commit()


@db_write
def add_roll(roll_dict):
    sql = "INSERT INTO rolls " + str(tuple(roll_dict.keys())) + " VALUES " + str(tuple(roll_dict.values())) + ";"
    sql = sql.replace("'ъъъ'", 'NOT NULL')
    cursor.execute(sql)
    conn.commit()
    return cursor.lastrowid


@db_read
def get_params_by_name(name):
    table = 'orders_' if CONNECT_1C else 'orders'
    sql = f"""SELECT width, fold, thickness, density_factor FROM {table} WHERE name='{name}'"""
    cursor.execute(sql)
    return cursor.fetchone()


@db_write
def extr_new_shift(worker_id, start_time):
    sql = f"""INSERT INTO extr_shifts VALUES (NOT NULL, '{worker_id}','{start_time}','',0,0,0,0,0,'0:00:00',0)"""
    cursor.execute(sql)
    conn.commit()
    return cursor.lastrowid


@db_write
def  extr_end_shift(shift_id, end_time):
    sql = f"""UPDATE extr_shifts SET end_time = '{end_time}' WHERE shift_id='{shift_id}'"""
    cursor.execute(sql)
    conn.commit()
    return cursor.lastrowid


@db_read
def get_meterage(order_no, position):
    sql = f"""SELECT SUM(lenght) FROM rolls WHERE order_no='{order_no}' AND position='{position}' AND is_waste=0 AND is_edge=0 AND is_scrap=0"""
    cursor.execute(sql)
    result = cursor.fetchone()[0]
    return result if result is not None else 0


@db_read
def get_total_meterage(order_no):
    sql = f"""SELECT SUM(lenght) FROM rolls WHERE order_no='{order_no}' AND is_waste=0 AND is_edge=0 AND is_scrap=0"""
    cursor.execute(sql)
    result = cursor.fetchone()[0]
    return result if result is not None else 0


@db_read
def get_weight(order_no, position):
    sql = f"""SELECT SUM(weight) FROM rolls WHERE order_no='{order_no}' AND position='{position}' AND is_waste=0 AND is_edge=0 AND is_scrap=0"""
    cursor.execute(sql)
    result = cursor.fetchone()[0]
    return result if result is not None else 0


@db_read
def get_waste(order_no, position):
    sql = f"""SELECT SUM(weight) FROM rolls WHERE order_no='{order_no}' AND position='{position}' AND is_waste=1"""
    cursor.execute(sql)
    result = cursor.fetchone()[0]
    return result if result is not None else 0


@db_read
def get_edge(order_no, position):
    sql = f"""SELECT SUM(weight) FROM rolls WHERE order_no='{order_no}' AND position='{position}' AND is_edge=1"""
    cursor.execute(sql)
    result = cursor.fetchone()[0]
    return result if result is not None else 0


@db_read
def get_scrap(order_no, position):
    sql = f"""SELECT SUM(weight) FROM rolls WHERE order_no='{order_no}' AND position='{position}' AND is_scrap=1"""
    cursor.execute(sql)
    result = cursor.fetchone()[0]
    return result if result is not None else 0


@db_read
def is_roll_control(roll_id: int):
    sql = f"""SELECT add_control FROM rolls WHERE roll_id='{roll_id}'"""
    cursor.execute(sql)
    result = cursor.fetchone()[0]
    return result == 1


@db_write
def add_control_mark(roll_id: int):
    sql = f"""UPDATE rolls SET add_control='1' WHERE roll_id='{roll_id}'"""
    cursor.execute(sql)
    conn.commit()


@db_read
def get_orders_by_state(state: str):
    table = 'orders_' if CONNECT_1C else 'orders'
    sql = f"""SELECT order_no, name FROM {table} WHERE state='{state[0]}'"""
    cursor.execute(sql)
    result=cursor.fetchall()
    return result


@db_write
def extr_new_order_started(order_no, id):
    sql = f"""UPDATE orders SET extr_id='{id}' WHERE order_no='{order_no}'"""
    cursor.execute(sql)
    conn.commit()


@db_write
def extr_set_idle(extr_id: int, state: bool):
    sql = f"""UPDATE extruders SET is_idle={state} WHERE extr_id='{extr_id}'"""
    cursor.execute(sql)
    conn.commit()


@db_write
def extr_idle_start(order_no: str, position: str, time: str, worker_id: int, comment: str, extr_id: int, shift_id: int):
    sql = f"""INSERT INTO rolls (roll_id, order_no, position, extr_time, extr_author_id, comment, extr_id, is_stop, is_start, add_control, is_waste, is_scrap, is_edge, shift_id) VALUES
    (NOT NULL,'{order_no}','{position}','{time}','{worker_id}','{comment}','{extr_id}', 1, 0, 0, 0, 0, 0, {shift_id})"""
    cursor.execute(sql)
    conn.commit()
    return cursor.lastrowid


@db_write
def extr_idle_stop(order_no: str, position: str, time: str, worker_id: int, extr_id: int, shift_id: int):
    sql = f"""INSERT INTO rolls (roll_id, order_no, position, extr_time, extr_author_id, extr_id, is_stop, is_start, add_control, is_waste, is_scrap, is_edge, shift_id) VALUES
    (NOT NULL,'{order_no}','{position}','{time}','{worker_id}','{extr_id}', 0, 1, 0, 0, 0, 0, {shift_id})"""
    cursor.execute(sql)
    conn.commit()
    return cursor.lastrowid


@db_read
def get_users_as_dict():
    # TODO добавить остальные данные юзеров в dict
    sql = 'SELECT * FROM users'
    cursor.execute(sql)
    users = cursor.fetchall()
    users_dict = {}
    for user in users:
        users_dict.update({user[0]: user[1]})
    return users_dict


@db_write
def write_properties(guids_dict):
    script = ''
    for x in guids_dict:
        script += f"""INSERT OR REPLACE INTO guids VALUES ('{x}','{guids_dict[x]}');"""
    cursor.executescript(script)
    conn.commit()


@db_read
def get_by_guid(guid):
    sql = f"""SELECT value FROM guids WHERE guid='{guid}'"""
    cursor.execute(sql)
    result = cursor.fetchone()
    return result[0] if result else None

@db_write
def write_nomenclature(nom_list: list):
    sql = ''
    for x in nom_list:
        query = "INSERT OR REPLACE INTO nomenclature " + str(tuple(x.keys())) + " VALUES" + str(tuple(x.values())) + ";"
        sql += query
    cursor.executescript(sql)
    conn.commit()


@db_write
def write_orders_1s(orders_list: list):
    sql = ''
    for x in orders_list:
        query = "INSERT OR REPLACE INTO orders_ " + str(tuple(x.keys())) + " VALUES" + str(tuple(x.values())) + ";"
        sql += query
    cursor.executescript(sql)
    conn.commit()



@db_read
def get_extr_orders_guids():
    sql = f"""SELECT extr_id, current_order FROM extruders"""
    cursor.execute(sql)
    result = cursor.fetchall()
    return result


@db_read
def get_order_fields_1s(key):
    sql = f"""SELECT * FROM orders_ WHERE Ref_Key='{key}'"""
    # print(sql)
    output_obj = cursor.execute(sql)
    results = cursor.fetchall()
    for row in results:
        order = {output_obj.description[i][0]: row[i] for i in range(len(row))}
    return order


@db_read
def get_nom_name_by_guid(key):
    sql = f"""SELECT Description FROM nomenclature WHERE Ref_Key='{key}'"""
    cursor.execute(sql)
    results = cursor.fetchone()
    return results[0]


@db_read
def get_nom_params_by_name(name):
    sql = f"""SELECT * FROM nomenclature WHERE Description='{name}'"""
    output_obj = cursor.execute(sql)
    results = cursor.fetchone()
    for row in results:
        fields = {output_obj.description[i][0]: row[i] for i in range(len(row))}
    return fields


@db_read
def get_order_no_by_guid(key):
    sql = f"""SELECT order_no FROM orders_ WHERE Ref_Key='{key}'"""
    cursor.execute(sql)
    results = cursor.fetchone()
    return results[0]


@db_read
def extr_get_last_shift():
    sql = f"""SELECT * FROM extr_shifts ORDER BY rowid DESC LIMIT 1"""
    output_obj = cursor.execute(sql)
    results = cursor.fetchall()
    for row in results:
        shift = {output_obj.description[i][0]: row[i] for i in range(len(row))}
    return shift


def extr_get_shift_idle_time_total(shift_id):
    extruders = get_extr_ids_list()
    orders = set()
    for extr_id in extruders:
        sql = f"""SELECT order_no FROM rolls WHERE shift_id ='{shift_id}' and extr_id='{extr_id}'"""
        cursor.execute(sql)
        res = cursor.fetchall()
        orders.update(res)
    orders = [x[0] for x in orders]
    idles = []
    for order in orders:
        idle = extr_get_shift_idle_time(order, shift_id)
        idles.append(str(idle))
    return time_sum(idles)


@db_read
def extr_get_shift_summary(shift_id):
    summary = {}
    sql = f"""SELECT SUM(weight) FROM rolls WHERE shift_id='{shift_id}' AND is_waste=0 AND is_edge=0 AND is_scrap=0"""
    cursor.execute(sql)
    weight = cursor.fetchone()[0]
    weight = weight if weight else 0
    sql = f"""SELECT SUM(weight) FROM rolls WHERE shift_id='{shift_id}' AND is_waste=1 AND is_edge=0 AND is_scrap=0"""
    cursor.execute(sql)
    waste = cursor.fetchone()[0]
    waste = waste if waste else 0
    sql = f"""SELECT SUM(weight) FROM rolls WHERE shift_id='{shift_id}' AND is_waste=0 AND is_edge=1 AND is_scrap=0"""
    cursor.execute(sql)
    edge = cursor.fetchone()[0]
    edge = edge if edge else 0
    sql = f"""SELECT SUM(weight) FROM rolls WHERE shift_id='{shift_id}' AND is_waste=0 AND is_edge=0 AND is_scrap=1"""
    cursor.execute(sql)
    scrap = cursor.fetchone()[0]
    scrap = scrap if scrap else 0
    shift_idle = extr_get_shift_idle_time_total(shift_id)
    summary.update({'shift_id': shift_id, 'weight': weight, 'waste': waste, 'edge': edge, 'scrap': scrap, 'idle_time': shift_idle})
    return summary


@db_write
def extr_write_shift_summary(shift_id):
    summary = extr_get_shift_summary(shift_id)
    sql = f"""UPDATE extr_shifts SET shift_output={summary['weight']},waste={summary['waste']},edge={summary['edge']},scrap={summary['scrap']},idle_time='{summary['idle_time']}' WHERE shift_id={shift_id};"""
    cursor.execute(sql)
    conn.commit()


@db_read
def extr_shift_get_readjustments(shift_id):
    sql = f"""SELECT readjustments FROM extr_shifts WHERE shift_id={shift_id}"""
    cursor.execute(sql)
    rea_qty = cursor.fetchone()[0]
    return rea_qty


@db_write
def extr_shift_increase_readjustments(shift_id):
    value = extr_shift_get_readjustments(shift_id)
    value = 0 if value == '' else value
    value += 1
    sql = f"""UPDATE extr_shifts SET readjustments={value} WHERE shift_id={shift_id}"""
    cursor.execute(sql)
    conn.commit()
    return value


@db_read
def get_order_key_by_no(order_no):
    sql = f"""SELECT Ref_Key FROM orders_ WHERE order_no='{order_no}'"""
    # print(sql)
    cursor.execute(sql)
    result = cursor.fetchone()[0]
    return result


@db_write
def extr_update_current_order(order_no, extr_id):
    sql = f"""UPDATE extruders SET current_order='{order_no}' WHERE extr_id={extr_id}"""
    cursor.execute(sql)
    conn.commit()


@db_read
def extr_get_order_idle_time(order_no):
    order_start = extr_get_start_time(order_no)
    sql = f"""SELECT extr_time FROM rolls WHERE order_no='{order_no}' and is_stop = 1"""
    cursor.execute(sql)
    stops = cursor.fetchall()
    sql = f"""SELECT extr_time FROM rolls WHERE order_no='{order_no}' and is_start = 1"""
    cursor.execute(sql)
    starts = cursor.fetchall()
    if not starts and not stops:
        return '0:00:00'
    idles = []
    starts_stops = []
    for x in starts:
        starts_stops.append(f'{x[0]}|start')
    for x in stops:
        starts_stops.append(f'{x[0]}|stop')
    starts_stops = sorted(starts_stops)
    if 'start' in starts_stops[0]:
        starts_stops.insert(0, f'{order_start}|stop')
    for x in range(0, len(starts_stops), 2):
        stop = datetime.strptime(starts_stops[x].split('|')[0], '%Y-%m-%d %H:%M:%S')
        try:
            start = datetime.strptime(starts_stops[x+1].split('|')[0], '%Y-%m-%d %H:%M:%S')
        except IndexError:
            start = datetime.now().replace(microsecond=0)
        idles.append(start - stop)
    idles = sum(idles, timedelta())
    return idles


@db_read
def extr_get_shift_idle_time(order_no, shift_id):
    if not shift_id:
        return '0:00:00'
    shift_start = get_shift_start(shift_id)
    shift_start = datetime.strptime(shift_start, '%Y-%m-%d %H:%M:%S')
    sql = f"""SELECT end_time FROM extr_shifts WHERE shift_id={shift_id}"""
    cursor.execute(sql)
    shift_end = cursor.fetchone()[0]
    shift_end = datetime.strptime(shift_start, '%Y-%m-%d %H:%M:%S') if shift_end else datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    sql = f"""SELECT extr_time FROM rolls WHERE order_no='{order_no}' and is_start = 1 and shift_id={shift_id}"""
    cursor.execute(sql)
    starts = cursor.fetchall()
    sql = f"""SELECT extr_time FROM rolls WHERE order_no='{order_no}' and is_stop = 1 and shift_id={shift_id}"""
    cursor.execute(sql)
    stops = cursor.fetchall()
    starts_stops = []
    idles = []
    for x in starts:
        starts_stops.append(f'{x[0]}|start')
    for x in stops:
        starts_stops.append(f'{x[0]}|stop')
    if not starts_stops:
        return '0:00:00'
    starts_stops = sorted(starts_stops)
    if 'start' in starts_stops[0]:
        starts_stops.insert(0, f'{(shift_start)}|stop')
    if 'stop' in starts_stops[-1]:
        starts_stops.append(f'{datetime.now().replace(microsecond=0)}|stop')
    for x in range(0, len(starts_stops), 2):
        stop = datetime.strptime(starts_stops[x].split('|')[0], '%Y-%m-%d %H:%M:%S')
        start = datetime.strptime(starts_stops[x+1].split('|')[0], '%Y-%m-%d %H:%M:%S')
        idles.append(start - stop)
    idles = sum(idles, timedelta())
    return idles


@db_read
def extr_is_idle(extr_id):
    sql = f"""SELECT is_idle FROM extruders WHERE extr_id={extr_id}"""
    # print(sql)
    cursor.execute(sql)
    result = cursor.fetchone()[0]
    return True if result==1 else False


@db_read
def is_roll_idle_start(roll_id):
    sql = f"""SELECT is_start FROM rolls WHERE roll_id={roll_id}"""
    # print(sql)
    cursor.execute(sql)
    result = cursor.fetchone()[0]
    return True if result == 1 else False


@db_read
def is_roll_idle_stop(roll_id):
    sql = f"""SELECT is_stop FROM rolls WHERE roll_id={roll_id}"""
    # print(sql)
    cursor.execute(sql)
    result = cursor.fetchone()[0]
    return True if result == 1 else False


@db_read
def get_order_positions(order_no):
    table = 'orders_' if CONNECT_1C else 'orders'
    sql = f"""SELECT * FROM {table} WHERE order_no='{order_no}'"""
    output_obj = cursor.execute(sql)
    results = cursor.fetchall()
    orders = list()
    for row in results:
        orders.append({output_obj.description[i][0]: row[i] for i in range(len(row))})
    return orders


@db_read
def get_extruder_name_by_id(extr_id):
    sql = f"""SELECT name FROM extruders WHERE extr_id={extr_id}"""
    # print(sql)
    cursor.execute(sql)
    result = cursor.fetchone()[0]
    return result


@db_read
def get_order_comment(order_no):
    table = 'orders_' if CONNECT_1C else 'orders'
    sql = f"""SELECT position_description, order_description, name FROM {table} WHERE order_no='{order_no}'"""
    cursor.execute(sql)
    result = cursor.fetchone()
    return result


@db_read
def get_roll_info(roll_id):
    sql = f"""SELECT * FROM rolls WHERE roll_id='{roll_id}'"""
    output_obj = cursor.execute(sql)
    results = cursor.fetchall()
    for row in results:
        row_as_dict = {output_obj.description[i][0]: row[i] for i in range(len(row))}
    return row_as_dict


@db_read
def extr_get_shift_info(shift_id):
    shift ={}
    sql = f"""SELECT * FROM extr_shifts WHERE shift_id='{shift_id}'"""
    output_obj = cursor.execute(sql)
    results = cursor.fetchall()
    for row in results:
        shift = {output_obj.description[i][0]: row[i] for i in range(len(row))}
    output = {}
    output_list = []
    for extr_id in get_all_extr_ids_list():
        sql = f"""SELECT SUM(weight) FROM rolls WHERE shift_id='{shift_id}' AND extr_id={extr_id} 
        AND is_waste=0 AND is_edge=0 AND is_scrap=0 AND is_start=0 AND is_stop=0"""
        cursor.execute(sql)
        weight = cursor.fetchone()[0]
        sql = f"""SELECT SUM(weight) FROM rolls WHERE shift_id='{shift_id}' AND extr_id={extr_id} 
                AND is_waste=1 AND is_edge=0 AND is_scrap=0 AND is_start=0 AND is_stop=0"""
        cursor.execute(sql)
        waste = cursor.fetchone()[0]
        sql = f"""SELECT SUM(weight) FROM rolls WHERE shift_id='{shift_id}' AND extr_id={extr_id} 
                AND is_waste=0 AND is_edge=1 AND is_scrap=0 AND is_start=0 AND is_stop=0"""
        cursor.execute(sql)
        edge = cursor.fetchone()[0]
        sql = f"""SELECT SUM(weight) FROM rolls WHERE shift_id='{shift_id}' AND extr_id={extr_id} 
                AND is_waste=0 AND is_edge=0 AND is_scrap=1 AND is_start=0 AND is_stop=0"""
        cursor.execute(sql)
        scrap = cursor.fetchone()[0]
        output.update({extr_id: {'weight': weight, 'waste': waste,'scrap': scrap, 'edge': edge}})
        output_list.append(output)
        shift.update(output)
    return shift


@db_write
def extr_start_order(order_no):
    table = 'orders_' if CONNECT_1C else 'orders'
    time = datetime.now().replace(microsecond=0)
    sql = f"""UPDATE {table} SET extr_start='{time}' WHERE order_no='{order_no}'"""
    cursor.execute(sql)
    conn.commit()
    return str(time)


@db_write
def extr_end_order(order_no):
    table = 'orders_' if CONNECT_1C else 'orders'
    time = datetime.now().replace(microsecond=0)
    sql = f"""UPDATE {table} SET extr_end='{time}' WHERE order_no='{order_no}'"""
    cursor.execute(sql)
    conn.commit()
    return str(time)


@db_read
def extr_get_start_time(order_no):
    table = 'orders_' if CONNECT_1C else 'orders'
    sql = f"""SELECT extr_start FROM {table} WHERE order_no='{order_no}'"""
    cursor.execute(sql)
    return cursor.fetchone()[0]


@db_read
def extr_get_avg_prod(extr_id):
    sql = f"""SELECT avg_productivity FROM extruders WHERE extr_id='{extr_id}'"""
    cursor.execute(sql)
    return cursor.fetchone()[0]


def extr_shift_avg_output(shift_id, order_no):
    order_start = extr_get_start_time(order_no)
    shift_start = get_shift_start(shift_id)
    if not shift_start:
        return
    now = datetime.now().replace(microsecond=0)
    sql = f"""SELECT SUM(weight) from rolls WHERE order_no='{order_no}' AND shift_id='{shift_id}' AND is_waste=0 AND is_edge=0 AND is_scrap=0"""
    cursor.execute(sql)
    result = cursor.fetchone()[0]
    shift_start = datetime.strptime(shift_start, '%Y-%m-%d %H:%M:%S')
    duration = (now - shift_start).total_seconds()/3600
    return result/duration if result else 0


def get_shift_start(shift_id):
    if not shift_id:
        return
    sql = f"""SELECT start_time FROM extr_shifts WHERE shift_id={shift_id}"""
    cursor.execute(sql)
    shift_start = cursor.fetchone()[0]
    return shift_start


def submit_repair_request(request_dict: dict):
    date_created = str(datetime.now().replace(microsecond=0))
    request_dict.update({'date_created': date_created})
    sql = f"""INSERT INTO repair_service_requests {str(tuple(request_dict.keys()))} VALUES {str(tuple(request_dict.values()))}"""
    cursor.execute(sql)
    conn.commit()
    return cursor.lastrowid


def get_repair_requests():
    sql = """SELECT * FROM repair_service_requests"""
    output_obj = cursor.execute(sql)
    results = cursor.fetchall()
    row_as_dict = {}
    output = []
    for row in results:
        row_as_dict = {output_obj.description[i][0]: row[i] for i in range(len(row))}
        output.append(row_as_dict)
    return output


def get_user_role(user_id):
    sql = f"""SELECT role FROM users WHERE user_id={user_id}"""
    cursor.execute(sql)
    return cursor.fetchone()[0]

