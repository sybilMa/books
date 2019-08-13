"""books URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.urls import re_path, path, include
import xadmin
xadmin.autodiscover()
from xadmin.plugins import xversion
xversion.register_models()
from django.conf import settings
from django.views.static import serve


urlpatterns = [
    path(r'xadmin/', xadmin.site.urls),
    re_path(r'^media/(?P<path>.*)', serve, {'document_root': settings.MEDIA_ROOT}),  # 这是media用户上传文件路由
    path('user/', include('user.urls')),
    path('book/', include('book.urls')),
    path('order/', include('order.urls')),
    # path('docs/', include_docs_urls(title='站点页面标题')),
    path('', include('home.urls')),
]
