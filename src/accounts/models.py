from django.db import models

from django.contrib.auth.models import UserManager
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

class MyUserManager(UserManager):
   
    def create_user(self, email, password, **kwargs):
        user = self.model(email=email, **kwargs)
        # user.site = 'support.onlinejain.com'
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **kwargs):
        user = self.model(email=email, is_staff=True,
                          is_superuser=True, **kwargs)
        # user.site = 'support.onlinejain.com'
        user.set_password(password)
        user.save()
        return user

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), blank=False, unique=True)
    is_staff = models.BooleanField(_('staff status'), default=False)
    is_active = models.BooleanField(_('active'), default=True)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        ordering = ['-id']

    @property
    def name(self):
        if self.display_name:
            return self.display_name
        return 'SMS_' + str(self.pk)


    