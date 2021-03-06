from django.conf import settings
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import ugettext_lazy as _

from django.utils.crypto import get_random_string


class UserManager(BaseUserManager):
    def create_user(self, email, password, **kwargs):
        print("create user function")
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **kwargs)
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        return self.create_user(
            email, password, is_staff=True, is_superuser=True, **extra_fields
        )

class User(AbstractUser):
    email = models.EmailField(unique=True)
    address = models.CharField(_('address'), max_length=256, blank=True)
    phone = models.IntegerField(null=True)
    avatar = models.ImageField(upload_to="user-avatars", blank=True, null=True)

    USERNAME_FIELD = "email"
    objects = UserManager()
    REQUIRED_FIELDS = []

    class Meta:
        ordering = ('email',)

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     if not self.username:
    #         self.username = self.email.split('@')[0]

    def __str__(self):
        return self.email