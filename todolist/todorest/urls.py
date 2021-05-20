from django.urls import path
from django.urls.resolvers import URLPattern

from . import views

app_name = 'todorest'
urlpatterns = [
    path('register', views.register_user),
    path('users/<int:pk>/lists', views.crud_list),
    path('users/<int:pk>/tasks', views.crud_tasks),
    path('users/<int:pk>/category', views.crud_category)
]
# todorest/<int:userId>/list/<int:listId>
# todorest/<int:userId>/task/<int:taskId>
# todorest/<int:userId>/category/<int:categoryId>
