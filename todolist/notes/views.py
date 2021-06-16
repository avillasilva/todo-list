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
        print(data.get('content'))
        note.save()
        return JsonResponse(note_encoder(note))
    except User.DoesNotExist:
        return HttpResponse('User does not exist', status=400)


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