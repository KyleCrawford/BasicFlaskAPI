from flask import Flask, request, Response
import json

import aiohttp
import asyncio
from operator import itemgetter
import requests_cache

CACHE_EXPIRE_TIME = 180

flask_app = Flask(__name__)

requests_cache.install_cache('temp_cache', expire_after=CACHE_EXPIRE_TIME)

# ping route to check connection
# returns success: true if connection successful
@flask_app.route("/api/ping", methods=['GET'])
def ping():
    response_body = {}
    response_body['success'] = "true"
    return Response(json.dumps(response_body), status=200, mimetype='application/json')

# ensures the passed parameters are valid for our application
# returns tuple (tags, soryBy, direction)
def parseQueryString(tags, sortBy, direction):
        # parse query string args
    return_tags = ''
    return_sortBy = ''
    return_direction = ''

    if tags is None or tags == '':
        raise ValueError('tags')
    else :
        tags = tags.split(',')
        return_tags = tags
    
    if (sortBy is None):
        return_sortBy = 'id'
    elif (type(sortBy) is not str):
        raise ValueError('sortBy')
    elif sortBy == 'id':
        return_sortBy = 'id'
    elif sortBy == 'reads':
        return_sortBy = 'reads'
    elif sortBy == 'likes':
        return_sortBy = 'likes'
    elif sortBy == 'popularity':
        return_sortBy = 'popularity'
    else :
        raise ValueError('sortBy')

    if (direction == None):
        # this parameter is optional, default is False (asc)
        return_direction = False
    elif (type(direction) is not str):
        raise ValueError('direction')
    elif str.lower(direction) == 'asc':
        # False, as this will be the isReverse bool for the sort
        return_direction = False
    elif str.lower(direction) == 'desc':
        # True, as this will be the isReverse bool for the sort
        return_direction = True
    else :
        raise ValueError('direction')

    return (return_tags, return_sortBy, return_direction)
    
# single fetch, meant to be used by fetch_all
async def fetch(session, url):
    async with session.get(url) as response:
        return await response.json()

# perform multiple async http calls
async def fetch_all(urls, loop):
    async with aiohttp.ClientSession(loop=loop) as session:
        results = await asyncio.gather(*[fetch(session, url) for url in urls], return_exceptions=True)
        return results

# This route will display the results matching the query string parameters
# tags - the filter to select which data to display
# sortBy - the paramter to sort the data by
# direction - ascending or descending sort
@flask_app.route("/api/posts", methods=['GET'])
def getPosts():
    tags = request.args.get('tags')             # get the tags from the query string
    sortBy = request.args.get('sortBy')         # get sortBy from query string
    direction = request.args.get('direction')   # get direction from query string

    final_list = []     # list used to hold final values
    query_string = ()   # holds the tuple of the query string parameters

    id_list = []            # used to keep track of the id of the item to prevent adding duplicates to our list
    post_dict = {}          # used to hold the post entries as we go through the responses
    post_dict['posts'] = []
    urls = []               # used to hold the urls we will be requesting from

    # parse the query string, returns errors if there is an issue with a parameter
    try:
        query_string = parseQueryString(tags, sortBy, direction)
    except ValueError as err:
        error_string = {}
        if 'tags' in err.args:
            error_string['error'] = "Tags parameter is required"
        elif 'sortBy' in err.args:
            error_string['error'] = "sortBy parameter is invalid"
        elif 'direction' in err.args:
            error_string['error'] = "direction parameter is invalid"
        else:
            error_string['error'] = "An unknown error has occured with " + err.args[0]
        
        if (len(error_string) > 0):
            return Response(json.dumps(error_string), 400, mimetype='application/json')

    tags, sortBy, direction = query_string
    
    #changing to add a new event loop as Flask acts a bit weird otherwise
    #loop = asyncio.get_event_loop()
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    for tag in tags:
        urls.append('https://api.hatchways.io/assessment/blog/posts?tag=' + tag)
    responses = loop.run_until_complete(fetch_all(urls, loop))

    # loops through the list of responses and combines all the results into one list of dictionaries
    for dict_list in responses:
        # now we are dealing with the dictionaries
        for post in dict_list['posts']:
            if post['id'] not in id_list:
                # this post has not been added yet
                post_dict['posts'].append(post)
                id_list.append(post['id'])

    # the final sort
    final_list = sorted(post_dict['posts'], key=itemgetter(sortBy), reverse=direction)

    return Response(json.dumps(final_list), 200, mimetype='application/json')
