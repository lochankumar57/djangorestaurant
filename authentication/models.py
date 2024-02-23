from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# class usersm(BaseUserManager):
#     def create_user(self, username, password=None):
#         if not username:
#             raise ValueError('The Username field must be set')
#         user = self.model(username=username)
#         user.set_password(password)
#         user.save(using=self._db)
#         return user

#     def create_superuser(self, username, password=None):
#         return self.create_user(username, password)

# class user(AbstractBaseUser):
#     username = models.CharField(max_length=100,unique=True)
#     password = models.CharField(max_length=100)

#     objects = usersm()
#     USERNAME_FIELD = 'username'

#     def __str__(self):
#         return self.username

class userm(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError('The Username field must be set')
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(username, password, **extra_fields)
    
class users(AbstractBaseUser):
    username = models.CharField(max_length=150, unique=True)
    
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = userm()

    USERNAME_FIELD = 'username'

    groups = models.ManyToManyField('auth.Group', related_name='user_groups', blank=True)
    user_permissions = models.ManyToManyField('auth.Permission', related_name='user_permissions', blank=True)

    def __str__(self):
        return self.username


class Item(models.Model):
    username = models.CharField(max_length=50)
    name = models.CharField(max_length=100)
    totalprice = models.FloatField()
    datetime = models.DateTimeField(auto_now_add=True)


class rating(models.Model):
    name = models.CharField(max_length=100)
    rating = models.FloatField()