from django.urls import path
from .views import TodoListApiView, TodoDetailApiView

urlpatterns = [
    path('api', TodoListApiView.as_view(), name='get_all_todo'),
    path('api/<int:todo_id>/', TodoDetailApiView.as_view(), name='get_single_todo'),
]
