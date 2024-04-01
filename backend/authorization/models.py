from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.validators import RegexValidator
from django.db import models

from .managers import UserManager


phone_number_validator = RegexValidator(
    regex=r'^\+7\d{10}$',
    message='Phone number must start with "+7" followed by 10 digits.',
    code='invalid_phone_number'
)


class UserRoles(models.TextChoices):
    EMPLOYEE = "Employee", "Сотрудник"
    PARENT = "Parent", "Родитель"
    STUDENT = "Student", "Ученик"


class User(PermissionsMixin, AbstractBaseUser):
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    role = models.CharField(max_length=20, choices=UserRoles.choices, default=UserRoles.EMPLOYEE)
    full_name = models.CharField(max_length=200, blank=True, null=True)
    email = models.EmailField(max_length=100, blank=True, null=True, unique=True)
    iin = models.CharField(max_length=12, blank=True, null=True, unique=True)
    mobile_phone = models.CharField(max_length=25, unique=True, validators=[phone_number_validator])

    objects = UserManager()

    USERNAME_FIELD = "mobile_phone"
    REQUIRED_FIELDS = ['role', 'full_name', 'password', 'iin', 'email']

    def clean(self):
        pass

    def __str__(self):
        return self.mobile_phone

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        db_table = 'users'


class UserInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_info')
    photo_avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    address = models.CharField(max_length=200, blank=True, null=True)
    num_of_doc = models.CharField(max_length=20, blank=True, null=True)
    issued_by = models.CharField(max_length=100, blank=True, null=True)
    issued_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.user.mobile_phone

    class Meta:
        verbose_name = 'User Info'
        verbose_name_plural = 'Users Info'
        db_table = 'users_info'
        ordering = ['user']
