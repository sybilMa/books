from django.shortcuts import render
from rest_framework.views import APIView
from books.libs.alipay import payinit
import time
import hashlib
from django.core.cache import cache
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from book.models import BookCart
# Create your views here.


class AlipayAPIView(APIView):
    """
        返回所有图书信息.
        """
    # 获取前台商品的信息
    def post(self, request, *args, **kwargs):
        # 商品的信息
        subject = request.data.get('subject')
        # 商品的金额
        money = request.data.get('money')
        money = money[:-1]
        alipay = payinit.ali()
        # 生成订单号
        info = str(time.time()) + str(subject) + str(money)
        # 订单号--存放到redis中，之后回调成功了我们在将redis中的信息更改，然后同步到MySQL
        pay_num = hashlib.md5(info.encode('utf-8')).hexdigest()
        # 生成支付链接--redis存储
        cache.set(pay_num, False, 300)
        # 生成订单链接
        try:
            query_params = alipay.direct_pay(
                subject=subject,  # 商品简单描述
                out_trade_no=pay_num,  # 商户订单号
                total_amount=money,  # 交易金额(单位: 元 保留俩位小数)
            )
            pay_url = "https://openapi.alipaydev.com/gateway.do?{}".format(query_params)
        except:
            return Response({})
        return Response({
            'pay_num': pay_num,
            'pay_url': pay_url
        })


class AlibackViewSet(ViewSet):
    """
    list:
    返回图书列表数据

    retrieve:
    返回图书详情数据

    latest:
    返回最新的图书数据

    read:
    修改图书的阅读量
    """
    def get(self, request, *args, **kwargs):
        alipay = payinit.ali()
        params = request.GET.dict()
        sign = params.pop('sign', None)
        status = alipay.verify(params, sign)
        print('GET验证', status)
        if status:
            # 获取订单状态，显示给用户
            return render(request, 'user/alipay.html')

    def post(self, request, *args, **kwargs):
        alipay = payinit.ali()
        from urllib.parse import parse_qs
        body_str = request.body.decode('utf-8')
        post_data = parse_qs(body_str)
        post_dict = {}
        for k, v in post_data.items():
            post_dict[k] = v[0]
        print('转完之后的字典', post_dict)
        # 做二次验证
        sign = post_dict.pop('sign', None)
        # 通过调用alipay的verify方法去认证
        status = alipay.verify(post_dict, sign)
        print('POST验证', status)
        if status:
            # 修改自己订单状态
            pass
        return Response('验证成功')