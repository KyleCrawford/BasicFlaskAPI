from operator import itemgetter
from flask import Flask, request, Response
import json
import requests

import aiohttp
import asyncio

tag_list = []
tag_list.append('tech')
tag_list.append('health')

response_list = []

# This works, No Touchy (replaced by async method)
#for tag in tag_list:
#    response_list.append(requests.get('https://api.hatchways.io/assessment/blog/posts?tag=' + tag))

async def funcNow(tags):
    async with aiohttp.ClientSession() as session:
        for tag in tags:
            url = 'https://api.hatchways.io/assessment/blog/posts?tag=' + tag
            async with session.get(url) as resp:
                results = await resp.json()
                return results

loop = asyncio.get_event_loop()
urls = ''
response_list.append(loop.run_until_complete(funcNow(tag_list)))

response_list.append(asyncio.run(funcNow(tag_list)))


# this is done automatically for me now.... (in the other file)
post_list = []
for res in response_list:
    post_list.append(res) # res.json() #changed with async


# I now need all this stuff
id_list = []
post_dict = {}
post_dict['posts'] = []

for dict_list in post_list:
    # now we are dealing with the dictionaries
    for post in dict_list['posts']:
        if post['id'] not in id_list:
            # this post has not been added yet
            post_dict['posts'].append(post)
            id_list.append(post['id'])

print(post_list)

print(len(post_list))
print(len(post_dict['posts']))
print(post_dict['posts'])
print(id_list)



# now we sort that beezitch

new_list = []
new_list = sorted(post_dict['posts'], key=itemgetter('id'))

print("yar har fiddle de dee")
print(new_list)



def oldStuff():
    test_dict = {}
    test_list = []
    id_list = []

    dict_two = {}
    new_dict = {}

    response = requests.get('https://api.hatchways.io/assessment/blog/posts?tag=tech')
    test_list.append(response)

    response = requests.get('https://api.hatchways.io/assessment/blog/posts?tag=health')
    test_list.append(response)

    test_dict = test_list[0].json()

    dict_two = test_list[1].json()





    print(len(test_dict['posts']))
    print(len(dict_two['posts']))
    print("work time")
    for post in dict_two['posts']:
        # check if our current id exists in the list
        if post['id'] not in id_list:
            # we can add ourselves to the new dictionary
            test_dict['posts'].append(post)
            id_list.append(post['id'])

    #print(test_dict['posts'][0]['id'])
    print(len(test_dict['posts']))
    print(test_dict)
    print("it's a living")
    print(id_list)





####### Below here is not nesessarily good
def holdMe(test_dict, dict_two, response):

    test_dict.update(dict_two)

    print(type(test_dict))
    print(type(dict_two))

    print(len(test_dict['posts']))

    print (response.json()['posts'][0])