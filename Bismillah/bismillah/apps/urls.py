from django.contrib import admin
from django.urls import path,include
from . import views
urlpatterns = [
    path("",views.home,name="home"),
    path("registration_pg",views.Registration,name="Registration"),
    path("login_pg",views.Login,name="Login"),
    path("logout_pg",views.Logout,name="Logout"),
    path('add_cart/<rice_uid>/',views.add_cart,name="add_cart"),
    path("cart",views.cart,name="cart"),
    path("delete_items/<cart_item_uid>/",views.remove_cart_items,name="delete_items"),
    path("order",views.orders,name="order"),

]

# for media file
from django.conf import settings
from django.conf.urls.static import static
if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL,
                        document_root=settings.MEDIA_ROOT)