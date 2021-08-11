from django.contrib import admin
from api_requests.models import OptionForAPI, RequestForApi
from api_requests.models import CompilationR
from django.db import models 
# Register your models here.
from django.forms import SelectMultiple

class RequestAdmin(admin.ModelAdmin):
    
    formfield_overrides = {
        models.ManyToManyField:{'widget':SelectMultiple},
    }

admin.site.register(OptionForAPI)
admin.site.register(RequestForApi,RequestAdmin)
admin.site.register(CompilationR)
