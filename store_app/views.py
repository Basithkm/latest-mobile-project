from django.shortcuts import render,redirect
from django.http import HttpResponse
from . models import *
from django.http import JsonResponse
from django.urls import reverse
from django.shortcuts import render,redirect,get_object_or_404
from django.views.decorators.csrf import csrf_exempt
import json
import razorpay

from cart.forms import CartAddProductForm


# Create your views here.



def index(request):
    product= MobileBrand.objects.all()
    context ={
        'brand_products':product
    }
    return render(request,'store/index.html',context)


def filter_brand(request,id):
    product = PhoneName.objects.filter(brand_name=id)
    context ={
        'phone_product':product
    }
    return render(request,'store/brand_page.html',context)



def filter_phone(request,id):
    product = MobilePouch.objects.filter(phone_name=id)
    context ={
        'pouch_product':product
    }
    return render(request,'store/brand_page.html',context)




def spaceautocomplete(request):
    if request.method == 'GET':
        # Retrieve search query from GET request
        query = request.GET.get('term', '')

        # Filter products based on search query
        products = MobilePouch.objects.filter(
            phone_name__phone_name__icontains=query,
            brand_name__brand_name__icontains=query,
            product_name__icontains=query
        )


        data = []
        for product in products:
            data.append(product.product_name)
            data.append(product.phone_name.phone_name)
            data.append(product.brand_name.brand_name)
            
  
            

        # Remove duplicates and empty strings
        data = list(set(filter(None, data)))

        # Return data as JSON response
        return JsonResponse(data, safe=False)
    

def search(request):
    if request.method == 'GET':
 
        # Retrieve search query from GET request
        query = request.GET.get('query', '')

        # Filter products based on search query
        products = MobilePouch.objects.filter(phone_name__phone_name__icontains=query)

        context = {

            'search_product':products,
        }
           
    context = {

            'search_product':products,
 
        }
    return render(request,'store/brand_page.html', context)


def product_inner_page(request,id):
    product = MobilePouch.objects.get(id=id)
    cart_product_form = CartAddProductForm()

    
    context ={
    
        'product':product,
        'cart_product_form':cart_product_form
    }
    return render(request,'store/product_inner_page.html',context)




