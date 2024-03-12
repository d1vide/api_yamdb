from rest_framework import serializers
from django.shortcuts import get_object_or_404
from django.db.models import Avg, IntegerField

from reviews.models import Category, Comment, Genre, Review, Title, TitleGenre
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор модели User."""
    email = serializers.EmailField(max_length=254, required=True)
    username = serializers.SlugField(max_length=50, required=True)

    class Meta:
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )
        model = User
        read_only_field = ('role',)

    def validate(self, data):
        email = data.get('email')
        username = data.get('username')
        if (not User.objects.filter(email=email).exists()
                and User.objects.filter(username=username).exists()):
            raise serializers.ValidationError(
                'Эта электронная почта уже занята".'
            )
        if (User.objects.filter(email=email).exists()
                and not User.objects.filter(username=username).exists()):
            raise serializers.ValidationError(
                'Эта электронная почта уже занята.'
            )
        if username == 'me':
            raise serializers.ValidationError(
                'Нельзя использовать "me" как имя.'
            )
        return data


class JWTSerializer(serializers.Serializer):
    """Сериализатор запроса JWT токена."""
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        exclude = ('id',)


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        exclude = ('id',)


class TitleGenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = TitleGenre
        exclude = ('id',)


class TitleGetSerializer(serializers.ModelSerializer):
    category = CategorySerializer(many=False, read_only=True)
    genre = GenreSerializer(many=True, read_only=True)
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'description', 'genre', 'category',
                  'rating')

    def get_rating(self, obj):
        rating = Review.objects.filter(title_id=obj.pk).aggregate(
            Avg('score', output_field=IntegerField()))
        return rating['score__avg']


class TitleSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(slug_field='slug',
                                            queryset=Category.objects.all())
    genre = serializers.SlugRelatedField(slug_field='slug',
                                         queryset=Genre.objects.all(),
                                         many=True)

    def to_representation(self, instance):
        serializer = TitleGetSerializer(instance)
        return serializer.data

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)

    class Meta:
        model = Title
        fields = ('name', 'year', 'description', 'category', 'genre',)


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault()
    )
    title = serializers.SlugRelatedField(
        slug_field='id',
        many=False,
        read_only=True
    )

    class Meta:
        model = Review
        fields = '__all__'

    def validate(self, data):
        if self.context['request'].method != 'POST':
            return data
        title = get_object_or_404(
            Title, pk=self.context['view'].kwargs.get('title_id')
        )
        author = self.context['request'].user
        if Review.objects.filter(title_id=title, author=author).exists():
            raise serializers.ValidationError(
                'Вы уже оставили отзыв!'
            )
        return data


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault()
    )
    review = serializers.SlugRelatedField(
        slug_field='text',
        many=False,
        read_only=True
    )

    class Meta:
        model = Comment
        fields = '__all__'
