from django.urls import path
from .views import TodoApiView

urlpatterns = [
    path('api', TodoApiView.as_view())
]
