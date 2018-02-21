from django.conf import settings
from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.core import validators
from django.db import models
from django.utils.deconstruct import deconstructible


class AccountManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, telephone, username, email, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        if not username:
            raise ValueError('The given username must be set')
        email = self.normalize_email(email)
        username = self.model.normalize_username(username)
        user = self.model(telephone=telephone, username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, telephone, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(telephone, username, email, password, **extra_fields)

    def create_superuser(self, telephone, username, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(telephone, username, email, password, **extra_fields)


class Account(AbstractUser):
    """
    用户资料,仅仅存储Profile信息,但是包含头像
    telephone
    password
    register_source
    register_time
    is_active
    is_social
    """

    username = models.CharField(
        '用户名',
        max_length=150,
        unique=True,
        help_text='',
        validators=[
            # username_validator
            # TODO : 这里需要用户名和密码
        ],
        error_messages={
            'unique': "用户名已重复",
        },
    )
    telephone = models.CharField(max_length=20, blank=True, db_index=True, null=True, unique=True, verbose_name="手机")
    avatar_url = models.URLField(max_length=255, blank=True, verbose_name="头像链接")

    register_source = models.CharField(max_length=10, default=0, verbose_name="注册来源")
    register_time = models.DateTimeField(auto_now_add=True, verbose_name="注册时间")

    objects = AccountManager()

    REQUIRED_FIELDS = ['telephone']
    USERNAME_FIELD = 'username'

    def __str__(self):
        return '<Account # %d, %s>' % (self.id, self.username)

    @property
    def avatar(self):
        if not self.avatar_url:
            return settings.AVATAR_URL_PREFIX + settings.DEFAULT_AVATAR

    class Meta:
        verbose_name = "用户账号"
        verbose_name_plural = "用户账号"
