from django.contrib import admin
from .models import Watch

# Register your models here.
# admin.site.register(Watch)

class WatchAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'brand', 'price', 'condition', 'gender')  # Define the fields you want to display in the list view
    ordering = ('id',)  # Order by the 'price' field in ascending order
    search_fields = ('title', 'id')  # Add a search bar to the admin page and search by the 'title' field

# Register the Watch model with the custom admin options
admin.site.register(Watch, WatchAdmin)

