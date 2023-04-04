from django.contrib import admin
from django.urls import path,include
from imageProcessor import views
urlpatterns = [
    path('',views.index,name='home'),
    path('processData',views.processData,name='dataProcessor')
]