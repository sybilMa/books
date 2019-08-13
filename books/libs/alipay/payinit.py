from .pay import AliPay
import os


def ali():
    # 沙箱环境地址：https://openhome.alipay.com/platform/appDaily.htm?tab=info
    # s  appid
    app_id = "2016101000653326"
    # 支付宝收到用户的支付,会向商户发两个请求,一个get请求,一个post请求
    # POST请求，用于最后的检测
    notify_url = "http://127.0.0.1:8000/order/aliback/"
    # GET请求，用于页面的跳转展示
    return_url = "http://127.0.0.1:8000/order/aliback/"
    # 自己的私钥
    alipay_private_key_path = os.path.join(os.path.dirname(__file__), 'alipay_private_2048.txt')
    # 支付宝公钥
    alipay_public_key_path = os.path.join(os.path.dirname(__file__), 'alipay_public_2048.txt')
    # 生成一个AliPay的对象
    alipay = AliPay(
        appid=app_id,
        app_notify_url=notify_url,
        return_url=return_url,
        app_private_key_path=alipay_private_key_path,
        alipay_public_key_path=alipay_public_key_path,  # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥
        debug=True,  # 默认False,
    )
    return alipay