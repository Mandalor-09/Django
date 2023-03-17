from django.views import View
from accounts.models.user import User
from accounts.models.profile import Profile
from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect,HttpResponse
from django.contrib import messages
from accounts.backend import SettingsBackend
from django.contrib.auth import get_user_model
User = get_user_model()

class Login(View):
    def get(self, request, *args, **kwargs):
        return render(request,'accounts/login.html')

    def post(self, request, *args, **kwargs):
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = User.objects.filter(email=email)
        if not user.exists():
            messages.error(request,'User not excits')
            return HttpResponseRedirect(request.path_info)
        user1 = User.objects.get(email=email)
        print('User is ',user)
        user = SettingsBackend.authenticate(self=user,email=email,password=password)
        print('User is ',type(user),user)
        if user:
            user =SettingsBackend.login(request,user1)

            request.session['email'] = email
            profile = Profile.objects.get(user_id=user.id)
            print(profile ,"<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>")
            print(profile.name,profile.email)
            request.session['name']=profile.name
            request.session['email']=profile.email
            
            if not request.session.get('cart'):
               request.session['cart']={}
               return redirect('home')
            print(request.session)
            messages.success(request,'Login Success')
            print('Login Success')
            return redirect('home')
        else:
            messages.error(request,'Invalid Crediential')
            print('Invalid Crediential')
            return HttpResponseRedirect(request.path_info)