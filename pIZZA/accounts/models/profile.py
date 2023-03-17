from accounts.models.user import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.db import models
from base.models.basemodel import BaseModel
from uuid import uuid4
from django.core.mail import send_mail
from django.conf import settings

class Profile(BaseModel):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=100,blank=True, null=True)
    mobile = models.CharField(max_length=12,blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    email_token = models.CharField(max_length=255,blank=True, null=True)
    is_user_verified = models.BooleanField(default=False) 
    image = models.ImageField(upload_to='Uploads/user_images')

    @receiver(post_save, sender=User)
    def _post_save_receiver(sender,instance,created,*args, **kwargs):
        if created:
            try:
                email_token = str(uuid4())
                user = Profile.objects.create(user = instance,email_token=email_token)
                email = instance.email

                subject='Verify your account'
                message=f'Click on the link to verify your account http://127.0.0.1:8000/activation/{email_token}'
                from_email=settings.EMAIL_HOST_USER
                email=[email]
                
                send_mail(subject,message,from_email,email)
                print('email sent')
            except Exception as e:
                print(e)
            

    