from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models


class CustomUserManager(UserManager):
    def create_user(self, login, password=None, is_active=False, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_active', is_active)

        user = self.model(mobile_phone=login, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, login, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(login, password, **extra_fields)


class User(AbstractUser):
    """ Custom user model """

    ROLES = (
        ('Employee', 'Employee'),
        ('Parent', 'Parent'),
        ('Student', 'Student'),
    )

    role = models.CharField(max_length=20, choices=ROLES, default='Employee')
    full_name = models.CharField(max_length=200, blank=True, null=True)
    email = models.EmailField(max_length=100, blank=True, null=True, unique=True)
    iin = models.CharField(max_length=12, blank=True, null=True, unique=True)
    mobile_phone = models.CharField(max_length=25, blank=True, null=True, unique=True)

    username = None
    first_name = None
    last_name = None
    groups = None
    user_permissions = None

    objects = UserManager()

    USERNAME_FIELD = 'mobile_phone'
    REQUIRED_FIELDS = ['role', 'full_name', 'password', 'iin', 'email']

    def __str__(self):
        return self.mobile_phone

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        db_table = 'users'
        ordering = ['id']
