
from django.http import HttpResponse, JsonResponse,HttpResponseServerError
from django.shortcuts import render,redirect
from django.views import View
from django.contrib import messages
from django.core.mail import send_mail
from accounts.models.profile import Profile
from random import randint
from django.conf import settings
from accounts.models.user import User


def forgotPasswordMail(request, to_email):
    try:
        if not request.session.get('cart'):
               request.session['cart']={}
        profile = Profile.objects.get(email=to_email)
        otp = randint(0, 99999)
        profile.resetPassword = otp
        profile.save()
        subject = 'You Forgot Your Account Password'
        message = f"Enter the Below otp to reset your Password{otp}"
        from_email = settings.EMAIL_HOST_USER
        to_email = [to_email,]
        send_mail(subject=subject, message=message, from_email=from_email,
                  recipient_list=to_email, fail_silently=True)
        return True
    except Profile.DoesNotExist:
        messages.error(request, 'No User With the Entered Email')
        return False
    
class ForgotPasswordView(View):
    def get(self, request, *args, **kwargs):
        print(request.GET)
        email = request.GET.get('email')
        context = {}
        user = User.objects.filter(email =email)
        if email is not None:
            if user.exists():
                forgotPasswordMail(request,to_email=email)
                messages.success(request,'Please enter the code send on Your Email')
                context['email'] = email
                print(email,'<<<<<<<<<<<<<<<<<<<')
                return render(request,'accounts/forgotpassword.html',context)
            return redirect('register')
        
        return render(request,'accounts/forgotpassword.html',context)
        

    def post(self, request, *args, **kwargs):
        print(request.POST)
        email = request.POST.get('email')
        request.session['email']=email
        otp = request.POST.get('password1')
        profile = Profile.objects.get(email = email,resetPassword = otp)
        if profile:
            messages.success(request,'OTP Verified Successfully')
            return redirect('passwordresetpage') 
        else:
            messages.warning(request,'Otp Incorrect Correct')
            return JsonResponse({'status':'warning','msg':'Otp Incorrect'})
        
