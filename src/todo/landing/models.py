from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from django.contrib.auth.hashers import make_password

class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        if not email: 
            raise ValueError('User must have an email address')
        if not username:
            raise ValueError('User must have a username')
        
        user = self.model(
            email=self.normalize_email(email),
            username=username
        )

        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, username, email, password=None):
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password
        )
        user.is_admin = True
        user.save(using=self._db)
        return user
    
class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(max_length=255, unique=True)
    password = models.CharField(max_length=255)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        db_table = "users"

    def __str__(self):
        return self.email
    
    def has_perm(self, perm, obj=None):
        return self.is_admin
    
    def has_module_perms(self, app_label):
        return True
    
    def is_staff(self):
        return self.is_admin
    
    @property
    def is_anonymous(self):
        return False

    @property
    def is_authenticated(self):
        return True
    
    def set_password(self, raw_password):
        self.password = make_password(raw_password)