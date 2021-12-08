import uuid

from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import constraints

from api.validators import year_validator


class User(AbstractUser):
    USER = 'user'
    ADMIN = 'admin'
    MODERATOR = 'moderator'
    ROLES = ((USER, 'user'), (MODERATOR, 'moderator'), (ADMIN, 'admin'))
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=10, choices=ROLES, verbose_name='Роль')
    confirmation_code = models.CharField(
        max_length=50,
        null=False,
        default=uuid.uuid4(),
        verbose_name='Код подтверждения',
    )
    bio = models.TextField(
        blank=True, null=True, verbose_name='Информация о себе'
    )

    @property
    def is_user(self):
        return self.role == self.USER

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    @property
    def is_admin(self):
        return self.is_staff or self.role == self.ADMIN

    class Meta:
        ordering = ('first_name', 'last_name')
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        constraints = [
            models.UniqueConstraint(
                fields=['username', 'confirmation_code'],
                name='unique_confirmation_code',
            )
        ]

    def __str__(self):
        return f'{self.username}: {self.role}'


class Category(models.Model):
    name = models.CharField('Название категории', max_length=200)
    slug = models.SlugField('Ссылка на категорию', unique=True)

    class Meta:
        ordering = ('slug',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField('Название жанра', max_length=200)
    slug = models.SlugField('Ссылка на жанр', unique=True)

    class Meta:
        ordering = ('slug',)
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField('Название произведения', max_length=100)
    year = models.IntegerField(
        'Год выпуска', blank=True, null=True, validators=[year_validator]
    )
    category = models.ForeignKey(
        Category,
        verbose_name='Категория',
        related_name='titles',
        on_delete=models.SET_NULL,
        null=True,
    )
    description = models.TextField(
        blank=True, null=True, verbose_name='Описание'
    )
    genre = models.ManyToManyField(
        Genre, related_name='titles', blank=True, verbose_name='Жанр'
    )

    class Meta:
        ordering = ('name', 'year')
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name


class TitleGenre(models.Model):
    genre = models.ForeignKey(
        Genre, on_delete=models.SET_NULL, blank=True, null=True
    )
    title = models.ForeignKey(
        Title, on_delete=models.SET_NULL, blank=True, null=True
    )

    def __str__(self):
        return f'{self.genre} {self.title}'


class Review(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews'
    )
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='reviews'
    )
    text = models.TextField()
    score = models.IntegerField(
        validators=[
            MinValueValidator(1, message='Оценка должна быть больше 1'),
            MaxValueValidator(10, message='Оценка должна быть меньше 10'),
        ]
    )
    pub_date = models.DateTimeField(
        'Дата публикации', auto_now_add=True, db_index=True
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = [
            constraints.UniqueConstraint(
                fields=['author', 'title'],
                name='unique_review'
            )
        ]

    def __str__(self):
        return (
            f'Отзыв {self.author} на ' f'{self.title} ({self.title.category})'
        )


class Comment(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        null=True,
        related_name='comments',
        verbose_name='Произведение',
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Отзыв',
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments'
    )
    text = models.TextField()

    pub_date = models.DateTimeField(
        'Дата публикации', auto_now_add=True, db_index=True
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return f'{self.author}: {self.text}'
