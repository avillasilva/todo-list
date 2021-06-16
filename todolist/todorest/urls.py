from django.urls import path, re_path
from django.urls.resolvers import URLPattern

from . import views

app_name = 'todorest'
urlpatterns = [
    path('register', views.register_user),
    path('login', views.login_user),
    path('logout', views.logout_user),
    
    path('tasklist/', views.create_or_get_lists, name='create_or_get_lists'),
    path('tasklist/<int:list_id>', views.crud_list, name='crud_list'),
    
    path('task/', views.create_or_get_tasks, name='create_or_get_tasks'),
    path('task/<int:task_id>', views.crud_task, name='crud_task'),

    path('category/', views.create_or_get_categories, name='create_or_get_categories'),
    path('category/<int:category_id>', views.crud_category, name='crud_category'),

    path('note/', views.create_or_get_notes, name='create_or_get_notes'),
    path('note/<int:note_id>', views.crud_category, name='crud_note')
]
