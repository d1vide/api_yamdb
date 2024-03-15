from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

from users.models import User
from reviews.constants import (MAX_LENGTH, MAX_TEXT_LENGTH, MAX_VALUE_REVIEW,
                               MIN_VALUE_REVIEW)


class NameSlugBaseModel(models.Model):
    name = models.CharField(max_length=MAX_LENGTH, verbose_name='Название')
    slug = models.SlugField(unique=True, verbose_name='Идентификатор',
                            help_text=('Идентификатор страницы для URL; '
                                       'разрешены символы латиницы, цифры, '
                                       'дефис и подчёркивание.'))

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class Category(NameSlugBaseModel):

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'


class Genre(NameSlugBaseModel):

    class Meta:
        verbose_name = 'жанр'
        verbose_name_plural = 'Жанры'


class Title(models.Model):
    name = models.CharField(max_length=MAX_LENGTH, verbose_name='Название')
    year = models.SmallIntegerField()
    description = models.TextField(blank=True, null=True)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name='title')
    genre = models.ManyToManyField(Genre)

    class Meta:
        ordering = ('name',)
        verbose_name = 'произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name

 
class ReviewAndCommentsModel(models.Model):
    pub_date = models.DateTimeField("Дата публикации", auto_now_add=True)

    class Meta:
        abstract = True
        ordering = ("-pub_date",)

    def __str__(self):
        return self.text[:MAX_TEXT_LENGTH]


class Review(ReviewAndCommentsModel):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name="reviews",
    )
    text = models.TextField("Текст", help_text="Отзыв")
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="reviews",
        verbose_name="Автор",
    )
    score = models.SmallIntegerField(
        verbose_name="Оценка",
        validators=[MinValueValidator(MIN_VALUE_REVIEW),
                    MaxValueValidator(MAX_VALUE_REVIEW)],
    )

    class Meta:
        verbose_name = 'отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = [
            models.UniqueConstraint(
                fields=["author", "title"], name="unique_review"
            )
        ]


class Comment(ReviewAndCommentsModel):
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name="comments"
    )
    text = models.TextField("Текст", help_text="Комментарий")
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="comments"
    )

    class Meta:
        verbose_name = 'комментарий'
        verbose_name_plural = 'Комментарии'
