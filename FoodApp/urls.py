from django.urls import path
from .views import GetUserView, CreateUserView

urlpatterns = [
    path('get-user/<int:user_id>', GetUserView.as_view(), name='get-user'), #Get
    path('create-user/', CreateUserView.as_view(), name='create-user'), #Post
]