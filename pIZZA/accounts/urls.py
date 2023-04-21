from django.urls import path
from accounts.views.activation import activation
from accounts.views.register import Register
from accounts.views.login import Login
from accounts.views.logout import Logout
from accounts.views.forgotpassword import ForgotPasswordView
from accounts.views.resetpassword import ResetPasswordView

urlpatterns = [
    path('activation/<email_token>',activation,name='activation'),
    path('register/',Register.as_view(),name = 'register'),
    path('login',Login.as_view(),name='login'),
    path('logout/',Logout.as_view(),name='logout'),
    path('forgotpassword/',ForgotPasswordView.as_view(),name = 'forgotpassword'),
    
    path('resetpassword/',ResetPasswordView.as_view(),name = 'passwordresetpage')
]
