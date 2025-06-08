from rest_framework import serializers
from django.contrib.auth import get_user_model
from movies.models import Movie, Article
from django.contrib.auth.password_validation import validate_password
from rest_framework.validators import UniqueValidator

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("pk", "username", "profile_pic")


class ArticleMovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = (
            "pk",
            "title",
        )


class SimpleMovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ("pk", "title", "poster_path")


class ProfileSerializer(serializers.ModelSerializer):
    class FollowFollowingSerializer(serializers.ModelSerializer):
        class Meta:
            model = User
            fields = ("id", "username", "profile_pic")

    class ArticleSerializer(serializers.ModelSerializer):
        class LikeUserSerializer(serializers.ModelSerializer):
            class Meta:
                model = User
                fields = ("pk",)

        like_users = LikeUserSerializer(read_only=True)
        like_user_count = serializers.IntegerField(
            source="like_users.count", read_only=True
        )
        movie = SimpleMovieSerializer(read_only=True)
        user = UserSerializer(read_only=True)

        class Meta:
            model = Article
            fields = "__all__"
            read_only_fields = ("movie",)

    class MovieSerializer(serializers.ModelSerializer):
        class Meta:
            model = Movie
            fields = (
                "id",
                "title",
                "overview",
                "poster_path",
                "release_date",
                "like_users",
            )

    followers = FollowFollowingSerializer(many=True, read_only=True)
    followings = FollowFollowingSerializer(many=True, read_only=True)
    follower_count = serializers.IntegerField(source="followers.count", read_only=True)
    following_count = serializers.IntegerField(
        source="followings.count", read_only=True
    )
    articles = ArticleSerializer(many=True)
    like_movies = MovieSerializer(many=True)
    articles_count = serializers.IntegerField(source="articles.count", read_only=True)
    like_count = serializers.SerializerMethodField()

    def get_like_count(self, obj):
        return obj.like_articles.count()

    class Meta:
        model = User
        fields = "__all__"



# 회원정보 수정
class ProfileUpdateSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())],
    )
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())],
    )

    class Meta:
        model = User
        fields = ("profile_pic", "username", "email")  # ← email 추가!

# 비밀번호 변경
class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True, required=True)
    new_password = serializers.CharField(write_only=True, required=True)

    def validate_new_password(self, value):
        validate_password(value)  # Django 기본 비밀번호 정책 검사
        return value

    def validate(self, attrs):
        user = self.context['request'].user
        if not user.check_password(attrs['old_password']):
            raise serializers.ValidationError({"old_password": "기존 비밀번호가 틀렸습니다."})
        return attrs

    def save(self, **kwargs):
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])
        user.save()
        return user


class LikeProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ("id", "user", "like_users")


