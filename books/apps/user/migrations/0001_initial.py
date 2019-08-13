# Generated by Django 2.2.3 on 2019-07-29 14:29

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('info', models.CharField(max_length=64, null=True, verbose_name='用户信息')),
                ('avatar', models.ImageField(default='static/img/name.png', upload_to='avatar/', verbose_name='用户头像')),
                ('sex', models.IntegerField(choices=[(1, '男'), (2, '女'), (3, '保密')], default=3, verbose_name='用户性别')),
                ('idcard', models.CharField(blank=True, max_length=64, null=True, verbose_name='用户身份证')),
                ('score', models.IntegerField(default=0, verbose_name='信誉积分')),
                ('phone', models.BigIntegerField(blank=True, null=True, verbose_name='用户手机号')),
                ('d_money', models.IntegerField(default=0, verbose_name='押金')),
                ('num', models.CharField(max_length=64, null=True, verbose_name='快递单号')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': '用户表',
                'verbose_name_plural': '用户表',
                'db_table': 'user',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='RentHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField(default=0, verbose_name='租借数量')),
                ('a_money', models.DecimalField(decimal_places=3, default=0, max_digits=8, verbose_name='借阅总价格')),
                ('is_online', models.BooleanField(default=0)),
                ('rent_time', models.DateTimeField(auto_now_add=True, verbose_name='租书日期')),
                ('back_time', models.DateTimeField(null=True, verbose_name='还书日期')),
                ('max_time', models.IntegerField(default=30)),
                ('user', models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.DO_NOTHING, related_name='renthistory', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '租借历史',
                'verbose_name_plural': '租借历史',
                'db_table': 'user_renthistory',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField(default=0, verbose_name='租借数量')),
                ('a_money', models.DecimalField(decimal_places=3, default=0, max_digits=8, verbose_name='借阅总价格')),
                ('order_time', models.DateTimeField(auto_now_add=True, verbose_name='预约日期')),
                ('user', models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.DO_NOTHING, related_name='order', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '用户预约',
                'verbose_name_plural': '用户预约',
                'db_table': 'user_order',
            },
        ),
    ]
