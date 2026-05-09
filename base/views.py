from django.shortcuts import render,redirect
from .models import *
from django.db.models import Q
from django.contrib.auth.decorators import login_required

# Create your views here.
def home(request):
    if request.user.is_authenticated:
        cartproducts_count = CartModel.objects.filter(host = request.user).count()
    else:
        cartproducts_count= False
    # print(request.method)
    # print(request.GET)#<QueryDict: {}> <QueryDict: {'q': ['DELL']}>
    no_match = False
    trend = False
    offer = False
    if 'q' in request.GET:
        q = request.GET['q']
        print(q)#dell
        all_products = Product.objects.filter(Q(pname__icontains=q) | Q(pdesc__icontains=q))
        print(len(all_products))#<QuerySet []>
        if len(all_products)==0:
            no_match = 'True'
       
    elif 'cat' in request.GET:
        cat = request.GET['cat']
        all_products = Product.objects.filter(pcategory = cat)
    elif 'trending' in request.GET:
        all_products = Product.objects.filter(trending = True)
        trend = True
    elif 'offer' in request.GET:
        all_products = Product.objects.filter(offer = True)
        offer = True
    else:
        all_products = Product.objects.all()
    
    #category check
    category = []
    a = Product.objects.all()
    for i in a:
        # print(i.pcategory)
        if i.pcategory not in category:
            category+=[i.pcategory]
    # print(category)
    print(cartproducts_count)
    return render(request,'home.html',{'all_products':all_products,'no_match':no_match,'category':category,'home':True,'cartproduct_count':cartproducts_count,'trend':trend,'offer':offer})

@login_required(login_url='login_')
def addtocart(request,id):
    product = Product.objects.get(id=id)
    try:
        cp = CartModel.objects.get(pname = product.pname,host=request.user)#get will throw error when the particular  product is not present in db
        #if product is not prsent in cartmodel the product need to be create in db
        #if get is not returning error that time we need to update quantity and totalprice
        cp.quantity+=1
        cp.totalprice+=product.price
        cp.save()
    except:
        CartModel.objects.create(
            pname = product.pname,
            price = product.price,
            pcategory = product.pcategory,
            quantity = 1,
            totalprice = product.price,
            host = request.user
        )
    return redirect('home')

def cart(request):
    cartproducts_count = CartModel.objects.filter(host = request.user).count()
    # print(cartproducts_count)
    TA = 0
    cartproducts = CartModel.objects.filter(host = request.user)
    for i in cartproducts:
        # print(i.totalprice)
        TA+=i.totalprice
    # print(TA)#340000
    return render(request,'cart.html',{'cartproducts':cartproducts,'TA': TA,'cartproduct_count':cartproducts_count})

def remove(request,id):
    cartproduct = CartModel.objects.get(id=id)
    cartproduct.delete()
    return redirect('cart')

def increment(request,id):
    cartproduct = CartModel.objects.get(id=id)
    cartproduct.quantity+=1
    cartproduct.totalprice += cartproduct.price
    
    cartproduct.save()
    return redirect('cart')

def decrement(request,id):
    cartproduct = CartModel.objects.get(id=id)
    if cartproduct.quantity>1:
        cartproduct.quantity-=1
        cartproduct.totalprice -= cartproduct.price
        cartproduct.save()
    else:
        cartproduct.delete()
    return redirect('cart')

def about(request):
    cartproduct_count = 0
    if request.user.is_authenticated:
        cartproduct_count = CartModel.objects.filter(host = request.user).count()
    return render(request,'about.html',{'cartproduct_count':cartproduct_count})

def support(request):
    cartproduct_count = 0
    if request.user.is_authenticated:
        cartproduct_count = CartModel.objects.filter(host = request.user).count()
    
    return render(request,'support.html',{'cartproduct_count':cartproduct_count})