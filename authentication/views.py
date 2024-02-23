import json
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login as auth_login,logout
from django.contrib.auth.models import User
from django.contrib import messages
from .models import users,Item,rating
from django.views.decorators.cache import never_cache, cache_control






@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def home(request):
    username = request.session.get('username')
    return render(request,"authentication/index.html",{'username':username})



@never_cache
def login(request):
    logout(request)
    if request.method=="POST":
        username=request.POST['user_name']
        password=request.POST['psw']

        user=authenticate(request,username=username, password=password)
        if user is not None:
            auth_login(request,user)
            request.session['username'] = username
            return redirect('home')
        # ,"authentication/index.html",{'username':username}
            
        else:
            messages.error(request,"incorrect Credentials!")
            return redirect('home')

    return render(request,"authentication/login.html")




@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def menu(request):
    username = request.session.get('username')
    if  username is None:
        return redirect('login')
    else:
        items = rating.objects.all()
        return render(request, "authentication/menu.html",{'username':username,'items': items})




@never_cache
def reg(request):
    if request.method=="POST":
        username=request.POST['user_name']
        password=request.POST['psw']
        password2=request.POST['psw-repeat']

        myuser=users.objects.create_user(username,password)
        myuser.save()
        messages.success(request,"your account is created sucssesfully")
        return redirect("home")

    return render(request,"authentication/reg.html")




@never_cache
def signout(request):
    logout(request)
    messages.success(request, "logged out succesfully")
    return redirect('login')





@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def manage(request):
    username = request.session.get('username')
    if  username is None:
        return redirect('login')
    else:
        if request.method == 'POST':
            user = request.user
            if user is not None and user.is_authenticated:
                password = request.POST['old-password']
                newpassword = request.POST['new-password']
                reenter_newpassword = request.POST['new-password-repeat']

                # Use authenticate to check user credentials
                auth_user = authenticate(username=user.username, password=password)

                if auth_user is not None:
                    if newpassword == reenter_newpassword:
                        # Use set_password to update the password
                        auth_user.set_password(newpassword)
                        auth_user.save()
                        messages.success(request, "Profile updated successfully!")
                        return redirect('home')
                    else:
                        messages.error(request, "passwords do not match!")
                else:
                    messages.error(request, "Wrong previous password!")
            else:
                return render(request, 'authentication/index.html')
        
        user_orders = Item.objects.filter(username=username)


        ratings = rating.objects.all()
        return render(request, "authentication/manage.html",{'ordhis':user_orders,'ratings': ratings})




@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def payments(request):
    # t1=""
    # t2=0
    if request.method == 'POST':
        cartl=request.POST['cart']
    #     pairs = cartl.split(',')
    #     print(pairs)
    #     for i in pairs:
    #         a = i.split(':')
    #         t1+=a[0]+","
    #         t2+=int(a[1])
    #     t1=t1[0:len(t1)-1]
    request.session['cartl'] = cartl
    username = request.session.get('username')
    return render(request,"authentication/payments.html",{'username':username})




def conforder(request):
    username = request.session.get('username')
    t1=""
    t2=0
    if request.method == 'POST':
        cartl = request.session.get('cartl')
        pairs = cartl.split(',')
        print(pairs)
        for i in pairs:
            a = i.split(':')
            t1+=a[0]+","
            t2+=int(a[1])
        t1=t1[0:len(t1)-1]
        item=Item.objects.create(username=username,name=t1,totalprice=t2)
        item.save()
        return redirect('home')
    




def ratings(request):
    if request.method == 'POST':
        iname=request.POST['productId']
        irating=request.POST['rating']

        item=rating.objects.create(name='Dum-Biryani',rating=5)
        item.save()
        
        pr = rating.objects.filter(id=iname)
        update = rating.objects.get(id=iname)
        for r in pr:
            a=(r.rating+int(irating))/2
        update.rating = a
        update.save()
        return redirect('manage')