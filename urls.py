#map URL to view function
from django.urls import path, include
from . import views

#URL Configuration
urlpatterns = [
    #path('', views.say_hello)
    path('', views.home, name='home'),
    #path('home/', views.home, name='home'),
    path('form/', views.form, name="form"),
    path('thankyou/', views.thankyou, name="thankyou"),
    path("todirectory/", views.todirectory, name="todirectory"),
    path("seating/", views.makechart, name="seating")
   
]