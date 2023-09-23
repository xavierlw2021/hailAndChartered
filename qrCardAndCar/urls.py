from django.contrib import admin
from django.urls import path, re_path
import hailAndChartered.views

urlpatterns = [
    path("admin/", admin.site.urls),    
    re_path(r'^callback', hailAndChartered.views.callback),
]
