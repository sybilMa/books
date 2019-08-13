# 发送短信的接口
"""
mobile: 电话 13355667788
code_expire_tuple: (验证码, 失效时间m) (123456, 5)
temp_id: 短信模板 1
"""
from .sms import send_sms