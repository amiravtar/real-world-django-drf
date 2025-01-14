from django.shortcuts import get_object_or_404, redirect
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import (
    RetrieveUpdateAPIView,
    RetrieveAPIView,
    ListCreateAPIView,
    ListAPIView,
    RetrieveUpdateDestroyAPIView,
    DestroyAPIView,
)
from rest_framework.permissions import IsAuthenticated
from user.serializers import (
    UserRegistrationSerializer,
    UserLoginSerializer,
    UserSerializer,
    ProfileSerializer,
)
from django.contrib.auth import authenticate
from blog.serializers import ArticleSerializer, CommentSerializer
from rest_framework_simplejwt.tokens import RefreshToken, Token
from django.db.models import F
from user.models import Profile
from blog.models import Article, Tag, Comment


class UserRegistration(APIView):
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data.get("user", {}))
        if serializer.is_valid():
            user = serializer.save()
            profile = Profile(user=user)
            token: Token = RefreshToken.for_user(user=user)
            profile.token = token.access_token
            profile.save()
            data = UserSerializer(user).data

            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLogin(APIView):
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
        data = UserSerializer(user).data
        return Response(data, status=status.HTTP_200_OK)


class UserView(RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class ProfileView(RetrieveAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return get_object_or_404(Profile, user__username=self.kwargs["user"])

    def get_serializer(self, *args, **kwargs):
        return self.get_serializer_class()(
            observer_user=self.request.user, instance=self.get_object()
        )


class FollowUser(APIView):
    def post(self, request, user):
        user_to_follow = get_object_or_404(Profile, user__username=user)
        if not user_to_follow.followers.contains(request.user):
            user_to_follow.followers.add(request.user)
            user_to_follow.save()
        return redirect("api:profile_view", user=user)

    def delete(self, request, user):
        user_to_unfollow = get_object_or_404(Profile, user__username=user)
        if user_to_unfollow.followers.contains(request.user):
            user_to_unfollow.followers.remove(request.user)
            user_to_unfollow.save()
        return redirect("api:profile_view", user=user)


class ArticleCreatListView(ListCreateAPIView):
    serializer_class = ArticleSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.request.method == "POST":
            # Require authentication for POST requests
            return [IsAuthenticated()]
        else:
            # Allow anonymous access for GET requests
            return []

    def get_queryset(self):
        queryset = Article.objects.all()

        # Filter by tag
        tag = self.request.query_params.get("tag")
        if tag:
            queryset = queryset.filter(tags__name=tag)

        # Filter by author
        author = self.request.query_params.get("author")
        if author:
            queryset = queryset.filter(author__user__username=author)

        # Filter by favorited
        favorited_by = self.request.query_params.get("favorited")
        if favorited_by:
            queryset = queryset.filter(favorited_by__user__username=favorited_by)

        queryset = queryset.order_by("-createdAt")

        # Apply limit and offset
        limit = self.request.query_params.get("limit", 20)
        offset = self.request.query_params.get("offset", 0)
        queryset = queryset[int(offset) : int(offset) + int(limit)]

        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        data = {"articles": serializer.data, "articlesCount": queryset.count()}
        return Response(data)


class ArticleFeedListView(ListAPIView):
    serializer_class = ArticleSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Article.objects.filter(author__in=self.request.user.followings.all())

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        data = {"articles": serializer.data, "articlesCount": queryset.count()}
        return Response(data)


class ArticleDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = ArticleSerializer
    lookup_field = "slug"
    queryset = Article.objects.all()


class ArticleFavoriteView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, slug):
        article = get_object_or_404(Article, slug=slug)
        if not article.favorited_by.contains(request.user.profile):
            article.favorited_by.add(request.user.profile)
            article.favoritesCount += F("favoritesCount") + 1
            article.save()
        return redirect("api:article_detail", slug=slug)

    def delete(self, request, slug):
        article = get_object_or_404(Article, slug=slug)
        if article.favorited_by.contains(request.user.profile):
            article.favorited_by.remove(request.user.profile)
            article.favoritesCount += F("favoritesCount") - 1
            article.save()

        return redirect("api:article_detail", slug=slug)


class TagsListView(APIView):
    def get(self, request):
        tags = Tag.objects.all()
        return Response({"tags": list(tags.values_list("name", flat=True))})


class AddGetCommentsView(ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]
    def get_permissions(self):
        if self.request.method == "POST":
            # Require authentication for POST requests
            return [IsAuthenticated()]
        else:
            # Allow anonymous access for GET requests
            return []
    def get_queryset(self):
        return Comment.objects.filter(article__slug=self.kwargs["slug"])

    def get_serializer_context(self):
        data = super().get_serializer_context()
        data["request"] = self.request
        data["slug"] = self.kwargs["slug"]
        return data

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        data = {"comments": serializer.data, "commentsCount": queryset.count()}
        return Response(data)


class DeleteCommentView(DestroyAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]
    queryset = Comment.objects.all()
    lookup_field = "id"
