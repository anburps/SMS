from django.db import models

from django.contrib.auth.models import UserManager
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

class MyUserManager(UserManager):
   
    def create_user(self, email, password=None, **kwargs):
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
    display_name = models.CharField(_('display name'), max_length=99, blank=True, null=True, unique=False)
    email = models.EmailField(_('email address'), blank=False, unique=True)
    phone = models.CharField(_('Contact number'), max_length=30, blank=True, null=True)
    is_staff = models.BooleanField(_('staff status'), default=False)
    is_active = models.BooleanField(_('active'), default=True)
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    created_date = models.DateTimeField(
                    auto_now=True
                )

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        ordering = ['-id']
        verbose_name = _('user')
        verbose_name_plural = _('users')
        db_table = 'auth_user'
        abstract = False

    @property
    def name(self):
        if self.display_name:
            return self.display_name
        return 'guest_rep_' + str(self.pk)


    # def get_slug(self):
    #     if self.display_name:
    #         slugify = self.display_name.lower().replace(" ", "_").replace(".","")
    #         return slugify
    #     return 'guest_rep' + str(self.pk)

