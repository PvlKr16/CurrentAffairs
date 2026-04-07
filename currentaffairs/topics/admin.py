from django.contrib import admin
from .models import Topic


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'is_open', 'created_at')
    list_filter = ('is_open',)
    search_fields = ('title', 'description')
