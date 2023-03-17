from base.models.basemodel import BaseModel
from django.db import models
from django.utils.text import slugify

class Category(BaseModel):
    name = models.CharField(max_length=255)
    slug = models.CharField(max_length=255,blank=True, null=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
       self.slug = str(slugify(self.name))
       super(Category, self).save(*args, **kwargs) # Call the real save() method
    
