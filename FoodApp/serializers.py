# serializers.py
from rest_framework import serializers
from .models import User
from django.utils import timezone
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'role', 'phone']

    def create(self, validated_data):
        user = User.objects.create_user(
            full_name=validated_data['full_name'],
            email=validated_data['email'],
            password=validated_data['password'],
            role= "user",
            is_staff=False,
            is_active=True,
            date_joined=timezone.now(),
            phone=validated_data['phone']
        )
        return user
