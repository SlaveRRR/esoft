from django.db import models

# Create your models here.

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    nickname = models.CharField(max_length=255, blank=True, unique=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    first_name = models.CharField(max_length=255, blank=True, null=True)
    middle_name = models.CharField(max_length=255, blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    commission = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    is_realtor = models.BooleanField(null=True)
    email = models.EmailField(blank=True, null=True)
    Active = models.SmallIntegerField(null=True, default=1)
    
    objects = CustomUserManager()

    USERNAME_FIELD = 'nickname'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.nickname

class RealEstate(models.Model):
    id = models.AutoField(primary_key=True)
    heading = models.CharField(max_length=255, default=1)
    type = models.CharField(max_length=255, null=True)
    city = models.CharField(max_length=255, null=True)
    street = models.CharField(max_length=255, null=True)
    house_number = models.CharField(max_length=255, null=True)
    apartment_number = models.CharField(max_length=255, null=True)
    latitude = models.CharField(max_length=255, null=True)
    longitude = models.CharField(max_length=255, null=True)
    floor = models.CharField(max_length=255, null=True)
    number_of_floors = models.CharField(max_length=255, null=True)
    number_of_rooms = models.CharField(max_length=255, null=True)
    square = models.CharField(max_length=255, null=True)

class User_Real_estate(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    user_real_estate = models.ForeignKey(RealEstate, on_delete=models.CASCADE)
