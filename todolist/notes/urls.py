from django.urls import path, re_path
from django.urls.resolvers import URLPattern

from . import views

app_name = 'notes'
urlpatterns = [
    path('register', views.register_user),
    path('login', views.login_user),
    path('logout', views.logout_user),
    
    path('notes/', views.create_or_get_notes, name='create_or_get_notes'),
    # path('notes/<int:note_id>', views.crud_notes, name='crud_note'),
]
