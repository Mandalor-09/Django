from accounts.models.user import User
from accounts.models.profile import Profile
from django.contrib import messages
from django.shortcuts import redirect
from django.http import HttpResponse

def activation(request,email_token):
    if email_token:
        profile = Profile.objects.get(email_token=email_token)
        if profile:
            profile.is_user_verified = True
            profile.save()
            messages.success(request,'Your Account is now verified')
            return HttpResponse('Home page')
        return HttpResponse('Somthing went wrong')