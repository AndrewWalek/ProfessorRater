from django.contrib import admin
from .models import Module, ModuleInstances, Professors, Rating

# Register your models here.

admin.site.register(ModuleInstances)
admin.site.register(Professors)
admin.site.register(Rating)
admin.site.register(Module)