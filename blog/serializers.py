from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Article, Tag
from user.serializers import ProfileSerializer

User = get_user_model()


class ArticleSerializer(serializers.ModelSerializer):
    tagList = serializers.SerializerMethodField()
    createdAt = serializers.DateTimeField(
        format="%Y-%m-%dT%H:%M:%S.%fZ", required=False
    )
    updatedAt = serializers.DateTimeField(
        format="%Y-%m-%dT%H:%M:%S.%fZ", required=False
    )
    author = serializers.SerializerMethodField(read_only=True)
    favorited=serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Article
        fields = [
            "slug",
            # "author",
            "title",
            "description",
            "body",
            "createdAt",
            "updatedAt",
            "favoritesCount",
            "tagList",
            "author",
            "favorited"
        ]

    def __init__(self, observer_user=None, *args, **kwargs):
        # Extract the required variable from kwargs
        self.observer_user = observer_user
        super().__init__(*args, **kwargs)
        # Pass the variable to ProfileSerializer when initializing

    def create(self, validated_data):
        tag_names = validated_data.pop("tagList", [])

        # Create the article
        article = Article.objects.create(
            author=self.observer_user.profile, **validated_data
        )

        # Create or retrieve tags and associate them with the article
        for tag_name in tag_names:
            tag, _ = Tag.objects.get_or_create(name=tag_name)
            article.tags.add(tag)
            tag.save()
        return article

    def get_tagList(self, instance: Article):
        return list(instance.tags.values_list("name", flat=True))

    def get_author(self, instance: Article):
        if self.observer_user and self.instance:
            return ProfileSerializer(
                observer_user=self.observer_user, instance=instance.author
            ).data
    def get_favorited(self, obj: Article):
        if not self.observer_user:
            return False
        if self.observer_user.profile.favorite_articles.contains(obj):
            return True
        return False
    def to_internal_value(self, data: dict):
        if "article" not in data:
            raise serializers.ValidationError("Incomming json is not valid")
        data = data["article"]
        tagslist = data.pop("tagList", [])
        data = super().to_internal_value(data)
        data["tagList"] = tagslist
        return data

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["author"] = data["author"]["profile"]
        return {"article": data}
