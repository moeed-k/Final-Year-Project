from django.urls import path
from . import views

urlpatterns = [
    path('process_data/', views.process_data),
    path('get_report/',views.getReport),
    path('get_sessionID/',views.getSessionID)
]