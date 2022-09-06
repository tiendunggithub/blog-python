from django.contrib import admin

from .models import Blog

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'created_on')
    list_filter = ('status',)
    search_fields = ['title', 'description']

admin.site.register(Blog, PostAdmin)
