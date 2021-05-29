from django.contrib import admin
from .models import OptionForAPI, RequestForApi
from django.db import models 
# Register your models here.
from django.forms import SelectMultiple

class RequestAdmin(admin.ModelAdmin):
    
    formfield_overrides = {
        models.ManyToManyField:{'widget':SelectMultiple},
    }

admin.site.register(OptionForAPI)
admin.site.register(RequestForApi,RequestAdmin)
