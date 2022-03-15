from django.contrib import admin

# Register your models here.
from ads.models import Ads, Categories, City, User

admin.site.register(Ads)
admin.site.register(Categories)
admin.site.register(City)
admin.site.register(User)