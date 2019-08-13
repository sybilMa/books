from django.db import models
from user.models import RentHistory, Order, User
# from user.models import


# 图书详情表
class Book(models.Model):
    author = models.ManyToManyField(to='Author', related_name='books', db_constraint=False)
    user = models.ForeignKey(to=User, db_constraint=False, on_delete=models.DO_NOTHING,
                             related_name='books', null=True, blank=True)
    category = models.ForeignKey(to='Category', db_constraint=False, on_delete=models.DO_NOTHING,
                                 related_name='books', null=True, blank=True)
    rent = models.ForeignKey(to=RentHistory, db_constraint=False, on_delete=models.DO_NOTHING,
                             related_name='books', null=True, blank=True)
    order = models.ForeignKey(to=Order, db_constraint=False, on_delete=models.DO_NOTHING,
                              related_name='books', null=True, blank=True)
    name = models.CharField(max_length=64, verbose_name='书名')
    image = models.ImageField(upload_to='static/img/', verbose_name='封面', blank=True)
    price = models.DecimalField(max_digits=5, decimal_places=3, verbose_name='租书价格', default=0)
    amount = models.IntegerField(verbose_name='可借数量', default=0)
    publish_date = models.DateField(verbose_name='出版日期')
    pages = models.IntegerField(verbose_name='书籍页数')
    stars = models.DecimalField(max_digits=3, decimal_places=2, verbose_name='推荐指数')
    desc = models.CharField(max_length=255, verbose_name='书本简介')
    b_money = models.DecimalField(max_digits=4, decimal_places=2, verbose_name='所需押金', null=True, blank=True)
    buy_price = models.DecimalField(max_digits=8, decimal_places=3, verbose_name='购买价格', null=True, blank=True)
    publishers = models.CharField(max_length=64, verbose_name='出版社')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'book'
        verbose_name = '图书表'
        verbose_name_plural = verbose_name

    @property
    def author_detail(self):
        authors = self.author.all()
        author_list = []
        for author in authors:
            dic = {'name': author.name, 'info': author.info, 'image': author.image}
            author_list.append(dic)
        return author_list

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
    def category_detail(self):
        categorys = self.category.objects.all()
        category_list = []
        for category in categorys:
            dic = {'name': category.get_name_display()}
            category_list.append(dic)
        return category_list

    @property
    def tag_detail(self):
        tags = self.tag.all()
        tag_list = []
        for tag in tags:
            dic = {'name': tag.get_name_display()}
            tag_list.append(dic)
        return tag_list

    @property
    def rent_detail(self):
        rents = self.rent.objects.all()
        rent_list = []
        for rent in rents:
            dic = {'amount': rent.amount, 'rent_time': rent.rent_time, 'back_time': rent.back_time}
            rent_list.append(dic)
        return rent_list

    @property
    def order_detail(self):
        orders = self.order.objects.all()
        order_list = []
        for order in orders:
            dic = {'amount': order.amount, 'order_time': order.order_time, 'user': order.user.username}
            order_list.append(dic)
        return order_list


# 作者表
class Author(models.Model):
    name = models.CharField(max_length=64, verbose_name='作者姓名')
    info = models.CharField(max_length=255, verbose_name='作者简介', null=True, blank=True)
    image = models.ImageField(default='static/img/name.png', upload_to='static/img/', verbose_name='作者图片')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'author'
        verbose_name = '作者表'
        verbose_name_plural = verbose_name

    @property
    def book_detail(self):
        books = self.books.all()
        book_list = []
        for book in books:
            dic = {'name': book.name, 'desc': book.desc, 'pages': book.pages, 'publishers': book.publishers,
                   'image': book.image, 'stars': book.stars, 'amount': book.amount, 'price': book.price, 'id': book.id}
            book_list.append(dic)
        return book_list


# 分类表
class Category(models.Model):
    cate_type = (
        (1, '中国文学'),
        (2, '外国文学'),
    )
    name = models.IntegerField(choices=cate_type, verbose_name='图书分类', default=1)

    def __str__(self):
        return self.names

    class Meta:
        db_table = 'book_category'
        verbose_name = '图书分类表'
        verbose_name_plural = verbose_name

    @property
    def names(self):
        return self.get_name_display()

    @property
    def book_detail(self):
        books = self.books.all()
        book_list = []
        for book in books:
            dic = {'name': book.name, 'desc': book.desc, 'pages': book.pages, 'publish_date': book.publish_date,
                   'image': book.image, 'stars': book.stars, 'id': book.id}
            book_list.append(dic)
        return book_list


# 标签表
class Tags(models.Model):
    cate_type = (
        (1, '文学类'),
        (2, '流行'),
        (3, '文化'),
        (4, '生活'),
        (5, '经管'),
        (6, '科技')
    )
    name = models.IntegerField(choices=cate_type, verbose_name='书籍标签')
    book = models.ManyToManyField(to='Book', related_name='tag', db_constraint=False)

    def __str__(self):
        return self.names

    class Meta:
        db_table = 'home_tags'
        verbose_name = '标签表'
        verbose_name_plural = verbose_name

    @property
    def names(self):
        return self.get_name_display()

    @property
    def book_detail(self):
        books = self.book.all()
        book_list = []
        for book in books:
            dic = {'name': book.name, 'desc': book.desc, 'pages': book.pages, 'publish_date': book.publish_date,
                   'image': book.image, 'stars': book.stars, 'id': book.id}
            book_list.append(dic)
        return book_list


# 加入购物车
class BookCart(models.Model):
    user = models.ForeignKey(to=User, db_constraint=False, on_delete=models.DO_NOTHING, related_name='cart')
    book = models.ForeignKey(to='Book', db_constraint=False, on_delete=models.DO_NOTHING, related_name='cart')
    amount = models.IntegerField(verbose_name='购买数量')

    def __str__(self):
        return self.book.name

    class Meta:
        verbose_name = '购物车表'
        verbose_name_plural = verbose_name

    # @property
    # def book_detail(self):  # 一对多的一方，点all拿不到所以可以直接使用外键
    #     print(12221)
    #     books = self.book
    #     print(books)
    #     book_list = []
    #     for book in books:
    #         dic = {'name': book.name, 'image': book.image, 'buy_price': book.buy_price, 'id': book.pk,
    #                'price': book.amount*book.buy_price}
    #         book_list.append(dic)
    #     return book_list

    # @property
    # def user_detail(self):  # 错误信息同上
    #     print(111)
    #     users = self.user.objects.all()
    #     print(users)
    #     user_list = []
    #     for user in users:
    #         dic = {'id': user.pk, 'name': user.username}
    #         user_list.append(dic)
    #     return user_list


# 用户租借（是否在线租借字段）
class Rent(models.Model):
    book = models.ForeignKey(to=Book, db_constraint=False, on_delete=models.DO_NOTHING, related_name='rented')
    user = models.ForeignKey(to=User, db_constraint=False, on_delete=models.DO_NOTHING, related_name='rented')
    amount = models.IntegerField(verbose_name='租借数量', default=0)
    rent_time = models.DateTimeField(auto_now_add=True, verbose_name='租书日期')
    back_time = models.DateField(null=True, verbose_name='还书日期')
    # 租书时间
    max_time = models.IntegerField(default=30)

    class Meta:
        db_table = 'book_rent'
        verbose_name = '租借'
        verbose_name_plural = verbose_name


class Ordered(models.Model):
    book = models.ForeignKey(to='Book', db_constraint=False, on_delete=models.DO_NOTHING, related_name='ordered')
    user = models.ForeignKey(to=User, db_constraint=False, on_delete=models.DO_NOTHING, related_name='ordered')
    amount = models.IntegerField(verbose_name='租借数量', default=0)
    a_money = models.DecimalField(max_digits=8, decimal_places=3, verbose_name='预约价格', default=0)
    order_time = models.DateTimeField(auto_now_add=True, verbose_name='预约日期')

    class Meta:
        db_table = 'book_ordered'
        verbose_name = '预约'
        verbose_name_plural = verbose_name