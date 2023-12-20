from django.contrib import admin
from django.urls import path, include 
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup', views.signup, name='signup'),
    path('signin', views.signin, name='signin'),
    path('signout', views.signout, name='signout'),
    path('success', views.success, name='success'),
    path('fav', views.fav, name='fav'),
    path('lease', views.lease, name='lease'),
    path('rent_ski', views.rent_ski, name='rent_ski'),

 ]

