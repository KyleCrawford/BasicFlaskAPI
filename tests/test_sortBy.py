#import testGlobalSettings as settings
import tests.testGlobalSettings as settings
import sys, os
from pathlib import Path

from utils import utility

path = Path(__file__)
sys.path.insert(0, os.path.join(sys.path[0], path.parent.parent.absolute()))
from app import flask_app

flask_client = flask_app.test_client()

WRONG_SORT_CATEGORY = 'name'

error_string = {}
error_string['error'] = "sortBy parameter is invalid"

def test_missing_value():
    # 1. missing argument sortBy= - return error
    response = flask_client.get('/api/posts?tags='+ settings.DEFAULT_TAG +'&sortBy=')
    assert response.get_json() == error_string
    assert response.status_code == settings.ERROR_STATUS_CODE

# 2. missing entirely  - should default sort by id
def test_missing_arg():
    response = flask_client.get('/api/posts?tags=tech')
    assert (utility.list_of_dict_issorted_by_key(response.get_json(), settings.DEFAULT_SORT_CATEGORY))
    assert response.status_code == settings.SUCCESS_STATUS_CODE

# 3. not correct field to sort by - return error
def test_incorrect_sortBy():
    response = flask_client.get('/api/posts?tags=tech&sortBy=' + WRONG_SORT_CATEGORY)
    assert response.get_json() == error_string
    assert response.status_code == 400

def test_sortBy_id():
    response = flask_client.get('/api/posts?tags=tech&sortBy=id')
    assert utility.list_of_dict_issorted_by_key(response.get_json(), 'id')

def test_sortBy_reads():
    response = flask_client.get('/api/posts?tags=tech&sortBy=reads')
    assert utility.list_of_dict_issorted_by_key(response.get_json(), 'reads')

def test_sortBy_likes():
    response = flask_client.get('/api/posts?tags=tech&sortBy=likes')
    assert utility.list_of_dict_issorted_by_key(response.get_json(), 'likes')

def test_sortBy_popularity():
    response = flask_client.get('/api/posts?tags=tech&sortBy=popularity')
    assert utility.list_of_dict_issorted_by_key(response.get_json(), 'popularity')

