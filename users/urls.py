from .views import *
from django.urls import path


urlpatterns = [

    path('', getUsers, name="users"),

    path('<str:pk>', getUserById, name='user'),

    path('update/<str:pk>', updateUser, name='user-update'),

    path('delete/<str:pk>', deleteUser, name='user-delete'),
]
