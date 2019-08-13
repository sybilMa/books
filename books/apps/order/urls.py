from django.urls import path
from . import views

urlpatterns = [
    # 客户端请求支付
    path('alipay/', views.AlipayAPIView.as_view()),
    # 支付宝校验请求结果
    path('aliback/', views.AlibackViewSet.as_view({'get': 'get', 'post': 'post'})),
    # 客户校验状态
]
