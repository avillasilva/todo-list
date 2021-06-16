from django.shortcuts import render
from .util import *

def register_user(request):
    return proxy_todolist(request, 'register')

def login_user(request):
    return proxy_todolist(request, 'login')

def logout_user(request):
    return proxy_todolist(request, 'logout')


def create_or_get_lists(request):
    if request.method == 'POST':
        return TaskList_Proxy.post(request, request.body)
    elif request.method == 'GET':
        return TaskList_Proxy.list(request)

def crud_list(request, list_id):
    list_id = str(list_id)
    if request.method == 'GET':
        return TaskList_Proxy.get(request, list_id)
    elif request.method == 'PUT':
        return TaskList_Proxy.put(request, list_id, request.body)
    elif request.method == 'DELETE':
        return TaskList_Proxy.delete(request, list_id)
    else:
        return HttpResponse(status=400)
