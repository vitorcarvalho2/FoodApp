from django.contrib import admin

# Register your models here.
from .models import FoodCategory, OptionGroups, Products, OrderItems, Orders, Restaurant, User, Address, RestaurantCategory, RestaurntReview, Options, OrderItemOptions

admin.site.register(User)
admin.site.register(Restaurant)
admin.site.register(Address)
admin.site.register(RestaurntReview)
admin.site.register(Orders)
admin.site.register(Products)
admin.site.register(OptionGroups)
admin.site.register(Options)
admin.site.register(OrderItems)
admin.site.register(OrderItemOptions)
admin.site.register(FoodCategory)
admin.site.register(RestaurantCategory)