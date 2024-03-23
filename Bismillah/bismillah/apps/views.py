from django.shortcuts import render,redirect
from . import models
from .models import *
# Create your views here.

# homepage
from django.contrib.auth.decorators import login_required
@login_required(login_url="/login_pg")
def home(request):
    alldata=rice.objects.all()
    context={'data':alldata}
    images=request.FILES.get('images')
    return render(request,"home.html",context)

# registration
from django.contrib.auth.models import User
from django.contrib import messages
def Registration(request):
    if request.method=="POST":
        first_name=request.POST.get("first_name")
        last_name=request.POST.get("last_name")
        username=request.POST.get("username")
        password=request.POST.get("password")

        user=User.objects.filter(username=username)
        if user.exists():
            messages.info(request,"username is already exists ,choos another username")
            return redirect("/registration_pg")
        user=User.objects.create(
            first_name=first_name,
            last_name=last_name,
            username=username
        )
        user.set_password(password)
        user.save()
        messages.info(request,"Successfully register")
        return redirect("/registration_pg")
    return render(request,"Registration.html")

# login
from django.contrib.auth import authenticate,login
def Login(request):
    if request.method == "POST":
        username=request.POST.get("username")
        password=request.POST.get("password")

        user=User.objects.filter(username=username)
        if not user.exists():
            messages.error(request,"invalid usename")
            return redirect("/login_pg")
        checkauthentication=authenticate(username=username,password=password)
        if checkauthentication is None:
            messages.error(request,"Invalid password")
            return redirect("/login_pg")
        else:
            login(request,checkauthentication)
            return redirect("/")
    return render(request,"Login.html")

# logout
from django.contrib.auth import logout
def Logout(request):
    logout(request)
    return redirect("/login_pg")

# add cart
def add_cart(request,rice_uid):
    user=request.user
    rice_obj=rice.objects.get(uid=rice_uid)
    cart , _ =Cart.objects.get_or_create(user=user,is_paid=False)

    cart_items=cartItems.objects.create(
        cart=cart,
        rice=rice_obj
    )
    return redirect("/")

# insta mojo se try karte time ka code
# from instamojo_wrapper import Instamojo #ye payment k liye instamojo import kiye
# from django.conf import settings
# api = Instamojo(api_key=settings.API_KEY,
#                 auth_token=settings.AUTH_TOKEN ,endpoint="https://test.instamojo.com/api/1.1/")

#
# # razorpay
# import razorpay
# from django.conf import settings
# from .models import cartItems
# # cart show
# client = razorpay.Client(auth=(settings.RAZORPAY_API_KEY, settings.RAZORPAY_API_SECRERT_KEY))
# def cart(request):
#     cart=Cart.objects.get(is_paid=False,user=request.user)
#     # ye rozarpay integration
#     current_user = request.user
#     amount = int(Cart.objects.filter(user=current_user, is_paid=False).first())*100
#     if amount:
#         # Call the get_total() method to calculate the total
#         amount = amount.get_total()
#     else:
#         amount = 0
#     # print(amount)
#     currency='INR'
#     payment = client.order.create({'amount': amount, 'currency': currency,'payment_capture': 1})
#     payment_id=payment['id']
#     data={"carts":cart,"amount":amount,'api_key':settings.RAZORPAY_API_KEY,'payment_id':payment_id}
#
#
#     # # ye use karenge payment k liye insta mojo
#     # response=api.payment_request_create(
#     #     amount=cart.get_total(),
#     #     purpose="order",
#     #     buyer_name=request.user.username,
#     #     email="shaikhlaptop8691@gmail.com",
#     #     redirect_url="http://127.0.0.1:8000/success/"
#     # )
#     # print(response)
#
#
#     return render(request,"cart.html",data)

# razorpay
import razorpay
from django.conf import settings
from .models import cartItems

# cart show
client = razorpay.Client(auth=(settings.RAZORPAY_API_KEY, settings.RAZORPAY_API_SECRERT_KEY))
def cart(request):
    cart = Cart.objects.get(is_paid=False, user=request.user)
    # Calculate the total amount using the get_total() method
    amount = cart.get_total() * 100
    currency = 'INR'
    payment = client.order.create({'amount': amount, 'currency': currency, 'payment_capture': 1})
    payment_id = payment['id']
    data = {"carts": cart, "amount": amount, 'api_key': settings.RAZORPAY_API_KEY, 'payment_id': payment_id}
    return render(request, "cart.html", data)


# Delete items
def remove_cart_items(request,cart_item_uid):
    try:
        cartItems.objects.get(uid=cart_item_uid).delete()
        return redirect("cart")
    except Exception as e:
        print(e)


def orders(request):
    orders=Cart.objects.filter(is_paid=True,user=request.user)
    context={"data":orders}
    return render(request,"orders.html",context)