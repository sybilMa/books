from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.LoginAPIView.as_view()),
    path('register/', views.RegisterAPIView.as_view()),
    path('logout/', views.LogoutAPIView.as_view()),
    path('sms/', views.SMSAPIView.as_view()),
    path('password/', views.PasswordAPIView.as_view()),
    path('avatar/', views.AvatarAPIView.as_view()),
    path('info/', views.InfoAPIView.as_view()),
    path('order/', views.OrderAPIView.as_view()),
    path('rent/', views.RentAPIView.as_view()),
    path('message/', views.MessageAPIView.as_view()),
    path('edit/', views.EditAPIView.as_view()),
    path('shop/delete/', views.DeleteBook.as_view()),
    path('rent/delete/', views.DeleteRent.as_view()),
    path('shop/', views.ShopAPIView.as_view()),
    path('codes/', views.get_code),
    path('settle/', views.SettleAPIView.as_view()),


]
