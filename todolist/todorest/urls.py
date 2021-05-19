from django.urls import path
from django.urls.resolvers import URLPattern

from . import views

app_name = 'todorest'
urlpatterns = [
    path('register', views.register_user)
]