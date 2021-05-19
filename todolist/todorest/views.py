from django.contrib.auth.models import User
from django.http.response import Http404
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from .models import *

def register_user(request):
    if request.method == 'POST':
        user = User.objects.create_user(request['username'], request['email'], request['password'])
        user.save()
        return HttpResponse(user.id)
    else:
        return HttpResponse(status=400)

def create_list(request):
    tasklist = TaskList(owner = request.user , title = request['title'])
    tasklist.save()
    return HttpResponse(tasklist.id)

def get_list(request):
    if request.get('listId'):
        return TaskList.objects.get(id=request['listId'])
    else:    
        return TaskList.objects.filter(owner=request.user)
    
def update_list(request):
    tasklist = TaskList.objects.get(id=request['listId'])
    tasklist.title = request['title']
    tasklist.save()

def delete_list(request):
    return TaskList.objects.delete(id=request['listId'])

def crud_list(request):
    if request.method == 'POST':
        return create_list(request)
    elif request.method == 'GET':
        return get_list(request)
    elif request.method == 'PUT':
        return update_list(request)
    elif request.method == 'DELETE':
        return delete_list(request)
    else:
        return HttpResponse(status=400)