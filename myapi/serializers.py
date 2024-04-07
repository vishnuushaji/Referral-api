from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    timestamp_of_registration = serializers.DateTimeField(source='date_joined', read_only=True)

    class Meta:
        model = User
        fields = ('id', 'email', 'referral_code', 'timestamp_of_registration')
