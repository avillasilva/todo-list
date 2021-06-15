from django.urls import path, re_path
from django.urls.resolvers import URLPattern

from . import views

app_name = 'notes'
urlpatterns = [
    path('notes/', views.create_or_get_notes, name='create_or_get_notes'),
    # path('notes/<int:note_id>', views.crud_notes, name='crud_note'),
]
