from django.conf import settings
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.hashers import check_password
from accounts.models.user import User

class SettingsBackend(BaseBackend):
    def authenticate(self, email, password):
        
        try:
            user = User.objects.get(email=email)
            auth = check_password(password,user.password)
            print('auth',auth)
            if auth:
                return True
            return False
        except Exception as e:
            print(e)
        
    def login(request,user):
        return User.objects.get(id=user.id)

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None