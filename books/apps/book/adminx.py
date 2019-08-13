import xadmin
from book import models


xadmin.site.register(models.Author)
xadmin.site.register(models.Book)
xadmin.site.register(models.Tags)
xadmin.site.register(models.Category)
xadmin.site.register(models.BookCart)
