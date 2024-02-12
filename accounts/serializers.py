from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}
    
class LoginDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [ 'email', 'username']


class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username','password']