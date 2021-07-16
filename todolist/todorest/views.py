from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from todolist.util import token_or_cookie_required, generate_user_token
from .models import *
import json
from datetime import datetime
from .serializers import *

TOKEN_FIELD = 'TOKEN'

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
        return HttpResponse(TOKEN_FIELD + ':' + generate_user_token(user), status=200)
    else:
        return HttpResponse('Error', status=400)

def logout_user(request):
    logout(request)
    return HttpResponse('Logged out')

######################## CRUD ###########################################

def create_list(request):
    data = json.loads(request.body.decode('utf-8'))
    try:
        tasklist = TaskList(owner=request.user, title=data.get('title'))
        tasklist.save()
        return JsonResponse(tasklist_encoder(tasklist))
    except User.DoesNotExist:
        return HttpResponse('User does not exist', status=400)

def get_lists(request):
    try:
        lists = TaskList.objects.filter(owner=request.user)
        return JsonResponse([tasklist_encoder(l) for l in lists], safe=False)
    except Exception as e:
        return HttpResponse(str(e), status=400)

def get_list(request, list_id):
    try:
        tasklist = TaskList.objects.get(pk=list_id)
        
        if tasklist.owner.id != request.user.id:
            raise Exception('Not allowed')
        
        return JsonResponse(tasklist_encoder(tasklist))
    except TaskList.DoesNotExist:
        return HttpResponse('Tasklist does not exist', status=400)


def update_list(request, list_id):
    data = json.loads(request.body.decode('utf-8'))
    try:
        tasklist = TaskList.objects.get(pk=list_id)
        
        if tasklist.owner.id != request.user.id:
            raise Exception('Not allowed')
        
        tasklist.title = data.get('title')
        tasklist.save()
        return JsonResponse(tasklist_encoder(tasklist))
    except TaskList.DoesNotExist:
        return HttpResponse('Tasklist does not exist', status=400)


def delete_list(request, list_id):
    try:
        tasklist = TaskList.objects.get(pk=list_id)

        if tasklist.owner.id != request.user.id:
            raise Exception('Not allowed')

        tasklist.delete()
        return JsonResponse({ 'message': 'tasklist deleted' })
    except TaskList.DoesNotExist:
        return HttpResponse('Tasklist does not exist', status=400)

@token_or_cookie_required(token_field=TOKEN_FIELD)
def create_or_get_lists(request):
    if request.method == 'POST':
        return create_list(request)
    elif request.method == 'GET':
        return get_lists(request)

@token_or_cookie_required(token_field=TOKEN_FIELD)
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
        tasklist = TaskList.objects.get(pk=data.get('tasklist'))
        category = Category.objects.get(pk=data.get('category'))

        if tasklist.owner.id != request.user.id or category.owner.id != request.user.id:
            raise Exception('Not allowed')

        task = Task(ownerList=tasklist, title=data.get('title'), category=category, description=data.get('description'))
        task.deadline =  datetime.strptime(data.get('deadline'), "%Y-%m-%d")
        task.save()
        return JsonResponse(task_encoder(task), safe=False)
    except Exception as e:
        return HttpResponse(str(e), status=400)

def get_tasks(request):
    try:
        tasklists = TaskList.objects.filter(owner=request.user)
        tasks = []
        for tasklist in tasklists:
            for task in Task.objects.filter(ownerList=tasklist.id):
                tasks.append(task_encoder(task))
        
        return JsonResponse(tasks, safe=False)
    except Exception as e:
        return HttpResponse(str(e), status=400)

def get_task(request, task_id):
    try:
        task = Task.objects.get(pk=task_id)

        if task.ownerList.owner.id != request.user.id:
            raise Exception('Not allowed')
        
        return JsonResponse(task_encoder(task), safe=False)
    except Exception as e:
        return HttpResponse(str(e), status=400)


def update_task(request, task_id):
    data = json.loads(request.body.decode('utf-8'))
    try:
        tasklist = TaskList.objects.get(pk=data.get('list_id'))
        category = Category.objects.get(pk=data.get('category_id'))
        task = Task.objects.get(pk=task_id)

        if task.ownerList.owner.id != request.user.id or tasklist.owner.id != request.user.id or category.owner.id != request.user.id:
            raise Exception('Not allowed')

        task.ownerList = tasklist
        task.category = category
        task.title = data.get('title')
        task.description = data.get('description')
        task.finished = data.get('finished')
        task.save()
        return JsonResponse(task_encoder(task), safe=False)
    except Exception as e:
        return HttpResponse(str(e), status=400)


def delete_task(request, task_id):
    try:
        task = Task.objects.get(pk=task_id)

        if task.ownerList.owner.id != request.user.id:
            raise Exception('Not allowed')
        
        task.delete()
        return JsonResponse({ 'message': 'Task deleted' })
    except Task.DoesNotExist:
        return HttpResponse('Task does not exist', status=400)

@token_or_cookie_required(token_field=TOKEN_FIELD)
def create_or_get_tasks(request):
    if request.method == 'POST':
        return create_task(request)
    elif request.method == 'GET':
        return get_tasks(request)

@token_or_cookie_required(token_field=TOKEN_FIELD)
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
        user = User.objects.get(pk=request.user.id)
        category = Category(owner=user,
                            title=data.get('title'),
                            description=data.get('description'))
        category.save()
        return JsonResponse(category_encoder(category), safe=False)
    except User.DoesNotExist:
        return HttpResponse('User does not exist', status=400)

def get_categories(request):
    try:
        categories = Category.objects.filter(owner=request.user)
        return JsonResponse([category_encoder(c) for c in categories], safe=False)
    except Exception as e:
        return HttpResponse(str(e), status=400)

def get_category(request, category_id):
    try:
        category = Category.objects.get(pk=category_id)
        if category.owner.id != request.user.id:
            raise Exception('Not allowed')

        return JsonResponse(category_encoder(category), safe=False)
    except Category.DoesNotExist:
        return HttpResponse('category does not exist', status=400)

def update_category(request, category_id):
    data = json.loads(request.body.decode('utf-8'))
    try:
        category = Category.objects.get(pk=category_id)
        if category.owner.id != request.user.id:
            raise Exception('Not allowed')

        category.title = data.get('title')
        category.description = data.get('description')
        category.save()
        return JsonResponse(category_encoder(category), safe=False)
    except Exception as e:
        return HttpResponse(str(e), status=400)


def delete_category(request, category_id):
    try:
        category = Category.objects.get(pk=category_id)
        if category.owner.id != request.user.id:
            raise Exception('Not allowed')
        category.delete()
        return JsonResponse({ 'message': 'Category deleted' })
    except Exception as e:
        return HttpResponse(str(e), status=400)

@token_or_cookie_required(token_field=TOKEN_FIELD)
def create_or_get_categories(request):
    if request.method == 'POST':
        return create_category(request)
    elif request.method == 'GET':
        return get_categories(request)

@token_or_cookie_required(token_field=TOKEN_FIELD)
def crud_category(request, category_id):
    if request.method == 'GET':
        return get_category(request, category_id)
    elif request.method == 'PUT':
        return update_category(request, category_id)
    elif request.method == 'DELETE':
        return delete_category(request, category_id)
    else:
        return HttpResponse(status=400)
