from rest_framework import serializers
from rest_framework.generics import get_object_or_404
from rest_framework.relations import SlugRelatedField

from reviews.models import Category, Comment, Genre, Review, Title, User

from .xclasses import ContextTitle


class UserSerializer(serializers.ModelSerializer):
    role = serializers.CharField(default=User.USER)

    class Meta:
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role',
        )
        read_only_fields = ('role',)
        model = User

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError('username не может быть: me')
        return value

    def validate_role(self, value):
        if value not in [User.USER, User.MODERATOR, User.ADMIN]:
            raise serializers.ValidationError(
                'Вы не можете назначать произвольные роли.'
                'Доступные: user, moderator, admin'
            )
        return value

    def update(self, instance, validated_data):
        if instance.is_user:
            validated_data['role'] = User.USER
        return super().update(instance, validated_data)


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)

    def validate_username(self, value):
        get_object_or_404(User, username=value)
        return value

    def validate(self, data):
        if not User.objects.filter(
            confirmation_code=data['confirmation_code']
        ).exists():
            raise serializers.ValidationError(
                'Неправильный confirmation code.'
            )
        return data


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        exclude = ('id',)
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        exclude = ('id',)
        model = Genre


class TitleWriteSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        slug_field='slug', queryset=Category.objects.all()
    )
    genre = serializers.SlugRelatedField(
        slug_field='slug', queryset=Genre.objects.all(), many=True
    )

    class Meta:
        fields = '__all__'
        model = Title


class TitleReadSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(read_only=True, many=True)
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        fields = '__all__'
        model = Title


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault(),
    )

    title = serializers.HiddenField(default=ContextTitle())

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date', 'title')


class CommentSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        model = Comment
