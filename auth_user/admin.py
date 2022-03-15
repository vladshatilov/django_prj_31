from django.contrib import admin

# Register your models here.
from auth_user.models import Profile

admin.site.register(Profile)