from django.contrib import admin
from main.models.category import Category
from main.models.product import Product,Images,Combo


class CategoryAdmin(admin.ModelAdmin):
    list_display=['name','slug']
admin.site.register(Category,CategoryAdmin)

class ImageAdmin(admin.StackedInline):
    model = Images

class ProductAdmin(admin.ModelAdmin):
    inlines = [ImageAdmin,]
    list_display = ['name','finalprice','is_offer','is_combo','is_active']
admin.site.register(Product,ProductAdmin)

class ComboAdmin(admin.ModelAdmin):
    list_display=['name','slug','product1','product2']
admin.site.register(Combo,ComboAdmin)