from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from user.serializers import UserRegistrationSerializer, UserLoginSerializer,UserSerializer
from rest_framework_simplejwt.tokens import RefreshToken, Token
from django.contrib.auth import authenticate


from user.models import Profile


class UserRegistrationAPIView(APIView):
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data.get("user", {}))
        if serializer.is_valid():
            user = serializer.save()
            profile = Profile(user=user)
            token: Token = RefreshToken.for_user(user=user)
            profile.token=token.access_token
            profile.save()
            data=UserSerializer(user).data
            
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginAPIView(APIView):
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data.get("user", {}))
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        email = serializer.validated_data.get("email")
        password = serializer.validated_data.get("password")
        user = authenticate(username=email, password=password)
        if not user:
            return Response(
                {"message": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED
            )
        data=UserSerializer(user).data
        return Response(data, status=status.HTTP_200_OK)
