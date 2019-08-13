import xadmin
from user import models


xadmin.site.register(models.RentHistory)
xadmin.site.register(models.Order)
