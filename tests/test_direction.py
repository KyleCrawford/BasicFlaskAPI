#import testGlobalSettings as settings
import tests.testGlobalSettings as settings
import sys, os
from pathlib import Path

from utils import utility

path = Path(__file__)
sys.path.insert(0, os.path.join(sys.path[0], path.parent.parent.absolute()))
from app import flask_app

flask_client = flask_app.test_client()

INCORRECT_DIRECTION = 'notASCorDESC'
error_string = {}
error_string['error'] = "direction parameter is invalid"

# direction=
def test_missing_value():
    response = flask_client.get('/api/posts?tags='+ settings.DEFAULT_TAG +'&sortBy=id&direction=')
    assert response.get_json() == error_string
    assert response.status_code == settings.ERROR_STATUS_CODE

def test_missing_arg():
    response = flask_client.get('/api/posts?tags='+ settings.DEFAULT_TAG +'&sortBy=id')
    assert (utility.list_of_dict_issorted_by_key(response.get_json(), settings.DEFAULT_SORT_CATEGORY))
    assert response.status_code == settings.SUCCESS_STATUS_CODE
    

def test_direction_not_exist():
    response = flask_client.get('/api/posts?tags=tech&sortBy=' + settings.DEFAULT_SORT_CATEGORY + '&direction=' + INCORRECT_DIRECTION)
    assert response.get_json() == error_string
    assert response.status_code == settings.ERROR_STATUS_CODE


def test_asc():
    response = flask_client.get('/api/posts?tags='+ settings.DEFAULT_TAG +'&sortBy=' + settings.DEFAULT_SORT_CATEGORY + '&direction=asc')
    assert (utility.list_of_dict_issorted_by_key(response.get_json(), settings.DEFAULT_SORT_CATEGORY))
    assert response.status_code == settings.SUCCESS_STATUS_CODE

def test_desc():
    response = flask_client.get('/api/posts?tags='+ settings.DEFAULT_TAG +'&sortBy=' + settings.DEFAULT_SORT_CATEGORY + '&direction=desc')
    assert (utility.list_of_dict_issorted_by_key_reverse(response.get_json(), settings.DEFAULT_SORT_CATEGORY))
    assert response.status_code == settings.SUCCESS_STATUS_CODE
