from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Profile


class UserRegistrationSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
        )
        return user


class UserLoginSerializer(serializers.Serializer):
    # make email and password field that are required
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)


class UserSerializer(serializers.ModelSerializer):
    token = serializers.SerializerMethodField()
    bio = serializers.CharField(source="profile.bio", read_only=True)
    image = serializers.CharField(source="profile.image", read_only=True)

    class Meta:
        model = User
        fields = ("username", "email", "token", "bio", "image")

    def get_token(self, obj):
        try:
            profile: Profile = obj.profile
            token: str | None = profile.token
            if token:
                return str(token)
        except:
            pass
        # If token doesn't exist or is expired, generate a new token
        refresh = RefreshToken.for_user(obj)
        return str(refresh.access_token)
    def to_representation(self, instance):
        data = super().to_representation(instance)
        return {'user': data}