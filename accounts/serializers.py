from rest_framework import serializers
from .models import CustomUser
from django.contrib.auth import authenticate


# 🟢 Register Serializer
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'phone']

    def create(self, validated_data):
        return CustomUser.objects.create_user(**validated_data)


# 🟢 Login Serializer (email login)
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(
            username=data['email'],   # 🔥 email is used as username
            password=data['password']
        )
        if not user:
            raise serializers.ValidationError("Invalid credentials")
        return user


# 🟢 Profile Serializer
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'phone']
