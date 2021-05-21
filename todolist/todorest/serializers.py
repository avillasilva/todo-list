from .models import *

def tasklist_encoder(tasklist):
    return { 'id': tasklist.id, 'title': tasklist.title, 'owner': tasklist.owner.username }

def category_encoder(category):
    return { 'id': category.id, 'title': category.title, 'description': category.description }

def task_encoder(task):
    return { 'id': task.id,
            'title': task.title,
            'owner_list': tasklist_encoder(task.ownerList),
            'description': task.description,
            'deadline': task.deadline,
            'category': category_encoder(task.category) }