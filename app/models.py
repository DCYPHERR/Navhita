from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from .managers import UserManager
from django.contrib.auth.models import PermissionsMixin
# Create your models here.
class User(AbstractBaseUser):
    email = models.EmailField(unique=True)
    is_patient = models.BooleanField(default=False)
    is_caretaker = models.BooleanField(default=False)
    
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    otp = models.CharField(max_length=7, null=True, blank=True, default=None)
    
    def get_short_name(self):
        # The user is identified by their email
        return self.email
    
    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True
    
    def has_module_perms(self, app_label):
           return True
    
    def __str__(self):
        return self.email
    
    
class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='patient')
    name = models.CharField(max_length=100, null=False, blank=False)
    phone = models.CharField(max_length=10)
    address = models.TextField(null=True, blank=True, default=None)
    country = models.CharField(max_length=100, null=True, blank=True, default=None)
    state = models.CharField(max_length=100, null=True, blank=True, default=None)
    city = models.CharField(max_length=100, null=True, blank=True, default=None)
    pincode = models.CharField(max_length=6, null=True, blank=True, default=None)
    guardian_name = models.CharField(max_length=100, null=True, blank=True, default=None)
    guardian_email = models.EmailField(null=True, blank=True, default=None)
    guardian_phone = models.CharField(max_length=10, null=True, blank=True, default=None)
    emergency_contact = models.CharField(max_length=10, null=True, blank=True, default=None)
    caretaker = models.ForeignKey('CareTaker', on_delete=models.SET_NULL, related_name='patient', null=True, blank=True, default=None)
    
    def __str__(self):
        return self.user.email
    
class CareTaker(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='caretaker')
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=10)
    address = models.TextField(null=True, blank=True, default=None)
    country = models.CharField(max_length=100, null=True, blank=True, default=None)
    state = models.CharField(max_length=100, null=True, blank=True, default=None)
    city = models.CharField(max_length=100, null=True, blank=True, default=None)
    pincode = models.CharField(max_length=6, null=True, blank=True, default=None)
    
    def __str__(self):
        return self.user.email
    
class service(models.Model):
    name = models.CharField(max_length=250, blank=False, null=False, unique=True)
    description = models.TextField(blank=True,null=True)
    def __str__(self):
        return self.name