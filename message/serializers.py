from rest_framework import serializers
from django.contrib.auth.models import User


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'first_name', 'last_name']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
        )
        return user


# class LoginUserSerializer(serializers.Serializer):
#     username = serializers.CharField(max_length=50)
#     password = serializers.CharField(max_length=100)
#
#     def validate(self, attrs):
#         username = attrs.get('username')
#         password = attrs.get('password')
#         user = User.objects.filter(username=username, password=password)
#         if not user:
#             raise serializers.ValidationError('username or password wrong')
#
#         return attrs
