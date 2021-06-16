from django.shortcuts import render
from .util import *

def register_user(request):
    return proxy_todolist(request, 'register')

def login_user(request):
    return proxy_todolist(request, 'login')

def logout_user(request):
    return proxy_todolist(request, 'logout')
