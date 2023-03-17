from django.contrib import admin
from accounts.models.profile import Profile
from accounts.models.user import User

admin.site.register(User)

class ProfileAdmin(admin.ModelAdmin):
    list_display = ['name','email','mobile','id','user_id']
admin.site.register(Profile,ProfileAdmin)
