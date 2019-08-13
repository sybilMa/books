from rest_framework.serializers import ModelSerializer
from . import models


class UserModelSerializer(ModelSerializer):
    class Meta:
        model = models.User
        fields = ['info', 'avatar', 'sex', 'idcard', 'score', 'phone', 'order', 'email',
                  'd_money', 'num', 'book_detail', 'rent_detail', 'order_detail', 'id']


class RentHisModelSerializer(ModelSerializer):
    class Meta:
        model = models.RentHistory
        fields = ['user_detail', 'book_detail', 'amount', 'a_money', 'is_online',
                  'rent_time', 'back_time', 'max_time']


class OrderModelSerializer(ModelSerializer):
    class Meta:
        model = models.Order
        fields = ['user_detail', 'book_detail', 'amount', 'a_money', 'order_time', 'id']
