from django.urls import path

from app import views

urlpatterns = [
    path('api/task/', views.TaskListView.as_view(), name='list_task'),
    path('api/task/', views.TaskCreateView.as_view(), name='create_task'),
    path('api/login/', views.login, name='login')
]