from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import ugettext_lazy as _
# Create your models here.

class UserManager(BaseUserManager):
    
    use_in_migrations = True
    
    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The given email must be set')
        emai = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)
        
    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('SUperuser must have is_superuser=True')
        return self._create_user(email, password, **extra_fields)
        








class User(AbstractUser):
    username = models.CharField(max_length=40, blank=True, null=True)
    email = models.EmailField(_('email address'), unique=True)
    date_of_birth = models.DateField(blank=True, null=True)
    height = models.FloatField(blank=True, null=True)
    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'email'
    objects = UserManager()