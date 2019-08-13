from django.db import models
# 失败的原因是books没有注册
# from books.apps.user.models import User
from user.models import User
# Create your models here.


class Alipay(models.Model):
    pay_num = models.CharField(max_length=64, verbose_name='订单号')
    pay_status = models.BooleanField(default=False, verbose_name='订单状态')
    pay_user = models.ForeignKey(to=User, db_constraint=False, on_delete=models.DO_NOTHING,
                                verbose_name='支付者信息', related_name='alipay')

    class Meta:
        db_table = 'book_alipay'
        verbose_name = '订单'
        verbose_name_plural = verbose_name


