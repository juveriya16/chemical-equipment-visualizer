from django.urls import path
from . import views

urlpatterns = [
    path("upload/", views.upload_csv),
    path("history/", views.upload_history),
    path("report/pdf/", views.generate_pdf), 
]