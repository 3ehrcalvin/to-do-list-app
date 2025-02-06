from django.urls import path
from .views import TodoApiView, TodoDetailApiView

urlpatterns = [
    path('api', TodoApiView.as_view()),
    path('api/<int:todo_id>', TodoDetailApiView.as_view())
]
