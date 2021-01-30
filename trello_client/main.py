"""
Три элемента, на которых держится структура организации проектов в Trello:

    доска (board),
    список (list), columns
    карточка (card).
"""

from os import environ

import fire

from trello_client.api import TrelloApi

env = environ

AUTH_PARAMS = {
    "key": env["API_KEY"],
    "token": env["API_TOKEN"],
}

BOARD_ID = env["BOARD_ID"]

def read():
    """Печать списка задач"""
    api = TrelloApi(AUTH_PARAMS["key"], AUTH_PARAMS["token"], BOARD_ID)
    for list_ in api.lists():
        task_data = api.cards(list_["id"])
        print(f"{list_['name']}   Количество задач {len(task_data)}")
        if not task_data:
            print("\t" + "Нет задач!")
            continue
        for task in task_data:
            print("\t" + task["name"])


def crete_task(name, column_name):
    """Создание задачи

    name - имя карты задачи
    column_name - имя листа
    """
    api = TrelloApi(AUTH_PARAMS["key"], AUTH_PARAMS["token"], BOARD_ID)
    id_lists = list(filter(lambda x: x["name"] == column_name, api.lists()))
    if id_lists:
        api.new_card(name, id_lists[0]["id"])
    else:
        print(f"Error, колонка {column_name} не существует")


def crete_list(name):
    """Создание колонки

    name - имя колонки (list)
    """
    api = TrelloApi(AUTH_PARAMS["key"], AUTH_PARAMS["token"], BOARD_ID)
    api.new_list(name)


def move_task(task_name, column_name):
    """Перемещение карточки в колонку

    name - имя карты задачи
    column_name - имя листа куда надо переместить карту задачу
    """
    api = TrelloApi(AUTH_PARAMS["key"], AUTH_PARAMS["token"], BOARD_ID)

    id_tasks = list(filter(lambda x: x["name"] == task_name, api.all_cards_board()))
    if len(id_tasks) > 1:
        print("Уточните какую задачу перемещать")
        for count, item in enumerate(id_tasks, start=1):
            print(f"{count} - {item['id']}, {item['name']}")
        print("Введите номер задачи")
        while True:
            try:
                response = input()
                id_task = id_tasks[int(response) - 1]["id"]
            except (IndexError, ValueError):
                print("Невалидный номер")
            else:
                break
    elif len(id_tasks) == 1:
        id_task = id_tasks[0]["id"]
    else:
        print(f"Error, задача {task_name} не существует")

    id_lists = list(filter(lambda x: x["name"] == column_name, api.lists()))
    if len(id_lists) > 1:
        print("Уточните в какую list колонку перемещать задачу")
        for count, item in enumerate(id_lists, start=1):
            print(f"{count} - {item['id']}, {item['name']}")
        print("Введите номер list колонку")
        while True:
            try:
                response = input()
                id_list = id_lists[int(response) - 1]["id"]
            except (IndexError, ValueError):
                print("Невалидный номер")
            else:
                break
    elif len(id_lists) == 1:
        id_list = id_lists[0]["id"]
    else:
        print(f"Error, колонка {column_name} не существует")
        return None

    data = {"idList": id_list}
    api.update_card(id_task, data)


def cli():
    fire.Fire(
        {
            "read": read,
            "create_task": crete_task,
            "move": move_task,
            "create_colmn": crete_list,
        }
    )
