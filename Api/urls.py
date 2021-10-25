from django import urls
from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('check/<slug:video_id>', views.check)
]