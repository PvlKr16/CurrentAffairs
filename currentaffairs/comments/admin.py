from django.contrib import admin
from .models import Comment


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'topic',
        'author',
        'title',
        'has_file',
        'created_at',
    )

    list_filter = (
        'created_at',
        'topic',
    )

    search_fields = (
        'title',
        'content',
        'author__email',
        'topic__title',
    )

    ordering = ('-created_at',)

    def has_file(self, obj):
        return bool(obj.file)

    has_file.boolean = True
    has_file.short_description = 'File'
