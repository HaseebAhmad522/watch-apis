from django.contrib import admin
from .models import Watch

# Register your models here.
# admin.site.register(Watch)

class WatchAdmin(admin.ModelAdmin):
    list_display = ('title', 'brand', 'price', 'condition', 'gender')  # Define the fields you want to display in the list view
    ordering = ('id',)  # Order by the 'price' field in ascending order

# Register the Watch model with the custom admin options
admin.site.register(Watch, WatchAdmin)

