from django.http import HttpResponse
from django.shortcuts import render,get_object_or_404
from .models import Product,Category_list
from django.urls import reverse
from django.db.models import Q
def home(request):
    obj=Product.objects.all()
    obj1=Category_list.objects.all()
    return render(request,'index.html',{'obj':obj,'obj1':obj1})

def Category_lists(request,c_slug=None):
    product=None
    if c_slug:
        c_page=get_object_or_404(Category_list,slug=c_slug)
        product=Product.objects.filter(Category=c_page,availability=True)
        return render(request,'Category_lists.html',{'product':product,'c_page':c_page})
    
def product_detail(request,c_slug,product_slug):
        pro=Product.objects.get(Category__slug=c_slug, slug=product_slug)
        return render(request,'product_details.html',{'pro':pro})

def search(request):
    product=None
    query=None
    if 'q' in request.GET:
        query=request.GET.get('q')
        product=Product.objects.all().filter(Q(name__icontains=query)|Q(description__icontains=query), availability=True)
    return render(request,'search.html',{'product':product,'query':query})