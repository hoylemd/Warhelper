from models import ModelProfile
from django.contrib import admin

# register the ModelProfile model
class ModelProfileAdmin(admin.ModelAdmin):
    model = ModelProfile
#
admin.site.register(ModelProfile, ModelProfileAdmin)
