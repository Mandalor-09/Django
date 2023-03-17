from django.urls import path
from accounts.views.activation import activation
from accounts.views.register import Register
from accounts.views.login import Login
from accounts.views.logout import Logout
urlpatterns = [
    path('activation/<email_token>',activation,name='activation'),
    path('register/',Register.as_view(),name = 'register'),
    path('login',Login.as_view(),name='login'),
    path('logout/',Logout.as_view(),name='logout'),
]
