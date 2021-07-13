from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'first_name',
                'last_name', 'address', 'avatar', 'phone',
                'last_login'
                ]
        read_only_fields = ['last_login', 'id']