from urllib import request
from accounts.models.user import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.db import models
from base.models.basemodel import BaseModel
from uuid import uuid4
from django.core.mail import send_mail
from django.conf import settings


def welcomeMail(toemail):
    subject = f'Wellcome {toemail} to Pizza Shop' 
    message = "Dear [User],\nWe're thrilled to welcome you to Pizza Shop! Thank you for signing up and becoming a part of our community.\nAs a member of  Pizza Shop, you'll have access to many Feture. We hope you find these features useful and that you'll enjoy using our platform.\nIf you have any questions or concerns, don't hesitate to reach out to our support team at karmamaster@gmail.com . We're always happy to help.\nThank you again for joining  Pizza Shop! We look forward to seeing you around the site.\n\nBest regards,\nOm Singh\nPizza Shop\n"
    from_email = settings.EMAIL_HOST_USER
    to_email = [toemail,]
    send_mail(subject=subject,message=message,from_email=from_email,recipient_list=to_email,fail_silently=True)


def EmailTokkeneMail(toemail,emailToken):
    subject = f'Hello {toemail} Your Accounts need to be Verified' 
    message = f"Click on the Link to verify Your Account http://127.0.0.1:8000/activation/{emailToken}"
    from_email = settings.EMAIL_HOST_USER
    to_email = [toemail,]
    send_mail(subject=subject,message=message,from_email=from_email,recipient_list=to_email,fail_silently=True)


class Profile(BaseModel):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=100,blank=True, null=True)
    mobile = models.CharField(max_length=12,blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    email_token = models.CharField(max_length=255,blank=True, null=True)
    is_user_verified = models.BooleanField(default=False) 
    image = models.ImageField(upload_to='Uploads/user_images')
    resetPassword = models.CharField(max_length=8,blank=True, null=True)
    
    
    @receiver(post_save, sender= User,)
    def CreateProfileObjects(sender,instance,created,*args, **kwargs):
        if created:
            email_token = str(uuid4())
            profile = Profile.objects.create(user = instance,email=instance.email,email_token=email_token,name = instance.email)
            
            welcomeMail(toemail=instance.email)
            EmailTokkeneMail(toemail=instance.email,emailToken=email_token)

    