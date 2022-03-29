#import testGlobalSettings as settings
import tests.testGlobalSettings as settings
import sys, os
from pathlib import Path

path = Path(__file__)
sys.path.insert(0, os.path.join(sys.path[0], path.parent.parent.absolute()))
from app import flask_app

flask_client = flask_app.test_client()
NON_EXISTANT_TAG = 'fhqwhgads'

error_string = {}
error_string['error'] = "Tags parameter is required"
    
# 1. missing argument tags=
def test_missing_value():
    response = flask_client.get('/api/posts?tags=')
    assert response.get_json() == error_string
    assert response.status_code == settings.ERROR_STATUS_CODE

# 2. missing entirely '', with other args
def test_missing_arg():
    response = flask_client.get('/api/posts?sortBy=id&direction=desc')
    assert response.get_json() == error_string
    assert response.status_code == settings.ERROR_STATUS_CODE

# 3. tag that does not exist (should return nothing (empty list))
def test_tag_not_exist():
    response = flask_client.get('/api/posts?tags=' + NON_EXISTANT_TAG)
    assert response.get_json() == []
    assert response.status_code == settings.SUCCESS_STATUS_CODE

# 4. correct parameter (tag=tech,health)
# no additional params
# Not a good test, relies on the data not changing, or knowing ahead of time what the number of results would be
#def test_correct_with_tags():
#    response = flask_client.get('api/posts?tags=tech,health')
#    assert len(response.get_json()) == settings.NUMBER_OF_TEST_POSTS
#    assert response.status_code == settings.SUCCESS_STATUS_CODE


