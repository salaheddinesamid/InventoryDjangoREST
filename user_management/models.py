from django.db import models
from django.contrib.auth.models import AbstractUser


class Role(models.Model):
    ROLE_CHOICES = (
        ("USER", "USER"),
        ("ADMIN", "ADMIN"),
    )

    role_name = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        unique=True
    )

    def __str__(self):
        return self.role_name


class User(AbstractUser):
    username = None

    email = models.EmailField(unique=True)

    first_name = models.CharField(
        max_length=200,
        null=True,
        blank=True
    )

    last_name = models.CharField(
        max_length=200,
        null=True,
        blank=True
    )

    roles = models.ManyToManyField("Role", blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
