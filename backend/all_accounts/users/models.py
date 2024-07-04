from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
from utils.common import BaseTimestampModel


class User(BaseTimestampModel, AbstractUser):
    is_email_verified = models.BooleanField(default=False)

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        ordering = ["-id"]

    def __str__(self):
        return self.email