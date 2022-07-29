from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login

from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import User

class AuthUserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'email',
            'password',
            'phone_number'
        )

    def create(self, validated_data):
        auth_user = User.objects.create_user(**validated_data)
        return auth_user

class AuthUserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(max_length=128, write_only=True)
    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)
    role = serializers.CharField(read_only=True)

    def create(self, validated_date):
        pass

    def update(self, instance, validated_data):
        pass
    

    def validate(self, data):
        email = data['email']
        password = data['password']
        user = authenticate(email=email, password=password)

        if user is None:
            raise serializers.ValidationError("Invalid login credentials")

        try:
            refresh = RefreshToken.for_user(user)
            refresh['role'] = user.role

            refresh_token = str(refresh)
            access_token = str(refresh.access_token)

            update_last_login(None, user)

            validation = {
                'access': access_token,
                'refresh': refresh_token,
                'email': user.email,
                #'full_name': user.get_full_name(),
                'role': user.role,
            }

            return validation
        except User.DoesNotExist:
            raise serializers.ValidationError("Invalid login credentials")
        
        
class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # fields = (
        #     'email',
        #     'role',
        #     'phone_number',
        # )
        fields = '__all__'
        
        
# Custom Serializer for custom jwt
# class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
#     # Override get_token of TokenObtainPairSerializer
#     def get_token(cls, user):
#         # Get token from TokenObtainPairSerializer
#         token = super().get_token(user)

#         # Adding role to token
#         token['role'] = user.profile.role

#         return token