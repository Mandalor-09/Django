from base.models.basemodel import BaseModel
from django.db import models
from django.utils.text import slugify
from .category import Category
from tinymce.models import HTMLField

class Product(BaseModel):
    category = models.ManyToManyField(Category,related_name='product')
    name = models.CharField(max_length=255)
    slug = models.CharField(max_length=255,blank=True, null=True)
    price = models.PositiveIntegerField()
    discount = models.SmallIntegerField(default=0)
    finalprice = models.PositiveIntegerField(blank=True, null=True)
    detail =  HTMLField(blank=True, null=True)
    is_offer = models.BooleanField(default=False)
    is_combo = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
       self.slug = str(slugify(self.name))
       super(Product, self).save(*args, **kwargs) # Call the real save() method
    
class Images(BaseModel):
    product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name='images')
    images = models.ImageField(upload_to='Uploads/productimage')


class Combo(BaseModel):
    name = models.CharField(max_length=255)
    slug = models.CharField(max_length=255,blank=True, null=True)
    product1 = models.ForeignKey(Product,on_delete=models.CASCADE,related_name='combo1',blank=True, null=True)
    product2 = models.ForeignKey(Product,on_delete=models.CASCADE,related_name='combo2',blank=True, null=True)
    discount = models.SmallIntegerField(default=0)
    fianlprice = models.PositiveIntegerField(blank=True, null=True)

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs):
       self.slug = str(slugify(self.name))
       super(Combo, self).save(*args, **kwargs) # Call the real save() method
    