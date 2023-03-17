from django.views import View
from accounts.models.user import User
from accounts.models.profile import Profile
from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect,HttpResponse
from django.contrib import messages


class Register(View):
    def get(self, request, *args, **kwargs):
        return render(request,'accounts/register.html')

    def post(self, request, *args, **kwargs):
        name = request.POST.get('name')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        
        if password1 != password2:
            messages.error(request,'Password Mis-matched')
            return HttpResponseRedirect(request.path_info)
        if User.objects.filter(email=email).exists():
            messages.error(request,'User Already Excits')
            return HttpResponseRedirect(request.path_info)
        password = password1
        user = User.objects.create_user(email=email,password=password)
        request.session['cart']={}
        user = User.objects.get(email=email)
        profile = Profile.objects.get(user_id = user.id)
        profile.name = name
        profile.email = email
        profile.save()
        return redirect('login')