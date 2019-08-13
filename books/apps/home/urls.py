from django.urls import path
from . import views

urlpatterns = [
    path('msg/', views.SMSAPIView.as_view()),
    path('', views.Home.as_view()),

]
