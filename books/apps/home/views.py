from django.shortcuts import render, HttpResponse, redirect
from books.settings import constant
from rest_framework.views import APIView
from book.serializers import BookModelSerializer, TagModelSerializer, CategoryModelSerializer, AuthorModelSerializer
from user.serializers import UserModelSerializer, RentHisModelSerializer, OrderModelSerializer
from book.models import Book, Author, Tags, Category, User, RentHistory, Order
import re
import random
from django.core.cache import cache
from books.libs.yuntongxun import send_sms
from rest_framework.response import Response
# Create your views here.


# 主页面
# @method_decorator(login_auth, name='get')
class Home(APIView):
    """
       返回所有图书信息.
       """
    def get(self, request, *args, **kwargs):
        book_obj = Book.objects.all()
        book_list = BookModelSerializer(instance=book_obj, many=True).data
        tag_obj = Tags.objects.all()
        tags_list = TagModelSerializer(instance=tag_obj, many=True).data
        author_obj = Author.objects.all()[4:8]
        author_list = AuthorModelSerializer(instance=author_obj, many=True).data
        category_obj = Category.objects.all()
        category_list = CategoryModelSerializer(instance=category_obj, many=True).data
        # 轮播图单个页面渲染
        i = book_list[:3]
        m = book_list[3:6]
        n = book_list[6:9]
        p = book_list[9:12]
        q = book_list[12:15]
        # 前端标签渲染
        d = book_list[11:15]
        x = book_list[15:19]

        return render(request, 'home.html', locals())


# 短信发送接口
class SMSAPIView(APIView):
    """
       返回所有图书信息.
       """
    def post(self, request, *args, **kwargs):
        print(request.data)
        mobile = request.data.get('username')
        if not mobile:
            return Response({
                'status': 400,
                'msg': 'mobile参数是必须的'
            })
        # 后台要多mobile数据进行安全校验
        if not re.match(r'^1[3-9]\d{9}$', mobile):
            return Response({
                'status': 300,
                'msg': '手机号有误'
            })
        # # 生成随机的验证码
        code = ''
        for i in range(6):
            code += str(random.randint(0, 9))
        # redis 存储
        cache.set(mobile, code, constant.SMS_EXPIRE_TIME)
        # 调用短信第三方发送短信
        result = send_sms('17621948046', (code, constant.SMS_EXPIRE_TIME), 1)
        if not result:
            return Response({
                'status': 200,
                'result': '短信发送失败'
            })
        return Response({
            'status': 100,
            'result': '短信发送成功'
        })
