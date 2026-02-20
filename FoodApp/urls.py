from django.urls import path
from .views.user_views import UserView

urlpatterns = [
    path('user/<int:user_id>', UserView.as_view()), #Get / Put / Delete
    path('user/', UserView.as_view()), #Post
]