from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.utils import timezone

class UserManager(BaseUserManager):
    def create_user(self, email, name=None, password=None, referral_code=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        if not name:
            name = ''        
        if referral_code is None:
            referral_code = ''

        user = self.model(email=email, name=name, referral_code=referral_code, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        
        # Handle referral points
        if referral_code:
            referring_user = self.model.objects.filter(referral_code=referral_code).first()
            if referring_user:
                referring_user.points += 1
                referring_user.save(using=self._db)
        
        return user


class User(AbstractBaseUser):
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    referral_code = models.CharField(max_length=100, default='') 
    points = models.IntegerField(default=0)
    date_joined = models.DateTimeField(default=timezone.now)

    is_active = models.BooleanField(default=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.email
