from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from base.models import CartModel

# Create your views here.
def login_(request):
    print("METHOD: ", request.method)
    print("GET:  ", request.GET)
    print("POST: ", request.POST)
    if request.method == 'POST':
        a = request.POST['username']
        b = request.POST['password']
        u = authenticate(username = a,password = b)
        if u:
            login(request,u)
            return redirect('home')
        else:
            return render(request,'login_.html',{'status':'username or password are invalid'})
    return render(request,'login_.html')

def register(request):
    if request.method == 'POST':
        a = request.POST['fname']
        b = request.POST['lname']
        c = request.POST['email']
        d = request.POST['username']
        e = request.POST['password']
        try:
            v= User.objects.get(username=d)
            return render(request,'register.html',{'status':'username already exists'})
        except:
            u = User.objects.create(
            first_name = a,
            last_name = b,
            email = c,
            username = d,
            )
            u.set_password(e)
            u.save()
    return render(request,'register.html')

@login_required(login_url='login_')
def profile(request):
    cartproduct_count = CartModel.objects.filter(host = request.user).count() 
    return render(request,'profile.html',{'cartproduct_count':cartproduct_count})

@login_required(login_url='login_')
def logout_(request):
    logout(request)
    return redirect('login_')

@login_required(login_url='login_')
def reset_pass(request):
    cartproduct_count = CartModel.objects.filter(host = request.user).count()
    if request.method == 'POST':
        if 'oldpasw' in request.POST:
            a = request.POST['oldpasw']
            auth = authenticate(username=request.user.username,password=a)
            if auth:
                return render(request,'reset_pass.html',{'new_pass':True})
            else:
                return render(request,'reset_pass.html',{'wrong':True})
        if 'newpasw' in request.POST:
            b=request.POST['newpasw']
            if request.user.check_password(b):
                return render(request,'reset_pass.html',{'same':True})
            request.user.set_password(b)
            request.user.save()
            return redirect('login_')
    return render(request,'reset_pass.html',{'cartproduct_count':cartproduct_count})

def forget_pass(request):
    if request.method == 'POST':
        u = request.POST['username']
        try:
            a = User.objects.get(username=u)
            request.session['fp_user']=a.username
            return redirect('new_password')
        except:
            return render(request,'forget_pass.html',{'error':True})
    return render(request,'forget_pass.html')

def new_password(request):
    username = request.session.get('fp_user')
    if username is None:
        return redirect('forget_pass')
    user = User.objects.get(username=username)
    if request.method == 'POST':
        new = request.POST['password']
        if user.check_password(new): 
            return render(request,'new_password.html',{'error':True})
        user.set_password(new)
        user.save()
        del request.session['fp_user']
        return redirect('login_')
    return render(request,'new_password.html')


'''
write logic for 
register
login
profile
logout
reset password
forgot password
'''