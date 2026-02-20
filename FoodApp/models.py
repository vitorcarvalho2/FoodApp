from django.db import models
from django.db.models import Q

class User(models.Model):
    username = models.CharField(max_length=100)
    role = models.ForeignKey('Roles', on_delete=models.SET_NULL, null=True)
    phone = models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    password_hash = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    cpf = models.CharField(max_length=14, unique=True, blank=True, null=True)
    
    def __str__(self):
        return self.username


class Restaurant(models.Model):
    name = models.CharField(max_length=100)
    owner_id = models.ForeignKey(User, on_delete=models.CASCADE)
    cnpj = models.CharField(max_length=20, unique=True)
    profile_picture = models.URLField(blank=True, null=True)
    profile_banner = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.name
    

class Roles(models.Model):
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        verbose_name = "Role"
        verbose_name_plural = "Roles"

    def __str__(self):
        return self.name
class Address(models.Model):
    street = models.CharField(max_length=200)
    number = models.CharField(max_length=20)
    complement = models.CharField(max_length=100)
    neighborhood = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=20)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)

    user_id = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, limit_choices_to={'is_staff': False})
    restaurant_id = models.ForeignKey(Restaurant, on_delete=models.CASCADE, blank=True, null=True, limit_choices_to={'is_staff': False})

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Address"
        verbose_name_plural = "Addresses"
        constraints = [
            models.CheckConstraint(
                condition=(
                    Q(user_id__isnull=False, restaurant_id__isnull=True) |
                    Q(user_id__isnull=True, restaurant_id__isnull=False)
                ),
                name='address_user_xor_restaurant'
            )
        ]
    def __str__(self):
        return f"{self.street}, {self.number} - {self.city}/{self.state}"

class RestaurantReview(models.Model):
    restaurant_id = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField()
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Review by {self.user_id.username} for {self.restaurant_id.name}"
    
    

class Order(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    restaurant_id = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    status = models.ForeignKey('OrderStatus', on_delete=models.SET_NULL, null=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class OrderStatus(models.Model):
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        verbose_name = "Order Status"
        verbose_name_plural = "Order Status"

    def __str__(self):
        return self.name
    
class Product(models.Model):
    restaurant_id = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    photo = models.URLField(blank=True, null=True)
    base_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"

    def __str__(self):
        return f"{self.name} - {self.restaurant_id.name}"
    
class OptionGroups(models.Model):
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    is_required = models.BooleanField(default=False)
    min_selection = models.IntegerField(default=0)
    max_selection = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Option Groups"
        verbose_name_plural = "Option Groups"

    def __str__(self):
        return f"{self.name} - {self.product_id.name}"
    

class Options(models.Model):
    option_group_id = models.ForeignKey(OptionGroups, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    extra_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Options"
        verbose_name_plural = "Options"

    def __str__(self):
        return f"{self.name} - {self.option_group_id.name}"
    
class OrderItems(models.Model):
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    base_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Order Items"
        verbose_name_plural = "Order Items"
    def __str__(self):
        return f"{self.quantity}x {self.product_id.name} for Order #{self.order_id.id}"
    
class OrderItemOptions(models.Model):
    order_item_id = models.ForeignKey(OrderItems, on_delete=models.CASCADE)
    option_id = models.ForeignKey(Options, on_delete=models.CASCADE)
    
    class Meta:
        verbose_name = "Order Item Options"
        verbose_name_plural = "Order Item Options"

    def __str__(self):
        return f"{self.option_id.name} for {self.order_item_id.product_id.name}"
    
class FoodCategory(models.Model):
    name = models.CharField(max_length=100)
    photo = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Food Category"
        verbose_name_plural = "Food Categories"

    def __str__(self):
        return self.name
    
class RestaurantCategory(models.Model):
    restaurant_id = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    food_category_id = models.ForeignKey(FoodCategory, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Restaurant Category"
        verbose_name_plural = "Restaurant Categories"
        constraints = [
            models.UniqueConstraint(
                fields=['restaurant_id', 'food_category_id'],
                name='unique_restaurant_food_category'
            )
        ]

    def __str__(self):
        return f"{self.restaurant_id.name} - {self.category_id.name}"