from django.db import models
from django.contrib.auth.models import AbstractBaseUser, UserManager
from django.utils.translation import gettext_lazy as _

class MyUserManager(UserManager):
    def create_user(self, email, password=None, **kwargs):
        if not email:
            raise ValueError(_('The Email field must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **kwargs)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **kwargs):
        user = self.create_user(email=email, password=password, **kwargs)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return usera

class User(AbstractBaseUser):
    email = models.EmailField(_('email address'), unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        ordering = ['-id']

    @property
    def name(self):
        if hasattr(self, 'display_name') and self.display_name:
            return self.display_name
        return 'SMS_' + str(self.pk)
