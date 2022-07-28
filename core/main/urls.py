from django.urls import path
from .views import *


urlpatterns = [
    path('', HomeListView.as_view(), name='home'),
    path('shop/', ShopListView.as_view(), name='shop'),
    path("register/", register_request, name="register"),
    path("login/", login_request, name="login"),
    path("logout", logout_request, name="logout"),
    path("add-to-cart", add_to_cart, name="add-to-cart"),
    path("cart_quantity_update", cart_quantity_update, name="cart_quantity_update"),
    path("cart_quantity_delete", cart_quantity_delete, name="cart_quantity_delete"),
    path("cart", cartview, name="cart"),

]