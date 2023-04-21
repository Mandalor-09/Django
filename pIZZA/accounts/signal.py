from allauth.account.signals import user_signed_up
from allauth.socialaccount.models import SocialAccount
from django.dispatch import receiver
from accounts.models import User

@receiver(user_signed_up)
def create_third_party_user(sender, instance, **kwargs):
    social_account = SocialAccount.objects.get(user=instance)
    email = social_account.extra_data.get('email')
    if not User.objects.filter(email=email).exists():
        user = User.objects.create_user(email=email)