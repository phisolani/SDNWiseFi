from django.contrib import admin

from .models import Controller, Tenant, Graph

# Register your models here.
admin.site.register(Controller)
admin.site.register(Tenant)
admin.site.register(Graph)