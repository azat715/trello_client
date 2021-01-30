"""
попытался сделать тесты, но замокать весь API трелло сложно, поэтому как есть
"""
import pytest
from pytest_mock import mocker
from pathlib import Path

from trello_client.api import TrelloApi

AUTH_PARAMS = {
        "key": 123,
        "token": 456,
    }
BOARD_ID = 678

TEST_DATA_DIR = Path(__file__).resolve().parent / 'test_config'

api = TrelloApi(AUTH_PARAMS["key"], AUTH_PARAMS["token"], BOARD_ID)

def test_id_board(mocker):
    mocker.patch(
        'trello_client.api.TrelloApi._get',
        return_value={'id':'123fo'}
    )   
    assert api.id_board == '123fo'

@pytest.mark.datafiles(TEST_DATA_DIR)
def test_lists(mocker, datafiles):
    path = Path(datafiles, 'list.txt')
    mocker.patch(
        'trello_client.api.TrelloApi._get',
        return_value=path.read_text()
    )   
    assert api.lists() == path.read_text()
