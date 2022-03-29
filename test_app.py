import json

from app import flask_app



# check if list is sorted
#all(l[i] <= l[i+1] for i in range(len(l) - 1))



def test_direction_param():
    f = flask_app.test_client()
    response = f.get('api/posts')

    # tests for direction param
    # 1. missing argument direction= - return error
    # 2. missing entirely  - should default sort to asc
    # 3. incorrect value - return error
    # 4. correct
    # 5. error status code
    # 6. success status code

def test_ping():
    response_body = {}
    response_body['success'] = "true"
    f = flask_app.test_client()
    response = f.get('api/ping')

    # Tests with ping
    # 1. Post to ping - won't allow
    # 2. Server on - do we get the response we expect?
    # 3. Server off - do we get the correct response
    # 4. correct
    # 5. error status code
    # 6. success status code