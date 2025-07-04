from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.validators import UniqueValidator

User = get_user_model()

class UserRegisterSerializer(serializers.Serializer):
    username   = serializers.CharField(
        min_length=3,
        max_length=150,
        validators=[UniqueValidator(User.objects.all())],
    )
    email      = serializers.EmailField(
        validators=[UniqueValidator(User.objects.all())],
    )
    password   = serializers.CharField(write_only=True, min_length=8)
    first_name = serializers.CharField(required=False, allow_blank=True)
    last_name  = serializers.CharField(required=False, allow_blank=True)

    def create(self, validated):
        return User.objects.create_user(
            username   = validated["username"],
            email      = validated["email"],
            password   = validated["password"],
            first_name = validated.get("first_name", ""),
            last_name  = validated.get("last_name", ""),
        )
    
class UserPublicSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "email", "first_name", "last_name")
        read_only_fields = fields