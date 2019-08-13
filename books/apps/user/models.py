from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
    info = models.CharField(max_length=64, verbose_name='用户信息', null=True)
    avatar = models.ImageField(default='img/name.png', upload_to='avatar/', verbose_name='用户头像')
    sex = models.IntegerField(choices=((1, '男'), (2, '女'), (3, '保密')), verbose_name='用户性别', default=3)
    idcard = models.CharField(max_length=64, verbose_name='用户身份证', null=True, blank=True)
    score = models.IntegerField(verbose_name='信誉积分', default=0)
    phone = models.BigIntegerField(verbose_name='用户手机号', null=True, blank=True)
    d_money = models.IntegerField(default=0, verbose_name='押金')
    num = models.CharField(max_length=64, verbose_name='快递单号', null=True)
    address = models.CharField(max_length=128, null=True)

    def __str__(self):
        return self.username

    class Meta:
        db_table = 'user'
        verbose_name = '用户表'
        verbose_name_plural = verbose_name

    @property
    def book_detail(self):
        books = self.books.all()
        book_list = []
        for book in books:
            dic = {'name': book.name, 'desc': book.desc, 'pages': book.pages, 'publish_date': book.publish_date,
                   'image': book.image, 'stars': book.stars}
            book_list.append(dic)
        return book_list

    @property
    def rent_detail(self):
        rents = self.renthistory.all()
        rent_list = []
        for rent in rents:
            dic = {'amount': rent.amount, 'rent_time': rent.rent_time, 'back_time': rent.back_time}
            rent_list.append(dic)
        return rent_list

    @property
    def order_detail(self):
        orders = self.order.all()
        order_list = []
        for order in orders:
            dic = {'amount': order.amount, 'order_time': order.order_time, 'user': order.user.username}
            order_list.append(dic)
        return order_list


# 用户租借（是否在线租借字段）
class RentHistory(models.Model):
    user = models.ForeignKey(to='User', db_constraint=False, on_delete=models.DO_NOTHING, related_name='renthistory')
    amount = models.IntegerField(verbose_name='租借数量', default=0)
    a_money = models.DecimalField(max_digits=8, decimal_places=3, verbose_name='借阅总价格', default=0)
    # 是否在线租借图书
    is_online = models.BooleanField(default=0)
    rent_time = models.DateTimeField(auto_now_add=True, verbose_name='租书日期')
    back_time = models.DateTimeField(null=True, verbose_name='还书日期')
    # 租书时间
    max_time = models.IntegerField(default=30)

    def __str__(self):
        return self.user.username

    class Meta:
        db_table = 'user_renthistory'
        verbose_name = '租借历史'
        verbose_name_plural = verbose_name

    @property
    def user_detail(self):
        users = self.user.objects.all()
        user_list = []
        for user in users:
            dic = {'name': user.username, 'phone': user.phone, 'score': user.score, 'sex': user.sex,
                   'avatar': user.avatar}
            user_list.append(dic)
        return user_list

    @property
    def book_detail(self):
        books = self.books.all()
        book_list = []
        for book in books:
            dic = {'name': book.name, 'desc': book.desc, 'pages': book.pages, 'publish_date': book.publish_date,
                   'image': book.image, 'stars': book.stars}
            book_list.append(dic)
        return book_list


# 用户预约
class Order(models.Model):
    user = models.ForeignKey(to='User', db_constraint=False, on_delete=models.DO_NOTHING, related_name='order')
    amount = models.IntegerField(verbose_name='租借数量', default=0)
    a_money = models.DecimalField(max_digits=8, decimal_places=3, verbose_name='借阅总价格', default=0)
    order_time = models.DateTimeField(auto_now_add=True, verbose_name='预约日期')

    def __str__(self):
        return self.user.username

    class Meta:
        db_table = 'user_order'
        verbose_name = '用户预约'
        verbose_name_plural = verbose_name

    @property
    def user_detail(self):
        users = self.user.objects.all()
        user_list = []
        for user in users:
            dic = {'name': user.username, 'phone': user.phone, 'score': user.score, 'sex': user.sex,
                   'avatar': user.avatar}
            user_list.append(dic)
        return user_list

    @property
    def book_detail(self):
        books = self.books.all()
        book_list = []
        for book in books:
            dic = {'name': book.name, 'desc': book.desc, 'pages': book.pages, 'publish_date': book.publish_date,
                   'image': book.image, 'stars': book.stars}
            book_list.append(dic)
        return book_list



