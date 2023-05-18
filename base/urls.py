from django.urls import path
from . import views

urlpatterns=[
    path('',views.home, name='home'),
    path('room/<str:pk>/',views.room,name='room'),
    path('login/',views.loginPage,name="login"),
    path('register/',views.registerUser,name="register"),
    path('logout/',views.logOut,name="logout"),
    path('create-room/',views.createRoom,name="create-room"),
    path('update-room/<str:pk>/', views.updateRoom, name="update-room"),
    path('delete-room/<str:pk>/', views.deleteRoom, name="delete-room"),
    path('delete-message/<str:pk>/', views.deleteMessage, name="delete-message"),
    path('update-message/<str:pk>/', views.updateMessage, name="update-message")
]