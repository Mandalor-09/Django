from django.views import View
from accounts.models.user import User
from accounts.models.profile import Profile
from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect,HttpResponse
from django.contrib import messages
from accounts.backend import SettingsBackend

class Logout(View):

    def get(self, request, *args, **kwargs):
        user = request.user
        if user:
            session = request.session
            session.clear()
            request.user = None
            user = request.user
            messages.success(request,'Logout Succesfully')
            messages.success(request,'Logout Succesful')
            return redirect('login')
            
        return None