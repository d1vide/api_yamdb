from rest_framework import serializers

from reviews.models import Category, Genre, Title, TitleGenre


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

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'description', 'genre', 'category',)


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
