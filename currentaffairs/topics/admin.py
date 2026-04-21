from django.contrib import admin
from django.utils.html import format_html

from .models import (
    Topic,
    TopicReadStatus,
    Poll,
    PollOption,
    PollVote,
    PollReadStatus,
)


# ==================================================
# TOPICS
# ==================================================

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

    list_filter = (
        'is_open',
        'created_at',
    )

    search_fields = (
        'title',
        'description',
        'content',
        'author__email',
        'author__first_name',
        'author__last_name',
    )

    ordering = ('-created_at',)

    filter_horizontal = ('participants',)

    readonly_fields = (
        'created_at',
        'updated_at',
    )

    def participants_count(self, obj):
        return obj.participants.count()

    participants_count.short_description = 'Users'

    def comments_count(self, obj):
        return obj.comments.count()

    comments_count.short_description = 'Comments'

    def has_file(self, obj):
        return bool(obj.file)

    has_file.boolean = True
    has_file.short_description = 'File'

    def open_link(self, obj):
        return format_html(
            '<a href="/topic/{}/" target="_blank">Open</a>',
            obj.id
        )

    open_link.short_description = 'View'


@admin.register(TopicReadStatus)
class TopicReadStatusAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'topic',
        'last_read_at',
    )

    search_fields = (
        'user__email',
        'topic__title',
    )

    ordering = ('-last_read_at',)


# ==================================================
# POLLS
# ==================================================

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
        'is_anonymous',
        'allow_multiple',
        'participants_count',
        'votes_count',
        'completed',
        'has_file',
        'created_at',
        'open_link',
    )

    list_filter = (
        'is_open',
        'is_anonymous',
        'allow_multiple',
        'created_at',
    )

    search_fields = (
        'question',
        'author__email',
        'author__first_name',
        'author__last_name',
    )

    ordering = ('-created_at',)

    filter_horizontal = ('participants',)

    inlines = [PollOptionInline]

    readonly_fields = ('created_at',)

    def short_question(self, obj):
        return obj.question[:60]

    short_question.short_description = 'Question'

    def participants_count(self, obj):
        return obj.participants.count()

    participants_count.short_description = 'Users'

    def votes_count(self, obj):
        return obj.votes.count()

    votes_count.short_description = 'Votes'

    def completed(self, obj):
        voters = obj.votes.values('user').distinct().count()
        users = obj.participants.count()
        return users > 0 and voters >= users

    completed.boolean = True

    def has_file(self, obj):
        return bool(obj.file)

    has_file.boolean = True
    has_file.short_description = 'File'

    def open_link(self, obj):
        return format_html(
            '<a href="/poll/{}/" target="_blank">Open</a>',
            obj.id
        )

    open_link.short_description = 'View'


@admin.register(PollVote)
class PollVoteAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'poll',
        'option',
        'user',
        'created_at',
    )

    list_filter = ('created_at',)

    search_fields = (
        'poll__question',
        'user__email',
    )

    ordering = ('-created_at',)


@admin.register(PollReadStatus)
class PollReadStatusAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'poll',
        'last_read_at',
    )

    search_fields = (
        'user__email',
        'poll__question',
    )

    ordering = ('-last_read_at',)
