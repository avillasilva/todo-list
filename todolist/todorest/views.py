from django.contrib.auth.models import User
from django.http.response import Http404
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from .models import *


def register_user(request):
    if request.method == 'POST':
        user = User.objects.create_user(
            request['username'], request['email'], request['password'])
        user.save()
        return HttpResponse(user.id)
    else:
        return HttpResponse(status=400)


def create_list(request):
    tasklist = TaskList(owner=request.user, title=request['title'])
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


def create_task(request):
    tasklist = TaskList.objects.get(id=request['listId'])

    category = Category.objects.filter(title=request['category'])

    task = Task(ownerList=tasklist, title=request['title'], category=category,
                deadline=request['deadline'], description=request['description'])
    task.save()
    return HttpResponse(task.id)


def get_task(request):
    if request.get('listId'):
        return Task.objects.get(id=request['taskId'])
    else:
        return Task.objects.filter(ownerList=request['listId'])


def update_task(request):
    task = Task.objects.get(id=request['taskId'])

    task.category_id = request['categoryId']
    task.title = request['title']
    task.description = request['description']
    task.save()


def delete_task(request):
    return Task.objects.delete(id=request['taskId'])


def crud_task(request):
    if request.method == 'POST':
        return create_task(request)
    elif request.method == 'GET':
        return get_task(request)
    elif request.method == 'PUT':
        return update_task(request)
    elif request.method == 'DELETE':
        return delete_task(request)
    else:
        return HttpResponse(status=400)


def create_category(request):
    category = Category(owner=request.user,
                        title=request['title'], description=request['description'])
    category.save()
    return HttpResponse(category.id)


def get_category(request):
    if request.get('categoryId'):
        return Category.objects.get(id=request['categoryId'])
    else:
        return Category.objects.filter(owner=request['ownerId'])


def update_category(request):
    category = Category.objects.get(id=request['categoryId'])

    category.title = request['title']
    category.description = request['description']
    category.save()


def delete_category(request):
    return Category.objects.delete(id=request['categoryId'])


def crud_category(request):
    if request.method == 'POST':
        return create_category(request)
    elif request.method == 'GET':
        return get_category(request)
    elif request.method == 'PUT':
        return update_category(request)
    elif request.method == 'DELETE':
        return delete_category(request)
    else:
        return HttpResponse(status=400)
