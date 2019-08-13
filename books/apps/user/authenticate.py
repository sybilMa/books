import re
from .models import User
from django.contrib.auth.backends import ModelBackend


# 多种方式注册
class JWTModelBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        # 不管username是用户名还是电话，还是邮箱都提供认证
        try:
            if re.match(r'^1[3-9]\d{9}$', username):
                user = User.objects.get(phone=username)
            elif re.match(r'.*@.*', username):
                user = User.objects.get(email=username)
            else:
                user = User.objects.get(username=username)
        except:
            return None  # 认证失败就返回None即可，jwt就无法签发token

        if user.check_password(password) and self.user_can_authenticate(user):
            return user


# 短信频率认证
from rest_framework.throttling import SimpleRateThrottle


class SMSRateThrottle(SimpleRateThrottle):
    scope = 'sms'

    def get_cache_key(self, request, view):
        mobile = request.query_params.get('mobile')
        return 'Throttle:%s' % mobile