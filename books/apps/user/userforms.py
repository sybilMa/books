from django import forms
from django.forms import widgets
from . import models


class Myform(forms.Form):
    password = forms.CharField(
        min_length=6,
        error_messages={
            'min_length': '密码最少要6位',
            'required': '密码输入不可以为空',
        },
        label='密码',
        widget=widgets.PasswordInput(attrs={'class': 'form-control'})
    )
    confirm_password = forms.CharField(
        min_length=6,
        error_messages={
            'min_length': '再次输入密码最小为6位',
            'required': '再次输入密码不可以为空'
        },
        label='确认密码',
        widget=widgets.PasswordInput(attrs={'class': 'form-control'})
    )

    def clean_username(self):
        username = self.cleaned_data.get('username')
        # 校验用户名是否存在
        user_obj = models.UserInfo.objects.filter(username=username).first()
        if user_obj:
            self.add_error('username', '用户名以存在')
        return username

    def clean(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        # 校验两次密码是否一致
        if password != confirm_password:
            self.add_error('confirm_password', '两次密码不一致')
        return self.cleaned_data