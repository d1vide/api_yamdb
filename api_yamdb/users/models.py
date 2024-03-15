from api.constants import (
    MAX_LENGTH_EMAIL, MAX_LENGTH_NAME, MAX_LENGTH_ROLE
)
from django.contrib.auth.models import AbstractUser
from django.core.validators import EmailValidator, RegexValidator
from django.db import models


class Roles(models.TextChoices):
    """Пользовательские роли: пользователь, модератор, администратор."""
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'


class User(AbstractUser):
    """Переопределенная модель user с дополнительными полями."""
    username = models.CharField(
        'Имя пользователя',
        max_length=MAX_LENGTH_NAME,
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^[\w.@+-]+\Z',
                message='Имя пользователя содержит недопустимый символ',)
        ],
    )
    first_name = models.CharField(max_length=MAX_LENGTH_NAME, blank=True)
    last_name = models.CharField(max_length=MAX_LENGTH_NAME, blank=True)
    email = models.EmailField(
        'Электронная почта пользователя',
        max_length=MAX_LENGTH_EMAIL,
        unique=True,
        validators=[EmailValidator])
    bio = models.TextField('Биография пользователя', blank=True)
    role = models.CharField(
        'Роль пользователя',
        max_length=MAX_LENGTH_ROLE,
        choices=Roles.choices,
        default=Roles.USER,
    )

    @property
    def is_admin(self):
        return (
            self.role == Roles.ADMIN
            or self.is_superuser
        )

    @property
    def is_moderator(self):
        return (
            self.role == Roles.MODERATOR
        )

    class Meta:
        ordering = ('username',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
