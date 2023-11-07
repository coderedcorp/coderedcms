from django.contrib import admin

from .models import CustomDocument
from .models import CustomImage


admin.site.register(CustomDocument)
admin.site.register(CustomImage)
