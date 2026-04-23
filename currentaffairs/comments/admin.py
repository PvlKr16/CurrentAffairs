from django.contrib import admin
from .models import Comment, CommentAttachment


class CommentAttachmentInline(admin.TabularInline):
    model = CommentAttachment
    extra = 0


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

    inlines = [CommentAttachmentInline]

    actions = ['clear_files']

    def clear_files(self, request, queryset):
        for obj in queryset:
            if obj.file:
                obj.file.delete(save=False)
                obj.file = None
                obj.save()

    def has_file(self, obj):
        return bool(obj.file)

    has_file.boolean = True
