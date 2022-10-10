# from pprint import pprint
from re import search
from PyQt5.QtWidgets import QApplication
import db
from settings import *
import requests
import json
from exceptions import *


def get_val(value):
    s = search(r'^[0-9A-Fa-f\-]{36}$', value)
    try:
        value = int(value)
    except ValueError:
        try:
            value = float(value)
        except ValueError:
            if value == 'true':
                value = 1
            elif value == 'false':
                value = 0
    return db.get_by_guid(s.group(0)) if s else value


def get_order_states(sp):
    sp.ui.splash_label.setText('Чтение состояний заказов из 1С...')
    QApplication.processEvents()
    req = requests.get(API_URL + f"Catalog_СостоянияЗаказовНаПроизводство?&$format=json&$select=Ref_Key,Description", auth=(ODATA_USER, ODATA_PASS))
    out = req.json()['value']
    states = {}
    for state in out:
        states.update({state['Ref_Key']: state['Description']})
    db.write_properties(states)
    print('order states loaded!')


def get_meas_units(sp):
    sp.ui.splash_label.setText('Запись единиц измерения в DB...')
    QApplication.processEvents()
    req = requests.get(API_URL + f"Catalog_КлассификаторЕдиницИзмерения?&$format=json&$select=Ref_Key,Description", auth=(ODATA_USER, ODATA_PASS))
    out = req.json()['value']
    meas_units = {}
    for prop in out:
        meas_units.update({prop['Ref_Key']: prop['Description']})
    db.write_properties(meas_units)
    print('meas_units loaded!')


def get_picture(nom_image_guid='5b08318b-e061-11e5-80d7-cf56af1d0024'):
    req = requests.get(API_URL + f"Catalog_НоменклатураПрисоединенныеФайлы(guid'{nom_image_guid}')/?$format=json",
                       auth=(ODATA_USER, ODATA_PASS))
    print(req)
    out = req.json()
    correct_json = json.dumps(out, ensure_ascii=False, indent=2)
    with open("nom", "w") as file:
        file.write(str(correct_json))
    return correct_json


def get_property_owner(guid):
    req = requests.get(API_URL + f"Catalog_ДополнительныеРеквизитыНоменклатуры(guid'{guid}')?&$format=json", auth=(ODATA_USER, ODATA_PASS))
    print(req.text)
    out = req.json()
    return out


def get_properties_values(sp):
    sp.ui.splash_label.setText('Загрузка свойств из 1С...')
    QApplication.processEvents()
    with open('order_fields_guids.json', 'r') as file:
        owner_keys = json.load(file)
    valid_properties = {}
    for key in owner_keys.keys():
        req = requests.get(API_URL +
                           f"Catalog_ЗначенияСвойствОбъектов?&$filter=DeletionMark eq false and Owner_Key eq guid'{key}'&$format=json&$select=Ref_Key,Description",
                           auth=(ODATA_USER, ODATA_PASS))
        out = req.json()['value']
        for prop in out:
            valid_properties.update({prop['Ref_Key']: prop['Description']})
    valid_properties.update(owner_keys)
    sp.ui.splash_label.setText('Запись свойств в DB...')
    QApplication.processEvents()
    db.write_properties(valid_properties)
    print('properties written to DB!')


def set_order_state(order_guid, state=IN_WORK_STATE[1]):
    url = f"Document_ЗаказНаПроизводство(guid'{order_guid}')?$format=json"
    body = '{"СостояниеЗаказа_Key": "'+state+'"}'
    req = requests.patch(f'{API_URL}{url}', body.encode(encoding='utf-8'), auth=(ODATA_USER, ODATA_PASS))
    return req.status_code


def get_orders(sp):
    sp.ui.splash_label.setText('Загрузка заказов из 1С...')
    QApplication.processEvents()
    states = [IN_WORK_STATE[1], EXTRUSION_STATE[1], FLEX_STATE[1], SEAL_STATE[1]]
    orders_list = []
    for state in states:
        req = requests.get(API_URL + f"Document_ЗаказНаПроизводство?$filter=СостояниеЗаказа_Key eq guid'{state}' and DeletionMark ne true&$format=json&$select="
                                     f"Ref_Key,СостояниеЗаказа_Key,Number,Date,Комментарий,Старт,Финиш,Продукция", auth=(ODATA_USER, ODATA_PASS))
        out = req.json()['value']
        orders_list += out
    orders_to_db = []
    for order in orders_list:
        for pos in order['Продукция']:
            # формируем primary_key
            line_len = len(pos['LineNumber'])
            p_key = pos['Ref_Key']+PKEY_SEPARATOR+((PKEY_LINE_LENGHT-line_len)*'0')+pos['LineNumber']
            nom_req = requests.get(API_URL + f"Catalog_Номенклатура(guid'{pos['Номенклатура_Key']}')?&$format=json"
                                         f"&$select=Ref_Key,ФайлКартинки_Key,Description,Code,ЕдиницаИзмерения_Key,ДатаИзменения,ДополнительныеРеквизиты,НаименованиеПолное,"
                                         f"Комментарий", auth=(ODATA_USER, ODATA_PASS))
            nom_out = nom_req.json()
            nom_dict = dict()
            nom_dict.update(read_requisits(nom_out['ДополнительныеРеквизиты']))
            nom_dict.update({'name': nom_out['Description'], 'quantity': pos['Количество'], 'meas_unit': get_val(nom_out['ЕдиницаИзмерения_Key']), 'position_description':
                             nom_out['Комментарий'], 'ЕдиницаИзмерения_Key':nom_out['ЕдиницаИзмерения_Key']})
            nom_dict.update({'primary_key': p_key, 'Ref_Key': order['Ref_Key'], 'order_no': order['Number'], 'doc_date': order['Date'],
                             'order_description': order['Комментарий'], 'start': order['Старт'], 'finish': order['Финиш'],
                             'state': get_val(order['СостояниеЗаказа_Key'])})
            # pprint(nom_dict)
            orders_to_db.append(nom_dict)
    # pprint(orders_to_db)
    sp.ui.splash_label.setText('Запись заказов в DB...')
    QApplication.processEvents()
    db.write_orders_1s(orders_to_db)
    print('orders loaded!')
    return


def read_requisits(requisits):
    # TODO иногда возвращает числа строками =\
    out_dict = dict()
    for req in requisits:
        key = db.get_by_guid(req['Свойство_Key'])
        value = get_val(req['Значение']) if 'Значение' in req else db.get_by_guid(req['Значение_Key'])
        if value and key:
            out_dict.update({key: value})
    return out_dict


def get_nomenclature(sp):
    sp.ui.splash_label.setText('Загрузка номенклатуры из 1С...')
    QApplication.processEvents()
    req = requests.get(API_URL+f"Catalog_Номенклатура?$filter=КатегорияНоменклатуры_Key eq guid'{PROD_CAT_GUID}' and DeletionMark eq false&$format=json&"
                               f"$select=Ref_Key,ФайлКартинки_Key,Description,Code,ЕдиницаИзмерения_Key,ДатаИзменения,ДополнительныеРеквизиты,НаименованиеПолное,"
                               f"Комментарий", auth=(ODATA_USER, ODATA_PASS))
    out = req.json()['value']
    total_list = []
    for pos in out:
        nom_dict = dict()
        nom_dict.update(read_requisits(pos['ДополнительныеРеквизиты']))
        nom_dict.update({'Ref_Key': pos['Ref_Key'], 'ФайлКартинки_Key': pos['ФайлКартинки_Key'], 'name': pos['Description'],'Description': pos['Description'], 'Code': pos['Code'],
                     'ЕдиницаИзмерения_Key': pos['ЕдиницаИзмерения_Key'], 'ДатаИзменения': pos['ДатаИзменения'], 'НаименованиеПолное': pos['НаименованиеПолное'],
                     'Комментарий': pos['Комментарий'], 'meas_unit': db.get_by_guid(pos['ЕдиницаИзмерения_Key'])})
        total_list.append(nom_dict)
    sp.ui.splash_label.setText('Запись номенклатуры в DB...')
    QApplication.processEvents()
    db.write_nomenclature(total_list)
    print('nomenclature loaded!')

