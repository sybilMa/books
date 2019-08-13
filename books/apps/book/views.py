from django.shortcuts import render,redirect
from rest_framework.views import APIView
from . import models
from . import serializers
from books.libs.wrap import login_auth
from django.utils.decorators import method_decorator
from rest_framework.response import Response
# Create your views here.



# 图书详情页|购买|租借
@method_decorator(login_auth, name='get')
class BookAPIView(APIView):
    """
       返回所有图书信息.
       """
    def get(self, request, *args, **kwargs):
        if kwargs['condition'] == 'detail':  # 详情
            book_obj = models.Book.objects.all().filter(pk=kwargs['pk'])
            book = serializers.BookDetailSerai(instance=book_obj, many=True).data
            # print(book)
            return render(request, 'book/bookdetail.html', locals())
        elif kwargs['condition'] == 'buy':
            id = kwargs['pk']
            cart_obj = models.BookCart.objects.filter(book_id=id).first()
            if cart_obj:
                cart_obj.amount += 1
                cart_obj.save()
            else:
                models.BookCart.objects.create(book_id=id, user_id=request.user.id, amount=1)
            carts = models.BookCart.objects.filter(book_id=id)
            return render(request, 'user/shop.html', locals())
        elif kwargs['condition'] == 'rent':  # 租借
            rent_obj = models.Rent.objects.filter(book_id=kwargs['pk']).first()
            if rent_obj:
                rent_obj.amount += 1
                rent_obj.save()
            else:
                models.Rent.objects.create(book_id=kwargs['pk'], user_id=request.user.id, amount=1)
            rent = models.Rent.objects.filter(book_id=kwargs['pk'])
            return render(request, 'user/rent.html', locals())
        elif kwargs['condition'] == 'order':  # 预约
            order_obj = models.Ordered.objects.filter(book_id=kwargs['pk']).first()
            if order_obj:
                order_obj.amount += 1
                order_obj.save()
            else:
                models.Ordered.objects.create(book_id=kwargs['pk'], user_id=request.user.id, amount=1)
            orders = models.Ordered.objects.filter(book_id=kwargs['pk'])
            return render(request, 'user/order.html', locals())
        else:  # 加入购物车页面
            pk = kwargs['pk']
            books = models.BookCart.objects.filter(book_id=pk).first()
            if books:
                books.amount += 1
                books.save()
            else:
                models.BookCart.objects.create(amount=1, user_id=request.user.id, book_id=pk)
            # return redirect('/home')

            return Response({
                'start': 100,
                'msg': 'ok',
            })


# 作者详情、作者书籍页面
@method_decorator(login_auth, name='get')
class AuthorAPIView(APIView):
    """
       返回所有图书信息.
       """
    def get(self, request, *args, **kwargs):
        # print(kwargs)
        author_obj = models.Author.objects.all().filter(pk=kwargs['pk']).first()
        # print(cate_obj)
        author = serializers.AuthorModelSerializer(instance=author_obj).data
        # print(author)
        if kwargs['condition'] == 'author':
            # print(author['name'])
            return render(request, 'author/detail.html', locals())
        else:  # 书籍页面
            return render(request, 'author/book.html', locals())


# 标签详情页|分类详情页面
@method_decorator(login_auth, name='get')
class CaTaAPIView(APIView):
    """
       返回所有图书信息.
       """
    def get(self, request, *args, **kwargs):
        # print(kwargs)
        if kwargs['condition'] == 'category':
            cate_obj = models.Category.objects.all().filter(name=kwargs['pk']).first()
            # print(cate_obj)
            category = serializers.CategoryModelSerializer(instance=cate_obj).data
            # print(category)
            return render(request, 'book/category.html', locals())
        else:
            tag_obj = models.Tags.objects.all().filter(name=kwargs['pk']).first()
            tags = serializers.TagModelSerializer(instance=tag_obj).data
            # print(tags)
            return render(request, 'book/tag.html', locals())