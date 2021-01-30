"""
Три элемента, на которых держится структура организации проектов в Trello:

    доска (board),
    список (list), columns
    карточка (card).
"""

from dataclasses import dataclass, field
from os import environ
from typing import ClassVar, List
from urllib.parse import urljoin

import fire
import requests
from requests.exceptions import HTTPError

env = environ

AUTH_PARAMS = {
    "key": env["API_KEY"],
    "token": env["API_TOKEN"],
}

BOARD_ID = env["BOARD_ID"]


@dataclass
class Url:
    base: ClassVar[str] = "https://api.trello.com/1/"
    parts: List[str] = field(default_factory=list)

    def __str__(self):
        return urljoin(self.base, "/".join(self.parts))


class TrelloApi:
    def __init__(self, key, token, id_):
        """
        id - The ID of the board
        """
        self.key = key
        self.token = token
        self.AUTH_PARAMS = {
            "key": self.key,
            "token": self.token,
        }
        self.id_ = id_  # board ID

    def _get(self, url, query=None):
        if query:
            r = requests.get(url, params={**self.AUTH_PARAMS, **query})
        else:
            r = requests.get(url, params=self.AUTH_PARAMS)
        try:
            r.raise_for_status()
            res = r.json()
        except HTTPError as e:
            print(f"HTTP error occurred: {e}")
            raise Exception from e
        else:
            return res

    def _post(self, url, query):
        r = requests.post(url, data={**query, **self.AUTH_PARAMS})
        try:
            r.raise_for_status()
        except HTTPError as e:
            print(f"HTTP error occurred: {e}")
            raise Exception from e
        else:
            print(f"Статус - {r.status_code}")

    def _put(self, url, query):
        r = requests.put(url, data={**query, **self.AUTH_PARAMS})
        try:
            r.raise_for_status()
        except HTTPError as e:
            print(f"HTTP error occurred: {e}")
            raise Exception from e
        else:
            print(f"Статус - {r.status_code}")

    @property
    def id_board(self):
        """Get a field on a Board

        GET /1/boards/{id}/{field}
        """
        url = Url(["boards", self.id_])
        return self._get(url, query={"fields": "id"})["id"]

    def lists(self):  # columns
        """Get Lists on a Board

        GET /1/boards/{id}/lists
        id - The ID of the board
        """
        url = Url(["boards", self.id_, "lists"])
        return self._get(url)

    def new_list(self, name):
        """Create a new List on a Board

        POST /1/lists
        idBoard - id доски в полном формате
        """
        url = Url(["lists"])
        data = {"name": name, "idBoard": self.id_board}
        self._post(url, data)

    def cards(self, id_):
        """Get Cards in a List

        GET /1/lists/{id}/cards
        id - The ID of the list
        """
        url = Url(["lists", id_, "cards"])
        return self._get(url)

    def all_cards_board(self):
        """все карточки во всех листах доски"""
        for item in [self.cards(item["id"]) for item in self.lists()]:
            for i in item:
                yield i

    def new_card(self, name, id_):
        """Create a new Card

        POST /1/cards
        id_ = idList - The ID of the list the card should be created in
        """
        url = Url(["cards"])
        data = {"name": name, "idList": id_}
        self._post(url, data)

    def update_card(self, id_, data):
        """Update a Card

        PUT /1/cards/{id}
        id_ - The ID of the Card
        data - словарь с полями и значениями карточки которые нужно изменить
        """
        url = Url(["cards", id_])
        self._put(url, data)  # я передал значение idList через query


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
