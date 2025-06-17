from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse

class Category_list(models.Model):
        name=models.CharField(max_length=250,unique=True)
        slug=models.SlugField(max_length=250,unique=True)  
        image=models.ImageField(upload_to='category',default='default.jpg')
        class Meta:
            ordering = ('name',)
            verbose_name = 'Category'
            verbose_name_plural = 'Categories'

        def __str__(self):
            return self.name
        
 
class Product(models.Model):
    name=models.CharField(max_length=250,unique=True)
    slug=models.SlugField(max_length=250,unique=True) 
    image=models.ImageField(upload_to='products')
    description=models.TextField()
    stock=models.IntegerField()
    availability=models.BooleanField(default=True)
    offer=models.BooleanField(default=False)
    price=models.IntegerField()
    Category=models.ForeignKey(Category_list,on_delete=models.CASCADE)
    quantity=models.CharField(max_length=150,default=1)
    offer_price=models.IntegerField(default=10)
    actual_price=models.IntegerField(default=0)
    
    
    def get_url(self):
        return reverse('details',args=[self.Category.slug,self.slug])
    def __str__(self):
          return self.name