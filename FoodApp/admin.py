from django.contrib import admin
from .models import FoodCategory, OptionGroups, Product, OrderItems, Order, Restaurant, User, Address, RestaurantCategory, RestaurantReview, Options, OrderItemOptions

## fixos
from .models import Roles, OrderStatus

## Register your models here.
admin.site.register(User)
admin.site.register(Restaurant)
admin.site.register(Address)
admin.site.register(RestaurantReview)
admin.site.register(Order)
admin.site.register(Product)
admin.site.register(OptionGroups)
admin.site.register(Options)
admin.site.register(OrderItems)
admin.site.register(OrderItemOptions)
admin.site.register(FoodCategory)
admin.site.register(RestaurantCategory)
admin.site.register(Roles)
admin.site.register(OrderStatus)