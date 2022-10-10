class ODATAValueError(Exception):
    def __init__(self, args):
        print('Запрос в базу не возвратил value', f'\n{args}')