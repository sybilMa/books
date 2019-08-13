from rest_framework_jwt.serializers import jwt_payload_handler
from rest_framework_jwt.serializers import jwt_encode_handler

# 获取token的函数


def get_jwt_token(user):
   try:
       payload = jwt_payload_handler(user)
       token = jwt_encode_handler(payload)
       return token
   except:
       return None


from user.serializers import UserModelSerializer

# 自定义返回方式

def jwt_response_payload_handler(token, user=None, request=None):
    return {
        "token": token,
        "user": UserModelSerializer(user).data
    }