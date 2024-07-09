from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone


class CustomUserManager(BaseUserManager):
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

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(username, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):

    full_name = models.CharField(max_length=255)
    employee_number = models.CharField(max_length=50, unique=True)
    username = models.CharField(max_length=150, unique=True)
    region = models.CharField(max_length=100)
    department = models.CharField(max_length=100)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['full_name', 'employee_number', 'region', 'department']




class Entry(models.Model):

    receptionist = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    id_number = models.IntegerField()
    plate_number = models.CharField(max_length=20)
    fname = models.CharField(max_length=100)
    contact = models.IntegerField()
    nature_of_visit = models.CharField(max_length=50, null=False)
    destination = models.CharField(max_length=50)  
    visitee = models.CharField(max_length=20, null=False) 
    purpose = models.TextField()
    comments = models.CharField(max_length=255, blank=True, default='')
    is_signedout = models.BooleanField(default=False)
    is_released = models.BooleanField(default=False)
    status = models.BooleanField(default=False)
    created_at = models.DateTimeField()

    def save(self, *args, **kwargs):
        if not self.id:  # Check if the object is being created
            self.created_at = timezone.now()  # Set created_at only if it's a new object
        if self.is_signedout and self.is_released:
            self.status = True
        else:
            self.status = False
        super().save(*args, **kwargs)  # Call save() method of the parent class
    
    def __str__(self):
        return self.fname
    
class Group(models.Model):
    group_name = models.CharField(max_length=40)
    contact = models.IntegerField()
    plate_number2 = models.CharField(max_length=20)
    purpose = models.CharField(max_length=100)
    department = models.CharField(max_length=50)
    is_checked = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.group_name


class GroupMember(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='members')
    name = models.CharField(max_length=100)
    id_number = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

