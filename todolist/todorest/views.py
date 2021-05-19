from django.contrib.auth.models import User
from django.http.response import Http404
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse


def register_user(request):
    if request.method == 'POST':
        user = User.objects.create_user(request['username'], request['email'], request['password'])
        user.save()
        return HttpResponse(user.id)
    else:
        return HttpResponse(status=400)
