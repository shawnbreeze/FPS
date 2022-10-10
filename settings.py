# интерфейс
FUSION_THEME = True
DARK_THEME = True

# id ролей
PR_AREA = 0  # 0 - экструзия, 1 - флекс, 2 - склейка, 3 - ремонтная служба, 4 - ОТК, 5 - завсклад, 6 - нач. пр-ва, 7 - admin, 8 - зам. нач пр-ва

# состояния заказов
IN_WORK_STATE = ['В работе', 'ba0c30d7-cb14-11e5-a69e-00dbdf041cac']
EXTRUSION_STATE = ['Экструзия', '6d630288-dc54-11e5-80d7-cf56af1d0024']
GIVEN_STATE = ['Выдано сырье', '4ded9327-b2ff-11e6-80ef-a801d30ce59d']
FLEX_STATE = ['Флексография', '6d630289-dc54-11e5-80d7-cf56af1d0024']
SEAL_STATE = ['Склейка', '6d63028a-dc54-11e5-80d7-cf56af1d0024']
OPEN_STATE = ['Открыт', 'ba0c30d6-cb14-11e5-a69e-00dbdf041cac']
PERFORMED_STATE = ['Выполнен', 'ba0c30d8-cb14-11e5-a69e-00dbdf041cac']
COMPLETED_STATE = ['Отменен', 'a83b26ac-f2a0-11e6-80f1-d52a3d9b9e91']

# настройка допусков
MIN_RED = -5
MAX_RED = 5
MIN_YELLOW = (-4.9, -3)
MAX_YELLOW = (3, 4.9)
WASTE_CUTOFF_MIN = -15
WASTE_CUTOFF_MAX = 15

# процент на брак по умолчанию экструзия
WASTE_PERCENTAGE = 1.05

# списки вариантов экструзия
WASTE_REASONS_LIST = ['Брак при переходе', 'Запуск после замены сеток', 'Обрыв рукава', 'Сдув рукава', 'Выскочил боковой нож', 'Переход цвета', 'Брак по цвету/закрасу',
                      'Чешуя/гелики/пузырьки']
CONTROL_REASONS_LIST = ['Занижена толщина', 'Завышена толщина', 'Занижен размер', 'Завышен размер', 'Чешуя/гелики/пузырьки', 'Отклонения по цвету', 'Неровный рез ножа']
STOPPAGE_REASONS_LIST = ['Замена сетки А', 'Замена сетки В', 'Замена всех сеток', 'Замена дорна', 'Чистка обдува', 'Замена стабилизатора', 'Замена чулка',
                         'Обрыв рукава', 'Опустел бункер', 'Установка фальцующих щёк']

API_URL = 'http://127.0.0.1/1S/odata/standard.odata/'
ODATA_USER = 'kruger_'
ODATA_PASS = 'pass'

# GUID'S
PROD_CAT_GUID = '250637f8-d649-11e5-80d4-b898fac1a39d'

# 1C
CONNECT_1C = True
REFILL_NOMENCLATURE = False
REFILL_PROPERTIES = False
REFILL_ORDERS = False
REFILL_MEAS_UNITS = False
REFILL_STATES = False
##
# other
HIDE_ROLL_ID = False
PKEY_SEPARATOR = '_'
PKEY_LINE_LENGHT = 3

# TG bot
TG_BOT_URL = 'http://ovz2.9539986005.n50jp.vps.myjino.ru'

# рассылки
CONTROL_NOTIF_LIST = [490824260]
EXTR_SHIFT_OUT_NOTIF_LIST = [490824260]
WASTE_NOTIF_LIST = [490824260]

# служба ремонта
REPAIR_STATES = ['Создан', 'Просмотрен', 'Отложен', 'В работе', 'Выполнен']
REPAIR_AREAS = ['Экструзия', 'Флексография', 'Склейка', 'Компрессоры', 'Охлаждение', 'Цех']
REPAIR_PRIORITIES = ["Низкая", "Средняя", "Высокая"]
