######
from operator import itemgetter
from flask import Flask, request, Response
import json
import requests

import aiohttp
import asyncio
import ssl

async def fetch(session, url):
    async with session.get(url, ssl=ssl.SSLContext()) as response:
        return await response.json()


async def fetch_all(urls, loop):
    async with aiohttp.ClientSession(loop=loop) as session:
        results = await asyncio.gather(*[fetch(session, url) for url in urls], return_exceptions=True)
        return results

##############
loop = asyncio.get_event_loop()
tag_list = []
urls = []
tag_list.append('tech')
tag_list.append('health')
for tag in tag_list:
    urls.append('https://api.hatchways.io/assessment/blog/posts?tag=' + tag)
list_dict = loop.run_until_complete(fetch_all(urls, loop))

id_list = []
post_dict = {}
post_dict['posts'] = []

for dict_list in list_dict:
    # now we are dealing with the dictionaries
    for post in dict_list['posts']:
        if post['id'] not in id_list:
            # this post has not been added yet
            post_dict['posts'].append(post)
            id_list.append(post['id'])

print("here we go")

print(post_dict['posts'])

print(str(type(post_dict)))
print(str(type(post_dict['posts'])))
print(str(type(post_dict['posts'][0])))

k = 'id'

test = all(post_dict['posts'][i][k] <= post_dict['posts'][i+1][k] for i in range(len(post_dict['posts']) - 1))


import utils.utility as util

print("this is the test")
print(test)
print(util.list_of_dict_issorted_by_key(post_dict['posts'], 'id'))
#for post in post_dict['posts']:
#    print(post)

# sort zat beetch
new_list = []
new_list = sorted(post_dict['posts'], key=itemgetter('id'))

test = all(new_list[i][k] <= new_list[i+1][k] for i in range(len(new_list) - 1))
print("this is the FINAL test")
print(test)
print(util.list_of_dict_issorted_by_key(new_list, 'id'))

def gonnaError():
    raise ValueError('one', 'more', 'lots more')


def return_tuple():
    a_string = "hello chicken"
    a_list = ["two", "values"]
    a_bool = True

    return (a_string, a_list, a_bool)


def working_thing():

    return_tuple()

    test_tuple = return_tuple()

    test_string, test_list, test_bool = test_tuple

    print(test_tuple)
    print('the amazong jerry')
    print(test_string)
    print(test_bool)
    print(test_list)