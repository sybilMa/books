from django.shortcuts import render, HttpResponse, redirect
from rest_framework.views import APIView
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from books.settings import constant
from django.core.cache import cache
from rest_framework.response import Response
from django.contrib import auth
from books.libs.yuntongxun import send_sms
from books.libs.wrap import login_auth
import re
import random
from books.apps.user.util import isidcard
from .models import User
from .authenticate import SMSRateThrottle
from book import models
from django.utils.decorators import method_decorator


def get_random():
    return random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)


def words(n):
    import string
    return random.sample(string.ascii_uppercase + string.ascii_lowercase + string.digits, n)


def get_code(request):
    img_obj = Image.new('RGB', (265, 30), get_random())
    io_obj = BytesIO()
    imgDraw = ImageDraw.Draw(img_obj)
    imgFont = ImageFont.truetype(r'D:\SH_4.25\Rtbooks\books\books\static\font\222.ttf', 35)
    # 开始画字了
    code = ''
    for index, word in enumerate(words(5), 1):
        imgDraw.text((35 * index + 10, -5), word, get_random(), imgFont)
        code += word
    print(code)
    # 添加到缓存中
    cache.set('code', code, constant.EXPIRE_TIME)
    # 添加阴影
    for x in range(0, 265, 3):
        for y in range(0, 30, 3):
            imgDraw.point((x, y), get_random())
    img_obj.save(io_obj, 'png')
    return HttpResponse(io_obj.getvalue())


# 注册页面
class RegisterAPIView(APIView):
    """
       get:
       返回所有图书信息.

       post:
       新建图书.
       """
    def get(self, request, *args, **kwargs):
        return render(request, 'user/register.html')

    def post(self, request, *args, **kwargs):
        phone = request.data.get('username')
        password = request.data.get('password')
        passwords = request.data.get('confirm_password')
        msg = request.data.get('msg')
        old_msg = cache.get(phone)
        if not old_msg:
            return Response({
                'start': 200,
                'msg': '请先获取验证码'
            })
        if msg != old_msg:
            return Response({
                'start': 300,
                'msg': '验证码错误，请重新获取'
            })
        if password != passwords:
            return Response({
                'start': 500,
                'msg': '两次密码不一致'
            })
        user_obj = User.objects.filter(phone=phone).first()
        if user_obj:
            return Response({
                'start': 400,
                'msg': '当前账号已存在'
            })
        User.objects.create_user(phone=phone, password=password, username=phone)
        return Response({
            'start': 100,
            'msg': '注册成功',
            'url': '/user/login/'
        })


# 用的是图片验证码--auth认证
class LoginAPIView(APIView):
    """
       get:
       返回所有图书信息.

       post:
       新建图书.
       """
    def get(self, request, *args, **kwargs):
        return render(request, 'user/login.html', locals())

    def post(self, request, *args, **kwargs):
        # print(request.data)
        back_dic = {'start': 100, 'msg': ''}
        code = request.data.get('code')
        old_code = cache.get('code')
        if not old_code:
            back_dic['start'] = 200
            back_dic['msg'] = '请重新获取验证码'
            return Response(back_dic)
        if code != old_code:
            back_dic['start'] = 200
            back_dic['msg'] = '验证码错误，请重新获取'
            return Response(back_dic)
        username = request.data.get('username')
        password = request.data.get('password')
        # 用auth组件来校验--接收的就是JWTModelBackend返回的user
        user = auth.authenticate(username=username, password=password)
        if user:
            request.session['name'] = 'mccnihuishoude'
            auth.login(request, user=user)
            back_dic['start'] = 100
            back_dic['msg'] = '登录成功'
            back_dic['url'] = '/'
            return Response(back_dic)
        else:
            back_dic['start'] = 300
            back_dic['msg'] = '用户名或者密码错误'
            return Response(back_dic)


@method_decorator(login_auth, name='get')
class LogoutAPIView(APIView):
    """
       返回所有图书信息.
       """
    def get(self, request, *args, **kwargs):
        auth.logout(request)
        return redirect(to='/')


# 短信验证码--只有注册用了
class SMSAPIView(APIView):
    """
       返回所有图书信息.
       """
    throttle_classes = [SMSRateThrottle]

    def get(self, request, *args, **kwargs):
        phone = request.data.get('username')

        if not phone:
            return Response({
                'start': 200,
                'msg': '手机号码是必须的'
            })
        if not re.match(r'^1[3-9]\d{9}$', phone):
            return Response({
                'start': 300,
                'msg': '手机号码有误'
            })
        # 生成短信验证码
        message = ''
        for i in range(6):
            message += str(random.randint(0, 9))
        # redis存储
        cache.set(phone, message, constant.SMS_EXPIRE_TIME)
        # 调用第三方接口来发送短信
        result = send_sms(phone, (message, constant.SMS_EXPIRE_TIME // 60), 1)
        if result:
            return Response({
                'start': 100,
                'msg': '短信发送成功'
            })
        return Response({
            'start': 400,
            'msg': '发送失败，请重新获取'
        })


# 修改密码
@method_decorator(login_auth, name='get')
class PasswordAPIView(APIView):
    """
       get:
       返回所有图书信息.

       post:
       新建图书.
       """
    def get(self, request, *args, **kwargs):
        return render(request, 'user/password.html', locals())

    def post(self, request, *args, **kwargs):
        print(request.user)
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')
        confirm_password = request.data.get('confirm_password')
        user_obj = request.user.check_password(old_password)
        if not user_obj:
            return Response({
                'start': 200,
                'msg': '原密码错误'
            })
        if new_password != confirm_password:
            return Response({
                'start': 300,
                'msg': '两次密码不一致'
            })
        request.user.set_password(confirm_password)
        request.user.save()
        return Response({
            'start': 100,
            'msg': '密码修改成功',
            'url': '/user/login'
        })

    # form_obj = userforms.Myform()
    # # 从Ajax拿到的数据
    #     # print(request.POST)  # 'username': ['jason'], 'password': ['123'],
    #     form_obj = userforms.Myform(request.data)
    #     if form_obj.is_valid():
    #         data = form_obj.cleaned_data
    #         # print('222222',data)  # 后端字典 {'username': 'jason', 'password': '123456', 'confirm_password': '123456', 'email': '789@qq.com'}
    #         # 数据库要求的数据是没有再次密码确认的
    #         data.pop('confirm_password')
    #         # 拿到头像，然后判断头像是否上传
    #         # print(request.FILES)  # {'myfile': [<InMemoryUploadedFile: 7fa6def110194e05f14c60673654c5e8.jpeg (image/jpeg)>]}
    #         avatar_obj = request.FILES.get('myfile')
    #         # print(avatar_obj)  # 7fa6def110194e05f14c60673654c5e8.jpeg
    #         if avatar_obj:
    #             data['avatar'] = avatar_obj
    #         # print('==',data)
    #         models.UserInfo.objects.create_user(**data)
    #         # print('--',data)
    #         back_dic['msg'] = '注册成功'
    #         back_dic['url'] = '/login'
    #         return JsonResponse(back_dic)
    #     back_dic['msg'] = form_obj.errors  # 展示所有的错误信息
    #     back_dic['code'] = 200
    #     return JsonResponse(back_dic)


# 修改头像
@method_decorator(login_auth, name='post')
class AvatarAPIView(APIView):
    """
       返回所有图书信息.
       """
    def post(self, request, *args, **kwargs):
        # print(request)
        file_obj = request.FILES.get('myfile')
        # print(file_obj)
        if not file_obj:
            return Response({
                'start': 200,
                'msg': '用户没有上传头像'
            })
        user_obj = request.user
        # print(user_obj)

        user_obj.avatar = file_obj
        # print(user_obj.avatar)
        user_obj.save()
        return Response({
            'start': 100
        })


# 修改信息
@method_decorator(login_auth, name='post')
class InfoAPIView(APIView):
    """
       返回所有图书信息.
       """
    def post(self, request, *args, **kwargs):
        info = request.data.get('userinfo')
        user_obj = request.user
        user_obj.info = info
        user_obj.save()
        return Response({
            'start': 100,
            'msg': 'ok'
        })


# 用户预约信息展示
@method_decorator(login_auth, name='get')
class OrderAPIView(APIView):
    """
       返回所有图书信息.
       """
    def get(self, request, *args, **kwargs):
        orders = models.Ordered.objects.filter(user_id=request.user.id)
        class1 = "func"
        return render(request, 'user/order.html', locals())


@method_decorator(login_auth, name='get')
class RentAPIView(APIView):
    """
       返回所有图书信息.
       """
    def get(self, request, *args, **kwargs):
        # RentHistory.objects.create(user_id=request.user.id,amount=10,a_money=20,is_online=1)
        rent = models.Rent.objects.all()
        # for book in rent:
        #     print(book)
        #     print(book.book.name)
        class2 = "func"
        return render(request, 'user/rent.html', locals())


@method_decorator(login_auth, name='get')
class MessageAPIView(APIView):
    """
       返回所有图书信息.
       """
    def get(self, request, *args, **kwargs):
        user = User.objects.filter(pk=request.user.pk)
        class3 = "func"
        return render(request, 'user/message.html', locals())


# 校验手机号
def phonecheck(phone):
    dic = {'start': '100', 'msg': ''}
    if not phone:
        dic['start'] = '200'
        dic['msg'] = 'mobile参数是必须的'
        return dic
    # 后台要多mobile数据进行安全校验
    if not re.match(r'^1[3-9]\d{9}$', phone):
        dic['start'] = '300'
        dic['msg'] = '手机号有误'
        return dic
    try:
        User.objects.get(phone=phone)
    except:
        dic['start'] = '0'
        dic['msg'] = '手机号未注册'
        return dic
    dic['start'] = '1'
    dic['msg'] = '手机号已注册'
    return dic


# 用户信息编辑
@method_decorator(login_auth, name='get')
class EditAPIView(APIView):
    """
       get:
       返回所有图书信息.

       post:
       新建图书.
       """
    def get(self, request, *args, **kwargs):
        return render(request, 'user/edit.html', locals())

    def post(self, request, *args, **kwargs):
        # print(request.POST)
        # print(request.data)
        print(request.user)
        username = request.data.get('username')
        address = request.data.get('address')
        idcard = request.data.get('idcard')
        phone = request.data.get('phone')
        info = request.data.get('info')
        # print(username, type(username))
        # return HttpResponse('ok')
        # 身份证校验
        if idcard:
            if idcard != 'None':
                a, b = isidcard(idcard)
                if not a:
                    return Response({
                        'start': 200,
                        'msg': '身份号码错误'
                    })
        if phone == 'None':
            phone = None
            User.objects.filter(pk=request.user.pk).update(username=username, address=address,
                                                           idcard=idcard, phone=phone, info=info)
            return Response({
                'start': 100,
                'msg': 'ok',
                'url': '/user/message'
            })
        if phone:
            data = phonecheck(phone)
            if data['start'] == '200' or data['start'] == '300':
                return Response(data)
            if data['start'] == '1':  # 手机号已经注册
                return Response(data)
            else:
                User.objects.filter(pk=request.user.pk).update(username=username, address=address,
                                                               idcard=idcard, phone=phone, info=info)
                return Response({
                    'start': 100,
                    'msg': 'ok',
                    'url': '/user/message'
                })
        # 开始存数据
        else:
            User.objects.filter(pk=request.user.pk).update(username=username, address=address,
                                                           idcard=idcard, info=info)
            return Response({
                'start': 100,
                'msg': 'ok',
                'url': '/user/message'
            })


# 用户购物车页面
@method_decorator(login_auth, name='get')
class ShopAPIView(APIView):
    """
       返回所有图书信息.
       """
    def get(self, request, *args, **kwargs):
        carts = request.user.cart.all()  # queryset对象

        # data = serializers.CartModelSerializer(instance=cart_obj, many=True).data
        # print(data)  # 拿到的是id, amount

        # ok
        # print(cart_obj, type(cart_obj))
        # for car in cart_obj:
        #     # print(car, type(car))  # book.models.BookCart
        #     print('11111', car.book.name)
        #     print('11111', car.book.buy_price)
        #     print('11111', car.book.amount)
        class4 = "func"
        return render(request, 'user/shop.html', locals())


# 删除图书
@method_decorator(login_auth, name='get')
class DeleteBook(APIView):
    """
       返回所有图书信息.
       """
    def get(self, request, *args, **kwargs):
        # print(request.query_params.get("id"))
        id = request.query_params.get("id")
        book_obj = models.BookCart.objects.filter(pk=id).first()
        book_obj.delete()
        # obj.amount -= 1
        # if obj.amount == 0:
        #     obj.delete()
        # else:
        #     obj.save()
        return Response({
            'start': 100,
            'msg': 'ok',
            'book_id': book_obj.book_id
        })


@method_decorator(login_auth, name='get')
class DeleteRent(APIView):
    """
       返回所有图书信息.
       """
    def get(self, request, *args, **kwargs):
        id = request.query_params.get("id")
        # print(111, id)
        book_obj = models.Rent.objects.filter(book_id=id).first()
        book_obj.delete()
        # print(222,book_obj.book_id)
        return Response({
            'start': 100,
            'msg': 'ok',
            'book_id': book_obj.book_id
        })

# 用户支付订单
@method_decorator(login_auth, name='get')
class SettleAPIView(APIView):
    """
       get:
       返回所有图书信息.

       post:
       新建图书.
       """
    def get(self, request, *args, **kwargs):
        '''
        用户支付的页面
        :param request:
        :param args:
        :param kwargs:
        :return:
        '''
        cartId = request.query_params.get('cartId')
        cartId = list(map(lambda x: int(x), cartId[:-1].split(',')))
        book_set = models.BookCart.objects.filter(book_id__in=cartId)
        # ？我什么时候将购物车中的信息删掉，只要商品的id和
        money = 0
        amount = 0
        for book in book_set:
            money += book.book.buy_price * book.amount
            amount += book.amount
        pwd = 15
        money = round(money, 2)
        money2 = round(money + pwd, 2)
        return render(request, 'user/settle.html', locals())

    def post(self, request, *args, **kwargs):
        cartId = request.data.get('cartId')
        bookAmount = request.data.get('bookAmount')
        cartId = list(map(lambda x: int(x), cartId[:-1].split(',')))
        bookAmount = list(map(lambda x: int(x), bookAmount[:-1].split(',')))
        # 给用户一个用于支付的页面
        book_set = models.BookCart.objects.filter(book_id__in=cartId)
        print(bookAmount)
        for index, obj in enumerate(book_set):
            obj.amount = bookAmount[index]
            obj.save()
        return Response({
            'start': 100,
            'msg': '请求成功',
            'url': '/user/settle'
        })


