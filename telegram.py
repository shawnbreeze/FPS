import db
from settings import *
import requests
from datetime import datetime
## from pprint import pprint


def control_notification(roll_id):
    roll = db.get_roll_info(roll_id)
    text = f'<b><i>Отметка доп. контроль</i></b>\n' \
           f'<code>Рулон № {roll["roll_id"]}  {roll["weight"]} кг  {roll["lenght"]} м\n' \
           f'Заказ № {roll["order_no"]}\n' \
           f'{roll["position"]}\n' \
           f'{roll["comment"]}</code>'
    for user in CONTROL_NOTIF_LIST:
        req_text = TG_BOT_URL+f'/send-message?chat_id={user}&text={text}'
        req = requests.get(req_text)
        code = req.status_code


def waste_notification(roll_id):
    roll = db.get_roll_info(roll_id)
    text = f'<b><i>Брак></i></b>\n' \
           f'<code>Рулон № {roll["roll_id"]}  {roll["weight"]} кг  {roll["lenght"]} м\n' \
           f'Заказ № {roll["order_no"]}\n' \
           f'{roll["position"]}\n' \
           f'{roll["comment"]}</code>'
    for user in CONTROL_NOTIF_LIST:
        req_text = TG_BOT_URL+f'/send-message?chat_id={user}&text={text}'
        req = requests.get(req_text)
        code = req.status_code


def extr_shift_output_notification(shift_id):
    shift = db.extr_get_shift_info(shift_id)
    start_time = datetime.strptime(shift["start_time"], "%Y-%m-%d %H:%M:%S")
    end_time = datetime.strptime(shift["end_time"], "%Y-%m-%d %H:%M:%S")
    duration = (end_time - start_time)
    text = f'<b><i>Итоги смены участка "Экструзия"</i></b>\n' \
           f'<code>Оператор {db.get_user_name_by_id(shift["worker_id"])}\n' \
           f'Старт {start_time.strftime("%d.%m %H:%M")}\n' \
           f'Финиш {end_time.strftime("%d.%m %H:%M")}\n' \
           f'Длительность {int(duration.total_seconds()//3600)}ч {int((duration.total_seconds()//60)%60)}мин\n\n' \
           f'Выработка:\n'
    plan_prod = 0
    for extr in db.get_extruders():
        name = extr[1]
        extr_id = extr[0]
        in_repair = extr[10]
        avg_prod = extr[9]
        plan_prod += avg_prod if not in_repair else 0
        weight = shift[extr_id]["weight"]
        weight = 0 if weight is None else round(weight, 2)
        waste = shift[extr_id]["waste"]
        waste = f', брак {round(shift[extr_id]["waste"], 2)}' if waste else ''
        scrap = shift[extr_id]["scrap"]
        scrap = f', облой {round(shift[extr_id]["scrap"], 2)}' if scrap else ''
        edge = shift[extr_id]["edge"]
        edge = f', кромка {round(shift[extr_id]["edge"], 2)}' if edge else ''
        text += f'{name}: в ремонте\n' if in_repair else f'{name}: {weight} кг{waste}{scrap}{edge}\n'
    waste_scrap = shift["waste"] + shift["scrap"]
    waste_scrap = float(waste_scrap) if waste_scrap != '' else 0
    plan_prod = plan_prod*(duration.total_seconds()/3600)
    output = round(float(shift["shift_output"]), 2) # if shift["shift_output"] != '' else 0
    text += f'\nИтого: {output} кг\n'
    text += f'Переходы: {shift["readjustments"] if shift["readjustments"] else "нет"}\n'
    total_out = output+waste_scrap if output+waste_scrap > 0 else 1
    text += f'Брак: {round(waste_scrap, 2)} кг ({round((waste_scrap/total_out)*100, 2)}%)\n'
    text += f'Простои: {shift["idle_time"] if shift["idle_time"] else "нет"}\n'
    text += f'Эффективность: {int((output/plan_prod)*100)} %'
    text += '</code>'
    for user in EXTR_SHIFT_OUT_NOTIF_LIST:
        req_text = TG_BOT_URL+f'/send-message?chat_id={user}&text={text}'
        req = requests.get(req_text)
        code = req.status_code
