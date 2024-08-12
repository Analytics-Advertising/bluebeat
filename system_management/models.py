from django.db import models

# Create your models here.

from django.contrib.auth.models import AbstractUser, BaseUserManager


class UserManager(BaseUserManager):
   
    def _create_user(self, email, password, first_name, last_name, **extra_fields):
        # validation Checks
        if not email:
            raise ValueError("User must have an email address")
        if not password:
            raise ValueError("Must have password")
        if not first_name:
            raise ValueError("Must have first name")
        if not last_name:
            raise ValueError("Must have last name")
        # Create a User
        user_obj = self.model(
            email=self.normalize_email(email), 
            first_name=first_name,
            last_name=last_name,
            **extra_fields
        )
        user_obj.set_password(password)
        user_obj.save(using=self._db)
        return user_obj

    def create_user(self, email, first_name, last_name, user_type, password,
                    is_staff, is_active=True, is_admin=False):

        if not email:
            raise ValueError("Users must have an email address")

        if not password:
            raise ValueError('Must have password')

        user_obj = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            user_type=user_type,
            is_staff=is_staff,
        )
        user_obj.set_password(password)
        user_obj.staff = is_staff
        user_obj.admin = is_admin
        user_obj.active = is_active
        user_obj.save(using=self._db)
        return user_obj

        # The prototype of create_superuser() should accept the username field, plus all required fields as arguments.

    def create_superuser(self, email, password, first_name, last_name, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self._create_user(email, password, first_name, last_name, **extra_fields)

    def create_superuser(self, email, password, first_name, last_name, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self._create_user(email, password, first_name, last_name, **extra_fields)


# Create your models here.
class UserType(models.Model):
    USER_ROLES = (
        ('admin', 'Admin'),
        ('dealer', 'Dealer'),
          
    )
    name = models.CharField(max_length=50, choices=USER_ROLES)

    def __str__(self):
        return self.name


class User(AbstractUser):

    username = None
    email = models.EmailField(max_length=255, null=False, unique=True)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    user_type = models.ForeignKey(UserType, on_delete=models.CASCADE, null=True, blank=True)
    phone_number = models.CharField(max_length=10, null=True, blank=True)

   
    objects = UserManager()

    USERNAME_FIELD = 'email'

    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return self.email