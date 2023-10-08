from django.contrib import admin
from django.urls import path, re_path
import hailAndChartered.views
import keyCardTest.views

urlpatterns = [
    path("admin/", admin.site.urls),    
    re_path(r'^callback', hailAndChartered.views.callback),
    path('yourQRCode/<int:qid>', keyCardTest.views.show_QRCode),    
    path('confirm', hailAndChartered.views.confirmed, name= 'Confirm'),
]
