from django.contrib import admin
from . models import *

class cateadmin(admin.ModelAdmin):
    prepopulated_fields={'slug':('name',)}
admin.site.register(Category_list,cateadmin)    
    
class Productadmin(admin.ModelAdmin):
    list_display=['name','image','description','stock','Category','availability','offer','price','quantity','offer_price','actual_price']
    list_editable=['image','description','stock','availability','offer','price','quantity','offer_price','actual_price']
    prepopulated_fields={'slug':('name',)}
admin.site.register(Product,Productadmin)  

# class CartListAdmin(admin.ModelAdmin):
#     list_display = ['cart_id', 'date_added']
# admin.site.register(cartlist, CartListAdmin)


# class ItemsAdmin(admin.ModelAdmin):
#     list_display = ['prodt', 'quan', 'cart', 'active']
# admin.site.register(items, ItemsAdmin)

# class UserAdmin(admin.ModelAdmin):
#     pass
# admin.site.register(user,UserAdmin)