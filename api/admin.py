from django.contrib import admin
from .models import StellarAccount, PublicProfile

# Register your models here.
admin.site.register(StellarAccount)
admin.site.register(PublicProfile)
