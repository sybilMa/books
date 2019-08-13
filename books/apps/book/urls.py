from django.urls import path, re_path, include
from . import views

urlpatterns = [
    # 图书操作页面
    re_path('(?P<condition>detail|buy|rent|shop|order)/(?P<pk>\d+)/', views.BookAPIView.as_view()),
    # re_path('category/(?P<pk>\d+)/', views.CategoryAPIView.as_view()),
    # re_path('tag/(?P<pk>\d+)/', views.TagAPIView.as_view()),
    # 代码冗余，所以和为下面的一个方法
    re_path('(?P<condition>category|tag)/(?P<pk>\d+)/', views.CaTaAPIView.as_view()),
    re_path('(?P<condition>author|book)/(?P<pk>\d+)/', views.AuthorAPIView.as_view()),
    re_path(r'^search/', include('haystack.urls')),
]