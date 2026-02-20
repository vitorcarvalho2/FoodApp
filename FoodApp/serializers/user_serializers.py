# serializers.py
from rest_framework import serializers
from ..models import User, Roles
from django.contrib.auth.hashers import make_password
from django.utils import timezone
import re

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class CreateUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ["username", "phone", "email", "password", "cpf"]
        extra_kwargs = {
            "username": {"min_length": 6, "max_length": 50},
            "phone": {"required": True},
            "cpf": {"required": True},
        }

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Este email já está cadastrado.")
        return value.lower().strip()

    def validate_username(self, value):
        if len(value) < 6:
            raise serializers.ValidationError(
                "O username deve ter pelo menos 6 caracteres."
            )

        if not re.match(r"^[a-zA-Z0-9_ ]+$", value):
            raise serializers.ValidationError(
                "O username pode conter apenas letras, números e underscore (_)."
            )

        return value

    def validate_cpf(self, value):
        if not value:
            return value

        cpf = re.sub(r"[^0-9]", "", value)

        if len(cpf) != 11:
            raise serializers.ValidationError("CPF deve conter 11 dígitos.")

        if cpf == cpf[0] * 11:
            raise serializers.ValidationError("CPF inválido.")

        def calcular_digito(cpf, posicoes):
            soma = sum(int(cpf[i]) * posicoes[i] for i in range(len(posicoes)))
            resto = soma % 11
            return 0 if resto < 2 else 11 - resto

        if calcular_digito(cpf, [10, 9, 8, 7, 6, 5, 4, 3, 2]) != int(cpf[9]):
            raise serializers.ValidationError("CPF inválido.")

        if calcular_digito(cpf, [11, 10, 9, 8, 7, 6, 5, 4, 3, 2]) != int(cpf[10]):
            raise serializers.ValidationError("CPF inválido.")

        if User.objects.filter(cpf=cpf).exists():
            raise serializers.ValidationError("Este CPF já está cadastrado.")

        return cpf

    def validate_phone(self, value):
        if not value:
            raise serializers.ValidationError("O telefone é obrigatório.")

        phone = re.sub(r"[^0-9]", "", value)

        if len(phone) < 10 or len(phone) > 11:
            raise serializers.ValidationError("Telefone deve conter 10 ou 11 dígitos.")

        return phone

    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError(
                "A senha deve ter pelo menos 8 caracteres."
            )

        if not re.search(r"[a-zA-Z]", value):
            raise serializers.ValidationError(
                "A senha deve conter pelo menos uma letra."
            )

        if not re.search(r"[0-9]", value):
            raise serializers.ValidationError(
                "A senha deve conter pelo menos um número."
            )

        return value

    def validate(self, attrs):
        return attrs

    def create(self, validated_data):
        password = validated_data.pop("password")
        validated_data["password_hash"] = make_password(password)
        validated_data["role"] = Roles.objects.get(id=2)
        user = User.objects.create(**validated_data)
        return user


class EditUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ["username", "phone", "password"]
        extra_kwargs = {
            "username": {"min_length": 6, "max_length": 50},
            "password": {"write_only": True, "min_length": 8},
        }

    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError(
                "A senha deve ter pelo menos 8 caracteres."
            )

        if not re.search(r"[a-zA-Z]", value):
            raise serializers.ValidationError(
                "A senha deve conter pelo menos uma letra."
            )

        if not re.search(r"[0-9]", value):
            raise serializers.ValidationError(
                "A senha deve conter pelo menos um número."
            )
        return value

    def update(self, instance, validated_data):
        instance.username = validated_data.get("username", instance.username)
        instance.phone = validated_data.get("phone", instance.phone)
        password = validated_data.pop("password")
        instance.password_hash = make_password(password)
        instance.updated_at = timezone.now()
        instance.save(
            update_fields=["username", "phone", "password_hash", "updated_at"]
        )
        return instance