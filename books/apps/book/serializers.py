from rest_framework.serializers import ModelSerializer
from . import models


class BookModelSerializer(ModelSerializer):
    class Meta:
        model = models.Book
        fields = ['name', 'desc', 'image', 'price', 'amount', 'publish_date', 'pages', 'stars', 'b_money', 'buy_price',
                  'publishers', 'author_detail', 'user_detail', 'tag_detail', 'category_detail', 'rent_detail',
                  'order_detail', 'id']


class BookDetailSerai(ModelSerializer):
    class Meta:
        model = models.Book
        fields = ['name', 'image', 'desc',  'price', 'publish_date', 'pages',
                  'stars', 'b_money', 'buy_price', 'author_detail', 'amount', 'id']


class TagModelSerializer(ModelSerializer):
    class Meta:
        model = models.Tags
        fields = ['names', 'book_detail', 'id']
        
        
class AuthorModelSerializer(ModelSerializer):
    class Meta:
        model = models.Author
        fields = ['name', 'image', 'info', 'book_detail', 'id']
        

class CategoryModelSerializer(ModelSerializer):
    class Meta:
        model = models.Category
        fields = ['names', 'book_detail', 'id']


class CartModelSerializer(ModelSerializer):
    class Meta:
        model = models.BookCart
        fields = ['amount', 'id']
        
        
