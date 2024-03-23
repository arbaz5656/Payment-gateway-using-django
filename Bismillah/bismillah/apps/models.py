from django.db import models
from django.contrib.auth.models import User
import uuid
from django.db.models import Sum
# Create your models here.

class BaseModel(models.Model):
    uid=models.UUIDField(default=uuid.uuid4 ,editable=False,primary_key=True)
    crated_at=models.DateField(auto_now_add=True)
    updated_at=models.DateField(auto_now_add=True)

    class Meta:
        abstract = True

class chienesecategory(BaseModel):
    category_name=models.CharField(max_length=100)

    def __str__(self):
        return self.category_name

class rice(BaseModel):
    category = models.ForeignKey(chienesecategory,on_delete=models.CASCADE,related_name="rices")
    Rice_name=models.CharField(max_length=100)
    price=models.IntegerField(default=100)
    images=models.ImageField(upload_to='images')

    def __str__(self):
        return "%s %s" %(self.Rice_name,self.price)

class Cart(BaseModel):
    user=models.ForeignKey(User,null=True,blank=True,on_delete=models.SET_NULL,related_name="carts")
    is_paid=models.BooleanField(default=False)

    def __str__(self):
        return self.user

#    grand total
    def get_total(self):
        total = self.cart_items.aggregate(total_price=Sum('rice__price'))['total_price']
        return total if total else 0


class cartItems(BaseModel):
    cart=models.ForeignKey(Cart,on_delete=models.CASCADE,related_name="cart_items")
    rice=models.ForeignKey(rice, on_delete=models.CASCADE)

    def __str__(self):
        return self.rice
