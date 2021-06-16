from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
import json
from .serializers import *
from .util import *
from .models import *


def register_user(request):
    req = proxy_todolist(request, 'register')
    if req.status_code == 200:
        user = User.objects.create_user(request.POST['username'], 
                    request.POST['email'], 
                    request.POST['password'])
        user.save()
    return req

def login_user(request):
    req = proxy_todolist(request, 'login')
    if req.status_code == 200:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        login(request, user)
    return req

def logout_user(request):
    logout(request)
    return proxy_todolist(request, 'logout')


def create_note(request):
    data = json.loads(request.body.decode('utf-8'))
    try:
        note = Note(owner=request.user, title=data.get(
            'title'), content=data.get('content'), tasklist=data.get('tasklist'))
        print(data.get('content'))
        note.save()
        return JsonResponse(note_encoder(note, request))
    except User.DoesNotExist:
        return HttpResponse('User does not exist', status=400)


@login_required
def create_or_get_notes(request):
    if request.method == 'POST':
        return create_note(request)
    elif request.method == 'GET':
        return get_notes(request)


def get_notes(request):
    notelists = Note.objects.filter(owner=request.user)
    notes = []
    for note in notelists:
        notes.append(note_encoder(note, request))
    
    return JsonResponse(notes, safe=False)