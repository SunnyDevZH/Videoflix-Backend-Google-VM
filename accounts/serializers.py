from rest_framework import serializers
from django.contrib.auth.models import User

class RegisterSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration.
    - Accepts email and password.
    - Creates a new user with the email as the username.
    """
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'password']

    def create(self, validated_data):
        """
        Creates a new user with the provided email and password.
        """
        email = validated_data['email']
        user = User.objects.create_user(
            username=email,  
            email=email,
            password=validated_data['password']
        )
        return user