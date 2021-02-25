from rest_framework import serializers
from rest_framework.exceptions import ValidationError


from .models import Follow

class FollowSerrializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Follow
