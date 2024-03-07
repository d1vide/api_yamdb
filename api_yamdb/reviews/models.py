from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

MAX_LENGTH = 256
MAX_YEAR = 2026
MIN_YEAR = 0


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
    year = models.IntegerField(validators=[MaxValueValidator(MAX_YEAR),
                                           MinValueValidator(MIN_YEAR)
                                           ])
    description = models.TextField(blank=True, null=True)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name='title')
    genre = models.ManyToManyField(Genre, through='TitleGenre')

    class Meta:
        verbose_name = 'произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name


class TitleGenre(models.Model):
    title = models.ForeignKey(Title, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
