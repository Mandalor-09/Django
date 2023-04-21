from django.views import View
from django.contrib import messages
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from accounts.models.user import User
from accounts.models.profile import Profile
from django.contrib.auth.mixins import LoginRequiredMixin

class ResetPasswordView(LoginRequiredMixin,View):
    login_url='login'
    def get(self, request, *args, **kwargs):
        return render(request,'accounts/resetpassword.html')

    def post(self, request, *args, **kwargs):
        print(request.POST)
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        user = User.objects.filter(email=email)

        if password1 != password2:
            messages.warning(request, 'Password MisMatched')
            return HttpResponseRedirect(request.path_info)
        else:
            user = User.objects.get(email=email)
            user.set_password(password1)
            user.save()
            messages.success(request, 'Password Changed')
            return redirect('login')

