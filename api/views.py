from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
import redis
import json


# Connect to REDIS server
redis_storage = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=0)


# Operations which Django doing, if you don`t use key in request
# (.../api/items)
@api_view(['GET', 'POST'])
def manage_items(request, *args, **kwargs):

    # POST request - if you want to create new row in REDIS storage
    if request.method == 'POST':
        item = json.loads(request.body)
        key = list(item.keys())[0]
        value = item[key]
        redis_storage.set(key, value)
        response = {'MESSAGE': f"{value} successfully set to {key}"}
        return Response(response, 201)

    # GET request - if you want to get list with all rows in REDIS storage
    elif request.method == 'GET':
        items = {}
        count = 0
        for key in redis_storage.keys("*"):
            items[key.decode("utf-8")] = redis_storage.get(key)
            count += 1
        response = {
            'count': count,
            'MESSAGE': f"Found {count} items.",
            'items': items
        }
        return Response(response, status=200)


# Operations which Django doing, if you use key in request
# (.../api/items/{key})
@api_view(['GET', 'PUT', 'DELETE'])
def manage_item(request, *args, **kwargs):

    # GET request - if you want to get value from REDIS for your key
    if request.method == 'GET':
        if kwargs['key']:
            value = redis_storage.get(kwargs['key'])
            if value:
                response = {
                    'key': kwargs['key'],
                    'value': value,
                    'msg': 'success'
                }
                return Response(response, status=200)
            else:
                response = {
                    'key': kwargs['key'],
                    'value': None,
                    'msg': 'Not found'
                }
                return Response(response, status=404)

    # PUT request - if you want to update value from REDIS for your key
    elif request.method == 'PUT':
        if kwargs['key']:
            request_data = json.loads(request.body)
            new_value = request_data['new_value']
            value = redis_storage.get(kwargs['key'])
            if value:
                redis_storage.set(kwargs['key'], new_value)
                response = {
                    'key': kwargs['key'],
                    'value': value,
                    'msg': f"Successfully updated {kwargs['key']}"
                }
                return Response(response, status=200)
            else:
                response = {
                    'key': kwargs['key'],
                    'value': None,
                    'msg': 'Not found'
                }
                return Response(response, status=404)

    # DELETE request - if you want to delete row with key from REDIS
    elif request.method == 'DELETE':
        if kwargs['key']:
            result = redis_storage.delete(kwargs['key'])
            if result == 1:
                response = {'MESSAGE': f"{kwargs['key']} successfully deleted"}
                return Response(response, status=204)
            else:
                response = {
                    'key': kwargs['key'],
                    'value': None,
                    'msg': 'Not found'
                }
                return Response(response, status=404)
