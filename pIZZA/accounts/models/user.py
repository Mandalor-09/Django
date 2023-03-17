from django.contrib.auth.models import BaseUserManager,PermissionsMixin,AbstractBaseUser
from base.models.basemodel import BaseModel
from django.db import models

class MyBaseUserManager(BaseUserManager):
    def create_user(self,email,password):
        if email is None:
            return ValueError('Email not Found')
        if password is None:
            return ValueError('Password not Found')
        
        user = self.model(email = self.normalize_email(email))
        user.set_password(raw_password=password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self,email,password):
        user = self.create_user(email=email,password=password)
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser,PermissionsMixin,BaseModel):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
        
    )
    
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = MyBaseUserManager()

    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
    
    @property
    def is_authenticated(self):
        """
        Returns True if the user is authenticated, False otherwise.
        """
        return self.email
