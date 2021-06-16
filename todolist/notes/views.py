from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
import json
from .serializers import *
from .util import *
from .models import *


def register_user(request):
    return proxy_todolist(request, 'register')

def login_user(request):
    return proxy_todolist(request, 'login')

def logout_user(request):
    return proxy_todolist(request, 'logout')


def create_note(request):
    data = json.loads(request.body.decode('utf-8'))
    try:
        note = Note(owner=request.user, title=data.get(
            'title'), content=data.get('content'), tasklist=data.get('tasklist'))
        
        note.save()
        return JsonResponse(note_encoder(note))
    except User.DoesNotExist:
        return HttpResponse('User does not exist', status=400)

def update_note(request, note_id):
    data = json.loads(request.body.decode('utf-8'))
    try:
        note = Note.objects.get(pk=note_id)

        if note.owner.id != request.user.id:
            raise Exception('Not allowed')

        note.title = data.get('title')
        note.content = data.get('content')
        note.tasklist = data.get('tasklist')
        note.save()
        return JsonResponse(note_encoder(note), safe=False)
    except Exception as e:
        return HttpResponse(str(e), status=400)

def delete_note(request, note_id):
    try:
        note = Note.objects.get(pk=note_id)

        if note.ownerList.owner.id != request.user.id:
            raise Exception('Not allowed')
        
        note.delete()
        return JsonResponse({ 'message': 'Note deleted' })
    except note.DoesNotExist:
        return HttpResponse('Note does not exist', status=400)

@login_required
def create_or_get_notes(request):
    if request.method == 'POST':
        return create_note(request)


def get_notes(request):
    try:
        notelists = Note.objects.filter(owner=request.user)
        notes = []
        for notelist in notelists:
            for note in Note.objects.filter(ownerList=notelist.id):
                notes.append(note_encoder(notes))
        
        return JsonResponse(notes, safe=False)
    except Exception as e:
        return HttpResponse(str(e), status=400)

def get_note(request, note_id):
    try:
        note = Note.objects.get(pk=note_id)
        if note.ownerList.owner.id != request.user.id:
            raise Exception('Not allowed!')

        return JsonResponse(note_encoder(note),safe = False)
    except Exception as e:
        return HttpResponse(str(e),status = 400)


# @login_required
# def crud_note(request, note_id):
#     if request.method == 'GET':
#         return get_note(request, note_id)
#     elif request.method == 'PUT':
#         return update_note(request, note_id)
#     elif request.method == 'DELETE':
#         return delete_note(request, note_id)
#     else:
#         return HttpResponse(status=400)