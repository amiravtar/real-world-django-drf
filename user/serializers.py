from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Profile

User = get_user_model()


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
    token = serializers.SerializerMethodField(read_only=True)
    bio = serializers.CharField(source="profile.bio", required=False)
    image = serializers.CharField(source="profile.image", required=False)

    class Meta:
        model = User
        fields = ("username", "email", "token", "bio", "image", "password")
        extra_kwargs = {
            "password": {"write_only": True, "required": False},
            "username": {"required": False},
            "email": {"required": False},
        }

    def update(self, instance, validated_data: dict):
        profile_data = validated_data.pop("profile", None)
        if profile_data:
            profile = instance.profile
            for attr, value in profile_data.items():
                setattr(profile, attr, value)
            profile.save()
        if password := validated_data.pop("password", None):
            instance.set_password(password)
        return super().update(instance, validated_data)

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
        return {"user": data}

    def to_internal_value(self, data):
        # Convert nested "user" data to flat representation
        if "user" in data:
            data = data["user"]
        return super().to_internal_value(data)


class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username", read_only=True)
    following = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Profile
        fields = ["bio", "username", "image", "following"]
        extra_kwargs = {"image": {"default": ""}}

    def __init__(self, observer_user, instance=None, data=..., **kwargs):
        self.observer_user = observer_user
        super().__init__(instance, **kwargs)

    def get_following(self, obj: Profile):
        if not self.observer_user.is_authenticated:
            return False
        if obj.followers.contains(self.observer_user):
            return True
        return False

    def to_representation(self, instance):
        data = super().to_representation(instance)
        return {"profile": data}
