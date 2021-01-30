from dataclasses import dataclass, field
from typing import ClassVar, List
from urllib.parse import urljoin

import requests
from requests.exceptions import HTTPError


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