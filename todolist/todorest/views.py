from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import *
import json
from datetime import datetime
from .serializers import *

def register_user(request):
    if request.method == 'POST':
        user = User.objects.create_user(request.POST['username'], 
                    request.POST['email'], 
                    request.POST['password'])
        user.save()
        return HttpResponse(user.id)
    else:
        return HttpResponse(status=400)

def login_user(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return HttpResponse('Logged in', status=200)
    else:
        return HttpResponse('Error', status=400)

def logout_user(request):
    print(request.encode('utf-8'))
    logout(request)
    return HttpResponse('Logged out')

######################## CRUD ###########################################

def create_list(request):
    data = json.loads(request.body.decode('utf-8'))
    try:
        user = User.objects.get(pk=data.get('user_id'))
        tasklist = TaskList(owner=user, title=data.get('title'))
        tasklist.save()
        return HttpResponse(tasklist)
    except User.DoesNotExist:
        return HttpResponse('user does not exist')

def get_lists(request):
    data = json.loads(request.body.decode('utf-8'))
    try:
        lists = TaskList.objects.filter(owner=data.get('user_id'))
        return HttpResponse(lists)
    except Exception as e:
        return HttpResponse(e)

def get_list(request, list_id):
    try:
        tasklist = TaskList.objects.get(pk=list_id)
        return HttpResponse(tasklist)
    except TaskList.DoesNotExist:
        return HttpResponse('tasklist does not exist')


def update_list(request, list_id):
    data = json.loads(request.body.decode('utf-8'))
    try:
        tasklist = TaskList.objects.get(pk=list_id)
        tasklist.title = data.get('new_title')
        tasklist.save()
        return HttpResponse('Title changed')
    except TaskList.DoesNotExist:
        return HttpResponse('tasklist does not exist')


def delete_list(request, list_id):
    try:
        TaskList.objects.get(pk=list_id).delete()
        return HttpResponse('tasklist deleted')
    except TaskList.DoesNotExist:
        return HttpResponse('tasklist not found')

@login_required
def create_or_get_lists(request):
    if request.method == 'POST':
        return create_list(request)
    elif request.method == 'GET':
        return get_lists(request)

@login_required
def crud_list(request, list_id):
    if request.method == 'GET':
        return get_list(request, list_id)
    elif request.method == 'PUT':
        return update_list(request, list_id)
    elif request.method == 'DELETE':
        return delete_list(request, list_id)
    else:
        return HttpResponse(status=400)


######################## CRUD TASK ###########################################

def create_task(request):
    data = json.loads(request.body.decode('utf-8'))
    try:
        tasklist = TaskList.objects.get(pk=data.get('list_id'))
        category = Category.objects.get(pk=data.get('category_id'))
        print(data)
        task = Task(ownerList=tasklist, title=data.get('title'), category=category, description=data.get('description'))
        task.deadline =  datetime.strptime(data.get('deadline'), "%Y-%m-%d")
        task.save()
        return HttpResponse(task.id)
    except Exception:
        return HttpResponse('Error')

# Make this method return all the tasks of an user
def get_tasks(request):
    try:
        tasks = Task.objects.all()
        return HttpResponse(tasks)
    except Exception:
        return HttpResponse('There is no tasks')

def get_task(request, task_id):
    data = json.loads(request.body.decode('utf-8'))
    if data.get('list_id'):
        return HttpResponse(Task.objects.filter(ownerList=data.get('list_id')))
    else:
        return HttpResponse(Task.objects.get(pk=task_id))


def update_task(request, task_id):
    data = json.loads(request.body.decode('utf-8'))
    try:
        task = Task.objects.get(pk=task_id)
        task.title = data.get('title')
        task.category_id = data.get('category_id')
        task.description = data.get('description')
        task.save()
        return HttpResponse(task.id)
    except Exception:
        return HttpResponse('Error')


def delete_task(request, task_id):
    try:
        Task.objects.get(pk=task_id).delete()
        return HttpResponse('Deleted')
    except Task.DoesNotExist:
        return HttpResponse('Error')

@login_required
def create_or_get_tasks(request):
    if request.method == 'POST':
        return create_task(request)
    elif request.method == 'GET':
        return get_tasks(request)

@login_required
def crud_task(request, task_id):
    if request.method == 'GET':
        return get_task(request, task_id)
    elif request.method == 'PUT':
        return update_task(request, task_id)
    elif request.method == 'DELETE':
        return delete_task(request, task_id)
    else:
        return HttpResponse(status=400)

######################## CRUD CATEGORY #########################################

def create_category(request):
    data = json.loads(request.body.decode('utf-8'))
    try:
        user = User.objects.get(pk=data.get('user_id'))
        category = Category(owner=user,
                            title=data.get('title'),
                            description=data.get('description'))
        category.save()
        return HttpResponse(category.title)
    except User.DoesNotExist:
        return HttpResponse('User does not exist')

def get_categories(request):
    data = json.loads(request.body.decode('utf-8'))
    try:
        categories = Category.objects.filter(owner=data.get('user_id'))
        return HttpResponse(categories)
    except Exception:
        return HttpResponse('Error')

def get_category(request, category_id):
    try:
        category = Category.objects.get(pk=category_id)
        return HttpResponse(category.title)
    except Category.DoesNotExist:
        return HttpResponse('category does not exist')

def update_category(request, category_id):
    data = json.loads(request.body.decode('utf-8'))
    try:
        category = Category.objects.get(pk=category_id)
        category.title = data.get('title')
        category.description = data.get('description')
        category.save()
        return HttpResponse(category.title)
    except Exception:
        return HttpResponse('Error')


def delete_category(request, category_id):
    try:
        Category.objects.get(pk=category_id).delete()
        return HttpResponse('Deleted')
    except Exception:
        return HttpResponse('Error')

@login_required
def create_or_get_categories(request):
    if request.method == 'POST':
        return create_category(request)
    elif request.method == 'GET':
        return get_categories(request)

@login_required
def crud_category(request, category_id):
    if request.method == 'GET':
        return get_category(request, category_id)
    elif request.method == 'PUT':
        return update_category(request, category_id)
    elif request.method == 'DELETE':
        return delete_category(request, category_id)
    else:
        return HttpResponse(status=400)
