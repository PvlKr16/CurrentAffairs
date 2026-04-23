from django.contrib import admin
from django.utils.html import format_html

from .models import (
    Topic,
    TopicReadStatus,
    Poll,
    PollOption,
    PollVote,
    PollReadStatus,
    TopicAttachment,
    PollAttachment,
)


# ===================== ATTACHMENTS =====================

class TopicAttachmentInline(admin.TabularInline):
    model = TopicAttachment
    extra = 0


class PollAttachmentInline(admin.TabularInline):
    model = PollAttachment
    extra = 0


# ===================== TOPICS =====================

@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'title',
        'author',
        'is_open',
        'participants_count',
        'comments_count',
        'has_file',
        'created_at',
        'open_link',
    )

    list_filter = ('is_open', 'created_at')
    search_fields = ('title', 'description', 'content', 'author__email')
    ordering = ('-created_at',)
    filter_horizontal = ('participants',)

    inlines = [TopicAttachmentInline]

    actions = ['clear_files']

    def clear_files(self, request, queryset):
        for obj in queryset:
            if obj.file:
                obj.file.delete(save=False)
                obj.file = None
                obj.save()

    def participants_count(self, obj):
        return obj.participants.count()

    def comments_count(self, obj):
        return obj.comments.count()

    def has_file(self, obj):
        return bool(obj.file)

    has_file.boolean = True

    def open_link(self, obj):
        return format_html('<a href="/topic/{}/" target="_blank">Open</a>', obj.id)


# ===================== POLLS =====================

class PollOptionInline(admin.TabularInline):
    model = PollOption
    extra = 1


@admin.register(Poll)
class PollAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'short_question',
        'author',
        'is_open',
        'participants_count',
        'votes_count',
        'has_file',
        'created_at',
        'open_link',
    )

    inlines = [PollOptionInline, PollAttachmentInline]

    actions = ['clear_files']

    def clear_files(self, request, queryset):
        for obj in queryset:
            if obj.file:
                obj.file.delete(save=False)
                obj.file = None
                obj.save()

    def short_question(self, obj):
        return obj.question[:60]

    def participants_count(self, obj):
        return obj.participants.count()

    def votes_count(self, obj):
        return obj.votes.count()

    def has_file(self, obj):
        return bool(obj.file)

    has_file.boolean = True

    def open_link(self, obj):
        return format_html('<a href="/poll/{}/" target="_blank">Open</a>', obj.id)


# ===================== VOTES =====================

@admin.register(PollVote)
class PollVoteAdmin(admin.ModelAdmin):
    list_display = ('id', 'poll', 'option', 'user', 'created_at')


@admin.register(PollReadStatus)
class PollReadStatusAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'poll', 'last_read_at')


@admin.register(TopicReadStatus)
class TopicReadStatusAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'topic', 'last_read_at')
