import requests
from requests.exceptions import HTTPError
from urllib.parse import urljoin
from dataclasses import dataclass, field
from typing import ClassVar, List, NewType, Dict

# import re

AUTH_PARAMS = {
    "key": "16c6feac886fc425a8b0c295d99f63da",
    "token": "cfd7d28ef21413d51a486c88368375db8214a3e19f56237ef7cdbb03963c82b6",
}

BASE_UrlGet = "https://api.trello.com/1/"

BOARD_ID = "jmHbTyYV"


@dataclass
class Url:
    base: ClassVar[str] = "https://api.trello.com/1/"
    parts: List[str] = field(default_factory=list)

    def __str__(self):
        return urljoin(self.base, "/".join(self.parts))

class TrelloApi:
    def __init__(self, key, token):
        self.key = key
        self.token = token
        self.AUTH_PARAMS = {
            "key": self.key,
            "token": self.token,
        }

    def _get(self, url):
        r = requests.get(url, params=self.AUTH_PARAMS)
        try:
            r.raise_for_status()
            return r.json()
        except HTTPError as e:
            print(f"HTTP error occurred: {e}")
            raise Exception

    def _post(self, url, query):
        r = requests.post(url, data={**query, **self.AUTH_PARAMS})
        try:
            r.raise_for_status()
        except HTTPError as e:
            print(f"HTTP error occurred: {e}")
            raise Exception
    
    @staticmethod
    def _get_id_by_name(name, items):
        """
        name - имя листа в доске
        id - id
        items -
        """
        for item in items:
            if item["name"] == name:
                return item["id"]

    def lists(self, id):
        """
        GET /1/boards/{id}/lists
        id - The ID of the board
        """
        url = Url(["boards", id, "lists"])
        return self._get(url)

    def cards(self, id):
        """
        Get Cards in a List
        GET /1/lists/{id}/cards
        id - The ID of the list
        """
        url = Url(["lists", id, "cards"])
        return self._get(url)

    def all_cards(self, id):
        """
        все задачи во всех листах доски
        id - The ID of the board
        """
        res = []
        for item in self.lists(id):
            res.append(self.cards(item["id"]))
        return res

    def move(self, target, dest, id):
        """
        перемещение задачи между листами в опеределенной доске
        """
        target_id = self._get_id_by_name(target, self.all_cards())
        dest_id = self._get_id_by_name(dest, self.lists(id))

    def new_card(self, name, idList):
        """
        Create a new Card
        POST /1/cards
        idList - The ID of the list the card should be created in
        """
        url = Url(["cards"])
        data = {"name": name, "idList": idList}
        self._post(url, data)

def read():
    api = TrelloApi(AUTH_PARAMS["key"], AUTH_PARAMS["token"])
    for list_ in api.lists(BOARD_ID):
        print(list_["name"])
        task_data = api.cards(list_["id"])
        if not task_data:
            print("\t" + "Нет задач!")
            continue
        for task in task_data:
            print("\t" + task["name"])


def crete_task(name, column_name):
    """
    name - имя карты задачи
    column_name - имя листа 
    """
    idList = api._get_id_by_name(column_name, api.lists(BOARD_ID))
    api = TrelloApi(AUTH_PARAMS["key"], AUTH_PARAMS["token"])
    api.new_card(name, idList)

def move_task(name, column_name):
    """
    name - имя карты задачи
    column_name - имя листа куда надо переместить карту задачу
    """
    api = TrelloApi(AUTH_PARAMS["key"], AUTH_PARAMS["token"])
    column_data = api.lists(BOARD_ID)
    for column in column_data:
        column_tasks = api.cards(column['id'])





def search_id():
    api = TrelloApi(AUTH_PARAMS["key"], AUTH_PARAMS["token"])
    print(api._get_id_by_name("Нужно сделать", api.lists(BOARD_ID)))




if __name__ == '__main__':
    


# crete_task("задача1", "600484d1bfce4d7a447018ff")
# read()
# api = TrelloApi(AUTH_PARAMS["key"], AUTH_PARAMS["token"])
# print(api.lists(BOARD_ID))
# search_id()
crete_task("sdsds", "600484d1bfce4d7a447018ff")
