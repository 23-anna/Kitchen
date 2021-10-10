from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import requests
from django.views.decorators.csrf import csrf_exempt
import time
import random
import json
import threading
from threading import Thread
from operator import itemgetter
from colorama import init
from colorama import Fore, Back, Style
init()
# import thread
simulation_speed = 0.01

foods = [{
"id": 1,
"name": "pizza",
"preparation-time": 20 ,
"complexity": 2 ,
"cooking-apparatus": "oven"
},
 {
"id": 2,
"name": "salad",
"preparation-time": 10 ,
"complexity": 1 ,
"cooking-apparatus": "null"
},
{
"id": 3,
"name": "zeama",
"preparation-time": 7 ,
"complexity": 1 ,
"cooking-apparatus": "stove"
},
{
"id": 4,
"name": "Scallop Sashimi with Meyer Lemon Confit",
"preparation-time": 32 ,
"complexity": 3 ,
"cooking-apparatus": "null"
},
{
"id": 5,
"name": "Island Duck with Mulberry Mustard",
"preparation-time": 35 ,
"complexity": 3 ,
"cooking-apparatus": "oven"
},
{
"id": 6,
"name": "Waffles",
"preparation-time": 10 ,
"complexity": 1 ,
"cooking-apparatus": "stove"
},
{
"id": 7,
"name": "Aubergine",
"preparation-time": 20 ,
"complexity": 2 ,
"cooking-apparatus": "null"
},
{
"id": 8,
"name": "Lasagna",
"preparation-time": 30 ,
"complexity": 2 ,
"cooking-apparatus": "oven"
},
{
"id": 9,
"name": "Burger",
"preparation-time": 15 ,
"complexity": 1 ,
"cooking-apparatus": "oven"
},
{
"id": 10,
"name": "Gyros",
"preparation-time": 15 ,
"complexity": 1 ,
"cooking-apparatus": "null"
}]

cooks = [
{'rank': 1, 'proficiency': 1, 'name': 'Jessie Pinkman', 'catch_phrase': "Yo, yo, yo! 1-4-8-3 to the 3 to the 6 to the 9. representin' the ABQ. What up, Biatch? Leave at the tone."},
{'rank': 2, 'proficiency': 2, 'name': 'Pudge', 'catch_phrase': 'Fresh meat! Fresh meat!'},
{'rank': 3, 'proficiency': 3, 'name': 'The Duke', 'catch_phrase': 'I have been waiting for you, Mister Winters.'},
{'rank': 3, 'proficiency': 4, 'name': 'The Cook', 'catch_phrase': 'Повар спрашивает повара...'}
]


order_list = []

# @csrf_exempt
# def index(request):
#     dishes = []
#     total_dishes = []
#
#     items = requests.get('http://127.0.0.1:8000/dinning/')
#     tables = requests.get('http://127.0.0.1:8000/dinning/tables/')
#     print('TABLES: ', tables.text)
#
#     [dishes.append(item) for item in items.text if item.isnumeric()]
#
#     for dish in dishes:
#         preparation_time = foods[int(dish)]["preparation-time"]
#         dish_name = foods[int(dish)]["name"]
#         total_dishes.append(dish_name)
#
#         for i in range (1, preparation_time+1):
#             print("{} second(s) remaining...".format(preparation_time - i))
#             time.sleep(simulation_speed)
#
#     return HttpResponse('Order is ready! Dishes: {}'.format(total_dishes))
def check_priority(order):
    global order_list
    print('Order List', order_list)

    order_list.append(order)

    order_list = sorted(order_list, key=itemgetter('priority'), reverse=True)
    print(order_list, end='\n')
    print(len(order_list))


def cook(name, rank, proficiency, dishes):
    dishes_in_progress = dishes
    cook_rank = rank
    cook_proficiency = proficiency
    cook_name = name

    if (dishes_in_progress < proficiency):
        dishes_in_progress += 1
        result = search_dish(cook_rank)
        dish_id = result[0]
        ready = result[1]
        item  = result[2]
        if (dish_id != 0):
            cooking(dish_id)
        if  (ready == 1):
            headers = {'Content-Type' : 'application/json'}
            res = {'order_id': item, 'status' : 'ready'}
            order_list.remove(item)
            response = requests.post('http://127.0.0.2:8000/kitchen/', data=json.dumps(res), headers = headers)
        dishes_in_progress -= 1

def search_dish(rank):
    dish_id = 0
    dish_complexity = 0
    item = 0
    ready = 0

    while (dish_id == 0):
        for i in order_list[item]['items']:
            for f in foods:
                if (i == foods['id']):
                    dish_complexity = foods['complexity']
                    if (dish_complexity == cook_rank):
                        dish_id = i
                        order_list[item]['items'].remove(i)
                        if len(order_list[item]['items']) == 0:
                            ready = 1
                        break
        item +=1

    return [dish_id, ready, item]

def cooking(dish_id):
    preparation_time = 0

    for f in foods:
        if (dish_id == foods['id']):
            preparation_time = foods[f]['preparation-time']
            break

    time.sleep(preparation_time)



@csrf_exempt
def index(request):
    # request = requests.get('http://127.0.0.1:8000/dinning/waiter/')
    if request.method == 'POST':
        # new_json = requests.get('http://127.0.0.1:8000/dinning/waiter/').json()
        print(Fore.RED + '++++++++++++POST+++++++++++++' + Style.RESET_ALL)
        # print('++++++++++++POST+++++++++++++')
        received_order = json.loads(request.body.decode("utf-8"))
        print(received_order)

        check_priority(received_order)

        cook1 = threading.Thread(target=cook, name=cooks[0]['name'], args=(cooks[0]['name'], cooks[0]['rank'], cooks[0]['proficiency'], 0, ))
        cook1.start()

        cook2 = threading.Thread(target=cook, name=cooks[1]['name'], args=(cooks[1]['name'], cooks[1]['rank'], cooks[1]['proficiency'], 0, ))
        cook2.start()

        cook3 = threading.Thread(target=cook, name=cooks[2]['name'], args=(cooks[2]['name'], cooks[2]['rank'], cooks[2]['proficiency'], 0, ))
        cook3.start()

        cook4 = threading.Thread(target=cook, name=cooks[3]['name'], args=(cooks[3]['name'], cooks[3]['rank'], cooks[3]['proficiency'], 0, ))
        cook4.start()

    # info = requests.get('http://127.0.0.1:8000/dinning/')
    # print(info.text)
    # check_priority()
    # print('ORDER', info)
    # order_contents = requests.get('http://127.0.0.1:8000/dinning/waiter/')
    # print(order_contents.text)

    # headers = {'Content-Type' : 'application/json'}
    # response = requests.post('http://127.0.0.1:8000/dinning/', headers = headers, data = info)

    return HttpResponse('Order is ready! {}'.format('1'))
